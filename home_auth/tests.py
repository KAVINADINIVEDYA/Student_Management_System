from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import CustomUser

User = get_user_model()

class AuthenticationTest(TestCase):
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='testuser@example.com',
            email='testuser@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            is_student=True
        )
    
    def test_user_creation(self):
        """Test that a custom user can be created"""
        self.assertEqual(self.user.username, 'testuser@example.com')
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertTrue(self.user.is_student)
        self.assertFalse(self.user.is_teacher)
        self.assertFalse(self.user.is_admin)
    
    def test_login_view_get(self):
        """Test that login page loads correctly"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
    
    def test_login_post_valid_credentials(self):
        """Test login with valid credentials"""
        response = self.client.post(reverse('login'), {
            'email': 'testuser@example.com',
            'password': 'testpass123'
        })
        # Should redirect after successful login
        self.assertEqual(response.status_code, 302)
    
    def test_login_post_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = self.client.post(reverse('login'), {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        })
        # Should stay on login page
        self.assertEqual(response.status_code, 200)
    
    def test_signup_view_get(self):
        """Test that signup page loads correctly"""
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
