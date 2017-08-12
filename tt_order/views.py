from django.shortcuts import render,redirect
from tt_user.user_decorators import user_login
from tt_cart.models import *
from datetime import datetime
from django.db import transaction
from models import *
from tt_user.models import *
from tt_cart.models import *

# Create your views here.

@user_login
def order(request):
    dic = request.POST
    cids = dic.getlist('cid')
    cart_list = CartInfo.objects.filter(pk__in=cids)

    uname = request.session.get('uname')
    user = UserInfo.objects.filter(uname=uname)[0]

    context = {'user':user, 'cart_list':cart_list}

    return render(request, 'tt_order/order.html', context)

@transaction.atomic
def handle(request):

    sid = transaction.savepoint()
    try:
        dict = request.POST
        addr_id = int(dict.get('addr'))
        cids = dict.getlist('cid')

        uname = request.session.get('uname')
        user = UserInfo.objects.filter(uname=uname)[0]
        uid = user.id

        order = OrderInfo()
        order.oid = '%s%d'%(datetime.now().strftime('%Y%m%d%H%M%S'),uid)
        order.user = user
        order.ototal = 0
        order.oaddress_id = addr_id
        order.save()


        carts = CartInfo.objects.filter(pk__in=cids)
        total = 0
        for cart in carts:
            if cart.goods.gkucun < cart.count:
                transaction.savepoint_rollback(sid)
                return redirect('/cart/')
            else:
                goods = cart.goods

                detail = OrderDetailInfo()
                detail.goods = goods
                detail.order = order
                detail.price = goods.gprice6z
                detail.count = cart.count
                detail.save()

                goods.gkucun -= cart.count
                goods.save()

                total += detail.count * detail.price

                cart.delete()

        order.ototal = total
        order.save()

        transaction.savepoint_commit(sid)
        return redirect('/user/order/')

    except:
        transaction.savepoint_rollback(sid)
        return redirect('/cart/')
