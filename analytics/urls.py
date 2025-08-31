from django.urls import path
from . import views

urlpatterns = [
    path("", views.analytics_dashboard, name="analytics_dashboard"),
    path("add-grade/", views.add_student_grade, name="add_student_grade"),
    path("train-model/", views.train_ml_model, name="train_ml_model"),
]