from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Student, Parent

User = get_user_model()

class StudentModelTest(TestCase):
    def setUp(self):
        """Set up test data"""
        self.parent = Parent.objects.create(
            father_name="John Doe",
            father_mobile="1234567890",
            father_email="john@example.com",
            mother_name="Jane Doe",
            mother_mobile="0987654321",
            mother_email="jane@example.com",
            present_address="123 Main St",
            permanent_address="123 Main St"
        )
    
    def test_student_creation(self):
        """Test that a student can be created successfully"""
        student = Student.objects.create(
            first_name="Test",
            last_name="Student",
            student_id="STU001",
            gender="Male",
            date_of_birth="2000-01-01",
            student_class="10",
            religion="Christianity",
            joining_date="2024-01-01",
            mobile_number="1111111111",
            admission_number="ADM001",
            section="A",
            student_email="test@example.com",
            parent=self.parent
        )
        
        self.assertEqual(student.first_name, "Test")
        self.assertEqual(student.last_name, "Student")
        self.assertEqual(student.student_id, "STU001")
        self.assertEqual(str(student), "Test Student (STU001)")
    
    def test_student_slug_generation(self):
        """Test that slug is automatically generated"""
        student = Student.objects.create(
            first_name="Test",
            last_name="Student",
            student_id="STU002",
            gender="Male",
            date_of_birth="2000-01-01",
            student_class="10",
            religion="Christianity",
            joining_date="2024-01-01",
            mobile_number="1111111111",
            admission_number="ADM002",
            section="A",
            student_email="test2@example.com",
            parent=self.parent
        )
        
        self.assertEqual(student.slug, "test-student-stu002")


class ParentModelTest(TestCase):
    """Unit tests for Parent model"""
    
    def test_parent_creation(self):
        """Test parent can be created"""
        parent = Parent.objects.create(
            father_name="Test Father",
            father_occupation="Engineer",
            father_mobile="1111111111",
            father_email="father@test.com",
            mother_name="Test Mother", 
            mother_occupation="Doctor",
            mother_mobile="2222222222",
            mother_email="mother@test.com",
            present_address="Present Address",
            permanent_address="Permanent Address"
        )
        self.assertEqual(str(parent), "Test Father & Test Mother")
        self.assertEqual(parent.father_occupation, "Engineer")
        self.assertEqual(parent.mother_occupation, "Doctor")
    
    def test_parent_optional_fields(self):
        """Test parent with optional fields blank"""
        parent = Parent.objects.create(
            father_name="Father Only",
            father_mobile="1111111111", 
            father_email="father@test.com",
            mother_name="Mother Only",
            mother_mobile="2222222222",
            mother_email="mother@test.com",
            present_address="Address",
            permanent_address="Address"
        )
        self.assertEqual(parent.father_occupation, "")
        self.assertEqual(parent.mother_occupation, "")
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Student, Parent

User = get_user_model()

class StudentModelTest(TestCase):
    def setUp(self):
        """Set up test data"""
        self.parent = Parent.objects.create(
            father_name="John Doe",
            father_mobile="1234567890",
            father_email="john@example.com",
            mother_name="Jane Doe",
            mother_mobile="0987654321",
            mother_email="jane@example.com",
            present_address="123 Main St",
            permanent_address="123 Main St"
        )
    
    def test_student_creation(self):
        """Test that a student can be created successfully"""
        student = Student.objects.create(
            first_name="Test",
            last_name="Student",
            student_id="STU001",
            gender="Male",
            date_of_birth="2000-01-01",
            student_class="10",
            religion="Christianity",
            joining_date="2024-01-01",
            mobile_number="1111111111",
            admission_number="ADM001",
            section="A",
            student_email="test@example.com",
            parent=self.parent
        )
        
        self.assertEqual(student.first_name, "Test")
        self.assertEqual(student.last_name, "Student")
        self.assertEqual(student.student_id, "STU001")
        self.assertEqual(str(student), "Test Student (STU001)")
    
    def test_student_slug_generation(self):
        """Test that slug is automatically generated"""
        student = Student.objects.create(
            first_name="Test",
            last_name="Student",
            student_id="STU002",
            gender="Male",
            date_of_birth="2000-01-01",
            student_class="10",
            religion="Christianity",
            joining_date="2024-01-01",
            mobile_number="1111111111",
            admission_number="ADM002",
            section="A",
            student_email="test2@example.com",
            parent=self.parent
        )
        
        self.assertEqual(student.slug, "test-student-stu002")