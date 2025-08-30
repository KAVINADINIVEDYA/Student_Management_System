from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Student, Parent
from school.models import Notification

@login_required
def add_student(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        student_id = request.POST.get('student_id')
        student_email = request.POST.get('student_email')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        student_class = request.POST.get('student_class')
        religion = request.POST.get('religion')
        joining_date = request.POST.get('joining_date')
        mobile_number = request.POST.get('mobile_number')
        admission_number = request.POST.get('admission_number')
        section = request.POST.get('section')
        student_image = request.FILES.get('student_image')
        father_name = request.POST.get('father_name')
        father_occupation = request.POST.get('father_occupation')
        father_mobile = request.POST.get('father_mobile')
        father_email = request.POST.get('father_email')
        mother_name = request.POST.get('mother_name')
        mother_occupation = request.POST.get('mother_occupation')
        mother_mobile = request.POST.get('mother_mobile')
        mother_email = request.POST.get('mother_email')
        present_address = request.POST.get('present_address')
        permanent_address = request.POST.get('permanent_address')

        if Student.objects.filter(student_id=student_id).exists():
            messages.error(request, "A student with this Student ID already exists.")
            return render(request, "students/add-student.html")

        try:
            parent = Parent.objects.create(
                father_name=father_name,
                father_occupation=father_occupation,
                father_mobile=father_mobile,
                father_email=father_email,
                mother_name=mother_name,
                mother_occupation=mother_occupation,
                mother_mobile=mother_mobile,
                mother_email=mother_email,
                present_address=present_address,
                permanent_address=permanent_address
            )
            student = Student.objects.create(
                first_name=first_name,
                last_name=last_name,
                student_id=student_id,
                student_email=student_email,
                gender=gender,
                date_of_birth=date_of_birth,
                student_class=student_class,
                religion=religion,
                joining_date=joining_date,
                mobile_number=mobile_number,
                admission_number=admission_number,
                section=section,
                student_image=student_image,
                parent=parent
            )
            Notification.objects.create(
                user=request.user,
                message=f"Added Student: {student.first_name} {student.last_name}"
            )
            messages.success(request, "Student added successfully!")
            return redirect("student_list")
        except Exception as e:
            messages.error(request, f"Error adding student: {str(e)}")
            return render(request, "students/add-student.html")
    return render(request, "students/add-student.html")

@login_required
def edit_student(request, slug):
    student = get_object_or_404(Student, slug=slug)
    parent = student.parent
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        student_id = request.POST.get('student_id')
        student_email = request.POST.get('student_email')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        student_class = request.POST.get('student_class')
        religion = request.POST.get('religion')
        joining_date = request.POST.get('joining_date')
        mobile_number = request.POST.get('mobile_number')
        admission_number = request.POST.get('admission_number')
        section = request.POST.get('section')
        student_image = request.FILES.get('student_image') or student.student_image
        father_name = request.POST.get('father_name')
        father_occupation = request.POST.get('father_occupation')
        father_mobile = request.POST.get('father_mobile')
        father_email = request.POST.get('father_email')
        mother_name = request.POST.get('mother_name')
        mother_occupation = request.POST.get('mother_occupation')
        mother_mobile = request.POST.get('mother_mobile')
        mother_email = request.POST.get('mother_email')
        present_address = request.POST.get('present_address')
        permanent_address = request.POST.get('permanent_address')

        if student_id != student.student_id and Student.objects.filter(student_id=student_id).exists():
            messages.error(request, "A student with this Student ID already exists.")
            return render(request, "students/edit-student.html", {'student': student, 'parent': parent})

        try:
            parent.father_name = father_name
            parent.father_occupation = father_occupation
            parent.father_mobile = father_mobile
            parent.father_email = father_email
            parent.mother_name = mother_name
            parent.mother_occupation = mother_occupation
            parent.mother_mobile = mother_mobile
            parent.mother_email = mother_email
            parent.present_address = present_address
            parent.permanent_address = permanent_address
            parent.save()

            student.first_name = first_name
            student.last_name = last_name
            student.student_id = student_id
            student.student_email = student_email
            student.gender = gender
            student.date_of_birth = date_of_birth
            student.student_class = student_class
            student.religion = religion
            student.joining_date = joining_date
            student.mobile_number = mobile_number
            student.admission_number = admission_number
            student.section = section
            student.student_image = student_image
            student.save()

            Notification.objects.create(
                user=request.user,
                message=f"Updated Student: {student.first_name} {student.last_name}"
            )
            messages.success(request, "Student updated successfully!")
            return redirect("student_list")
        except Exception as e:
            messages.error(request, f"Error updating student: {str(e)}")
            return render(request, "students/edit-student.html", {'student': student, 'parent': parent})
    return render(request, "students/edit-student.html", {'student': student, 'parent': parent})

@login_required
def view_student(request, slug):
    student = get_object_or_404(Student, slug=slug)
    context = {'student': student}
    return render(request, "students/student-details.html", context)

@login_required
def delete_student(request, slug):
    if request.method == "POST":
        student = get_object_or_404(Student, slug=slug)
        student_name = f"{student.first_name} {student.last_name}"
        student.delete()
        Notification.objects.create(
            user=request.user,
            message=f"Deleted Student: {student_name}"
        )
        messages.success(request, "Student deleted successfully!")
        return redirect('student_list')
    return HttpResponseForbidden()

@login_required
def student_list(request):
    students = Student.objects.all()
    context = {
        'student_list': students,
        'unread_notification': Notification.objects.filter(user=request.user, is_read=False),
        'unread_notification_count': Notification.objects.filter(user=request.user, is_read=False).count()
    }
    return render(request, "students/students.html", context)