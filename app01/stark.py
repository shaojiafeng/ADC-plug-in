from django.shortcuts import HttpResponse,redirect,render
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

    show_search_form = True
    search_fields = ['name__contains', 'email__contains']

    show_actions = True

    def multi_del(self,request):
        # print(request.POST)
        pk_list = request.POST.getlist('pk')
        # print(pk_list)
        self.model_class.objects.filter(id__in=pk_list).delete()

        return redirect("http://www.baidu.com")
    multi_del.short_desc = "批量删除"

    def multi_init(self,request):
        pk_list = request.POST.getlist('pk')

    multi_init.short_desc = "初始化"

    actions = [multi_del,multi_init]


    #确定是否删除
    def delete_view(self, request, nid, *args, **kwargs):
        if request.method == 'GET':
            return render(request,'my_delete.html')

        else:
            self.model_class.objects.filter(pk=nid).delete()
            return redirect(self.get_list_url())

v1.site.register(models.UserInfo,UserInfoConfig)





class RoleConfig(v1.StarkConfig):

    list_display = ['id','caption',]

v1.site.register(models.Role,RoleConfig)




class HostConfig(v1.StarkConfig):

    #自定义列：
    def ip_port(self,obj=None,is_header=False):
        if is_header:
            return '自定制列'
        return "%s:%s" %(obj.ip,obj.port,)

    list_display = ['id', 'hostname', 'ip', 'port', ip_port]


    #添加按钮是否显示(False就不显示)
    show_add_btn = True

    #在app01/host/report    对请求的处理放在了自己的urlconfig里面
    def extra_url(self):
        urls = [
            url('^report/$',self.report_view)
        ]

        return urls
    def report_view(self,request):
        return HttpResponse('我是自定义报表')

    #重写删除按钮，进行限制代码优先寻找自己重写的方法
    def delete_view(self, request, nid, *args, **kwargs):
        if request.method == 'GET':
            return render(request,'my_delete.html')

        else:
            self.model_class.objects.filter(pk=nid).delete()
            return redirect(self.get_list_url())

v1.site.register(models.Host,HostConfig)








