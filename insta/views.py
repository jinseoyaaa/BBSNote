from django.shortcuts import render, redirect
from .parser import *
from .models import Insta
import pandas as pd

# Create your views here.

def index(request):
    results = insta_crawling()
    for row in results:
        insta = Insta(content=row[0], date=row[1], like=row[2], place=row[3], tags=row[4])
        insta.save()     
    return redirect('bbsnote:index')

def wordcloud(request):
    tags_all = Insta.objects.values('tags')
    tags_all_df = pd.DataFrame(tags_all)
    tags_total = []
    for tags in tags_all_df['tags']:
        tags_list = tags[2:-2].split("', '")
        for tag in tags_list:
            tags_total.append(tag)
    makeWordCloud(tags_total)
    return render(request, 'insta/wordcloud.html')

def map(request):
    places = Insta.objects.exclude(place='').values('place')
    places_df = pd.DataFrame(places)
    makeMap(places_df)
    return render(request, 'insta/map.html')