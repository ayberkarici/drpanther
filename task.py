# my_task.py
import time
from django.core.management import setup_environ
from drpanther import settings

setup_environ(settings)

# Your task logic here
while True:
    
    print('Hi!')
    
