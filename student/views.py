import csv
import io
from django.http import HttpResponse
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
    student = get_object_or_404(Student, student_id=slug)  # Use student_id
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


import csv
import io
from django.http import HttpResponse

@login_required
def bulk_import_students(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        
        # Check if file is CSV
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a CSV file.')
            return redirect('bulk_import_students')
        
        try:
            # Read CSV file
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            csv_reader = csv.DictReader(io_string)
            
            success_count = 0
            error_count = 0
            
            for row in csv_reader:
                try:
                    # Create parent first
                    parent = Parent.objects.create(
                        father_name=row.get('father_name', ''),
                        father_mobile=row.get('father_mobile', ''),
                        father_email=row.get('father_email', ''),
                        mother_name=row.get('mother_name', ''),
                        mother_mobile=row.get('mother_mobile', ''),
                        mother_email=row.get('mother_email', ''),
                        present_address=row.get('present_address', ''),
                        permanent_address=row.get('permanent_address', '')
                    )
                    
                    # Create student
                    student = Student.objects.create(
                        first_name=row.get('first_name'),
                        last_name=row.get('last_name'),
                        student_id=row.get('student_id'),
                        gender=row.get('gender'),
                        date_of_birth=row.get('date_of_birth'),
                        student_class=row.get('student_class'),
                        religion=row.get('religion', ''),
                        joining_date=row.get('joining_date'),
                        mobile_number=row.get('mobile_number'),
                        admission_number=row.get('admission_number'),
                        section=row.get('section'),
                        student_email=row.get('student_email'),
                        parent=parent
                    )
                    success_count += 1
                    
                except Exception as e:
                    error_count += 1
                    continue
            
            # Create notification
            Notification.objects.create(
                user=request.user,
                message=f"Bulk Import: {success_count} students added, {error_count} errors"
            )
            
            messages.success(request, f'Successfully imported {success_count} students. {error_count} errors.')
            return redirect('student_list')
            
        except Exception as e:
            messages.error(request, f'Error processing CSV file: {str(e)}')
    
    return render(request, 'students/bulk-import.html')


def download_csv_template(request):
    """Download a CSV template for bulk student import"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="student_import_template.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'first_name', 'last_name', 'student_id', 'student_email', 'gender',
        'date_of_birth', 'student_class', 'religion', 'joining_date',
        'mobile_number', 'admission_number', 'section', 'father_name',
        'father_mobile', 'father_email', 'mother_name', 'mother_mobile',
        'mother_email', 'present_address', 'permanent_address'
    ])
    
    # Add a sample row
    writer.writerow([
        'John', 'Doe', 'STU001', 'john.doe@email.com', 'Male',
        '2010-01-15', 'Grade 5', 'Christian', '2025-01-01',
        '1234567890', 'ADM001', 'A', 'John Doe Sr',
        '9876543210', 'father@email.com', 'Jane Doe', '9876543211',
        'mother@email.com', '123 Main St', '123 Main St'
    ])
    
    return response