from django.contrib import admin
from .models import Teacher

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'teacher_id', 'gender', 'department', 'mobile_number', 'email')
    search_fields = ('first_name', 'last_name', 'teacher_id', 'email')
    list_filter = ('gender', 'department')
    readonly_fields = ('teacher_image',)