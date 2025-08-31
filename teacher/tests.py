from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Teacher
from school.models import Notification

User = get_user_model()

class TeacherModelTest(TestCase):
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='teacher@example.com',
            email='teacher@example.com',
            password='testpass123',
            is_teacher=True
        )
    
    def test_teacher_creation(self):
        """Test that a teacher can be created successfully"""
        teacher = Teacher.objects.create(
            user=self.user,
            first_name="John",
            last_name="Smith",
            teacher_id="TCH001",
            gender="Male",
            date_of_birth="1980-01-01",
            department="Mathematics",
            mobile_number="1234567890",
            email="john.smith@example.com",
            joining_date="2024-01-01",
            address="123 Teacher St"
        )
        
        self.assertEqual(teacher.first_name, "John")
        self.assertEqual(teacher.last_name, "Smith")
        self.assertEqual(teacher.teacher_id, "TCH001")
        self.assertEqual(str(teacher), "John Smith (TCH001)")
    
    def test_teacher_slug_generation(self):
        """Test that slug is automatically generated"""
        teacher = Teacher.objects.create(
            user=self.user,
            first_name="Jane",
            last_name="Doe",
            teacher_id="TCH002",
            gender="Female",
            date_of_birth="1985-01-01",
            department="Science",
            mobile_number="1234567891",
            email="jane.doe@example.com",
            joining_date="2024-01-01",
            address="456 Teacher Ave"
        )
        
        self.assertEqual(teacher.slug, "jane-doe-tch002")

class TeacherViewTest(TestCase):
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='admin@example.com',
            email='admin@example.com',
            password='testpass123',
            is_teacher=True,
            is_superuser=True
        )
        
        self.teacher = Teacher.objects.create(
            user=self.user,
            first_name="Test",
            last_name="Teacher",
            teacher_id="TCH003",
            gender="Male",
            date_of_birth="1990-01-01",
            department="English",
            mobile_number="1234567892",
            email="test.teacher@example.com",
            joining_date="2024-01-01",
            address="789 School Rd"
        )
    
    def test_teacher_list_view_requires_login(self):
        """Test that teacher list requires authentication"""
        response = self.client.get(reverse('teacher_list'))
        # Should redirect to login if not authenticated
        self.assertEqual(response.status_code, 302)
    
    def test_teacher_list_view_authenticated(self):
        """Test teacher list view when authenticated"""
        self.client.login(username='admin@example.com', password='testpass123')
        response = self.client.get(reverse('teacher_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Teacher")