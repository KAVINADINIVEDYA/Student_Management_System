from django.shortcuts import render
from student.models import Student
from teacher.models import Teacher
from subject.models import Subject
from school.models import Notification

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    student_count = Student.objects.count()
    teacher_count = Teacher.objects.count()
    subject_count = Subject.objects.count()
    notifications = Notification.objects.filter(user=request.user)
    return render(request, 'Home/dashboard.html', {
        'student_count': student_count,
        'teacher_count': teacher_count,
        'subject_count': subject_count,
        'notifications': notifications
    })