from rest_framework_simplejwt.views import TokenVerifyView
from django.urls import path
from .views.login import StudentLoginView

urlpatterns = [
    path('auth/student/login/v1/', StudentLoginView.as_view(), name='student-login'),
    path('auth/tokens/verify/v1/', TokenVerifyView.as_view(), name='token-verify'),
]