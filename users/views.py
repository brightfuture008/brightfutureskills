from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def signup(request):
    """
    Handles new user registration.
    """
    if request.user.is_authenticated:
        return redirect('apply:home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in automatically
            return redirect('apply:add_student') # Redirect to the application form
    else:
        form = UserCreationForm()
    
    return render(request, 'users/signup.html', {'form': form})

def profile_redirect_view(request):
    """
    Redirects from the default /accounts/profile/ to the project's home page.
    """
    return redirect('apply:home')