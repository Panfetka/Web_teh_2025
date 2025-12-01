from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .managers import QuestionManager
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True)
    reputation = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    usage_count = models.IntegerField(default=0, db_index=True, help_text="Денормализованное поле. Количество использований тега. Обновляется автоматически."
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        indexes = [
            models.Index(fields=['-usage_count'], name='idx_popular_tags'),
        ]

    def __str__(self):
        return self.name


# class QuestionManager(models.Manager):
#     def new_questions(self):
#         return self.order_by('-created_at')
#
#     def hot_questions(self):
#         return self.order_by('-likes_count', '-created_at')
#
#     def by_tag(self, tag_name):
#         return self.filter(tags__name=tag_name)


class Question(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    tags = models.ManyToManyField(Tag, related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    views_count = models.IntegerField(default=0, help_text="Денормализованное поле. Количество просмотров.")
    answers_count = models.IntegerField(default=0, db_index=True, help_text="Денормализованное поле. Количество ответов. Используйте Question.answers.count() для точного подсчета.")
    likes_count = models.IntegerField(default=0, db_index=True, help_text="Денормализованное поле. Количество лайков. Используйте Question.question_likes.count() для точного подсчета.")
    is_closed = models.BooleanField(default=False)

    objects = QuestionManager()

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        indexes = [
            models.Index(fields=['-created_at'], name='idx_created_at_desc'),
            models.Index(fields=['-likes_count', '-created_at'], name='idx_hot_questions'),
            models.Index(fields=['-answers_count', '-created_at'], name='idx_popular_questions'),
            models.Index(fields=['author', '-created_at'], name='idx_user_questions'),
        ]

    def __str__(self):
        return self.title

    def update_answers_count(self):
        self.answers_count = self.answers.count()
        self.save(update_fields=['answers_count'])

    def update_likes_count(self):
        self.likes_count = self.question_likes.count()
        self.save(update_fields=['likes_count'])

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('question_detail', kwargs={'question_id': self.id})


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    likes_count = models.IntegerField(default=0, help_text="Денормализованное поле. Количество лайков. Используйте Answer.answer_likes.count() для точного подсчета.")
    is_correct = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-is_accepted', '-is_correct', '-likes_count', 'created_at']
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"
        indexes = [
            models.Index(fields=['question', '-created_at'], name='idx_question_answers'),
            models.Index(fields=['-is_accepted', '-created_at'], name='idx_accepted_answers'),
            models.Index(fields=['-likes_count', 'created_at'], name='idx_popular_answers'),
            models.Index(fields=['author', '-created_at'], name='idx_user_answers'),
        ]

    def __str__(self):
        return f"Answer to: {self.question.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.question.update_answers_count()

    def update_likes_count(self):
        self.likes_count = self.answer_likes.count()
        self.save(update_fields=['likes_count'])


class QuestionLike(models.Model):
    class LikeValue(models.IntegerChoices):
        LIKE = 1, 'Like'
        DISLIKE = -1, 'Dislike'

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_likes')
    value = models.SmallIntegerField(choices=[(1, 'Like'), (-1, 'Dislike')])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['question', 'user'], name='unique_question_like')
        ]

    def __str__(self):
        return f"{self.user.username} {'liked' if self.value == 1 else 'disliked'} question {self.question.id}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.question.update_likes_count()

    def clean(self):
        if self.value not in [1, -1]:
            raise ValidationError('Value must be 1 (like) or -1 (dislike)')


class AnswerLike(models.Model):
    class LikeValue(models.IntegerChoices):
        LIKE = 1, 'Like'
        DISLIKE = -1, 'Dislike'

    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='answer_likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer_likes')
    value = models.SmallIntegerField(choices=[(1, 'Like'), (-1, 'Dislike')])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['answer', 'user'], name='unique_answer_like')
        ]

    def __str__(self):
        return f"{self.user.username} {'liked' if self.value == 1 else 'disliked'} answer {self.answer.id}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Обновляем счетчик лайков в ответе
        self.answer.update_likes_count()

    def clean(self):
        if self.value not in [1, -1]:
            raise ValidationError('Value must be 1 (like) or -1 (dislike)')


# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()