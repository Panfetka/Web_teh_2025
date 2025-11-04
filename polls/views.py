from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views import View
from django.views.generic import TemplateView

# class IndexView(View):
#     ...

MOCK_QUESTIONS = [
    {"id": 1,
     "text": "Is it true that Makan is going to the army?",
     "description": "No official statements, announcements, or credible news reports confirm this claim.",
     "avatar": "avatar1.jpg",
     "likes": 5,
     "answers": 3,
     "tags": ["black-jack", "bender"]
     },

    {"id": 2,
     "text": "How to build a moon park?",
     "description": "Lorem ipsum dolor sit, amet consectetur adipisicing elit. Esse possimus minima officiis iure? Commodi illo quibusdam voluptates accusantium id deleniti natus nobis explicabo tempore? Porro, assumenda. Rem cumque dignissimos sint.",
     "avatar": "avatar2.jpg",
     "likes": 5,
     "answers": 3,
     "tags": ["black-jack", "bender"]
     },

    {"id": 3,
     "text": "How to build a moon park?",
     "description": "Lorem ipsum dolor sit, amet consectetur adipisicing elit. Esse possimus minima officiis iure? Commodi illo quibusdam voluptates accusantium id deleniti natus nobis explicabo tempore? Porro, assumenda. Rem cumque dignissimos sint.",
     "avatar": "avatar3.jpg",
     "likes": 5,
     "answers": 3,
     "tags": ["black-jack", "bender"],
     },

    {"id": 4,
     "text": "How to build a moon park?",
     "description": "Lorem ipsum dolor sit, amet consectetur adipisicing elit. Esse possimus minima officiis iure? Commodi illo quibusdam voluptates accusantium id deleniti natus nobis explicabo tempore? Porro, assumenda. Rem cumque dignissimos sint.",
     "avatar": "avatar4.jpg",
     "likes": 5,
     "answers": 3,
     "tags": ["black-jack", "bender"]
     }
]


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

# def index_view(request):
#     return render(request, "./public/index.html", context={"question_list": MOCK_QUESTIONS})

def index_view(request):
     questions = MOCK_QUESTIONS
     page_obj = paginate(questions, request, 2)
     return render(request, "public/index.html", {"page_obj": page_obj})

# def question_view(request):
#     return render(request, "public/question.html", context={"question": MOCK_QUESTIONS[0]})

def question_view(request, question_id):
       question = next((q for q in MOCK_QUESTIONS if q['id'] == question_id), MOCK_QUESTIONS[0])
       answers = [
        {"id": 1, "text": "No official statements confirm this claim.", "author": "Mr. Freeman", "likes": 15},
        {"id": 2, "text": "According to my sources, this is just a rumor.", "author": "Dr. House", "likes": 8},
        {"id": 3, "text": "This information needs verification.", "author": "Expert", "likes": 12},
        {"id": 4, "text": "I can confirm this is false.", "author": "Insider", "likes": 20},
        {"id": 5, "text": "More research is needed on this topic.", "author": "Researcher", "likes": 6},
       ]
       page_obj = paginate(answers, request, 2)
       return render(request, "public/question.html", {
             "question": question,
             "answers": page_obj
       })


def hot_questions(request):
      questions = MOCK_QUESTIONS
      page_obj = paginate(questions, request, 2)
      return render(request, "public/hot_questions.html", {"question_list": page_obj})


def tag_questions(request, tag):
      questions = [q for q in MOCK_QUESTIONS if tag in q.get('tags', [])]
      page_obj = paginate(questions, request, 2)
      return render(request, "public/tag_questions.html", {
      "question_list": page_obj,
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