from rest_framework.permissions import IsAuthenticated
from .models import Student

class IsStudent (IsAuthenticated) : 
    def has_permission(self, request, view):
        return super().has_permission(request, view) and hasattr(request.user, 'student')