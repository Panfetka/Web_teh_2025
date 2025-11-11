from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from polls.models import Question, Answer, Tag, Profile, QuestionLike, QuestionTag, AnswerLike
from faker import Faker
import random
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Fill database with test data'

    def add_arguments(self, parser):
        parser.add_argument('--ratio', type=int, default=1, help='Multiplication ratio for data volume')
    def handle(self, *args, **options):
        ratio = options["ratio"]

        self.stdout.write('Starting database filling...')

        users = self.create_users(10000 * ratio)
        tags = self.create_tags(10000 * ratio)
        questions = self.create_questions(100000 * ratio, users, tags)
        answers = self.create_answers(1000000 * ratio, users, questions)
        self.create_question_likes(1400000 * ratio, users, questions)
        self.create_answer_likes(600000 * ratio, users, answers)
        self.stdout.write(self.style.SUCCESS('Database filled successfully!'))

    def create_users(self, count):
        self.stdout.write(f'Creating {count} users...')

        users_to_create = []
        profiles_to_create = []

        for i in range(10_000):
            username = f"z_test_user{i}"
            email = f"z_test_user{i}@m.ru"
            user = User(email=email, username=username)
            users_to_create.append(user)

        created_users = User.objects.bulk_create(users_to_create, batch_size=1000)
        print(f"Было создано {len(created_users)} пользователей")

        for user in created_users:
            profile = Profile(user=user)
            profiles_to_create.append(profile)

        Profile.objects.bulk_create(profiles_to_create, batch_size=1000)
        self.stdout.write(f'Created {count} users and profiles')
        return list(created_users)

    def create_tags(self, count):
        self.stdout.write(f'Creating {count} tags...')

        fake = Faker()
        tags_to_create = []

        for i in range(count):
            name = f"tag_{i}_{fake.word()}"[:50]
            tag = Tag(name=name)
            tags_to_create.append(tag)

        created_tags = Tag.objects.bulk_create(tags_to_create, batch_size=1000)
        self.stdout.write(f'Created {count} tags')

        return list(created_tags)

    def create_questions(self, count, users, tags):
        self.stdout.write(f'Creating {count} questions...')

        fake = Faker()
        questions_to_create = []
        question_tags_to_create = []

        for i in range(count):
            author = random.choice(users)
            title = fake.sentence()[:255]
            description = fake.text(max_nb_chars=2000)

            question = Question(
                title=title,
                description=description,
                author=author,
                created_at=timezone.now() - timedelta(days=random.randint(0, 365)),
                views_count=random.randint(0, 1000),
                is_closed=random.random() < 0.1
            )
            questions_to_create.append(question)

        created_questions = Question.objects.bulk_create(questions_to_create, batch_size=1000)

        self.stdout.write('Adding tags to questions...')
        for question in created_questions:
            question_tags = random.sample(tags, random.randint(1, 5))
            for tag in question_tags:
                question_tag = QuestionTag(question=question, tag=tag)
                question_tags_to_create.append(question_tag)

        QuestionTag.objects.bulk_create(question_tags_to_create, batch_size=1000)
        self.update_tag_usage_counts(tags)

        self.stdout.write(f'Created {count} questions')
        return list(created_questions)

    def update_tag_usage_counts(self, tags):
        self.stdout.write('Updating tag usage counts...')
        for tag in tags:
            tag.usage_count = QuestionTag.objects.filter(tag=tag).count()

        Tag.objects.bulk_update(tags, ['usage_count'], batch_size=1000)

    def create_answers(self, count, users, questions):
        self.stdout.write(f'Creating {count} answers...')

        fake = Faker()
        answers_to_create = []

        for i in range(count):
            author = random.choice(users)
            question = random.choice(questions)
            text = fake.text(max_nb_chars=1000)

            answer = Answer(
                text=text,
                author=author,
                question=question,
                is_correct=random.random() < 0.05,
                is_accepted=random.random() < 0.03,
                created_at=timezone.now() - timedelta(days=random.randint(0, 365))
            )
            answers_to_create.append(answer)

        created_answers = Answer.objects.bulk_create(answers_to_create, batch_size=1000)

        self.stdout.write('Updating answers count in questions...')
        for question in questions:
            question.answers_count = Answer.objects.filter(question=question).count()

        Question.objects.bulk_update(questions, ['answers_count'], batch_size=1000)

        self.stdout.write(f'Created {count} answers')
        return list(created_answers)

    def create_question_likes(self, count, users, questions):
        self.stdout.write(f'Creating {count} question likes...')

        likes_to_create = []
        existing_likes = set()

        for i in range(count):
            user = random.choice(users)
            question = random.choice(questions)

            like_key = (user.id, question.id)
            if like_key in existing_likes:
                continue

            existing_likes.add(like_key)

            like = QuestionLike(
                question=question,
                user=user,
                value=random.choice([1, -1]),
                created_at=timezone.now() - timedelta(days=random.randint(0, 365))
            )
            likes_to_create.append(like)

            if len(likes_to_create) >= 1000:
                QuestionLike.objects.bulk_create(likes_to_create, batch_size=1000)
                likes_to_create = []

        if likes_to_create:
            QuestionLike.objects.bulk_create(likes_to_create, batch_size=1000)

        self.stdout.write('Updating question likes count...')
        for question in questions:
            question.likes_count = QuestionLike.objects.filter(question=question).count()

        Question.objects.bulk_update(questions, ['likes_count'], batch_size=1000)

        self.stdout.write(f'Created {count} question likes')

    def create_answer_likes(self, count, users, answers):
        self.stdout.write(f'Creating {count} answer likes...')

        likes_to_create = []
        existing_likes = set()

        for i in range(count):
            user = random.choice(users)
            answer = random.choice(answers)

            like_key = (user.id, answer.id)
            if like_key in existing_likes:
                continue

            existing_likes.add(like_key)

            like = AnswerLike(
                answer=answer,
                user=user,
                value=random.choice([1, -1]),
                created_at=timezone.now() - timedelta(days=random.randint(0, 365))
            )
            likes_to_create.append(like)

            if len(likes_to_create) >= 1000:
                AnswerLike.objects.bulk_create(likes_to_create, batch_size=1000)
                likes_to_create = []

        if likes_to_create:
            AnswerLike.objects.bulk_create(likes_to_create, batch_size=1000)

        self.stdout.write('Updating answer likes count...')
        for answer in answers:
            answer.likes_count = AnswerLike.objects.filter(answer=answer).count()

        Answer.objects.bulk_update(answers, ['likes_count'], batch_size=1000)

        self.stdout.write(f'Created {count} answer likes')
