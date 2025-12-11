from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Student, Course, Region, District
from .forms import StudentForm, CourseForm

app_name = 'applications'

def home(request):
    all_courses = Course.objects.all()
    return render(request, 'applications/home.html', {'courses': all_courses})

def student_list(request):
    students = Student.objects.all()
    return render(request, 'applications/student_list.html', {'students': students})

def course_list(request):
    all_courses = Course.objects.all()
    return render(request, 'applications/course_list.html', {'courses': all_courses})

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            return redirect('applications:home')
    else:
        form = StudentForm()
    courses = Course.objects.all()
    regions = Region.objects.all()
    return render(request, 'applications/add_student.html', {
        'form': form,
        'courses': courses,
        'regions': regions,
    })

def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('applications:course_list')
    else:
        form = CourseForm()
    return render(request, 'applications/add_course.html', {'form': form})

def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'applications/student_detail.html', {'student': student})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'applications/course_detail.html', {'course': course})

def enroll_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('applications:student_detail', student_id=student.id)
    else:
        form = StudentForm(instance=student)
    return render(request, 'applications/enroll_student.html', {'form': form, 'student': student})

def ajax_districts(request, region_id):
    districts = list(District.objects.filter(region_id=region_id).values('id', 'name'))
    return JsonResponse({'districts': districts})




