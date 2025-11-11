from django.db import models
from django.db.models import Count
class QuestionManager(models.Manager):
    def new_questions(self):
        # return self.order_by('-created_at')
        return self.get_queryset().select_related('author').prefetch_related('tags') \
            .order_by('-created_at')

    def hot_questions(self):
        # return self.order_by('-likes_count', '-created_at')
        return self.get_queryset().select_related('author').prefetch_related('tags') \
            .order_by('-likes_count', '-answers_count', '-created_at')

    def by_tag(self, tag_name):
        return self.get_queryset().filter(tags__name=tag_name) \
            .select_related('author').prefetch_related('tags')

    def with_answers_count(self):
        return self.get_queryset().annotate(
            actual_answers_count=Count('answers')
        )

    def popular_tags(self, limit=10):
        from .models import Tag
        return Tag.objects.annotate(
            question_count=Count('questions')
        ).order_by('-question_count')[:limit]

    def popular_questions(self):
        return self.get_queryset().select_related('author').prefetch_related('tags') \
            .order_by('-answers_count', '-created_at')

    def user_questions(self, user):
        return self.get_queryset().filter(author=user) \
            .select_related('author').prefetch_related('tags')