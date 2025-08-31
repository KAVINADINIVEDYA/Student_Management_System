from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import Teacher
from school.models import Notification

def add_teacher(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        teacher_id = request.POST.get('teacher_id')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        department = request.POST.get('department')
        mobile_number = request.POST.get('mobile_number')
        email = request.POST.get('email')
        joining_date = request.POST.get('joining_date')
        address = request.POST.get('address')
        teacher_image = request.FILES.get('teacher_image')

        teacher = Teacher.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            teacher_id=teacher_id,
            gender=gender,
            date_of_birth=date_of_birth,
            department=department,
            mobile_number=mobile_number,
            email=email,
            joining_date=joining_date,
            address=address,
            teacher_image=teacher_image
        )
        Notification.objects.create(
            user=request.user,
            message=f"Added Teacher: {teacher.first_name} {teacher.last_name}"
        )
        messages.success(request, "Teacher added successfully")
        return redirect("teacher_list")
    return render(request, "teachers/add-teacher.html")

def teacher_list(request):
    teacher_list = Teacher.objects.all()
    unread_notification = Notification.objects.filter(user=request.user, is_read=False)
    context = {
        'teacher_list': teacher_list,
        'unread_notification': unread_notification
    }
    return render(request, "teachers/teachers.html", context)

def edit_teacher(request, slug):
    teacher = get_object_or_404(Teacher, slug=slug)
    if request.method == "POST":
        teacher.first_name = request.POST.get('first_name')
        teacher.last_name = request.POST.get('last_name')
        teacher.teacher_id = request.POST.get('teacher_id')
        teacher.gender = request.POST.get('gender')
        teacher.date_of_birth = request.POST.get('date_of_birth')
        teacher.department = request.POST.get('department')
        teacher.mobile_number = request.POST.get('mobile_number')
        teacher.email = request.POST.get('email')
        teacher.joining_date = request.POST.get('joining_date')
        teacher.address = request.POST.get('address')
        teacher.teacher_image = request.FILES.get('teacher_image') if request.FILES.get('teacher_image') else teacher.teacher_image
        teacher.save()
        Notification.objects.create(
            user=request.user,
            message=f"Updated Teacher: {teacher.first_name} {teacher.last_name}"
        )
        messages.success(request, "Teacher updated successfully")
        return redirect("teacher_list")
    return render(request, "teachers/edit-teacher.html", {'teacher': teacher})

def view_teacher(request, slug):
    teacher = get_object_or_404(Teacher, slug=slug)
    context = {
        'teacher': teacher
    }
    return render(request, "teachers/teacher-details.html", context)

def delete_teacher(request, slug):
    if request.method == "POST":
        teacher = get_object_or_404(Teacher, slug=slug)
        teacher_name = f"{teacher.first_name} {teacher.last_name}"
        teacher.delete()
        Notification.objects.create(
            user=request.user,
            message=f"Deleted Teacher: {teacher_name}"
        )
        messages.success(request, "Teacher deleted successfully")
        return redirect('teacher_list')
    return HttpResponseForbidden()