from django.shortcuts import HttpResponse
from django.utils.safestring import mark_safe
from stark.service import v1
from app01 import models
from django.conf.urls import url
from django.forms import ModelForm


#自定制数据表中的错误信息
class UserInfoModelForm(ModelForm):
    class Meta:
        model = models.UserInfo
        fields = "__all__"
        error_messages={
            'name':{
                'required':'用户名不能为空'
            }
        }


class UserInfoConfig(v1.StarkConfig):


    list_display = ['id','name']

    #是否显示添加按钮的配置
    show_add_btn = True

    #将model_form_class加进userinfoconfig的配置中
    model_form_class = UserInfoModelForm


v1.site.register(models.UserInfo,UserInfoConfig)


class RoleConfig(v1.StarkConfig):

    list_display = ['id','caption',]

v1.site.register(models.Role,RoleConfig)

# class RoleConfig(v1,StarkConfig):
#     list_display = ['caption']









