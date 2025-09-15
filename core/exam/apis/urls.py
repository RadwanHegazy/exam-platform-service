from django.urls import path
from .views import get

urlpatterns = [
    path('get/v1/', get.ListExamAPI.as_view(), name='list-exams'),
    path('get/v1/<int:id>/', get.RetrieveExamAPI.as_view(), name='retrieve-exam'),
    path('get/qs/v1/<int:exam_id>/', get.ListExamQuestionsAPI.as_view(), name='exam-qs'),
]