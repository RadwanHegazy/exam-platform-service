from rest_framework import serializers
from exam.models import Exam, Question, QuestionImages


class ListExamSerializer (serializers.ModelSerializer) : 

    class Meta:
        model = Exam
        fields = [
            'id',
            'name',
            'level',
            'time_in_hours',
        ]


class RetrieveExamSerializer(serializers.ModelSerializer) : 

    class Meta:
        model = Exam
        fields = "__all__"


class QuestionImagesSerializer (serializers.ModelSerializer) :
    class Meta:
        model = QuestionImages
        fields = [
            'id',
            'src',
        ]

class QuestionSerializer (serializers.ModelSerializer) : 
    images = QuestionImagesSerializer(many=True, read_only=True)
    
    class Meta:
        model = Exam
        exclude = [
            'created_by',
            'created_at',
            'updated_at',
            'correct',
        ]