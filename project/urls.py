from django.contrib import admin
from django.urls import include, re_path
from django.views.generic import RedirectView, TemplateView
from polls import views

urlpatterns = [
    re_path('admin/', admin.site.urls),
    re_path('polls/', include('polls.urls')),
    re_path(r'^$', RedirectView.as_view(url='/polls/')),
    re_path('question/<int:question_id>/', views.question_view, name='question_view'),
    # re_path('question/', question_view, name='question_view'),
    re_path('polls/settings.html', TemplateView.as_view(template_name='public/settings.html')),
    re_path('polls/login.html', TemplateView.as_view(template_name='public/login.html')),
    re_path('polls/register.html', TemplateView.as_view(template_name='public/register.html')),
]
