from django.db import models
from django.conf import settings
from django.utils.text import slugify

class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'is_teacher': True})
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    teacher_id = models.CharField(max_length=20, unique=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')])
    date_of_birth = models.DateField()
    department = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    joining_date = models.DateField()
    address = models.TextField()
    teacher_image = models.ImageField(upload_to='teachers/', blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.first_name}-{self.last_name}-{self.teacher_id}")
        super(Teacher, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.teacher_id})"
# Create your models here.
