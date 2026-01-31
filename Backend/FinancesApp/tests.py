from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Wallet

class RegisterTests(APITestCase):
    def test_create_user(self): #register test
        url = reverse('Register')  
        data = {
            "username": "testuser",
            "password": "testpass123",
            "email": "test@example.com"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')
        
        
        
class LoginTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        
    def test_jwt_login(self): #log-in test
        url = reverse('Token')  
        data = {
            "username": "testuser",
            "password": "testpass123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        
        

class WalletTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        #getting JWT token
        url = reverse('Token')
        data = {"username": "testuser", "password": "testpass123"}
        response = self.client.post(url, data, format='json')
        self.token = response.data['access']  #storing the access token
        
    def test_wallets(self):
            url = reverse('Wallets')
            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
            data = {
                
                "name": 'savings_wallet', 
                "balance": 1000
            }
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data['name'], 'savings_wallet')
            self.assertIn('id', response.data)


class TransactionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        #getting JWT token
        url = reverse('Token')
        data = {"username": "testuser", "password": "testpass123"}
        response = self.client.post(url, data, format='json')
        self.token = response.data['access']  #storing the access token
        self.wallet = Wallet.objects.create(name="Test Wallet", balance=1000, user=self.user)
        
    def test_trans(self):
            url = reverse('Transactions')
            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
            data = {
                "wallet": self.wallet.id,
                "trans_type": "income",
                "amount": 500,
                "trans_date": "2025-12-09",
                "category": "Salary",
                "desc": "December salary"
            }

            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(float(response.data['amount']), 500.00)
            self.assertIn('id', response.data)

    
    
    
class BudgetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        #getting JWT token
        url = reverse('Token')
        data = {"username": "testuser", "password": "testpass123"}
        response = self.client.post(url, data, format='json')
        self.token = response.data['access']  #storing the access token
        
    def test_budgs(self):
            url = reverse('Budgets')
            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
            data = {
                "category": "Groceries",
                "amount": 200,
                "budg_date": "2025-12-09",
                "desc": "Weekly grocery budget"
            }
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data['desc'], 'Weekly grocery budget')
            self.assertIn('id', response.data)

    
    

class GoalTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        #getting JWT token
        url = reverse('Token')
        data = {"username": "testuser", "password": "testpass123"}
        response = self.client.post(url, data, format='json')
        self.token = response.data['access']  #storing the access token
        
    def test_goals(self):
            url = reverse('Goals')
            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
            data = {
                "target_amount": 5000,
                "current_amount": 1500,
                "category": "Vacation",
                "start_date": "2025-12-01",
                "target_date": "2026-06-01",
                "desc": "Saving for summer vacation"
            }

            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(float(response.data['current_amount']), 1500.00)
            self.assertIn('id', response.data)

    
    
