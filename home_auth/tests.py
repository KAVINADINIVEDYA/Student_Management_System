from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from student.models import Student, Parent
from teacher.models import Teacher
from subject.models import Subject
from school.models import Notification

User = get_user_model()

class CompleteUserJourneyE2ETest(TestCase):
    """End-to-End tests simulating complete user journeys"""
    
    def setUp(self):
        """Set up test users and data"""
        self.client = Client()
        
        # Create different types of users
        self.admin_user = User.objects.create_user(
            username='admin@school.com',
            email='admin@school.com',
            password='admin123',
            is_admin=True,
            is_superuser=True,
            first_name='Admin',
            last_name='User'
        )
        
        self.teacher_user = User.objects.create_user(
            username='teacher@school.com',
            email='teacher@school.com',
            password='teacher123',
            is_teacher=True,
            first_name='Teacher',
            last_name='User'
        )
        
        self.student_user = User.objects.create_user(
            username='student@school.com',
            email='student@school.com',
            password='student123',
            is_student=True,
            first_name='Student',
            last_name='User'
        )

    def test_admin_complete_school_management_workflow(self):
        """E2E: Admin manages complete school operations"""
        
        # 1. Admin visits homepage
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        # 2. Admin logs in
        self.client.login(username='admin@school.com', password='admin123')
        
        # 3. Admin accesses dashboard
        dashboard_response = self.client.get(reverse('dashboard'))
        self.assertEqual(dashboard_response.status_code, 200)
        
        # 4. Admin views student list
        student_list_response = self.client.get(reverse('student_list'))
        self.assertEqual(student_list_response.status_code, 200)
        
        # 5. Admin accesses add student form
        add_student_form = self.client.get(reverse('add_student'))
        self.assertEqual(add_student_form.status_code, 200)
        
        # 6. Admin views teacher list  
        teacher_list_response = self.client.get(reverse('teacher_list'))
        self.assertEqual(teacher_list_response.status_code, 200)
        
        # 7. Admin views subject list
        subject_list_response = self.client.get(reverse('subject_list'))
        self.assertEqual(subject_list_response.status_code, 200)
        
        # 8. Admin logs out
        logout_response = self.client.get(reverse('logout'))
        self.assertEqual(logout_response.status_code, 302)
        
        # 9. Verify admin is logged out (can't access protected pages)
        protected_response = self.client.get(reverse('student_list'))
        self.assertEqual(protected_response.status_code, 302)  # Redirected to login

    def test_teacher_workflow_e2e(self):
        """E2E: Teacher user complete workflow"""
        
        # 1. Teacher logs in
        self.client.login(username='teacher@school.com', password='teacher123')
        
        # 2. Teacher views student list
        response = self.client.get(reverse('student_list'))
        self.assertEqual(response.status_code, 200)
        
        # 3. Teacher views subject list
        response = self.client.get(reverse('subject_list'))
        self.assertEqual(response.status_code, 200)
        
        # 4. Teacher logs out
        self.client.logout()
        
        # 5. Verify teacher is logged out
        response = self.client.get(reverse('student_list'))
        self.assertEqual(response.status_code, 302)

    def test_student_workflow_e2e(self):
        """E2E: Student user complete workflow"""
        
        # 1. Student logs in
        self.client.login(username='student@school.com', password='student123')
        
        # 2. Student accesses dashboard
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        
        # 3. Student views subject list
        response = self.client.get(reverse('subject_list'))
        self.assertEqual(response.status_code, 200)
        
        # 4. Student logs out
        self.client.logout()

    def test_complete_data_flow_e2e(self):
        """E2E: Test complete data flow - create teacher → create subject → assign teacher to subject"""
        
        # Login as admin
        self.client.login(username='admin@school.com', password='admin123')
        
        # Step 1: Create a teacher record
        teacher = Teacher.objects.create(
            user=self.teacher_user,
            first_name="John",
            last_name="Mathematics",
            teacher_id="TCH001",
            gender="Male",
            date_of_birth="1980-01-01",
            department="Mathematics",
            mobile_number="1234567890",
            email="john.math@school.com",
            joining_date="2024-01-01",
            address="School Campus"
        )
        
        # Step 2: Create a subject and assign teacher
        subject = Subject.objects.create(
            name="Advanced Mathematics",
            code="MATH101",
            teacher=teacher,
            description="Advanced mathematics course"
        )
        
        # Step 3: Verify relationship exists
        self.assertEqual(subject.teacher.first_name, "John")
        self.assertEqual(subject.teacher.teacher_id, "TCH001")
        
        # Step 4: Access subject list and verify subject appears
        response = self.client.get(reverse('subject_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Advanced Mathematics")
        self.assertContains(response, "MATH101")

    def test_notification_system_e2e(self):
        """E2E: Test notification system works across the application"""
        
        # Login as admin
        self.client.login(username='admin@school.com', password='admin123')
        
        # Create a notification
        notification = Notification.objects.create(
            user=self.admin_user,
            message="Test notification for E2E"
        )
        
        # Verify notification exists and is unread
        self.assertFalse(notification.is_read)
        
        # Access dashboard where notifications are shown
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        
        # Mark notification as read using AJAX endpoint
        mark_read_response = self.client.post(reverse('mark_notification_as_read'))
        self.assertEqual(mark_read_response.status_code, 200)
        
        # Verify notification is now marked as read
        notification.refresh_from_db()
        self.assertTrue(notification.is_read)