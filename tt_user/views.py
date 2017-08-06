#coding:utf-8
from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from hashlib import sha1
from models import *
from tt_goods.models import *
import random
from PIL import Image,ImageDraw,ImageFont
from user_decorators import user_login
# Create your views here.

def register(request):
    return render(request, 'tt_user/register.html',{'top':'0'})

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

def check_user_name(request):
    user_name = request.GET.get('user_name')
    result = UserInfo.objects.filter(uname=user_name).count()
    return JsonResponse({'result':result})

def login(request):
    uname = ''
    if request.COOKIES.has_key('uname'):
        uname = request.COOKIES.get('uname')
    context = {'uname':uname,'top':'0'}
    return render(request, 'tt_user/login.html/', context)

def verify_code(request):
    bgcolor = (random.randrange(20,100),random.randrange(20,100),255)
    width = 100
    height = 38
    im = Image.new('RGB', (width, height), bgcolor)
    draw = ImageDraw.Draw(im)
    for i in range(0,100):
        xy = (random.randrange(0,width), random.randrange(0, height))
        fill = (random.randrange(0,255), 255, random.randrange(0,255))
        draw.point(xy, fill)

    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    rand_str = ''
    for i in range(0,4):
        rand_str += str1[random.randrange(0,len(str1))]

    font = ImageFont.truetype('FreeMono.ttf', 26)
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    draw.text((5, 5), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 5), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 5), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 5), rand_str[3], font=font, fill=fontcolor)

    del draw

    request.session['verifycode'] = rand_str
    import cStringIO
    buf = cStringIO.StringIO()
    im.save(buf, 'png')

    return HttpResponse(buf.getvalue(), 'image/png')


def login_handle_nv(request):

    user_name = request.GET.get('user_name')
    verify = request.GET.get('verify')

    name_result = UserInfo.objects.filter(uname=user_name).count()

    verifycode = request.session['verifycode']
    verify_result = 'false'
    if verify == verifycode:
        verify_result = 'true'
    return JsonResponse({'name_result':name_result,'verify_result':verify_result})


def login_handle(request):
    dict = request.POST
    check = dict.get('check_input')
    uname = dict.get('username')
    upwd = dict.get('pwd')

    user = UserInfo.objects.filter(uname=uname)[0]

    s1 = sha1()
    s1.update(upwd)
    upwd_sha1=s1.hexdigest()

    if user.upwd == upwd_sha1:

        request.session['uname'] = uname

        path = request.session.get('url_path', '/')

        if check == 'y':
            response = redirect(path)
            response.set_cookie('uname', uname, max_age=60 * 60 * 24)
            return response
        else:
            return redirect(path)
    else:
        return render(request, 'tt_user/login.html', {'result':1, 'top':'0'})

def logout(request):
    request.session.flush()
    return redirect('/user/login/')

def index(request):
    return render(request, 'tt_user/../templates/tt_goods/index.html')

@user_login
def center(request):
        user = UserInfo.objects.filter(uname=request.session['uname'])[0]

        goods_list = []
        if request.COOKIES.get('goods_ids'):
            goods_ids = request.COOKIES.get('goods_ids').split(',')
            for gid in goods_ids:
                goods_list.append(GoodsInfo.objects.filter(pk=gid)[0])

        context = {'user':user, 'good_list':goods_list}
        return render(request,'tt_user/user_center_info.html',context)

@user_login
def order(request):
    context = {}
    return render(request,'tt_user/user_center_order.html')

@user_login
def site(request):
    user = UserInfo.objects.get(uname=request.session['uname'])
    if request.method == 'POST':
        dict = request.POST
        uaddr = UserAddrInfo()
        uaddr.urecipients = dict.get('recipients')
        uaddr.uaddress = dict.get('address')
        uaddr.uphone = dict.get('phone')
        uaddr.user_id = user.id
        uaddr.save()
    context = {'user':user}
    return render(request,'tt_user/user_center_site.html', context)