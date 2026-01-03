from django import template
from django.db.models import Avg
from chat.models import CourseComment

register = template.Library()

@register.filter
def average_rating(course):
    avg = CourseComment.objects.filter(course=course).aggregate(Avg('rating'))['rating__avg']
    return float(avg) if avg else 0.0

@register.filter
def get_range(value):
    return range(int(value))

@register.filter
def subtract(value, arg):
    return value - arg