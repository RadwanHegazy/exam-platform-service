from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.test import APITestCase
from globals.test_factory import create_student
from django.urls import reverse

class StVerifyTokensTestCase(APITestCase) : 

    def setUp(self):
        self.endpoint = reverse('token-verify')

    def test_no_body(self) : 
        req = self.client.post(self.endpoint)
        self.assertEqual(req.status_code, 400)

    def test_invalid_tokens(self) : 
        data = {
            'token' : '123321'
        }
        req = self.client.post(self.endpoint, data=data)
        self.assertEqual(req.status_code, 401)

    def test_valid_tokens(self) : 
        data = {
            'token' : str(AccessToken().for_user(create_student()))
        }
        req = self.client.post(self.endpoint, data=data)
        self.assertEqual(req.status_code, 200)

    
