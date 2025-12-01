from .models import Question, Answer, Tag
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count, Prefetch
from django.contrib.auth import get_user_model

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

def get_sidebar_data():
    popular_tags = Tag.objects.annotate(
        question_count=Count('questions')
    ).order_by('-question_count')[:10]

    User = get_user_model()
    best_members = User.objects.annotate(
        question_count=Count('questions'),
        answer_count=Count('answers')
    ).order_by('-question_count', '-answer_count')[:5]

    return {
        'popular_tags': popular_tags,
        'best_members': best_members,
    }

def index_view(request):
     questions = Question.objects.new_questions()
     page_obj = paginate(questions, request, 10)
     sidebar_data = get_sidebar_data()
     context = {
         "page_obj": page_obj,
         **sidebar_data
     }
     return render(request, "public/index.html", context)

def new_questions(self):
    return self.get_queryset().select_related('author', 'author_profile').prefetch_related('tags').order_by('-likes_count', '-created_at')

def hot_questions(self):
    return self.get_queryset().select_related('author', 'author__profile') \
            .prefetch_related('tags').order_by('-likes_count', '-created_at')

def by_tag(self, tag_name):
    return self.get_queryset().select_related('author', 'author__profile') \
            .prefetch_related('tags').filter(tags__name=tag_name) \
            .order_by('-created_at')

def tag_questions(request, tag_name):
    tag_obj = get_object_or_404(Tag, name=tag_name)

    questions = tag_obj.questions.all().select_related('author__profile')\
    .prefetch_related('tags').order_by('-created_at')
    page_obj = paginate(questions, request, 10)
    sidebar_data = get_sidebar_data()
    return render(request, "public/tag_questions.html", {
      "page_obj": page_obj,
      "tag": tag_name,
      "tag_obj": tag_obj,
      **sidebar_data
      })


def question_view(request, question_id):
    question = get_object_or_404(Question.objects.select_related('author_profile').prefetch_related('tags').prefetch_related(
            Prefetch(
                'answers',
                queryset=Answer.objects
                    .select_related('author__profile')
                    .order_by('-is_accepted', '-is_correct', '-likes_count')
            )
        ),
        id=question_id
    )

    answers = question.answers.all()
    answers_page = paginate(answers, request, 10)
    sidebar_data = get_sidebar_data()

    return render(request, "public/question.html", {
        "question": question,
        "answers": answers_page,
        "page_obj": answers_page,
        **sidebar_data
    })
