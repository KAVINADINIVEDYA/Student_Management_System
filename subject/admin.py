from django.contrib import admin
from .models import Subject

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'teacher', 'created_at']
    search_fields = ['name', 'code']
    list_filter = ['teacher']