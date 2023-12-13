import os
import django
import time
import requests
from bs4 import BeautifulSoup
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drpanther.settings')
django.setup()

from process.models import *  # import your models here

def scrape_data():
    print("I'm in start")
    # Create or get a ScrapeProgress instance
    task_id = "books"  # This should be unique for each task
    progress_record, created = ScrapeProgress.objects.get_or_create(task_id=task_id)
    
    # Get all unique URLs that are not scrapped yet
    urls_to_scrape = ScrapedURL.objects.filter(is_scrapped=False)
    
    urls_to_scrape_clean = list(ScrapedURL.objects.values('url', 'category').filter(is_scrapped=False).distinct())
    total_urls = len(urls_to_scrape_clean) + Book.objects.count()
    print("I'm in")

    for idx, scraped_url in enumerate(urls_to_scrape):
        current_url = f"https://www.dr.com.tr/{scraped_url.url}"
        
        print(f"Processing - {current_url}")
        
        detail_response = None
        while detail_response is None:
            try:
                detail_response = requests.get(current_url)
                if detail_response.status_code != 200:
                    detail_response = None
                    raise requests.exceptions.RequestException

            except requests.exceptions.RequestException:
                urls_to_scrape[idx].error_count += 1
                
                if urls_to_scrape[idx].error_count > 3:
                    urls_to_scrape[idx].is_scrapped = True
                    urls_to_scrape[idx].save()
                    print(f"URL {current_url} marked as scrapped.")
                    break
                else:
                    print(f"No response from {current_url}. Retrying in 4 seconds...")
                    time.sleep(4)
                
        if urls_to_scrape[idx].error_count > 3:
            continue
        
        detail_soup = BeautifulSoup(detail_response.content, 'html.parser')
        
        # Extract book details
        try:
            title = detail_soup.select_one('.prd-name h1').text.strip()
        except AttributeError:
            title = None
            print("Title not found.")

        try:
            authors = detail_soup.select('.author.seo-heading a')
            author = authors[0].text.strip() if authors else None
        except (IndexError, AttributeError):
            author = None
            print("Author not found.")

        try:
            translator = authors[1].text.strip() if len(authors) > 1 else None
        except (IndexError, AttributeError):
            translator = None
            print("Translator not found.")

        try:
            publisher_name = detail_soup.select_one('#publisherName a').text.strip()
        except AttributeError:
            publisher_name = None
            print("Publisher name not found.")

        try:
            current_price = detail_soup.select_one('.current-price').text.strip()
        except AttributeError:
            current_price = None
            print("Current price not found.")

        
        # Parsing the detail page's content with BeautifulSoup
        detail_soup = BeautifulSoup(detail_response.content, 'html.parser')

        # Extract ISBN
        product_description = detail_soup.select_one('.product-description-body')
        if product_description:
            isbn_list_items = product_description.find_all('li')
            isbn = isbn_list_items[-1].find('span').text.strip() if isbn_list_items else ''
        else:
            isbn = ''

        # Extract Description
        description_tag = detail_soup.select_one('.product-description-header')
        description = description_tag.get_text(strip=True) if description_tag else ''

        # Extract Image URL
        image_tag = detail_soup.select_one('.js-prd-first-image')
        image_url = image_tag['src'] if image_tag and image_tag.has_attr('src') else ''

        # Handling cases where required data might be missing
        if not isbn or not description or not image_url:
            print('Required data not found')
            return False


        # Extract properties from .short-prop
        properties = {}
        for prop in detail_soup.select('.short-prop'):
            key = prop.select_one('span').text.strip().lower().replace(' ', '_').replace(':', '')
            value = prop.select_one('span:nth-of-type(2)').text.strip()
            properties[key] = value

        # Create or update the book record
        book, created = Book.objects.update_or_create(
            isbn=isbn,
            description=description,
            others=json.dumps(properties),
            defaults={
                'title': title,
                'author': author,
                'translator': translator,
                'publisher_name': publisher_name,
                'current_price': current_price,
                'image_url': image_url,
            }
        )

        if created:
            print(f"{title} - {current_url} added to database 🫡")
        else:
            print(f"{title} - {current_url} updated in database 🫡")

        # Mark URL as scrapped
        scraped_url.is_scrapped = True
        scraped_url.save()
        
        # Update progress
        progress = round((Book.objects.count() / total_urls) * 100, 4)
        progress_record.progress = progress
        progress_record.save()
        
    print('Scraping of book details completed successfully')
    
    return True


if __name__ == '__main__':
    
    while True:
        scrape_data()
        time.sleep(10)  # Wait for 60 seconds before next run