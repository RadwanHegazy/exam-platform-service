from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView
)

from rest_framework.permissions import IsAuthenticated
from users.permissions import IsStudent
from exam.apis.serializers import (
    ListExamSerializer,
    RetrieveExamSerializer
)
from exam.models import Exam


class ListExamAPI (ListAPIView) : 
    serializer_class = ListExamSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return Exam.objects.filter(
            level = self.request.user.student.level
        )

class RetrieveExamAPI (RetrieveAPIView) : 
    serializer_class = RetrieveExamSerializer
    permission_classes = [IsStudent]
    lookup_field = 'id'

    def get_queryset(self):
        return Exam.objects.filter(
            level = self.request.user.student.level
        )

