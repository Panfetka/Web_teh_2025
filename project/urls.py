from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from polls import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
    path('accounts/', include('accounts.urls')),
    re_path(r'^$', RedirectView.as_view(url='/polls/')),
    path('question/<int:question_id>/', views.question_view, name='question_view'),

]
