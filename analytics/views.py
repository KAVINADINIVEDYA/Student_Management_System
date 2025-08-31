from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from .models import StudentGrade, PerformanceAnalytics, MLModel
from student.models import Student
from subject.models import Subject
from school.models import Notification

@login_required
def analytics_dashboard(request):
    """Main analytics dashboard"""
    students = Student.objects.all()
    subjects = Subject.objects.all()
    recent_analytics = PerformanceAnalytics.objects.order_by('-created_at')[:10]
    
    # Simple HTML response for now
    html = f"""
    <h1>🤖 ML Analytics Dashboard</h1>
    <p><strong>Open-Source Integration:</strong> Random Forest from scikit-learn</p>
    <p>Students: {students.count()} | Subjects: {subjects.count()}</p>
    <p>Recent ML Predictions: {recent_analytics.count()}</p>
    <hr>
    <a href="/analytics/add-grade/" style="background:#007bff;color:white;padding:10px;text-decoration:none;border-radius:5px;">Add Grade & Run ML Prediction</a>
    <a href="/analytics/train-model/" style="background:#28a745;color:white;padding:10px;text-decoration:none;border-radius:5px;margin-left:10px;">Retrain ML Model</a>
    <a href="/dashboard/" style="background:#6c757d;color:white;padding:10px;text-decoration:none;border-radius:5px;margin-left:10px;">Back to Dashboard</a>
    <hr>
    """
    
    for analytics in recent_analytics:
        color = "red" if analytics.risk_level == 'HIGH' else "orange" if analytics.risk_level == 'MEDIUM' else "green"
        html += f"""
        <div style="border:1px solid {color}; padding:10px; margin:10px 0; border-radius:5px;">
            <strong>{analytics.student.first_name} {analytics.student.last_name}</strong><br>
            Predicted GPA: {analytics.predicted_gpa:.2f}<br>
            Risk Level: {analytics.risk_level}<br>
            Recommendations: {analytics.recommendations}
        </div>
        """
    
    return HttpResponse(html)

