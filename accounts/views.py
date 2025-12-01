from django.shortcuts import render
from django.http import HttpResponse
from polls.views import get_sidebar_data


def login_view(request):
    sidebar_data = get_sidebar_data()
    context = {**sidebar_data}
    return render(request, "public/login.html", context)


def signup_view(request):
    sidebar_data = get_sidebar_data()
    context = {**sidebar_data}
    return render(request, "public/register.html", context)


def ask_view(request):
    sidebar_data = get_sidebar_data()
    context = {**sidebar_data}
    return render(request, "public/ask.html", context)


def settings_view(request):
    sidebar_data = get_sidebar_data()
    context = {**sidebar_data}
    return render(request, "public/settings.html", context)