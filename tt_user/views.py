from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from hashlib import sha1
from models import *
from django.template import loader,RequestContext
# Create your views here.

def register(request):
    return render(request, 'tt_user/register.html')

def register_handle(request):
    dict = request.POST
    uname = dict.get('user_name')
    upwd = dict.get('pwd')
    ucpwd = dict.get('cpwd')
    uemail = dict.get('email')

    if ucpwd != upwd:
        return redirect('/user/register/')

    s1 = sha1()
    s1.update(upwd)
    upwd_sha1=s1.hexdigest()

    user = UserInfo()
    user.uname = uname
    user.upwd = upwd_sha1
    user.uemail = uemail
    user.save()

    return redirect('/user/login/')

def check_user_name(request, user_name):
    list = UserInfo.objects.filter(uname=user_name)
    if len(list) == 0:
        result = 'True'
    else:
        result = 'False'
    return JsonResponse({'result':result})

def login(request):
    uname = ''
    if request.COOKIES.has_key('uname'):
        uname = request.COOKIES.get('uname')
    context = {'uname':uname}
    return render(request, 'tt_user/login.html/', context)

def login_handle_name(request, user_name):
    list = UserInfo.objects.filter(uname=user_name)
    if len(list) == 0:
        result = 'False'
    else:
        result = 'True'
    return JsonResponse({'result':result})

def login_handle_pwd(request,user_name, user_pwd):

    list = UserInfo.objects.filter(uname=user_name)

    s1 = sha1()
    s1.update(user_pwd)
    user_pwd_sha1=s1.hexdigest()

    if list[0].upwd == user_pwd_sha1:
        pwd_result = 'True'
    else:
        pwd_result = 'False'

    return JsonResponse({'pwd_result':pwd_result})

def login_handle(request):
    dict = request.POST
    check = dict.get('check_input')
    uname = dict.get('username')

    if check == 'y':
        template = loader.get_template('tt_user/index.html/')
        context = RequestContext(request, {})
        response = HttpResponse(template.render(context))
        response.set_cookie('uname', uname, max_age=60*60*24)
    else:
        template = loader.get_template('tt_user/index.html/')
        context = RequestContext(request, {})
        response = HttpResponse(template.render(context))
        response.set_cookie('uname', '', max_age=60 * 60 * 24)
    return response


def index(request):
    return render(request, 'tt_user/index.html')