@login_required
def add_student_grade(request):
    """Add grades and trigger ML prediction"""
    if request.method == "POST":
        student_id = request.POST.get('student')
        subject_id = request.POST.get('subject')
        assignment_score = float(request.POST.get('assignment_score', 0))
        exam_score = float(request.POST.get('exam_score', 0))
        attendance = float(request.POST.get('attendance_percentage', 100))
        participation = float(request.POST.get('participation_score', 0))
        
        student = get_object_or_404(Student, id=student_id)
        subject = get_object_or_404(Subject, id=subject_id)
        
        # Calculate final grade using ML prediction
        predicted_grade, risk_level, recommendations = MLModel.predict_performance(
            assignment_score, exam_score, attendance, participation
        )
        
        # Save grade
        grade, created = StudentGrade.objects.get_or_create(
            student=student,
            subject=subject,
            defaults={
                'assignment_score': assignment_score,
                'exam_score': exam_score,
                'attendance_percentage': attendance,
                'participation_score': participation,
                'final_grade': predicted_grade
            }
        )
        
        if not created:
            grade.assignment_score = assignment_score
            grade.exam_score = exam_score
            grade.attendance_percentage = attendance
            grade.participation_score = participation
            grade.final_grade = predicted_grade
            grade.save()
        
        # Save analytics
        analytics, created = PerformanceAnalytics.objects.get_or_create(
            student=student,
            defaults={
                'predicted_gpa': predicted_grade,
                'risk_level': risk_level,
                'recommendations': recommendations
            }
        )
        
        if not created:
            analytics.predicted_gpa = predicted_grade
            analytics.risk_level = risk_level
            analytics.recommendations = recommendations
            analytics.save()
        
        # Create notification
        Notification.objects.create(
            user=request.user,
            message=f"ML Analysis completed for {student.first_name} {student.last_name}"
        )
        
        messages.success(request, f"Grade added and ML prediction completed! Predicted Grade: {predicted_grade:.2f}")
        return redirect('analytics_dashboard')
    
    students = Student.objects.all()
    subjects = Subject.objects.all()
    
    if request.method == "POST":
        # Form processing code stays the same
        student_id = request.POST.get('student')
        subject_id = request.POST.get('subject')
        assignment_score = float(request.POST.get('assignment_score', 0))
        exam_score = float(request.POST.get('exam_score', 0))
        attendance = float(request.POST.get('attendance_percentage', 100))
        participation = float(request.POST.get('participation_score', 0))
        
        student = get_object_or_404(Student, id=student_id)
        subject = get_object_or_404(Subject, id=subject_id)
        
        # Calculate final grade using ML prediction
        predicted_grade, risk_level, recommendations = MLModel.predict_performance(
            assignment_score, exam_score, attendance, participation
        )
        
        # Save grade
        grade, created = StudentGrade.objects.get_or_create(
            student=student,
            subject=subject,
            defaults={
                'assignment_score': assignment_score,
                'exam_score': exam_score,
                'attendance_percentage': attendance,
                'participation_score': participation,
                'final_grade': predicted_grade
            }
        )
        
        if not created:
            grade.assignment_score = assignment_score
            grade.exam_score = exam_score
            grade.attendance_percentage = attendance
            grade.participation_score = participation
            grade.final_grade = predicted_grade
            grade.save()
        
        # Save analytics
        analytics, created = PerformanceAnalytics.objects.get_or_create(
            student=student,
            defaults={
                'predicted_gpa': predicted_grade,
                'risk_level': risk_level,
                'recommendations': recommendations
            }
        )
        
        if not created:
            analytics.predicted_gpa = predicted_grade
            analytics.risk_level = risk_level
            analytics.recommendations = recommendations
            analytics.save()
        
        # Create notification
        Notification.objects.create(
            user=request.user,
            message=f"ML Analysis completed for {student.first_name} {student.last_name}"
        )
        
        return HttpResponse(f"""
        <h1>✅ ML Prediction Complete!</h1>
        <p><strong>Student:</strong> {student.first_name} {student.last_name}</p>
        <p><strong>Subject:</strong> {subject.name}</p>
        <p><strong>Predicted Grade:</strong> {predicted_grade:.2f}</p>
        <p><strong>Risk Level:</strong> {risk_level}</p>
        <p><strong>Recommendations:</strong> {recommendations}</p>
        <hr>
        <a href="/analytics/" style="background:#007bff;color:white;padding:10px;text-decoration:none;border-radius:5px;">Back to Analytics Dashboard</a>
        """)
    
    # Simple form HTML
    form_html = f"""
    <h1>🎯 Add Student Grade & ML Prediction</h1>
    <form method="post">
        <input type="hidden" name="csrfmiddlewaretoken" value="{request.META.get('CSRF_COOKIE', '')}">
        
        <p><label>Student:</label><br>
        <select name="student" required>
            <option value="">Choose student...</option>"""
    
    for student in students:
        form_html += f'<option value="{student.id}">{student.first_name} {student.last_name}</option>'
    
    form_html += """</select></p>
        
        <p><label>Subject:</label><br>
        <select name="subject" required>
            <option value="">Choose subject...</option>"""
    
    for subject in subjects:
        form_html += f'<option value="{subject.id}">{subject.name}</option>'
    
    form_html += """</select></p>
        
        <p><label>Assignment Score (0-100):</label><br>
        <input type="number" name="assignment_score" min="0" max="100" step="0.1" required></p>
        
        <p><label>Exam Score (0-100):</label><br>
        <input type="number" name="exam_score" min="0" max="100" step="0.1" required></p>
        
        <p><label>Attendance % (0-100):</label><br>
        <input type="number" name="attendance_percentage" min="0" max="100" step="0.1" value="100" required></p>
        
        <p><label>Participation Score (0-100):</label><br>
        <input type="number" name="participation_score" min="0" max="100" step="0.1" required></p>
        
        <button type="submit" style="background:#007bff;color:white;padding:10px;border:none;border-radius:5px;">🤖 Add Grade & Run ML Prediction</button>
    </form>
    <hr>
    <a href="/analytics/" style="background:#6c757d;color:white;padding:10px;text-decoration:none;border-radius:5px;">Back to Analytics</a>
    """
    
    return HttpResponse(form_html)

@login_required
def train_ml_model(request):
    """Endpoint to retrain the ML model"""
    try:
        model, mse = MLModel.train_and_save_model()
        Notification.objects.create(
            user=request.user,
            message=f"ML Model retrained successfully. MSE: {mse:.2f}"
        )
        messages.success(request, f"ML Model trained successfully! Mean Squared Error: {mse:.2f}")
    except Exception as e:
        messages.error(request, f"Error training model: {str(e)}")
    
    return redirect('analytics_dashboard')