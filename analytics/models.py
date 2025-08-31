from django.db import models
from student.models import Student
from subject.models import Subject
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pickle
import os

class StudentGrade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    assignment_score = models.FloatField(default=0)
    exam_score = models.FloatField(default=0)
    attendance_percentage = models.FloatField(default=100)
    participation_score = models.FloatField(default=0)
    final_grade = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('student', 'subject')
    
    def __str__(self):
        return f"{self.student.first_name} - {self.subject.name}: {self.final_grade}"

class PerformanceAnalytics(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    predicted_gpa = models.FloatField(default=0)
    risk_level = models.CharField(max_length=20, choices=[
        ('LOW', 'Low Risk'),
        ('MEDIUM', 'Medium Risk'), 
        ('HIGH', 'High Risk')
    ], default='LOW')
    recommendations = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.first_name} - Risk: {self.risk_level}"

class AttendanceRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[
        ('PRESENT', 'Present'),
        ('ABSENT', 'Absent'),
        ('LATE', 'Late'),
        ('EXCUSED', 'Excused')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('student', 'subject', 'date')
    
    def __str__(self):
        return f"{self.student.first_name} - {self.subject.name} - {self.date}: {self.status}"

class AttendanceAnalytics:
    """GitHub-inspired attendance analytics system"""
    
    @staticmethod
    def calculate_attendance_percentage(student, subject=None, days=30):
        """Calculate attendance percentage for student"""
        from django.utils import timezone
        from datetime import timedelta
        
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=days)
        
        query = AttendanceRecord.objects.filter(
            student=student,
            date__range=[start_date, end_date]
        )
        
        if subject:
            query = query.filter(subject=subject)
        
        total_records = query.count()
        if total_records == 0:
            return 100.0  # No records = 100%
        
        present_records = query.filter(status__in=['PRESENT', 'LATE']).count()
        return (present_records / total_records) * 100
    
    @staticmethod
    def get_attendance_trends(student, days=30):
        """Get attendance trends and generate alerts"""
        from django.utils import timezone
        from datetime import timedelta
        
        percentage = AttendanceAnalytics.calculate_attendance_percentage(student, days=days)
        
        # Generate automated alerts based on GitHub webhook-style system
        alerts = []
        if percentage < 75:
            alerts.append({
                'level': 'CRITICAL',
                'message': f'Attendance below 75% ({percentage:.1f}%)',
                'action': 'Immediate intervention required'
            })
        elif percentage < 85:
            alerts.append({
                'level': 'WARNING', 
                'message': f'Attendance declining ({percentage:.1f}%)',
                'action': 'Monitor closely'
            })
        else:
            alerts.append({
                'level': 'SUCCESS',
                'message': f'Good attendance ({percentage:.1f}%)',
                'action': 'Maintain current level'
            })
        
        return {
            'percentage': percentage,
            'alerts': alerts,
            'trend': 'DECLINING' if percentage < 80 else 'STABLE'
        }

class MLModel:
    @staticmethod
    def generate_sample_data():
        """Generate sample student performance data for ML training"""
        np.random.seed(42)
        n_samples = 100
        
        # Features: assignment_score, exam_score, attendance_percentage, participation_score
        data = {
            'assignment_scores': np.random.normal(75, 15, n_samples),
            'exam_scores': np.random.normal(70, 20, n_samples),
            'attendance': np.random.normal(85, 10, n_samples),
            'participation': np.random.normal(80, 12, n_samples)
        }
        
        # Ensure realistic ranges
        data['assignment_scores'] = np.clip(data['assignment_scores'], 0, 100)
        data['exam_scores'] = np.clip(data['exam_scores'], 0, 100)
        data['attendance'] = np.clip(data['attendance'], 50, 100)
        data['participation'] = np.clip(data['participation'], 0, 100)
        
        # Calculate final grades with realistic weights
        final_grades = (
            0.3 * data['assignment_scores'] + 
            0.4 * data['exam_scores'] + 
            0.2 * data['attendance'] + 
            0.1 * data['participation']
        )
        
        X = np.column_stack([
            data['assignment_scores'],
            data['exam_scores'], 
            data['attendance'],
            data['participation']
        ])
        
        return X, final_grades
    
    @staticmethod
    def train_and_save_model():
        """Train a Random Forest model for grade prediction"""
        X, y = MLModel.generate_sample_data()
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train model (Random Forest from scikit-learn - common in educational analytics)
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        
        # Save model
        model_path = os.path.join('analytics', 'ml_model.pkl')
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
            
        return model, mse
    
    @staticmethod
    def predict_performance(assignment_score, exam_score, attendance, participation):
        """Predict student performance using trained model"""
        model_path = os.path.join('analytics', 'ml_model.pkl')
        
        if not os.path.exists(model_path):
            MLModel.train_and_save_model()
        
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        
        features = np.array([[assignment_score, exam_score, attendance, participation]])
        prediction = model.predict(features)[0]
        
        # Determine risk level
        if prediction >= 80:
            risk_level = 'LOW'
            recommendations = "Excellent performance! Keep up the good work."
        elif prediction >= 65:
            risk_level = 'MEDIUM' 
            recommendations = "Good performance. Focus on improving weaker areas."
        else:
            risk_level = 'HIGH'
            recommendations = "Needs attention. Consider additional tutoring and study support."
            
        return prediction, risk_level, recommendations