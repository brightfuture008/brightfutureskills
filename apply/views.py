from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.urls import reverse
from .models import Student, Course, Region, District, Session, Enrollment, User
from users.models import Profile
from .forms import StudentForm, CourseForm

def home(request):
    """
    Renders the home page for all users.
    """
    all_courses = Course.objects.all()
    return render(request, 'applications/home.html', {'courses': all_courses})

def student_list(request):
    students = Student.objects.all()
    return render(request, 'applications/student_list.html', {'students': students})

def course_list(request):
    all_courses = Course.objects.all()
    return render(request, 'applications/course_list.html', {'courses': all_courses})

@login_required
def application_start(request):
    """
    Redirects user to the correct step in the application process.
    """
    if hasattr(request.user, 'student'):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        if profile.payment_status == Profile.PaymentStatus.APPROVED:
            return redirect('apply:course_request')
        else:
            return redirect('apply:payment')
    return redirect('apply:personal_info')

@login_required
def personal_info_view(request):
    """
    Step 1: Collect personal information.
    """
    # Get existing student instance if it exists, otherwise None.
    student_instance = getattr(request.user, 'student', None)

    if request.method == 'POST':
        # Pass instance to the form to handle both creation and update.
        form = StudentForm(request.POST, instance=student_instance)
        if form.is_valid():
            student = form.save(commit=False)
            student.user = request.user
            student.save()
            messages.success(request, 'Personal information has been saved successfully.')
            return redirect('apply:payment')
    else:
        # For a GET request, pre-populate the form if the student exists.
        form = StudentForm(instance=student_instance)
    
    regions = Region.objects.all()
    return render(request, 'applications/personal_info.html', {
        'form': form,
        'regions': regions,
        'step': 'personal_info',
    })

@login_required
def payment_view(request):
    """
    Step 2: Display payment instructions.
    """
    if not hasattr(request.user, 'student'):
        messages.info(request, 'Please fill in your personal information first.')
        return redirect('apply:personal_info')
    
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if profile.payment_status == Profile.PaymentStatus.APPROVED:
        return redirect('apply:course_request')

    return render(request, 'applications/payment_instructions.html', {'step': 'payment'})

@login_required
def course_request_view(request):
    """
    Step 3: Select courses after payment approval.
    """
    if not hasattr(request.user, 'student'):
        messages.info(request, 'Please fill in your personal information first.')
        return redirect('apply:personal_info')

    # Get or create the profile to handle users created before the signal.
    profile, created = Profile.objects.get_or_create(user=request.user)

    # Check for payment approval
    if not request.user.is_staff and profile.payment_status != Profile.PaymentStatus.APPROVED:
        messages.warning(request, 'Your payment has not been approved yet.')
        return redirect('apply:payment')

    if request.method == 'POST':
        course1_id = request.POST.get('course1')
        session1_id = request.POST.get('session1')
        course2_id = request.POST.get('course2')
        session2_id = request.POST.get('session2')

        if course1_id and session1_id:
            with transaction.atomic():
                student = request.user.student
                # Clear previous enrollments to allow changes
                student.enrollments.all().delete()
                Enrollment.objects.create(student=student, course_id=course1_id, session_id=session1_id)
                if course2_id and session2_id:
                    Enrollment.objects.create(student=student, course_id=course2_id, session_id=session2_id)
            messages.success(request, 'Your course selection has been submitted successfully!')
            return redirect('apply:student_profile')
        else:
            messages.error(request, 'Please select at least the first course and session.')

    courses = Course.objects.all()
    sessions = Session.objects.all()
    return render(request, 'applications/course_request.html', {
        'courses': courses,
        'sessions': sessions,
        'step': 'course_request',
    })

def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
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
def payment_instructions(request):
    """
    DEPRECATED: Logic is now in payment_view.
    """
    return redirect('apply:payment')

@login_required
def approve_payments_list(request):
    """
    Admin view to see users who are pending payment approval or are unpaid.
    """
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('apply:home')
    
    pending_users = User.objects.filter(profile__payment_status=Profile.PaymentStatus.PENDING).select_related('profile')
    return render(request, 'applications/admin_approve_payments.html', {'users': pending_users})

@login_required
def mark_as_paid(request):
    """
    Allows a user to mark their payment as 'Pending' for admin review.
    """
    if request.method == 'POST':
        # Use get_or_create to prevent errors for users without a profile (e.g., superuser)
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile.payment_status = Profile.PaymentStatus.PENDING
        profile.save()
        messages.success(request, "Thank you! The admin has been notified. Your payment will be reviewed shortly.")
    return redirect('apply:payment_instructions')

@login_required
def approve_user_payment(request, user_id):
    user_to_approve = get_object_or_404(User, id=user_id)
    user_to_approve.profile.payment_status = Profile.PaymentStatus.APPROVED
    user_to_approve.profile.save()
    messages.success(request, f"Payment for {user_to_approve.username} has been approved.")
    return redirect('apply:approve_payments_list')

@login_required
def student_profile(request):
    """
    Displays the registered student's profile/details page.
    This view now renders the 'student_detail.html' template for a complete summary.
    """
    student = get_object_or_404(Student, user=request.user)
    return render(request, 'applications/student_detail.html', {'student': student})

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
    # Since any course can be in any session, we return all available sessions.
    sessions = list(Session.objects.all().values('id', 'name'))
    return JsonResponse({'sessions': sessions})
