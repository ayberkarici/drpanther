from django.db import models

# Create your models here.

class ScrapedURL(models.Model):
    url = models.URLField()
    category = models.CharField(max_length=256)
    is_scrapped = models.BooleanField(default=False)
    error_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.category}: {self.url}"

class ScrapeProgress(models.Model):
    task_id = models.CharField(max_length=255, unique=True)
    progress = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.task_id} - {self.progress}%"

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    author = models.CharField(max_length=255, null=True, blank=True)
    translator = models.CharField(max_length=255, null=True, blank=True)
    publisher_name = models.CharField(max_length=255, null=True, blank=True)
    current_price = models.CharField(max_length=50, null=True, blank=True)
    paper_type = models.CharField(max_length=100, null=True, blank=True)  # Example for 'Hamur Tipi'
    page_number = models.CharField(max_length=100, null=True, blank=True)  # Example for 'Sayfa Sayısı'
    size = models.CharField(max_length=100, null=True, blank=True)  # Example for 'Ebat'
    first_print_year = models.CharField(max_length=50, null=True, blank=True)  # Example for 'İlk Baskı Yılı'
    print_number = models.CharField(max_length=50, null=True, blank=True)  # Example for 'Baskı Sayısı'
    language = models.CharField(max_length=50, null=True, blank=True)  # Example for 'Dil'
    isbn = models.CharField(max_length=20, null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    media_type = models.CharField(max_length=50, null=True, blank=True)  # Example for 'Medya Cinsi'
    original_title = models.CharField(max_length=255, null=True, blank=True) # Example for 'Orijinal Adı'
    original_language = models.CharField(max_length=50, null=True, blank=True) # Example for 'Orijinal Dili'
    book_set = models.CharField(max_length=50, null=True, blank=True) # Example for 'Kitap Seti'
    sensibility = models.CharField(max_length=50, null=True, blank=True) # Example for 'Hassasiyet'

    def __str__(self):
        return self.title
