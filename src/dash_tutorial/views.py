from django.shortcuts import render
from django.http.response import HttpResponse
# Create your views here.

from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.views import APIView


from .as_dash import dispatcher

### dash ###

def dash(request, **kwargs):
    return HttpResponse(dispatcher(request))


@csrf_exempt
def dash_ajax(request):
    return HttpResponse(dispatcher(request), content_type='application/json')