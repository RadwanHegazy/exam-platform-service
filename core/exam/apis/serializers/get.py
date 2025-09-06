from rest_framework import serializers
from exam.models import Exam


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