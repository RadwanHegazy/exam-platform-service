from django.contrib import admin
from .models import (
    Question,
    QuestionImages,
    Exam
)

@admin.register(Exam)
class ExamAdmin (admin.ModelAdmin) : 
    list_display = ['name','created_at','created_by','level']
    search_fields = ['name']
    list_filter = ['level']

@admin.register(Question)
class ExamAdmin (admin.ModelAdmin) : 
    list_display = ['name','exam', 'created_at', 'updated_at','created_by']
    search_fields = ['name']
    list_filter = ['exam', 'created_by']
    
@admin.register(QuestionImages)
class ExamAdmin (admin.ModelAdmin) : 
    list_display = ['src','created_at']

