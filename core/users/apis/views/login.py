from rest_framework.generics import CreateAPIView
from users.apis.serializers import StudentLoginSerializer

class StudentLoginView(CreateAPIView):
    serializer_class = StudentLoginSerializer
