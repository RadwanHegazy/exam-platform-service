from .models import Student
import jwt
from django.conf import settings

def from_jwt_to_student(jwt_token : str) -> Student :
    """return the student instance from the jwt tokens."""
    try:
        payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=["HS256"])
        student_id = payload.get("user_id")
        if student_id is None:
            return None
        return Student.objects.filter(id=student_id).first()
    except Exception as e:
        print(e)
        return None