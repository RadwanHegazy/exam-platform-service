from rest_framework.test import APITestCase
from globals.test_factory import create_student, create_headers, create_exam
from django.urls import reverse

class ListExamsTestCases(APITestCase) :

    def setUp(self):
        self.endpoint = reverse('list-exams')

    def test_no_headers(self) : 
        req = self.client.get(self.endpoint)
        self.assertEqual(req.status_code, 401)

    def test_forbidden(self) : 
        headers = create_headers()
        req = self.client.get(self.endpoint, headers=headers)
        self.assertEqual(req.status_code, 403)

    def test_list_empty_exams(self) :
        req = self.client.get(
            self.endpoint,
            headers=create_headers(user=create_student())
        )
        self.assertEqual(req.status_code, 200)
        self.assertEqual(len(req.json()), 0)

    
    def test_list_exams(self) :
        st = create_student()
        create_exam(level=st.level)
        create_exam(level=st.level)
        req = self.client.get(
            self.endpoint,
            headers=create_headers(st)
        )
        self.assertEqual(req.status_code, 200)
        self.assertEqual(len(req.json()), 2)