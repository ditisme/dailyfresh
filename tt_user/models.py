from django.db import models

# Create your models here.
class UserInfo(models.Model):
    uname = models.CharField(max_length=20)
    upwd = models.CharField(max_length=40)
    uemail = models.EmailField(max_length=40)

    class Meta:
        db_table = 'userinfo'

class UserAddrInfo(models.Model):
    urecipients = models.CharField(max_length=20, default='')
    uaddress = models.CharField(max_length=100, default='')
    uphone = models.CharField(max_length=11, default='')

    user = models.ForeignKey('UserInfo')

    class Meta:
        db_table='useraddr'
