from django.db import models
from users.models import Doctor, Level
from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

class Exam (models.Model) : 
    name = models.CharField(max_length=225)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_score = models.IntegerField()
    created_by = models.ForeignKey(
        Doctor,
        related_name='doc_exam',
        on_delete=models.CASCADE
    )
    level = models.ForeignKey(
        Level,
        related_name='exam_level',
        on_delete=models.CASCADE
    )
    time_in_hours = models.FloatField()

    def __str__(self):
        return self.name

class QuestionImages (models.Model) : 
    src = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)

class Question (models.Model) : 
    name = models.TextField()
    choice_a = models.CharField(max_length=225)
    choice_b = models.CharField(max_length=225)
    choice_c = models.CharField(max_length=225)
    choice_d = models.CharField(max_length=225)
    
    class CorrectChoice (models.TextChoices) : 
        A = "A", "A"
        B = "B", "B"
        C = "C", "C"
        D = "D", "D"
    
    correct = models.CharField(
        choices = CorrectChoice.choices,
        max_length=1
    )

    images = models.ManyToManyField(
        QuestionImages,
        related_name='qs_imgs',
        blank=True
    )

    exam = models.ForeignKey(
        Exam,
        related_name='qs_exam',
        on_delete=models.CASCADE
    )

    created_by = models.ForeignKey(
        Doctor,
        related_name='qs_doc',
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

@receiver(post_save, sender=Exam)
def update_exam_cache(sender, instance, **kwargs):
    from exam.apis.serializers.get import RetrieveExamSerializer
    cache_key = f'exam_{instance.id}'
    value = RetrieveExamSerializer(instance)
    cache.set(cache_key, value.data, None)


@receiver(post_save, sender=Question)
def set_exam_qs(sender, instance, **kwargs):
    from exam.apis.serializers.get import QuestionSerializer
    exam = instance.exam
    cache_key = f'exam_{exam.id}_qs'
    cached_exam = cache.get(cache_key)
    current_qs = QuestionSerializer(instance).data
    if cached_exam:
        cache.set(cache_key, [
            current_qs
        ], None) 
    else:
        cached_exam.append(current_qs)
        cache.set(cache_key, cached_exam, None)