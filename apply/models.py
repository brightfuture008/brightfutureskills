from django.db import models
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Session(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    course_id = models.CharField(max_length=20, unique=True, blank=True)  # human id / code
    title = models.CharField(max_length=200)
    lecturer = models.CharField(max_length=120, blank=True)
    duration_months = models.PositiveSmallIntegerField(default=1, help_text="Duration in months")    
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='course_images/', blank=True, null=True, help_text="Upload a picture for the course.")
    sessions = models.ManyToManyField(Session, blank=True, related_name='courses')

    def __str__(self):
        if self.course_id:
            return f"{self.title} ({self.course_id})"
        return self.title

class Region(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name

class District(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='districts')
    name = models.CharField(max_length=120)

    class Meta:
        unique_together = ('region', 'name')

    def __str__(self):
        return f"{self.name} ({self.region.name})"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    GENDER_CHOICES = (('M','Male'),('F','Female'))
    code = models.CharField(max_length=32, unique=True, editable=False)
    fullname = models.CharField(max_length=200)
    email = models.EmailField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    phone = models.CharField(max_length=20, blank=True)
    course = models.ManyToManyField(Course, blank=True, related_name='students')
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code:
            # Example code: BS2025-XXXX (random)
            while True:
                year = timezone.now().year
                rand = get_random_string(4, allowed_chars='0123456789')
                new_code = f"BS{year}-{rand}"
                if not Student.objects.filter(code=new_code).exists():
                    self.code = new_code
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.fullname} ({self.code})"