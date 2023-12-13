from django.contrib import admin

# Register your models here.


# Register the admin class with the associated model
from .models import *
admin.site.register(ScrapeProgress)