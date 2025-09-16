from rest_framework.test import APITestCase
from globals.test_factory import create_student, create_headers, create_exam, create_question
import requests

class TestSolveExamFastAPI(APITestCase) :

    def setUp(self):
        self.client = requests
        self.endpoint = "http://fastapi_exam:1234"

    def test_no_headers(self) : 
        req = self.client.post(self.endpoint)
        self.assertEqual(req.status_code, 401)


    def test_post_no_body(self) : 
        headers = create_headers()
        req = self.client.post(self.endpoint, headers=headers)
        self.assertEqual(req.status_code, 422)

    def test_post_body(self) :
        student = create_student()
        exam = create_exam()
        headers = create_headers(student)
        question = create_question(exam=exam)

        body = {
            "question_id" : question.id,
            "answer" : "A"
        }

        req = self.client.post(self.endpoint, headers=headers, data=body)
        self.assertEqual(req.status_code, 201)