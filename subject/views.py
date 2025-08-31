from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Subject
from teacher.models import Teacher
from school.models import Notification

def subject_list(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to view subjects.")
        return redirect('login')
    subjects = Subject.objects.all()
    return render(request, 'subjects/subject-list.html', {'subjects': subjects})

def add_subject(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to add a subject.")
        return redirect('login')
    if not request.user.is_teacher and not request.user.is_superuser:
        messages.error(request, "You do not have permission to add a subject.")
        return HttpResponseForbidden()
    if request.method == "POST":
        subject = Subject(
            name=request.POST.get('name'),
            code=request.POST.get('code'),
            teacher_id=request.POST.get('teacher'),
            description=request.POST.get('description', '')
        )
        subject.save()
        Notification.objects.create(
            user=request.user,
            message=f"Added Subject: {subject.name}"
        )
        messages.success(request, "Subject added successfully")
        return redirect("subject_list")
    teachers = Teacher.objects.all()
    return render(request, "subjects/add-subject.html", {'teachers': teachers})

def edit_subject(request, code):
    subject = Subject.objects.get(code=code)
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to edit a subject.")
        return redirect('login')
    if not request.user.is_teacher and not request.user.is_superuser:
        messages.error(request, "You do not have permission to edit a subject.")
        return HttpResponseForbidden()
    if request.method == "POST":
        subject.name = request.POST.get('name')
        subject.code = request.POST.get('code')
        subject.teacher_id = request.POST.get('teacher')
        subject.description = request.POST.get('description', '')
        subject.save()
        Notification.objects.create(
            user=request.user,
            message=f"Updated Subject: {subject.name}"
        )
        messages.success(request, "Subject updated successfully")
        return redirect("subject_list")
    teachers = Teacher.objects.all()
    return render(request, "subjects/edit-subject.html", {'subject': subject, 'teachers': teachers})

def delete_subject(request, code):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to delete a subject.")
        return redirect('login')
    if not request.user.is_teacher and not request.user.is_superuser:
        messages.error(request, "You do not have permission to delete a subject.")
        return HttpResponseForbidden()
    subject = Subject.objects.get(code=code)
    if request.method == "POST":
        subject_name = subject.name
        subject.delete()
        Notification.objects.create(
            user=request.user,
            message=f"Deleted Subject: {subject_name}"
        )
        messages.success(request, "Subject deleted successfully")
        return redirect("subject_list")
    return render(request, "subjects/delete-subject.html", {'subject': subject})