from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def hello_todo_list(request):
    return HttpResponse("Hello, to-do list!")