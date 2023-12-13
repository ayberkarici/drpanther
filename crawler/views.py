from django.shortcuts import render
from process.models import *

# Create your views here.

def index (request):
    context = {
        "key" : "value"
    }
    
    print("Selam")

    # ID'si 83145'ten küçük olan Book kayıtlarını sil
    Book.objects.all().delete()    
    
    return render(request, 'crawler/index.html', context)