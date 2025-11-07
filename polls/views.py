from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views import View
from django.views.generic import TemplateView

# class IndexView(View):
#     ...

MOCK_QUESTIONS = [
    {"id": 1,
     "title": "Is it true that Makan is going to the army?",
     "description": "No official statements, announcements, or credible news reports confirm this claim.",
     "avatar": "avatar1.jpg",
     "likes": 5,
     "tags": ["black-jack", "bender"]
     },

    {"id": 2,
     "title": "How to build a moon park?",
     "description": "Lorem ipsum dolor sit, amet consectetur adipisicing elit. Esse possimus minima officiis iure? Commodi illo quibusdam voluptates accusantium id deleniti natus nobis explicabo tempore? Porro, assumenda. Rem cumque dignissimos sint.",
     "avatar": "avatar2.jpg",
     "likes": 5,
     "tags": ["black-jack", "bender"]
     },

    {"id": 3,
     "title": "How to build a moon park?",
     "description": "Lorem ipsum dolor sit, amet consectetur adipisicing elit. Esse possimus minima officiis iure? Commodi illo quibusdam voluptates accusantium id deleniti natus nobis explicabo tempore? Porro, assumenda. Rem cumque dignissimos sint.",
     "avatar": "avatar3.jpg",
     "likes": 5,
     "tags": ["black-jack", "bender"],
     },

    {"id": 4,
     "title": "How to build a moon park?",
     "description": "Lorem ipsum dolor sit, amet consectetur adipisicing elit. Esse possimus minima officiis iure? Commodi illo quibusdam voluptates accusantium id deleniti natus nobis explicabo tempore? Porro, assumenda. Rem cumque dignissimos sint.",
     "avatar": "avatar4.jpg",
     "likes": 5,
     "tags": ["black-jack", "bender"]
     }
]


MOCK_ANSWERS = [
    {
        "id": 1,
        "question_id": 1,
        "text": "No official statements confirm this claim. The information appears to be circulating on social media without reliable sources.",
        "avatar": "avatars/expert1.jpg",
        "likes": 15,
        "is_correct": True,
        "author": "Mr. Freeman",
        "created_date": "2024-01-15"
    },
    {
        "id": 2,
        "question_id": 1,
        "text": "According to my sources in the ministry, this is just a rumor that has been spreading recently.",
        "avatar": "avatars/expert2.jpg",
        "likes": 8,
        "is_correct": False,
        "author": "Dr. House",
        "created_date": "2024-01-15"
    },
    {
        "id": 3,
        "question_id": 2,
        "text": "Building a moon park requires extensive planning and international cooperation. First, you need to consider...",
        "avatar": "avatars/space_expert.jpg",
        "likes": 12,
        "is_correct": True,
        "author": "Space Expert",
        "created_date": "2024-01-14"
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
     # questions = MOCK_QUESTIONS
     questions = get_questions_with_answers_count()
     page_obj = paginate(questions, request, 2)
     return render(request, "public/index.html", {"page_obj": page_obj})

# def question_view(request):
#     return render(request, "public/question.html", context={"question": MOCK_QUESTIONS[0]})

def question_view(request, question_id):
    question = next((q for q in MOCK_QUESTIONS if q['id'] == question_id), None)

    if not question:
        question = MOCK_QUESTIONS[0]

    # answers = [a for a in MOCK_ANSWERS if a['question_id'] == question_id]
    question_with_count = enrich_question_with_answers_count(question)
    answers = get_answers_for_question(question_id)

    return render(request, "public/question.html", {
        "question": question_with_count,
        "answers": answers
    })


def hot_questions(request):
      # questions = MOCK_QUESTIONS
      questions = get_questions_with_answers_count()
      hot_questions = sorted(questions, key=lambda x: (x['answers_count'], x['likes']), reverse=True)
      page_obj = paginate(hot_questions, request, 2)
      return render(request, "public/hot_questions.html", {"question_list": page_obj})


def tag_questions(request, tag):
      questions = [q for q in MOCK_QUESTIONS if tag in q.get('tags', [])]
      questions_with_counts = [enrich_question_with_answers_count(q) for q in questions]
      page_obj = paginate(questions_with_counts, request, 2)
      return render(request, "public/tag_questions.html", {
      "page_obj": page_obj,
      "tag": tag
      })

def get_answers_count(question_id):
    return len([a for a in MOCK_ANSWERS if a['question_id'] == question_id])

def get_answers_for_question(question_id):
    return [a for a in MOCK_ANSWERS if a['question_id'] == question_id]

def enrich_question_with_answers_count(question):
    question = question.copy()
    question['answers_count'] = get_answers_count(question['id'])
    return question

def get_questions_with_answers_count():
    return [enrich_question_with_answers_count(q) for q in MOCK_QUESTIONS]

def login_view(request):
      return render(request, "public/login.html")


def signup_view(request):
     return render(request, "public/register.html")


def ask_view(request):
     return render(request, "public/ask.html")

def settings_view(request):
    return render(request, "public/settings.html")