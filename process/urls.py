from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import *

app_name = 'process'
urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.index_books, name='index_books'),
    path('check-progress/', views.check_progress, name='check_progress'),
    path('scrape-category/', views.scrape_urls, name='scrape_urls'),
    path('scrape-books/', views.scrape_book_details, name='scrape_book_details'),
    
    
    
]