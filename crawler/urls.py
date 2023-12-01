from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import *

app_name = 'crawler'
urlpatterns = [
    path('', views.index, name='index'),
]