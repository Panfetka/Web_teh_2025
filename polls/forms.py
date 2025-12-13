from django import forms
from polls.models import Question, Answer, Tag


class QuestionForm(forms.ModelForm):
    tags_input = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'python, django, web-development'
        }),
        help_text='Enter tags separated by commas'
    )

    class Meta:
        model = Question
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Title of your question'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Detailed description of your question',
                'rows': 10
            })
        }
        labels = {
            'description': 'Question Text'
        }

    def save(self, commit=True, author=None):
        question = super().save(commit=False)
        if author:
            question.author = author

        if commit:
            question.save()

            # Обрабатываем теги
            tags_str = self.cleaned_data.get('tags_input', '')
            if tags_str:
                tag_names = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    question.tags.add(tag)
                    if created:
                        tag.usage_count = 1
                    else:
                        tag.usage_count += 1
                    tag.save()

        return question


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your answer here...',
                'rows': 6
            })
        }

    def save(self, commit=True, author=None, question=None):
        answer = super().save(commit=False)
        if author:
            answer.author = author
        if question:
            answer.question = question
        if commit:
            answer.save()
        return answer