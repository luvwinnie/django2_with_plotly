from django.urls import re_path

from .views import dash, dash_ajax
# from . import dash # this loads the Dash app

urlpatterns = [
    re_path('^_dash-', dash_ajax),
    re_path('^', dash),
]

