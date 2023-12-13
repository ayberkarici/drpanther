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
    isbn = models.CharField(max_length=20, null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    others = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
