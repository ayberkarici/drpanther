import csv
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drpanther.settings')
django.setup()

from process.models import Book  # Import your model

# Specify your custom delimiter here, for example, a semicolon
delimiter = '^'

# Open the file with UTF-8 encoding
with open("details_data.csv", mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=delimiter)

    # Write headers (optional)
    writer.writerow(['isbn', 'details'])  # Replace with your actual field names

    # Iterate over your data and write to the CSV file
    for entry in Book.objects.all():
        # Make others section with elements
        elements = ''
        if entry.paper_type is not None:
            paper_type = entry.paper_type
            elements += f"<b>Hamur Tipi: </b>{paper_type} <br>"
        if entry.page_number is not None:
            page_number = entry.page_number
            elements += f"<b>Sayfa Sayısı: </b>{page_number} <br>"
        if entry.size is not None:
            size = entry.size
            elements += f"<b>Ebat: </b>{size} <br>"
        if entry.first_print_year is not None:
            first_print_year = entry.first_print_year
            elements += f"<b>İlk Baskı Yılı: </b>{first_print_year} <br>"
        if entry.print_number is not None:
            print_number = entry.print_number
            elements += f"<b>Baskı Sayısı: </b>{print_number} <br>"
        if entry.language is not None:
            language = entry.language
            elements += f"<b>Dil: </b>{language} <br>"
        if entry.media_type is not None:
            media_type = entry.media_type
            elements += f"<b>Medya Cinsi: </b>{media_type} <br>"
        if entry.original_title is not None:
            original_title = entry.original_title
            elements += f"<b>Orijinal Adı: </b>{original_title} <br>"
        if entry.original_language is not None:
            original_language = entry.original_language
            elements += f"<b>Orijinal Dili: </b>{original_language} <br>"
        if entry.book_set is not None:
            book_set = entry.book_set
            elements += f"<b>Kitap Seti: </b>{book_set} <br>"
        if entry.sensibility is not None:
            sensibility = entry.sensibility
            elements += f"<b>Hassasiyet: </b>{sensibility} <br>"
        
        
        if entry.others is not None:    
            others = json.loads(entry.others)
            
                
            
            # Get all keys and values from others
            for key, value in others.items():
                key = key.replace('_', ' ').title()
                elements += f"<b>{key}: </b>{value} <br>"
        
        writer.writerow([entry.isbn, elements])  # Replace with your actual fields
        
with open("title_data.csv", mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=delimiter)

    # Write headers (optional)
    writer.writerow(['isbn', 'title'])  # Replace with your actual field names
    
    for entry in Book.objects.all():
        writer.writerow([entry.isbn, entry.title])
        
with open("image_data.csv", mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=delimiter)

    # Write headers (optional)
    writer.writerow(['isbn', 'image_url'])  # Replace with your actual field names
    
    for entry in Book.objects.all():
        writer.writerow([entry.isbn, entry.image_url])

with open("description_data.csv", mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=delimiter)

    # Write headers (optional)
    writer.writerow(['isbn', 'description'])  # Replace with your actual field names
    
    for entry in Book.objects.all():
        writer.writerow([entry.isbn, entry.description])
    
with open("author_data.csv", mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=delimiter)

    # Write headers (optional)
    writer.writerow(['isbn', 'author'])  # Replace with your actual field names
    
    for entry in Book.objects.all():
        writer.writerow([entry.isbn, entry.author])


with open("translator_data.csv", mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=delimiter)

    # Write headers (optional)
    writer.writerow(['isbn', 'translator'])  # Replace with your actual field names
    
    for entry in Book.objects.all():
        writer.writerow([entry.isbn, entry.translator])
        
with open("publisher_name_data.csv", mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=delimiter)

    # Write headers (optional)
    writer.writerow(['isbn', 'publisher_name'])  # Replace with your actual field names
    
    for entry in Book.objects.all():
        writer.writerow([entry.isbn, entry.publisher_name])
        
with open("current_price_data.csv", mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=delimiter)

    # Write headers (optional)
    writer.writerow(['isbn', 'current_price'])  # Replace with your actual field names
    
    for entry in Book.objects.all():
        writer.writerow([entry.isbn, entry.current_price])
                
        
# 'title', 'image_url', 'description', 'author', 'translator', 'publisher_name', 'current_price', 'isbn', 'others'