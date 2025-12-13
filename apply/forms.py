from django import forms
from .models import Student, Course, Region, District, Session
from django.forms.widgets import Select

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'middle_name', 'last_name', 'email', 'gender', 'phone', 'region', 'district']
        widgets = {
            'gender': forms.Select(attrs={'class':'form-select'}),
            'region': forms.Select(attrs={'class': 'form-select cascade-region'}),
            'district': forms.Select(attrs={'class': 'form-select cascade-district'}),
            'phone': forms.TextInput(attrs={'class':'form-control'}),
            'first_name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter your first name'}),
            'middle_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs and kwargs['instance'] and kwargs['instance'].region:
            self.fields['district'].queryset = District.objects.filter(region=kwargs['instance'].region).order_by('name')
        else:
            self.fields['district'].queryset = District.objects.none()

        if 'region' in self.data:
            self.fields['district'].queryset = District.objects.filter(region_id=self.data.get('region')).order_by('name')

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_id','title','lecturer','duration_months','cost','description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'lecturer': forms.TextInput(attrs={'class':'form-control'}),
            'duration_months': forms.NumberInput(attrs={'class':'form-control','min':1}),
            'cost': forms.NumberInput(attrs={'class':'form-control','step':'0.01'}),
            'description': forms.Textarea(attrs={'class':'form-control','rows':4}),
            'course_id': forms.TextInput(attrs={'class':'form-control'}),
        }
