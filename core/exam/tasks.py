from cassandra_orm.models import StudentAnswer, CassandraORM
from .models import Exam, Question, StudentDegrees
from celery import shared_task
from users.utlities import from_jwt_to_student
import os



@shared_task
def solve_student_qs(
    exam_id : int,

) : 
    """Get all questions and solve it from the cassandra db."""

    try:
        exam_instance = Exam.objects.get(id=exam_id)
    except Exam.DoesNotExist:
        print("Exam not found !")
        return
    
    CassandraORM.connect(
            hosts=[os.environ.get('CASSANDRA_HOST_1'), os.environ.get('CASSANDRA_HOST_2')],
            keyspace=os.environ.get('CASSANDRA_KEYSPACE')
    )

    exam_instance.status = Exam.StatusChoices.PENDING
    exam_instance.solve_status = Exam.SolveStatusChoices.IN_PROGRESS
    exam_instance.start_solve = False
    exam_instance.save()

    st_answers = StudentAnswer().get_by_key('exam_id', exam_id)
    for st_answer in st_answers : 
        # corect the answers here
        student = from_jwt_to_student(st_answer['student_jwt'])
        answer = str(st_answer['answer'])
        question = Question.objects.get(id=st_answer['question_id'])

        st_degree, _ = StudentDegrees.objects.get_or_create(student=student, exam=exam_instance)
        
        if answer.capitalize() == question.correct.capitalize():
            st_degree.final_score += 1

        st_degree.save()

    exam_instance.solve_status = Exam.SolveStatusChoices.COMPLETED
    exam_instance.save()
