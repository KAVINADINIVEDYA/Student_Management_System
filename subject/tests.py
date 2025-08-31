from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Subject
from teacher.models import Teacher

User = get_user_model()

class SubjectViewTest(TestCase):
    """Integration tests for Subject views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='teacher@school.com',
            email='teacher@school.com',
            password='teacher123',
            is_teacher=True,
            is_superuser=True
        )
        
        self.teacher = Teacher.objects.create(
            user=self.user,
            first_name="Subject",
            last_name="Teacher",
            teacher_id="STCH001",
            gender="Female",
            date_of_birth="1985-01-01",
            department="Science",
            mobile_number="5555555555",
            email="subject.teacher@school.com",
            joining_date="2024-01-01",
            address="Science Department"
        )
    
    def test_subject_list_requires_login(self):
        """Test subject list requires authentication"""
        response = self.client.get(reverse('subject_list'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_subject_list_authenticated(self):
        """Test subject list when authenticated"""
        self.client.login(username='teacher@school.com', password='teacher123')
        response = self.client.get(reverse('subject_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_add_subject_get(self):
        """Test add subject form loads"""
        self.client.login(username='teacher@school.com', password='teacher123')
        response = self.client.get(reverse('add_subject'))
        self.assertEqual(response.status_code, 200)
    
    def test_add_subject_post(self):
        """Test adding subject via POST"""
        self.client.login(username='teacher@school.com', password='teacher123')
        response = self.client.post(reverse('add_subject'), {
            'name': 'Test Subject',
            'code': 'TEST101',
            'teacher': self.teacher.id,
            'description': 'Test subject description'
        })
        
        # Should redirect after successful creation
        self.assertEqual(response.status_code, 302)
        
        # Verify subject was created
        subject = Subject.objects.get(code='TEST101')
        self.assertEqual(subject.name, 'Test Subject')
        self.assertEqual(subject.teacher, self.teacher)


class SchoolViewTest(TestCase):
    """Integration tests for School app views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='test@user.com',
            email='test@user.com',
            password='test123',
            is_student=True
        )
    
    def test_index_view(self):
        """Test index page loads"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
    
    def test_dashboard_requires_login(self):
        """Test dashboard requires authentication"""
        response = self.client.get(reverse('dashboard'))
        # Should redirect to login since not authenticated
        self.assertEqual(response.status_code, 302)
    
    def test_dashboard_authenticated(self):
        """Test dashboard when authenticated"""
        self.client.login(username='test@user.com', password='test123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)