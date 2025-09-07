from .users import create_level, create_doctor
from exam.models import Exam, Question


def create_exam(
    name: str = "Sample Exam",
    total_score = 100,
    created_by = None,
    level = None,
    time_in_hours = 1.0
) -> Exam:
    exam = Exam.objects.create(
        name=name,
        total_score=total_score,
        created_by=created_by or create_doctor(),
        level=level or create_level(),
        time_in_hours=time_in_hours
    )
    return exam


def create_question(
    name: str = "Sample Question",
    choice_a: str = "Choice A",
    choice_b: str = "Choice B",
    choice_c: str = "Choice C",
    choice_d: str = "Choice D",
    correct: str = "A",
    exam = None,
    created_by = None
) -> Question:
    question = Question.objects.create(
        name=name,
        choice_a=choice_a,
        choice_b=choice_b,
        choice_c=choice_c,
        choice_d=choice_d,
        correct=correct,
        exam=exam or create_exam(),
        created_by=created_by or create_doctor()
    )
    return question
