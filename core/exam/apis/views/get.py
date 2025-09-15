from exam.apis.serializers.get import QuestionSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView
)
from users.permissions import IsStudent
from exam.apis.serializers import (
    ListExamSerializer,
    RetrieveExamSerializer
)
from exam.models import Exam
from django.core.cache import cache

class ListExamAPI (ListAPIView) : 
    serializer_class = ListExamSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        querset = cache.get(
            f'level_{self.request.user.student.level.id}'
        )

        if querset:
            return querset
        
        return Exam.objects.filter(
            level = self.request.user.student.level
        )

class RetrieveExamAPI (RetrieveAPIView) : 
    serializer_class = RetrieveExamSerializer
    permission_classes = [IsStudent]
    lookup_field = 'id'

    def get_object(self):
        return self.get_queryset()

    def get_queryset(self):
        queryset = cache.get(
            f'exam_{self.kwargs["id"]}'
        )
        
        if not queryset:
            get_object_or_404(Exam, id=self.kwargs['id'])
        
        return queryset

class ListExamQuestionsAPI (APIView) : 
    permission_classes = [IsStudent]

    def get(self, request, exam_id) : 
        exam_qs = cache.get(f'exam_{exam_id}_qs')
        
        if not exam_qs : 
            return Response({
                'message' : 'not found'
            }, status=404)
        
        serializer = QuestionSerializer(exam_qs, many=True)
        return Response(serializer.data, status=200)
