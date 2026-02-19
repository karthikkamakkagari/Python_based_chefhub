from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CustomUser
from .forms import UpdateUserForm
from .forms import SignUpForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

def is_suprem(user):
    return user.account_type == 'SUPREM'

@login_required
@user_passes_test(is_suprem)
def user_management(request):
    users = CustomUser.objects.exclude(account_type='SUPREM')
    return render(request, 'accounts/user_management.html', {'users': users})

@login_required
@user_passes_test(is_suprem)
def edit_user(request, user_id):
    user_obj = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            return redirect('user_management')
    else:
        form = UpdateUserForm(instance=user_obj)
    return render(request, 'accounts/edit_user.html', {'form': form, 'user_obj': user_obj})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # change this to your dashboard URL name
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            error = "Invalid username or password"
            return render(request, 'accounts/login.html', {'error': error})
    return render(request, 'accounts/login.html')

@login_required
def dashboard_view(request):
    user = request.user
    return render(request, 'accounts/dashboard.html', {'user': user})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def edit_profile(request):
    user = request.user  # directly use the CustomUser instance

    if request.method == 'POST':
        # Update editable fields
        user.email = request.POST.get('email', user.email)
        user.preferred_language = request.POST.get('preferred_language', user.preferred_language)
        user.address = request.POST.get('address', user.address)
        user.phone_number = request.POST.get('phone_number', user.phone_number)
        user.sex = request.POST.get('sex', user.sex)

        # Handle profile picture upload
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']

        user.save()  # save changes directly to user model
        messages.success(request, "Profile updated successfully!")
        return redirect('dashboard')  # redirect back to dashboard

    context = {
        'user': user
    }
    return render(request, 'accounts/edit_profile.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # keeps user logged in after password change
            messages.success(request, 'Password changed successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'accounts/change_password.html', {'form': form})