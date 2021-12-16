from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.auth import authenticate
from django.contrib import messages, auth
from django.core.mail import send_mail

from .forms import SignupForm, ProfileForm
from checkout.models import Application
from .models import Account

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email,username=username, password=password)
            print('useruseruser', user)
            user.save()
            messages.success(request,'Signup Successful')
            return redirect('signup')
    else:
        form = SignupForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        print('email', email, password)

        user = authenticate(email=email, password=password)
        print('user', user)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials. Please check your Email and Password')
            return redirect('login')
    return render(request, 'accounts/login.html')

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'Logged out.')
    return redirect('login')

@login_required(login_url = 'login')
def dashboard(request):
    userprofile = get_object_or_404(Account, email=request.user)
    
    context = {
        'userprofile' : userprofile
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
def edit_profile(request):
    userprofile = get_object_or_404(Account, email=request.user)
    if request.method == 'POST':
        user_form = ProfileForm(request.POST, instance=userprofile)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Profile has been updated.')
            return redirect('edit_profile')
    else:
        userprofile = ProfileForm(instance=userprofile)
    context = {
        'userprofile': userprofile,
    }
    return render(request, 'accounts/edit_profile.html', context)

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user_details = Account.objects.get(email__exact=email)
            url = get_current_site(request)
            subject = 'Forgot Password'
            body = render_to_string('accounts/forgotPassword_template.html', {
                'user_details': user_details,
                'url': url,
                'uid': urlsafe_base64_encode(force_bytes(user_details.pk)),
                'token': default_token_generator.make_token(user_details),
            })
            send_mail( subject, body, 'ysoni0303@gmail.com', [email], fail_silently=False)
            messages.success(request, 'Please check your email address, for password reset link.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html')

def forgotPasswordLink(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user_details = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user_details = None

    if user_details is not None and default_token_generator.check_token(user_details, token):
        request.session['uid'] = uid
        messages.success(request, 'Please, reset password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'Sorry, Link has been expired!')
        return redirect('login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirmPassword']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            print('user', user)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password updated successfully.')
                return redirect('change_password')
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect('change_password')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('change_password')
    return render(request, 'accounts/change_password.html')


@login_required(login_url='login')
def application_history(request):
    applications = Application.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'applications': applications,
    }
    return render(request, 'accounts/application_history.html', context)

