from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import requests
from bs4 import BeautifulSoup
import time
import json

# Create your views here.

def index (request):
    context = {
        "key" : ""
    }
    
    return render(request, 'process/index.html', context)

def index_books (request):
    context = {
        "key" : ""
    }
    
    return render(request, 'process/detailcrawler.html', context)


def check_progress(request):
    if request.method == 'POST':
        try:        
            task_id = request.POST.get('task_id')
            progress_record = ScrapeProgress.objects.get(task_id=task_id)
            return JsonResponse({'progress': progress_record.progress})
        except ScrapeProgress.DoesNotExist:
            return JsonResponse({'error': 'Progress record not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

def scrape_urls(request):
    if request.method == 'POST':
        base_url = request.POST.get('url_text')
        category = request.POST.get('category')  # Extract category from POST data
        page_number = request.POST.get('page_number')  # Extract page number from POST data
        total_pages = int(page_number)

        print(base_url, category)

        # Create or get a ScrapeProgress instance
        task_id = "category"  # This should be unique for each task
        progress_record, created = ScrapeProgress.objects.get_or_create(task_id=task_id)

        # Add the scraping logic here
        for page in range(1, total_pages + 1):
            current_url = base_url + str(page)
            
            # Initialize response to None
            response = None

            while response is None:
                try:
                    response = requests.get(current_url)
                    # Check if the response is successful (200 OK)
                    if response.status_code != 200:
                        if response.status_code == 404:
                            print(f"404 URL found, skipping.. - {current_url}")

                        response = None
                        raise requests.exceptions.RequestException
                except requests.exceptions.RequestException:
                    print(f"No response from {current_url}. Retrying in 4 seconds...")
                    time.sleep(4)  # Wait for 4 seconds before retrying
            
            soup = BeautifulSoup(response.content, 'html.parser')

            for prd_info in soup.find_all(class_='prd-infos'):
                first_link = prd_info.find('a', href=True)
                if first_link:
                    if ScrapedURL.objects.filter(url=first_link['href'], category=category).exists():
                        print(first_link['href'], "already exists in database! 🫡")
                        continue
                    
                    ScrapedURL.objects.create(url=first_link['href'], category=category)
                    print(first_link['href'], "added to database! 🫡")
            
            # Update progress in the database
            progress = round((float(page) / float(total_pages)) * 100, 4)
            progress_record.progress = progress
            progress_record.save()

        return JsonResponse({'message': 'Scraping completed successfully'})

    return JsonResponse({'error': 'Invalid request'}, status=400)


def scrape_book_details(request):
    if request.method == 'POST':
        
        
        print("I'm in start")
        # Create or get a ScrapeProgress instance
        task_id = "books"  # This should be unique for each task
        progress_record, created = ScrapeProgress.objects.get_or_create(task_id=task_id)
        
        urls_to_scrape = ScrapedURL.objects.filter(is_scrapped=False)
        total_urls = urls_to_scrape.count()
        
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
                return JsonResponse({'error': 'Required data not found'}, status=400)


            # Extract properties from .short-prop
            properties = {}
            for prop in detail_soup.select('.short-prop'):
                key = prop.select_one('span').text.strip().lower().replace(' ', '_').replace(':', '')
                value = prop.select_one('span:nth-of-type(2)').text.strip()
                properties[key] = value

            # Define a mapping from extracted keys to your model fields
            key_mapping = {
                'baskı_sayısı': 'print_number',
                'dil': 'language',
                'ebat': 'size',
                'hamur_tipi': 'paper_type',
                'i̇lk_baskı_yılı': 'first_print_year',
                'sayfa_sayısı': 'page_number',
                'medya_cinsi': 'media_type',
                'orijinal_adı': 'original_title',
                'orijinal_dili': 'original_language',
                'kitap_seti' : 'book_set',
                'hassasiyet' : 'sensibility',
            }

            # Assuming properties is a dictionary with keys like 'baskı_sayısı', 'dil', etc.
            translated_properties = {key_mapping.get(k, k): v for k, v in properties.items()}

            # Create or update the book record
            book, created = Book.objects.update_or_create(
                isbn=isbn,
                description=description,
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
            
        return JsonResponse({'message': 'Scraping of book details completed successfully'})

    return JsonResponse({'error': 'Invalid request'}, status=400)

