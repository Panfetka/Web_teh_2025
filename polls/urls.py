from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('hot/', views.hot_questions, name='hot_questions'),
    path('tag/<str:tag>/', views.tag_questions, name='tag_questions'),
    path('question/<int:question_id>/', views.question_view, name='question_detail'),
    path('ask/', views.ask_view, name='ask'),
]

