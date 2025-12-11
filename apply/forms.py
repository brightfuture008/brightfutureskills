from django import forms
from .models import Student, Course, Region, District, Session

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['fullname','email','gender','phone','course','session','region','district']
        widgets = {
            'gender': forms.Select(attrs={'class':'form-select'}),
            'course': forms.Select(attrs={'class':'form-select select2-course'}),
            'region': forms.Select(attrs={'class':'form-select cascade-region'}),
            'district': forms.Select(attrs={'class':'form-select cascade-district'}),
            'phone': forms.TextInput(attrs={'class':'form-control'}),
            'fullname': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'session': forms.Select(attrs={'class':'form-select'}),
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_id','title','lecturer','duration_months','cost','description', 'sessions']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'lecturer': forms.TextInput(attrs={'class':'form-control'}),
            'duration_months': forms.NumberInput(attrs={'class':'form-control','min':1}),
            'cost': forms.NumberInput(attrs={'class':'form-control','step':'0.01'}),
            'description': forms.Textarea(attrs={'class':'form-control','rows':4}),
            'course_id': forms.TextInput(attrs={'class':'form-control'}),
            'sessions': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 4}),
        }
