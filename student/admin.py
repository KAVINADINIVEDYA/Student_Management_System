from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Parent, Student

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('father_name', 'mother_name', 'father_mobile', 'mother_mobile')
    search_fields = ('father_name', 'mother_name', 'father_mobile', 'mother_mobile')
    list_filter = ('father_name', 'mother_name')  # Consider removing or replacing with better filters

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'student_id', 'gender', 'date_of_birth', 'student_class', 'joining_date', 'mobile_number', 'admission_number', 'section', 'student_email')
    search_fields = ('first_name', 'last_name', 'student_id', 'student_class', 'admission_number', 'student_email')
    list_filter = ('gender', 'student_class', 'section')
    readonly_fields = ('student_image',)