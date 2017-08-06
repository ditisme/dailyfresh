from django.contrib import admin
from models import *

# Register your models here.
class GoodsAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['gtitle', 'gprice', 'gunit']

class TypeAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['ttitle']

admin.site.register(GoodsInfo,GoodsAdmin)
admin.site.register(TypeInfo,TypeAdmin)