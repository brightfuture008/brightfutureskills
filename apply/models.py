from django.db import models
from django.utils.crypto import get_random_string
from django.urls import reverse

class Course(models.Model):
    course_id = models.CharField(max_length=20, unique=True, blank=True)  # human id / code
    title = models.CharField(max_length=200)
    lecturer = models.CharField(max_length=120, blank=True)
    duration_months = models.PositiveSmallIntegerField(default=1, help_text="Duration in months")
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.course_id:
            # example: CRS-0001 (simple random string)
            self.course_id = f"CRS{get_random_string(6, allowed_chars='0123456789')}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.course_id})"

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

class Kitongoji(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='kitongoji')
    name = models.CharField(max_length=100)
    def __str__(self): return f"{self.name} ({self.district.name})"

class Student(models.Model):
    GENDER_CHOICES = (('M','Male'),('F','Female'))
    code = models.CharField(max_length=32, unique=True, editable=False)
    fullname = models.CharField(max_length=200)
    email = models.EmailField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    phone = models.CharField(max_length=20, blank=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    kitongoji = models.ForeignKey(Kitongoji, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code:
            # Example code: BS2025-XXXX (random)
            year = self.created_at.year if self.created_at else ""
            rand = get_random_string(6, allowed_chars='0123456789')
            self.code = f"BS{rand}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.fullname} ({self.code})"