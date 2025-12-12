from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Student, Course, Region, District, Session
from .forms import StudentForm, CourseForm

def home(request):
    """
    Renders the home page. If the user is logged in and has a student profile,
    it redirects them to their profile page.
    """
    if request.user.is_authenticated:
        # Check if a student profile exists for the logged-in user
        student = Student.objects.filter(user=request.user).first()
        if student:
            # Redirect to the student's success/details page
            return redirect('apply:student_profile')
            
    all_courses = Course.objects.all()
    return render(request, 'applications/home.html', {'courses': all_courses})

def student_list(request):
    students = Student.objects.all()
    return render(request, 'applications/student_list.html', {'students': students})

def course_list(request):
    all_courses = Course.objects.all()
    return render(request, 'applications/course_list.html', {'courses': all_courses})

@login_required
def add_student(request):
    """
    Handles student application form for logged-in users.
    If the user already has a student profile, it redirects them.
    """
    if hasattr(request.user, 'student'):
        # User is already registered as a student, show the 'already_registered' page
        profile_url = reverse('apply:student_profile')
        return render(request, 'applications/already_registered.html', {'profile_url': profile_url})

    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.user = request.user  # Link the student to the logged-in user
            student.save()
            return redirect('apply:student_profile')
    else:
        initial_data = {}
        course_id = request.GET.get('course')
        if course_id:
            initial_data['course'] = course_id
        form = StudentForm(initial=initial_data)
    
    regions = Region.objects.all()
    return render(request, 'applications/add_student.html', {
        'form': form,
        'regions': regions,
    })

def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('apply:course_list')
    else:
        form = CourseForm()
    return render(request, 'applications/add_course.html', {'form': form})

def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'applications/student_detail.html', {'student': student})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'applications/course_detail.html', {'course': course})

@login_required
def student_profile(request):
    """
    Displays the registered student's information.
    This view renders the 'registration_success.html' template.
    """
    student = get_object_or_404(Student, user=request.user)
    return render(request, 'applications/registration_success.html', {'student': student})

def enroll_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('apply:student_detail', student_id=student.id)
    else:
        form = StudentForm(instance=student)
    return render(request, 'applications/enroll_student.html', {'form': form, 'student': student})

@login_required
def edit_student(request):
    student = get_object_or_404(Student, user=request.user)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your information has been updated successfully!')
            return redirect('apply:student_profile')
    else:
        form = StudentForm(instance=student)
    
    return render(request, 'applications/edit_student.html', {'form': form})

def ajax_districts(request, region_id):
    districts = list(District.objects.filter(region_id=region_id).values('id', 'name'))
    return JsonResponse({'districts': districts})

def ajax_sessions(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    sessions = list(course.sessions.all().values('id', 'name'))
    return JsonResponse({'sessions': sessions})
