from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('hot/', views.hot_questions_view, name='hot_questions'),
    path('tag/<str:tag_name>/', views.tag_questions, name='tag_questions'),
    path('question/<int:question_id>/', views.question_view, name='question_detail'),
    path('question/<int:question_id>/answer/', views.add_answer_view, name='add_answer'),
]


