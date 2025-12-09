from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy


from polls.views import get_sidebar_data
from polls.forms import QuestionForm, AnswerForm
from .forms import LoginForm, SignupForm, ProfileEditForm
from polls.models import Question, Profile


def login_view(request):
    sidebar_data = get_sidebar_data()
    if request.user.is_authenticated:
        next_url = request.GET.get('continue', reverse('index'))
        return redirect(next_url)

    if request.method == "POST":
        form = LoginForm(data=request.POST)

        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user:
                auth.login(request, user)
                next_url = request.GET.get('continue', reverse('index'))
                return redirect(next_url)
            else:
                messages.error(request, "Неверный логин или пароль")
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме")
    else:
        form = LoginForm()

    context = {
        'form': form,
        'next_url': request.GET.get('continue', ''),
        **sidebar_data
    }
    return render(request, "public/login.html", context)


def signup_view(request):
    sidebar_data = get_sidebar_data()
    if request.user.is_authenticated:
        return redirect(reverse('index'))

    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect(reverse('index'))
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
    else:
        form = SignupForm()

    context = {
        'form': form,
        **sidebar_data
    }
    return render(request, "public/register.html", context)

def logout_view(request):
    next_url = request.GET.get('next', request.META.get('HTTP_REFERER', reverse('index')))
    auth.logout(request)
    return redirect(next_url)

@login_required(login_url=reverse_lazy('accounts:login'))
def ask_view(request):
    sidebar_data = get_sidebar_data()
    if request.method == "POST":

        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(author=request.user)
            messages.success(request, 'Вопрос успешно добавлен!')
            return redirect('question_detail', question_id=question.id)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
    else:
        form = QuestionForm()

    context = {
        'form': form,
        **sidebar_data
    }
    return render(request, "public/ask.html", context)

@login_required(login_url=reverse_lazy('accounts:login'))
def settings_view(request):
    sidebar_data = get_sidebar_data()
    profile, created = Profile.objects.get_or_create(user=request.user)
    if created:
        print(f"DEBUG: Created profile for user {request.user.username}")
    if request.method == "POST":
        form = ProfileEditForm(
            request.POST,
            request.FILES,
            user=request.user,
            instance=request.user.profile
        )

        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect(reverse('accounts:settings'))
            # return redirect('index')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
    else:
        form = ProfileEditForm(
            user=request.user,
            instance=request.user.profile
        )
    context = {
        'form': form,
        **sidebar_data
    }
    return render(request, "public/settings.html", context)

