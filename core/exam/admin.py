from django.contrib import admin
from import_export.admin import ExportActionModelAdmin
from .resources import StudentDegreesResource
from .models import (
    Question,
    QuestionImages,
    Exam,
    StudentDegrees
)

@admin.register(Exam)
class ExamAdmin (admin.ModelAdmin) : 
    list_display = ['name','created_at','created_by','level']
    search_fields = ['name']
    list_filter = ['level']

@admin.register(StudentDegrees)
class ExamAdmin (ExportActionModelAdmin) : 
    list_display = ['student','exam','created_at','final_score']
    search_fields = ['student__full_name', 'exam__name']
    list_filter = ['student','exam', 'created_at', 'final_score']
    resource_classes = [StudentDegreesResource]

@admin.register(Question)
class ExamAdmin (admin.ModelAdmin) : 
    list_display = ['name','exam', 'created_at', 'updated_at','created_by']
    search_fields = ['name']
    list_filter = ['exam', 'created_by']
    
@admin.register(QuestionImages)
class ExamAdmin (admin.ModelAdmin) : 
    list_display = ['src','created_at']

