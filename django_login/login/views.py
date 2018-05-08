from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from . import forms
import hashlib
# Create your views here.

def index(request):
    pass
    return render(request,'login/index.html')

def login(request):
    if request.session.get('is_login',None):
        return redirect('/index/')
    if request.method=="POST":
        login_form=forms.UserForm(request.POST)
        message="Please check your input"
        if login_form.is_valid():
            username=login_form.cleaned_data['username']
            password=login_form.cleaned_data['password']
            try:
                user=models.User.objects.get(name=username)
                if user.password==hash_code(password):
                    request.session['is_login']=True
                    request.session['user_id']=user.id
                    request.session['user_name']=user.name
                    return redirect('/index/')
                else:
                    message="Password is incorrect!"
            except:
                message="User is not exists!"
        return render(request,'login/login.html',locals())
    login_form=forms.UserForm()
    return render(request,'login/login.html',locals())

def register(request):
    if request.session.get('is_login',None):
        return redirect('/index/')
    if request.method=='POST':
        register_form=forms.RegisterForm(request.POST)
        message="Please input content!"
        if register_form.is_valid():
            username=register_form.cleaned_data['username']
            password1=register_form.cleaned_data['password1']
            password2=register_form.cleaned_data['password2']
            email=register_form.cleaned_data['email']
            sex=register_form.cleaned_data['sex']
            if password1!=password2:
                message="password is not inconsistent!"
                return render(request,'login/register.html',locals())
            else:
                same_name_user=models.User.objects.filter(name=username)
                if same_name_user:
                    message="User has already existed!"
                    return render(request,'login/register.html',locals())
                same_email_user=models.User.objects.filter(email=email)
                if same_email_user:
                    message="Email has already been used!"
                    return render(request,'login/register.html',locals())
                # if all ok, create an account
                new_user=models.User()
                new_user.name=username
                new_user.password=hash_code(password1)
                new_user.email=email
                new_user.sex=sex
                new_user.save()
                return redirect('/login/')
    register_form=forms.RegisterForm()
    return render(request,'login/register.html',locals())

def logout(request):
    if not request.session.get('is_login',None):
        return redirect('/index/')
    request.session.flush()
    return redirect('/index/')

def hash_code(s,salt="mysite"):
    h=hashlib.sha256()
    s+=salt
    h.update(s.encode())
    return h.hexdigest()