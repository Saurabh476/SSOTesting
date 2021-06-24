from django.shortcuts import render,redirect
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .auth_backend import PasswordlessAuthBackend as plb

# messages.success
# messages.error
# messages.warning
# messages.debug
# messages.info

# Create your views here.

def register(request):
    # create registration form using html with checks
    # we can use pre-exists forms in django
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():

            # saves the data in database
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request, f'Account created {username}! Please login')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request,'users/register.html',{'form': form})

# this is decorater which adds functionality
@login_required
def profile(request):
    return render(request, 'users/profile.html')

def login_user(request):
    plbObject = plb()
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = plbObject.authenticate(username=username)
        if user:
            if user.is_active:
                login(request,user)
                messages.success(request,'Login Successful')
                return redirect('blog-home')
        else:
            messages.error(request,'username or password not correct')
            return redirect(reverse('your_login_url'))
        
                
    else:
        form = AuthenticationForm()
    return render(request,'users/login.html',{'form':form})