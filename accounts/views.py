# from django.shortcuts import render
# def login_view(request):
#     return render(request, "public/login.html")
#
# def signup_view(request):
#     return render(request, "public/register.html")
#
# def settings_view(request):
#     return render(request, "public/settings.html")

from django.shortcuts import render
from django.http import HttpResponse

def login_view(request):
    return render(request, "public/login.html")

def signup_view(request):
    return render(request, "public/register.html")

def settings_view(request):
    return render(request, "public/settings.html")