from django.shortcuts import render, redirect
import math
import requests
requests.packages.urllib3.disable_warnings()
from bs4 import BeautifulSoup
from .models import Headline, UserProfile
import shutil
import os
from datetime import timedelta, timezone, datetime

def news_list(request):
    # user can only scrape once every 24 hours
    user_p = UserProfile.objects.filter(user=request.user).first()
    now = datetime.now(timezone.utc)
    time_difference = now - user_p.last_scrape
    time_difference_in_hours = time_difference / timedelta(minutes=60)
    next_scrape = 24 - time_difference_in_hours

    if time_difference_in_hours <= 24:
        hide_me = True
    else:
        hide_me = False

    headlines = Headline.objects.all()
    context = {
        'object_list': headlines,
        'hide_me': hide_me,
        'next_scrape': math.ceil(next_scrape)
    }
    return render(request, "news/home.html", context)

def scrape(request):
    user_p = UserProfile.objects.filter(user=request.user).first()
    print(user_p)
    user_p.last_scrape = datetime.now(timezone.utc)
    user_p.save()

    session = requests.Session()
    session.headers = {
        "User-Agent": "Mozilla/5,0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36"}
    url = "https://www.theonion.com"
    content = session.get(url, verify=False).content

    soup = BeautifulSoup(content, "html.parser")

    posts = soup.find_all(
        'div', {'class': 'curation-module__zone'})  # return a list

    for i in posts:
        link = i.find_all('a', {'class': 'js_curation-click'})[1]['href']
        title = i.find_all('a', {'class': 'js_curation-click'})[1].text
        image_source = i.find(
            'img', {'class': 'featured-image'})['data-src']
        
        if not image_source.startswith(("data:image", "javascript")):
            media_root = '/Users/cheesiang_leow/practice_django/dashboard/media_root'
            local_filename = image_source.split('/')[-1].split("?")[0]
            r = session.get(image_source, stream=True, verify=False)
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    f.write(chunk)

            current_image_absolute_path = os.path.abspath(local_filename)
            shutil.move(current_image_absolute_path, media_root)

        new_headline = Headline()
        new_headline.title = title
        new_headline.url = link
        new_headline.image = local_filename
        new_headline.save()
    return redirect('/home/')

