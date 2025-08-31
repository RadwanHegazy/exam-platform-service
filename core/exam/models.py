from django.db import models
from users.models import Doctor, Level


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

    def __init__(self, *args, **kwargs):
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