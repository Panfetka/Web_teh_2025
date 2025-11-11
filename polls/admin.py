from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile, Tag, QuestionTag, Answer, AnswerLike, QuestionLike, Question, QuestionManager

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    fields = ['avatar', 'bio', 'reputation', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']

class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'get_reputation']
    list_select_related = ['profile']

    def get_reputation(self, instance):
        return instance.profile.reputation

    get_reputation.short_description = 'Reputation'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

@admin.register(Profile)
class ProfileAdmine(admin.ModelAdmin):
    list_display = ['user', 'reputation', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'bio']
    readonly_fields = ['created_at', 'updated_at']
    fields = ['user', 'avatar', 'bio', 'reputation', 'created_at', 'updated_at']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'usage_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']
    readonly_fields = ['created_at', 'usage_count']
    fields = ['name', 'description', 'usage_count', 'created_at']

class QuestionTagInline(admin.TabularInline):
    model = QuestionTag
    extra = 1
    verbose_name = 'Tag'
    verbose_name_plural = 'Tags'

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1
    fields = ['author', 'text', 'is_correct', 'is_accepted', 'likes_count', 'created_at']
    readonly_fields = ['created_at', 'likes_count']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'answers_count', 'likes_count', 'views_count', 'is_closed']
    list_filter = ['created_at', 'is_closed', 'tags']
    search_fields = ['title', 'description', 'author__username']
    readonly_fields = ['created_at', 'updated_at', 'views_count', 'answers_count', 'likes_count']

    #autocomplete_fields = ['author']
    raw_id_fields = ['author']

    fields = [
        'title', 'description', 'author',
        'views_count', 'answers_count', 'likes_count',
        'is_closed', 'created_at', 'updated_at'
    ]
    inlines = [QuestionTagInline, AnswerInline]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author').prefetch_related('tags')

@admin.register(QuestionTag)
class QuestionTagAdmin(admin.ModelAdmin):
    list_display = ['question', 'tag']
    list_filter = ['tag']
    search_fields = ['question__title', 'tag__name']


@admin.register(QuestionLike)
class QuestionLikeAdmin(admin.ModelAdmin):
    list_display = ['question', 'user', 'value', 'created_at']
    list_filter = ['value', 'created_at']
    search_fields = ['question__title', 'user__username']
    readonly_fields = ['created_at']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('question', 'user')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['truncated_text', 'question', 'author', 'created_at', 'is_correct', 'is_accepted', 'likes_count']
    list_filter = ['created_at', 'is_correct', 'is_accepted']
    search_fields = ['text', 'author__username', 'question__title']
    readonly_fields = ['created_at', 'updated_at', 'likes_count']
    list_editable = ['is_correct', 'is_accepted']
    #autocomplete_fields = ['author', 'question']
    raw_id_fields = ['author']

    def truncated_text(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text

    truncated_text.short_description = 'Text'

    fields = [
        'question', 'author', 'text',
        'is_correct', 'is_accepted', 'likes_count',
        'created_at', 'updated_at'
    ]

@admin.register(AnswerLike)
class AnswerLikeAdmin(admin.ModelAdmin):
    list_display = ['answer', 'user', 'value', 'created_at']
    list_filter = ['value', 'created_at']
    search_fields = ['answer__text', 'user__username']
    readonly_fields = ['created_at']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('answer', 'user')