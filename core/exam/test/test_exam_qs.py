from rest_framework.test import APITestCase
from globals.test_factory import create_student, create_headers, create_exam, create_question
from django.urls import reverse

class RetrieveExamsQsTestCases(APITestCase) :

    def endpoint(self, id):
        return reverse('exam-qs', args=[id])

    def test_no_headers(self) : 
        req = self.client.get(self.endpoint(999))
        self.assertEqual(req.status_code, 401)

    def test_forbidden(self) : 
        headers = create_headers()
        req = self.client.get(self.endpoint(999), headers=headers)
        self.assertEqual(req.status_code, 403)

    def test_not_found(self) :
        req = self.client.get(
            self.endpoint(999),
            headers=create_headers(user=create_student())
        )
        self.assertEqual(req.status_code, 404)

    
    def test_exists_qs(self) :
        st = create_student()
        ex = create_exam(level=st.level)
        create_question(exam=ex) 
        create_question(exam=ex) 
        create_question(exam=ex) 
        req = self.client.get(
            self.endpoint(ex.id),
            headers=create_headers(st)
        )
        self.assertEqual(req.status_code, 200)
        self.assertEqual(len(req.json()), 3)
