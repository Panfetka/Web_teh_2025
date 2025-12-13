# from django.contrib import admin
# from django.urls import include, path
# from django.views.generic import RedirectView, TemplateView
# from polls import views
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('polls/', include('polls.urls')),
#     path(r'^$', RedirectView.as_view(url='/polls/')),
#     path('question/<int:question_id>/', views.question_view, name='question_view'),
#     # re_path('question/', question_view, name='question_view'),
#     path('login/', views.login_view, name='login'),
#     path('signup/', views.signup_view, name='signup'),
#     path('settings/', views.settings_view, name='settings'),
# ]


from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from polls import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('', RedirectView.as_view(url='/polls/')),
    path('question/<int:question_id>/', views.question_view, name='question_view'),

]