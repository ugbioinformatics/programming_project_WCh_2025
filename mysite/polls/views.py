from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def detail(request):
    return HttpResponse("Hello, world. You're at the polls detail.")

def results(request):
    return HttpResponse("Hello, world. You're at the polls results.")

def vote(request):
    return HttpResponse("Hello, world. You're at the polls vote.")
