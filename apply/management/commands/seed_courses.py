from django.core.management.base import BaseCommand
from apply.models import Course, Session
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Populate database with fake courses and sessions'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        
        # 1. Create Sessions
        session_names = [
            "Morning Session (08:00 AM - 12:00 PM)",
            "Afternoon Session (01:00 PM - 04:00 PM)",
            "Evening Session (05:00 PM - 08:00 PM)",
            "Weekend Intensive (Saturday & Sunday)",
            "Virtual / Online Class"
        ]
        
        sessions = []
        for name in session_names:
            obj, created = Session.objects.get_or_create(name=name)
            sessions.append(obj)
            if created:
                self.stdout.write(f'Created Session: {name}')

        # 2. Create Courses
        # Map filenames to titles
        course_data = [
            {
                "title": "Agribusiness Management",
                "image": "course_images/agribusiness.jpeg",
                "desc": "Master the business of agriculture. Learn supply chain management, sustainable farming practices, and agricultural economics to lead in the food sector.",
                "cost": 450000, "duration": 6, "lecturer": "Dr. Amani Juma"
            },
            {
                "title": "Artificial Intelligence & ML",
                "image": "course_images/AI.jpeg",
                "desc": "Dive into the future with AI. Covers neural networks, machine learning algorithms, and practical applications using Python and TensorFlow.",
                "cost": 850000, "duration": 8, "lecturer": "Prof. Sarah Connor"
            },
            {
                "title": "Applied Sciences Foundation",
                "image": "course_images/as_.png",
                "desc": "A comprehensive foundation in applied sciences, bridging the gap between theoretical knowledge and practical laboratory skills.",
                "cost": 500000, "duration": 12, "lecturer": "Mr. David Kim"
            },
            {
                "title": "Cybersecurity Defense",
                "image": "course_images/cybersecurity.jpeg",
                "desc": "Protect digital assets. Learn ethical hacking, network security, and risk management to become a certified cybersecurity analyst.",
                "cost": 900000, "duration": 6, "lecturer": "Ms. Robot"
            },
            {
                "title": "Data Science & Analytics",
                "image": "course_images/datascience.jpeg",
                "desc": "Transform data into insights. Master SQL, Python, and data visualization tools like Tableau to drive business decision-making.",
                "cost": 800000, "duration": 9, "lecturer": "Dr. Data Strange"
            },
            {
                "title": "Digital Marketing Mastery",
                "image": "course_images/digital-marketing.jpeg",
                "desc": "Dominate the digital space. Learn SEO, Social Media Marketing, Content Strategy, and Google Analytics.",
                "cost": 400000, "duration": 3, "lecturer": "Jane Influencer"
            },
            {
                "title": "Environmental Science",
                "image": "course_images/environmental-science.jpeg",
                "desc": "Study the interactions between physical, chemical, and biological components of the environment. Focus on sustainability and conservation.",
                "cost": 450000, "duration": 12, "lecturer": "Green Peace"
            },
            {
                "title": "Diploma in Nursing",
                "image": "course_images/nursing.jpeg",
                "desc": "Prepare for a rewarding career in healthcare. Covers patient care, anatomy, pharmacology, and clinical practice.",
                "cost": 1200000, "duration": 24, "lecturer": "Matron Nightingale"
            },
            {
                "title": "Project Management Professional",
                "image": "course_images/project-management.jpeg",
                "desc": "Learn to lead projects to success. Covers Agile, Scrum, and Waterfall methodologies with preparation for PMP certification.",
                "cost": 600000, "duration": 4, "lecturer": "Mr. Gantt"
            },
            {
                "title": "Renewable Energy Technologies",
                "image": "course_images/renewable-energy-resources.jpeg",
                "desc": "Explore the future of energy. Design and install solar, wind, and hydro energy systems for a sustainable future.",
                "cost": 700000, "duration": 8, "lecturer": "Elon Sun"
            },
            {
                "title": "Software Engineering",
                "image": "course_images/software-engineering.jpeg",
                "desc": "Become a full-stack developer. Learn HTML/CSS, JavaScript, Python/Django, and database management.",
                "cost": 950000, "duration": 12, "lecturer": "Linus Torvalds"
            }
        ]

        for i, data in enumerate(course_data):
            course, created = Course.objects.get_or_create(
                title=data['title'],
                defaults={
                    'course_id': f'CRS-{100+i}',
                    'description': data['desc'],
                    'duration_months': data['duration'],
                    'cost': data['cost'],
                    'lecturer': data['lecturer'],
                    'image': data['image']
                }
            )
            
            # Add all sessions to the course
            course.sessions.set(sessions)
            course.save()
            
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created Course: {data['title']}"))
            else:
                self.stdout.write(f"Updated Course: {data['title']}")

        self.stdout.write(self.style.SUCCESS('Successfully seeded database!'))
