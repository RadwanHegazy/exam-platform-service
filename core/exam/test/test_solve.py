import json
from exam.models import StudentDegrees
from rest_framework.test import APITestCase
from globals.test_factory import create_student, create_headers, create_exam, create_question
import requests

class TestSolveExamFastAPI(APITestCase) :

    def setUp(self):
        self.client = requests
        self.endpoint = "http://express-solver-1:3000/solver"

    def test_no_headers(self) : 
        req = self.client.post(self.endpoint)
        self.assertEqual(req.status_code, 401)


    def test_post_no_body(self) : 
        headers = create_headers()
        headers['Content-Type'] = 'application/json'
        req = self.client.post(self.endpoint, headers=headers)
        self.assertEqual(req.status_code, 400)

    def test_post_body(self) :
        student = create_student()
        exam = create_exam()
        headers = create_headers(student)
        headers['Content-Type'] = 'application/json'
        question = create_question(exam=exam)

        body = {
            "question_id" : question.id,
            "answer" : "A",
            'exam_id' : exam.id
        }

        req = self.client.post(self.endpoint, headers=headers, data=json.dumps(body))
        self.assertEqual(req.status_code, 200)

        # create celery task

        exam.start_solve = True
        exam.save()

        self.assertNotEqual(
            StudentDegrees.objects.filter(
                student = student,
                exam = exam
            ).count(), 
            0
        )
