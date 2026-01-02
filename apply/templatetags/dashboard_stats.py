from django import template
from django.apps import apps
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.contrib.auth import get_user_model
from django.core.exceptions import FieldError
import json
import datetime

register = template.Library()

@register.simple_tag
def get_dashboard_stats():
    stats = {
        'total_students': 0,
        'total_courses': 0,
        'total_regions': 0,
        'course_labels': '[]',
        'course_data': '[]',
        'region_labels': '[]',
        'region_data': '[]',
        'region_map_data': '{}',
        'growth_labels': '[]',
        'growth_data': '[]',
        'district_labels': '[]',
        'district_data': '[]',
        'suggestions': [],
    }
    
    try:
        # Dynamically get models to avoid import errors if app structure varies
        Student = apps.get_model('apply', 'Student')
        Course = apps.get_model('apply', 'Course')
        Region = apps.get_model('apply', 'Region')
        District = apps.get_model('apply', 'District')
        User = get_user_model()
        
        stats['total_students'] = Student.objects.count()
        stats['total_courses'] = Course.objects.count()
        stats['total_regions'] = Region.objects.count()

        # Course Statistics (Top 10 by enrollment)
        courses = Course.objects.annotate(count=Count('enrolled_students', distinct=True)).order_by('-count')[:10]
        top_courses = courses  # Already sliced or ordered
        stats['course_labels'] = json.dumps([c.title for c in top_courses])
        stats['course_data'] = json.dumps([c.count for c in top_courses])

        # Region Statistics
        # Try direct relation 'student', fallback to 'district__student' if needed
        try:
            regions = Region.objects.annotate(count=Count('student', distinct=True)).order_by('-count')
        except FieldError:
            regions = Region.objects.annotate(count=Count('district__student', distinct=True)).order_by('-count')

        stats['region_labels'] = json.dumps([r.name for r in regions[:10]])
        stats['region_data'] = json.dumps([r.count for r in regions[:10]])
        
        # Map Data (Name: Count mapping)
        map_data = {r.name: r.count for r in regions}
        stats['region_map_data'] = json.dumps(map_data)

        # Growth Stats (Users joined in last 12 months)
        one_year_ago = datetime.datetime.now() - datetime.timedelta(days=365)
        growth_qs = User.objects.filter(date_joined__gte=one_year_ago)\
            .annotate(month=TruncMonth('date_joined'))\
            .values('month')\
            .annotate(count=Count('id'))\
            .order_by('month')
        
        growth_labels = [entry['month'].strftime('%b %Y') for entry in growth_qs]
        growth_data = [entry['count'] for entry in growth_qs]
        stats['growth_labels'] = json.dumps(growth_labels)
        stats['growth_data'] = json.dumps(growth_data)

        # District Stats
        try:
            districts = District.objects.annotate(count=Count('student')).order_by('-count')[:10]
            stats['district_labels'] = json.dumps([d.name for d in districts])
            stats['district_data'] = json.dumps([d.count for d in districts])
        except Exception:
            pass

        # Suggestions / AI Insights
        suggestions = []
        if stats['total_students'] < 10:
            suggestions.append("Student numbers are low. Ensure your registration form is accessible and consider a launch campaign.")
        
        if top_courses and top_courses[0].count > 0:
            suggestions.append(f"'{top_courses[0].title}' is your most popular course. Consider creating advanced modules or similar content.")
        
        if regions and regions[0].count > 0:
            suggestions.append(f"High demand detected in {regions[0].name}. Consider hosting physical events or targeted ads there.")
            
        empty_courses = [c.title for c in courses if c.count == 0]
        if empty_courses:
            suggestions.append(f"Some courses have zero enrollments. Review content or pricing for: {', '.join(empty_courses[:3])}...")

        stats['suggestions'] = suggestions

    except LookupError:
        pass # Fail silently if models aren't found
    
    return stats
