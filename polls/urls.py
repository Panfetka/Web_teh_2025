from django.urls import include, re_path
from polls.views import index_view, question_view

# urlpatterns = [
#     # re_path(r'^', index_view, name="index_question_view"),
#     re_path('', index_view, name="index_question_view"),
#     re_path('question.html', question_view, name='question_view'),
# ]


from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('hot/', views.hot_questions, name='hot_questions'),
    path('tag/<str:tag>/', views.tag_questions, name='tag_questions'),
    path('question/<int:question_id>/', views.question_view, name='question_detail'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('ask/', views.ask_view, name='ask'),
    path('settings/', views.settings_view, name='settings'),
]

