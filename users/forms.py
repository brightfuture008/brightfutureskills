from django import forms
from django.contrib.auth.models import User
from apply.models import Student

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.')
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput, required=True)

    class Meta:
        model = Student
        fields = ['fullname', 'email', 'gender', 'phone', 'course', 'session', 'region', 'district']
        widgets = {
            'gender': forms.Select(attrs={'class':'form-select'}),
            'course': forms.Select(attrs={'class':'form-select select2-course'}),
            'region': forms.Select(attrs={'class':'form-select cascade-region'}),
            'district': forms.Select(attrs={'class':'form-select cascade-district'}),
            'session': forms.Select(attrs={'class':'form-select'}),
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('A user with that username already exists.')
        return username

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') and cd.get('password2') and cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd.get('password2')