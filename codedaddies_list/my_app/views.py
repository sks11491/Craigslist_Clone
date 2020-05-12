import requests
from requests.compat import quote_plus
from django.shortcuts import render
from bs4 import BeautifulSoup
from . import models


BASE_CRAIGSLIST_URL = "https://ahmedabad.craigslist.org/search/bbb?query={}&sort=rel"
BASE_IMAGE_URL = "https://images.craigslist.org/{}_300x300.jpg"


# Create your views here.

def home(request):
    return render(request, "base.html")


def new_search(request):
    search_keyword = request.POST.get('search')
    models.Search.objects.create(search=search_keyword)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search_keyword))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    post_listing = soup.find_all('li', {'class': 'result-row'})
    result_posts = []
    for post in post_listing:
        post_title = post.find(class_="result-title").text
        post_url = post.find("a").get('href')
        if post.find(class_="result-price"):
            post_price = post.find(class_="result-price").text
        else:
            post_price = "N/A"

        post_image = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Python.svg/768px-Python.svg.png"
        if post.find(class_="result-image"):
            string = post.find(class_="result-image").get('data-ids')
            if string != None:
                post_image = string.split(",")[0].split(":")[1]
                post_image = BASE_IMAGE_URL.format(post_image)

        result_posts.append((post_title, post_url, post_price, post_image))

    data_for_front = {
        'search': search_keyword,
        'post_results': result_posts
    }
    return render(request, "my_app/new_search.html", data_for_front)
