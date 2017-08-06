from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from models import *

# Create your views here.

def index(request):
    typelist = TypeInfo.objects.all()
    list = []
    for type in typelist:
        list.append({
            'type':type,
            'list_new':type.goodsinfo_set.order_by('-id')[0:4],
            'list_click':type.goodsinfo_set.order_by('gclick')[0:3]
        })
    context = {'cart':'0','list':list}
    return render(request,'tt_goods/index.html', context)

def list(request):
    type_id = request.GET.get('type',1)
    page_index = request.GET.get('page',1)
    order_by = request.GET.get('order_by','-id')

    type = TypeInfo.objects.filter(pk=type_id)[0]
    goodslist = type.goodsinfo_set.order_by(order_by)

    list_new = type.goodsinfo_set.order_by('-id')[0:2]

    paginator = Paginator(goodslist, 15)

    page_index = int(page_index)
    if page_index <= 0:
        page_index = 1
    if page_index >= paginator.num_pages:
        page_index = paginator.num_pages

    page = paginator.page(page_index)

    page_range = paginator.page_range
    if paginator.num_pages > 5:
        if page.number < 3:
            page_range = range(1,6)
        elif page.number > paginator.num_pages-2:
            page_range = range(paginator.num_pages-4,paginator.num_pages+1)
        else:
            page_range = range(page.number-2, page.number+3)

    context = {'cart':0, 'list_new':list_new,'page':page, 'page_range':page_range,'type_id':type_id,'order_by':order_by}
    return render(request, 'tt_goods/list.html', context)

def detail(request):
    gid = request.GET.get('gid')

    goods = GoodsInfo.objects.filter(pk=gid)[0]

    goods.gclick += 1
    goods.save()

    list_new = goods.gtype.goodsinfo_set.order_by('-id')[0:2]

    goods_ids = request.COOKIES.get('goods_ids')

    if goods_ids:
        goods_list = goods_ids.split(',')
        if gid in goods_list:
            goods_list.remove(gid)
        else:
            if len(goods_list) >= 5:
                goods_list = goods_list[:4]
        goods_list.insert(0,gid)
    else:
        goods_list = [gid]

    context = {'cart': 0, 'goods': goods, 'list_new': list_new}

    response = render(request,'tt_goods/detail.html', context)
    response.set_cookie('goods_ids',','.join(goods_list) ,max_age=60*60*24*7)

    return response