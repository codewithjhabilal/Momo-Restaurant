from django.shortcuts import render,redirect
from .models import *
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User 
from django.contrib.auth.password_validation import validate_password
import re

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordChangeForm
# Create your views here.

import logging

logger=logging.getLogger('django')

def index(request):
    cate=None
    momo=None

    try:
            

            cateid=request.GET.get('category')
            if cateid:
                momo=Momo.objects.filter(category=cateid)

            else:
                momo=Momo.objects.all()

            cate=Category.objects.all()

    except Exception as e:
        logger.error(str(e),exc_info=True)

    

    context={
        'cate':cate,
        'momo':momo,
        'date':datetime.now()
    }
    return render(request,'core/index.html',context)

def about(request):
    return render(request,'core/about.html')

@login_required(login_url='log_in')
def menu(request):
    return render(request,'core/menu.html')

@login_required(login_url='log_in')
def services(request):
    return render(request,'core/services.html')

def contact(request):
    if request.method=='POST':
        data=request.POST
        name=data['name']
        email=data['email']
        phone=data['phone']
        message=data['message']

        Contact.objects.create(name=name,email=email,phone=phone,message=message)

    return render(request,'core/contact.html')


"""
========================================================
========================================================
            Authentication-part
========================================================
========================================================


"""
def log_in(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        remember_me=request.POST.get('remember_me')

        if not User.objects.filter(username=username).exists():
            messages.error(request,'username is not register yet')
            return redirect('log_in')

        user=authenticate(username=username,password=password)

        if user is not None:
            login(request,user)

            if remember_me:
                request.session.set_expiry(120000000)
            else:
                request.session.set_expiry(0)

            next=request.POST.get('next','')
            return redirect(next if next else 'index')
        else:
            messages.error(request,'password does not match')
            return redirect('log_in')


    next=request.GET.get('next','')


    return render(request,'accounts/login.html',{'next':next})

def register(request):
    if request.method=='POST':
        fname=request.POST['first_name']
        lname=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password1=request.POST['password1']

        if password==password1:
            if User.objects.filter(username=username).exists():
                messages.error(request,'username already exists !!')
                return redirect('register')
            if User.objects.filter(email=email).exists():
                messages.error(request,'emailaddress already exists !!')
                return redirect('register')
            
            if not re.search(r'[A-Z]',password):
                messages.error(request,'Your password must at least contain one upper case')
                return redirect('register')
            
            
          
            # if not re.search(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$",password):
            #     messages.error(request,'Your password must at least contain one special character')
            #     return redirect('register')
            
            try:
                validate_password(password)
            
                User.objects.create_user(first_name=fname,last_name=lname,username=username,email=email,password=password)
                return redirect('register')
            except ValidationError as e:
                for i in e.messages:
                    messages.error(request,i)
                return redirect('register')

        else:
            messages.error(request,'Your password does not match')
            return redirect('register')


    return render(request,'accounts/register.html')


def log_out(request):
    logout(request)
    return redirect('log_in')

@login_required(login_url='log_in')
def password_change(request):

    form=PasswordChangeForm(user=request.user)
    if request.method=='POST':
        form=PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('log_in')
        
    return render(request,'accounts/password_change.html',{'form':form})


