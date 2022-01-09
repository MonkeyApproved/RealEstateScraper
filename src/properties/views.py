from django.shortcuts import render
from django.http import HttpResponse


def help(request):
    return render(request, "help.html")


def igmo(request):
    return HttpResponse("Hi this is Igmo")
