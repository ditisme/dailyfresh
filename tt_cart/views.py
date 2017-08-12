#coding=utf-8
from django.shortcuts import render
from django.http import JsonResponse
from tt_user.models import *
from models import *
from tt_user.user_decorators import user_login


# Create your views here.
def add(request):
    dict = request.GET
    gid = int(dict.get('gid'))
    count = int(dict.get('count'))
    uname = request.session.get('uname')
    uid = UserInfo.objects.filter(uname=uname)[0].id

    carts = CartInfo.objects.filter(user_id=uid,goods_id=gid)
    if len(carts) == 0:
        cart = CartInfo()
        cart.user_id = uid
        cart.goods_id = gid
        cart.count = count
        cart.save()
    else:
        carts[0].count += count
        carts[0].save()
    count = calc_count(uid)
    return JsonResponse({'isok':1, 'count': count})

@user_login
def cart(request):

    uname = request.session.get('uname')
    uid = UserInfo.objects.filter(uname=uname)[0].id

    cart_list = CartInfo.objects.filter(user_id=uid)

    context = {'cart':0, 'cart_list':cart_list}
    return render(request,'tt_cart/cart.html',context)


def set_num(request):
    dic = request.GET
    cid = dic.get('cart_id')
    num = int(dic.get('num'))
    cart = CartInfo.objects.filter(pk=cid)[0]
    cart.count = num
    count = cart.count
    cart.save()
    return JsonResponse({'isok':1, 'count':count})

def delcart(request):
    cid = request.GET.get('cart_id')
    cart = CartInfo.objects.filter(pk=cid)[0]
    print cart
    cart.delete()
    return JsonResponse({'isok':1})

def count(request):
    uname = request.session.get('uname')
    uid = UserInfo.objects.filter(uname=uname)[0].id
    count = calc_count(uid)
    return JsonResponse({'count':count})

def calc_count(uid):
    count = CartInfo.objects.filter(user_id=uid).count()
    # # 求商品总数，需要引入from django.db.models import Sum
    # c = CartInfo.objects.filter(user_id=uid).aggregate(Sum('count'))
    # count = c.get('count__sum')
    return count