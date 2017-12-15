from django.db import models

# Create your models here.

class Role(models.Model):
    caption = models.CharField(verbose_name='角色名称',max_length=32)

    def __str__(self):
        return self.caption



class UserInfo(models.Model):
    name = models.CharField(verbose_name='用户名称',max_length=32)
    email = models.EmailField(verbose_name='邮箱',max_length=32,default='123@live.com')
    pwd = models.CharField(verbose_name='密码',max_length=32,default='111')

    ut = models.ForeignKey(verbose_name='用户类型',to='UserType',default=1)

    def __str__(self):
        return self.name

class UserType(models.Model):
    xxx = models.CharField(verbose_name='类型名称',max_length=32)

    def __str__(self):
        return self.xxx
