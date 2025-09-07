from uuid import uuid4
from users.models import Student, Doctor, Level, CustomBaseUser
from rest_framework_simplejwt.tokens import AccessToken

def create_base_user(
    email: str = None,
    password: str = "123",
) : 
    user = CustomBaseUser.objects.create_user(
        email=email or f'user{uuid4()}@example.com',
        password=password
    )
    return user

def create_level (
    name: str = "Level 1"
) -> Level:
    level = Level.objects.create(name=name)
    return level

def create_student (
    email: str = None,
    password: str = "123",
    full_name: str = "Student Name",
    level: Level = None,
    id_number: int = 12345123

) -> Student:
    student = Student.objects.create_user(
        email=email or f'student{uuid4()}@example.com',
        password=password,
        full_name=full_name,
        level=level or create_level(),
        id_number = id_number
    )
    return student

def create_doctor (
    email: str = None,
    password: str = "123",
    full_name: str = "Doctor Name",
    subject: str = "Subject Name",

) -> Doctor:
    doctor = Doctor.objects.create_user(
        email=email or f'doctor{uuid4()}@example.com',
        password=password,
        full_name=full_name,
        subject=subject
    )
    return doctor


def create_tokens(user=None) :
    access = AccessToken().for_user(user or create_base_user())
    return {
        'access' : str(access)
    }

def create_headers(user=None) : 
    tokens = create_tokens(user)
    return {
        'Authorization' : f'Bearer {tokens["access"]}'
    }