from rest_framework.test import APITestCase
from globals.test_factory import create_student, create_doctor
from django.urls import reverse

class StLoginTestCase(APITestCase) : 

    def setUp(self):
        self.endpoint = reverse('student-login')

    def test_prof_login(self):
        doc = create_doctor(
            email='t@gmail.com',
            password='123'
        )
        req = self.client.post(self.endpoint, data={
            'email' : doc.email,
            'password' : '123'
        })

        self.assertEqual(req.status_code, 400)

    def test_student_login_invalid(self): 
        req = self.client.post(self.endpoint, data={
            'email' : "not.found@gmail.com",
            'password' : '123'
        })

        self.assertEqual(req.status_code, 400)

    def test_student_login_valid(self): 
        st = create_student(
            email='t@gmail.com',
            password='123'
        )
        req = self.client.post(self.endpoint, data={
            'email' : st.email,
            'password' : '123'
        })

        self.assertEqual(req.status_code, 201)