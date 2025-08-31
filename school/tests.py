from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from .models import Notification
import json

User = get_user_model()

class SchoolViewsTest(TestCase):
    """Comprehensive tests for school app views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='school@test.com',
            email='school@test.com',
            password='school123',
            is_admin=True
        )
    
    def test_index_view(self):
        """Test index view loads correctly"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
    
    def test_dashboard_authenticated(self):
        """Test dashboard when user is authenticated"""
        self.client.login(username='school@test.com', password='school123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
    
    def test_mark_notification_as_read(self):
        """Test marking notifications as read"""
        self.client.login(username='school@test.com', password='school123')
        
        # Create test notifications
        Notification.objects.create(user=self.user, message="Test notification 1")
        Notification.objects.create(user=self.user, message="Test notification 2")
        
        # Verify notifications are unread
        unread_count = Notification.objects.filter(user=self.user, is_read=False).count()
        self.assertEqual(unread_count, 2)
        
        # Mark as read via POST
        response = self.client.post(reverse('mark_notification_as_read'))
        self.assertEqual(response.status_code, 200)
        
        # Verify notifications are now read
        unread_count = Notification.objects.filter(user=self.user, is_read=False).count()
        self.assertEqual(unread_count, 0)
    
    def test_clear_all_notifications(self):
        """Test clearing all notifications"""
        self.client.login(username='school@test.com', password='school123')
        
        # Create test notifications
        Notification.objects.create(user=self.user, message="Test notification 1")
        Notification.objects.create(user=self.user, message="Test notification 2")
        
        # Verify notifications exist
        notification_count = Notification.objects.filter(user=self.user).count()
        self.assertEqual(notification_count, 2)
        
        # Clear all notifications
        response = self.client.post(reverse('clear_all_notification'))
        self.assertEqual(response.status_code, 200)
        
        # Verify notifications are deleted
        notification_count = Notification.objects.filter(user=self.user).count()
        self.assertEqual(notification_count, 0)
    
    def test_mark_notification_forbidden_get(self):
        """Test that GET request to mark notification is forbidden"""
        self.client.login(username='school@test.com', password='school123')
        response = self.client.get(reverse('mark_notification_as_read'))
        self.assertEqual(response.status_code, 403)  # Forbidden
    
    def test_clear_notification_forbidden_get(self):
        """Test that GET request to clear notifications is forbidden"""
        self.client.login(username='school@test.com', password='school123')
        response = self.client.get(reverse('clear_all_notification'))
        self.assertEqual(response.status_code, 403)  # Forbidden


class NotificationModelTest(TestCase):
    """Unit tests for Notification model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='notify@test.com',
            email='notify@test.com',
            password='notify123'
        )
    
    def test_notification_str_method(self):
        """Test notification string representation"""
        notification = Notification.objects.create(
            user=self.user,
            message="String test notification"
        )
        self.assertEqual(str(notification), "String test notification")
    
    def test_notification_default_values(self):
        """Test notification default field values"""
        notification = Notification.objects.create(
            user=self.user,
            message="Default values test"
        )
        self.assertFalse(notification.is_read)  # Default should be False
        self.assertIsNotNone(notification.created_at)
        self.assertIsNotNone(notification.id)  # UUID should be generated
    
    def test_notification_user_relationship(self):
        """Test notification-user relationship"""
        notification = Notification.objects.create(
            user=self.user,
            message="Relationship test"
        )
        self.assertEqual(notification.user, self.user)
        
        # Test reverse relationship
        user_notifications = self.user.notification_set.all()
        self.assertIn(notification, user_notifications)