from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def home(request):
    return JsonResponse({
        'info': 'E-Commerce WebSite Using Django + ReactJS',
        'name': 'Ashutosh Jaiswal'
    })

