from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import Student


class StudentLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    student = None

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        try:
            student = Student.objects.get(email=email)
        except Student.DoesNotExist:
            raise serializers.ValidationError({
                'message' : "Invalid email or password"
            })
        
        if not student.check_password(password):
            raise serializers.ValidationError({
                'message' : "Invalid email or password"
            })
        
        self.student = student
        return attrs
    
    def create(self, validated_data):
        return self.student
    
    def to_representation(self, instance):
        tokens = RefreshToken.for_user(instance)
        return {
            'refresh': str(tokens),
            'access': str(tokens.access_token),
        }