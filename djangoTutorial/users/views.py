from django.shortcuts import render,redirect,HttpResponse
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .auth_backend import PasswordlessAuthBackend as plb
from djangoTutorial import settings
from .middleware.oauth import OAuthMiddleware
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
# def profile(request):
#     print(render(request, 'users/profile.html'))
#     return HttpResponse("This is normal profile page")

def profile(request):
    return render(request, 'users/profile.html')

def authenticationProfile(request):
    plbObject = plb()
    userRollNo = request.session['user']['login']
    user, studentProfile = plbObject.authenticate(rollnumber=userRollNo)
    if user:
        if user.is_active:
            login(request,user)
            messages.success(request,'***Login Successful*** \n LoggedInUserName: '+str(user)+'\n CSE-UserName: '+str(studentProfile.cseusername)+'\n FirstName: '+str(studentProfile.firstname)+'\n LastName: '+str(studentProfile.lastname)+'\n RollNumber: '+str(studentProfile.rollnumber)+'\n Section:'+str(studentProfile.section))
            # messages.succes(request,'Username:')
            return redirect('blog-home')
    else:
        message = "User Name: "+ str(username)+" is Incorrect"
        return HttpResponse(message)

def login_user(request):
    print(request.path,'Path in login_user')
    oam = OAuthMiddleware()
    return oam.process_request(request)