from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings
from . import models
from . import forms
import datetime
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
                if not user.has_confirmed:
                    message="Email confirmation hasn't been done!"
                    return render(request,'login/login.html',locals())
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

                code=make_confirm_string(new_user)
                send_email(email,code)
                message="Email has been sent! Please Check!"
                return render(request,'login/confirm.html',locals())
    register_form=forms.RegisterForm()
    return render(request,'login/register.html',locals())

def logout(request):
    if not request.session.get('is_login',None):
        return redirect('/index/')
    request.session.flush()
    return redirect('/index/')

def user_confirm(request):
    code=request.GET.get('code',None)
    message=''
    try:
        confirm=models.ConfirmString.objects.get(code=code)
    except:
        message='Invalid Confirmation.'
        return render(request,'login/confirm.html',locals())
    c_time=confirm.c_time
    now=datetime.datetime.now()
    if now>c_time+datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message="Your email code has out of date!"
        return render(request,'login/confirm.html',locals())
    else:
        confirm.user.has_confirmed=True
        confirm.user.save()
        confirm.delete()
        message="thanks for confirmation. "
        return render(request,'login/confirm.html',locals())

def hash_code(s,salt="mysite"):
    h=hashlib.sha256()
    s+=salt
    h.update(s.encode())
    return h.hexdigest()

def make_confirm_string(user):
    now=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code=hash_code(user.name,now)
    models.ConfirmString.objects.create(code=code,user=user,)
    return code

def send_email(email,code):
    from django.core.mail import EmailMultiAlternatives
    subject="From lovesnowbest's check email"
    text_content="Welcome to this login page"
    html_content='''
        <p>Thanks for registering <a href="http://{}/confirm/?code={}"
         target=blank>www.lovesnowbest.site</a>,\
         This is lovensnowbest's login page.</p>
         <p>Please click link to confirm your registeration.</p>
    '''.format('127.0.0.1:8000',code,settings.CONFIRM_DAYS)
    msg=EmailMultiAlternatives(subject,text_content,settings.EMAIL_HOST_USER,[email])
    msg.attach_alternative(html_content,'text/html')
    msg.send()