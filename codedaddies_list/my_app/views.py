import requests
from django.shortcuts import render
from bs4 import BeautifulSoup


# Create your views here.

def home(request):
    return render(request, "base.html")


def new_search(request):
    search_keyword = request.POST.get('search')
    data_for_front = {
        'search': search_keyword
    }
    return render(request, "my_app/new_search.html", data_for_front)
