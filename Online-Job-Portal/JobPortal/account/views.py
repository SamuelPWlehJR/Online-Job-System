from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache

from account.forms import *
from jobapp.permission import user_is_employee, user_is_employer


def get_success_url(request):
    """
    Handle Success Url After LogIN
    """
    if 'next' in request.GET and request.GET['next'] != '':
        return request.GET['next']
    else:
        return reverse('jobapp:home')

@never_cache
def employee_registration(request):
    """
    Handle Employee Registration
    """
    form = EmployeeRegistrationForm(request.POST or None)
    if form.is_valid():
        form = form.save()
        return redirect('account:login')
    context = {
        'form': form
    }
    return render(request, 'account/employee-registration.html', context)

@never_cache
def employer_registration(request):
    """
    Handle Employer Registration 
    """
    form = EmployerRegistrationForm(request.POST or None)
    if form.is_valid():
        form = form.save()
        return redirect('account:login')
    context = {
        'form': form
    }
    return render(request, 'account/employer-registration.html', context)

@never_cache
@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def employee_edit_profile(request, id):
    """
    Handle Employee Profile Update Functionality
    """
    user = get_object_or_404(User, id=id)
    
    if request.method == 'POST':
        form = EmployeeProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Profile Was Successfully Updated!')
            return redirect(reverse("account:edit-profile", kwargs={'id': user.id}))
    else:
        form = EmployeeProfileEditForm(instance=user)

    context = {'form': form}
    return render(request, 'account/employee-edit-profile.html', context)

@never_cache
@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def employer_edit_profile(request, id):
    """
    Handle Employer Profile Update Functionality
    """
    user = get_object_or_404(User, id=id)
    
    if request.method == 'POST':
        form = EmployerProfileEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect(reverse("account:edit-profile-employer", kwargs={'id': user.id}))
    else:
        form = EmployerProfileEditForm(instance=user)

    context = {'form': form}
    return render(request, 'account/employer-edit-profile.html', context)

@never_cache
@csrf_protect
def user_logIn(request):
    """
    Handle user login with session creation
    """
    form = UserLoginForm(request.POST or None)
    
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            
            # Create a new session (Django does this automatically on login)
            request.session.cycle_key()  # Creates new session key for security
            
            # Set session timeout (optional)
            request.session.set_expiry(3600)
            
            messages.success(request, f'Welcome back, {user.username}!')
            return HttpResponseRedirect(get_success_url(request))
    
    context = {
        'form': form,
    }
    return render(request, 'account/login.html', context)

@never_cache
@login_required
def user_logOut(request):
    """
    Handle user logout with session destruction
    """
    # Store some information before logging out if needed
    username = request.user.username
    
    # Clear all session data
    request.session.flush()
    
    # Logout the user
    auth.logout(request)
    
    messages.success(request, f'You have been successfully logged out, {username}.')
    return redirect('account:login')