from django.shortcuts import render
from django.shortcuts import render,redirect
from django.http import HttpResponse
#from django.forms import inlineformset_factory
from .models import *
#from .forms import OrderForm
#from .filters import OrderFilter
from .forms import CreateUserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from .decorators import unauthenticated_user,allowed_users


# Create your views here.

# Registration Page
@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST) 
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request,'Account was created for '+ user) 
            return redirect('login')
    
    context={'form':form}
    return render(request,'accounts/register.html',context)


# Login Page
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
       
        user = authenticate(request,username=username, password = password)
        
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Username or Password is incorrect ')     
            
    context={}
    return render(request,'accounts/login.html',context)


# Logout page
def logoutUser(request):
    logout(request)
    return redirect('login')


# @allowed_users(allowed_roles=['admin'])
@login_required(login_url='login', redirect_field_name=None)
def home(request):
    return render(request,'accounts/dashboard.html')


# Profile View for the users profile
@login_required(login_url='login', redirect_field_name=None)
def profile(request):
    profiledata = {
        "name": request.user.username,
        "email": request.user.email,
        "rank": 1,
        "badge": "Great Sage",
    }
    return render(request, "accounts/profile.html", {
        "data": profiledata,
    })
