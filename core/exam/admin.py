from django.contrib import admin
from .models import (
    Question,
    QuestionImages,
    Exam
)

admin.site.register([
    QuestionImages,
    Question,
    Exam
])