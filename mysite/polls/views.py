from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def detail(request, question_id):
    return HttpResponse("Hello, world. You're at the polls detail. "+str(question_id))

def results(request, question_id):
    return HttpResponse("Hello, world. You're at the polls results. "+str(question_id))

def vote(request, question_id):
    return HttpResponse("Hello, world. You're at the polls vote. "+str(question_id))
