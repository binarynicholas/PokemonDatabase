from django.shortcuts import render
from django.http import HttpResponse

# root page: shows latest added Pokemon.

def index(request):
    return HttpResponse("Hello, world. It's ya POKEMON.")
