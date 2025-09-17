from django.db import models
from users.models import Doctor, Level, Student

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
    
    class StatusChoices (models.TextChoices) :
        PENDING = "PENDING", "PENDING"
        ACTIVE = "ACTIVE", "ACTIVE"
    
    status = models.CharField(
        choices=StatusChoices.choices,
        max_length=10,
        default=StatusChoices.PENDING
    )

    start_solve = models.BooleanField(default=False, null=True, blank=True)
    
    class SolveStatusChoices(models.TextChoices) :
        NOT_STARTED = "NOT_STARTED", "NOT_STARTED"
        IN_PROGRESS = "IN_PROGRESS", "IN_PROGRESS"
        COMPLETED = "COMPLETED", "COMPLETED"
    
    solve_status = models.CharField(
        choices=SolveStatusChoices.choices,
        max_length=15,
        default=SolveStatusChoices.NOT_STARTED
    )

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
    


class StudentDegrees(models.Model) : 
    student = models.ForeignKey(
        Student,
        related_name='student_degrees',
        on_delete=models.CASCADE   
    )

    exam = models.ForeignKey(
        Exam,
        related_name='st_degree_exams',
        on_delete=models.CASCADE
    )

    final_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student.full_name + " - " + self.exam.name
    
    class Meta:
        ordering = ['-created_at']