"""dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static

from news.views import scrape, news_list
from finance.views import company_article_list, ChartData, dash, dash_ajax

app_name = "notes"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('notes/', include('notepad.urls')),
    path('scrape/', scrape, name="scrape"),
    path('home/', news_list, name="home"),
    path('companies/', company_article_list, name="companies"),
    path('api/chart/data/', ChartData.as_view(), name="api-chart-data"),
    path('dash/', include('finance.urls')),
    # re_path('^_dash-', dash_ajax),
    # re_path('^', dash),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
