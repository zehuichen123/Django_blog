import os
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

os.environ['DJANGO_SETTINGS_MODULE'] ='django_login.settings'

if __name__=='__main__':
    subject,from_email,to='From lovesnowbest\'s check mail',\
        'lovesnowbest@sina.cn','672604803@qq.com'
    text_content="Welcome to lovesnowbest\'s login page~"
    html_content="<p>Welcome to <a href=\"https://lovesnowbest.site\">\
        Lovesnowbest</a>'s login page~"
    msg=EmailMultiAlternatives(subject,text_content,from_email,[to])
    msg.attach_alternative(html_content,'text/html')
    msg.send()