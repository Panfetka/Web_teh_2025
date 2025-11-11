from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView, TemplateView
from polls import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
    path(r'^$', RedirectView.as_view(url='/polls/')),
    path('question/<int:question_id>/', views.question_view, name='question_view'),
    # re_path('question/', question_view, name='question_view'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('settings/', views.settings_view, name='settings'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)