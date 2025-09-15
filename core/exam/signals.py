from exam.apis.serializers.get import QuestionSerializer
from .models import Exam, Question
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache

@receiver(post_save, sender=Exam)
def update_exam_cache(sender, instance : Exam, **kwargs):
    cache_key = f'exam_{instance.id}'
    cache.set(cache_key, instance, None)

    cache.set(
        f'level_{instance.level.id}',
        Exam.objects.filter(level=instance.level),
        None
    )

@receiver(post_save, sender=Question)
def set_exam_qs(sender, instance, **kwargs):
    exam = instance.exam
    cache_key = f'exam_{exam.id}_qs'
    # cached_exam = cache.get(cache_key)
    cache.set(
        cache_key,
        Question.objects.filter(exam=instance.exam)
    )
    # current_qs = QuestionSerializer(instance).data
    # if cached_exam:
    #     cache.set(cache_key, [
    #         current_qs
    #     ], None) 
    # else:
    #     cached_exam.append(current_qs)
    #     cache.set(cache_key, cached_exam, None)