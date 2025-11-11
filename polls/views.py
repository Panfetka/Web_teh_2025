from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views import View
from django.views.generic import TemplateView
from .models import Question, Answer, Tag
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page = request.GET.get('page', 1)

    try:
        objects_page = paginator.page(page)
    except PageNotAnInteger:
        objects_page = paginator.page(1)
    except EmptyPage:
        objects_page = paginator.page(paginator.num_pages)

    return objects_page


def index_view(request):
     questions = Question.objects.new_questions()
     page_obj = paginate(questions, request, 10)
     return render(request, "public/index.html", {"page_obj": page_obj})


def question_view(request, question_id):
    question = get_object_or_404(Question.objects.select_related('author').prefetch_related('tags'), id=question_id)
    answers = Answer.objects.filter(question=question).select_related('author').order_by('-is_accepted', '-is_correct', '-likes_count')

    return render(request, "public/question.html", {
        "question": question,
        "answers": answers
    })


def hot_questions(request):
      questions = Question.objects.hot_questions()
      page_obj = paginate(questions, request, 10)
      return render(request, "public/hot_questions.html", {"page_obj": page_obj})


def tag_questions(request, tag):
      questions = Question.objects.by_tag(tag)
      page_obj = paginate(questions, request, 10)
      return render(request, "public/tag_questions.html", {
      "page_obj": page_obj,
      "tag": tag
      })

def login_view(request):
      return render(request, "public/login.html")


def signup_view(request):
     return render(request, "public/register.html")


def ask_view(request):
     return render(request, "public/ask.html")

def settings_view(request):
    return render(request, "public/settings.html")