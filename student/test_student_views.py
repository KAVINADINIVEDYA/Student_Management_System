from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from student.models import Student, Parent

User = get_user_model()

class StudentViewsTestCase(TestCase):
    def setUp(self):
        """Set up test data"""
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser@example.com',
            email='testuser@example.com',
            password='testpass123',
            is_teacher=True  # Give permissions to add students
        )
        
        # Create a test parent
        self.parent = Parent.objects.create(
            father_name='John Doe',
            father_mobile='1234567890',
            father_email='john@example.com',
            mother_name='Jane Doe',
            mother_mobile='0987654321',
            mother_email='jane@example.com',
            present_address='123 Main St',
            permanent_address='123 Main St'
        )
        
        # Create a test student
        self.student = Student.objects.create(
            first_name='Test',
            last_name='Student',
            student_id='STU001',
            gender='Male',
            date_of_birth='2000-01-01',
            student_class='Grade 10',
            religion='Christianity',
            joining_date='2024-01-01',
            mobile_number='1111111111',
            admission_number='ADM001',
            section='A',
            student_email='test@example.com',
            parent=self.parent
        )
        
        self.client = Client()

    def test_student_list_requires_login(self):
        """Test that student list requires login"""
        response = self.client.get(reverse('student_list'))
        self.assertEqual(response.status_code, 302)  # Should redirect to login

    def test_student_list_with_login(self):
        """Test student list view when logged in"""
        self.client.login(username='testuser@example.com', password='testpass123')
        response = self.client.get(reverse('student_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Student')

    def test_add_student_get_request(self):
        """Test GET request to add student page"""
        self.client.login(username='testuser@example.com', password='testpass123')
        response = self.client.get(reverse('add_student'))
        self.assertEqual(response.status_code, 200)

    def test_view_student_details(self):
        """Test viewing student details"""
        self.client.login(username='testuser@example.com', password='testpass123')
        response = self.client.get(reverse('view_student', kwargs={'slug': self.student.student_id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Student')