from django.shortcuts import HttpResponse,render,redirect
from django.conf.urls import url
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.http import  QueryDict

from app01 import models
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

class ChangeList(object):
    def __init__(self,config):
        self.config = config

        self.list_display = config.get_list_display()
        self.model_class = config.model_class

    def head_list(self):
        """
        构造表头
        :return:
       """
        result = []
        for field_name in self.list_display():
            if isinstance(field_name,str):


                # 根据类和字段名称，获取字段对象的verbose_name
                verbose_name = self.model_class._meta.get_field(field_name).verbose_name

            else:
                verbose_name = field_name(self.config,is_header=True)

            result.append(verbose_name)
        return result



#StarkConfig类：用于为每一个类生成url的对应关系，并处理用户的请求
class StarkConfig(object):

    #1.定制列表页面显示的列
    def checkbox(self, obj=None, is_header=False):
        if is_header:
            return '选择'
        return mark_safe('<input type="checkbox" name="pk" values="%s" />' % (obj.id,))

    def edit(self, obj=None, is_header=False):
        if is_header:
            return '编辑'
        #获取条件
        query_str = self.request.GET.urlencode()
        if query_str:
            #重新构造
            params = QueryDict(mutable=True)
            params[self._query_param_key] = query_str

            return mark_safe('<a href="%s?%s">编辑</a>' % (self.get_change_url(obj.id),params.urlencode(),))
        return mark_safe('<a href="%s">编辑</a>' % (self.get_change_url(obj.id),))


    def delete(self, obj=None, is_header=False):
        if is_header:
            return '删除'
        return mark_safe('<a href="%s">删除</a>' % (self.get_delete_url(obj.id),))

    list_display = []

    def get_list_display(self):
        data = []

        if self.list_display:
            data.extend(self.list_display)
            data.append(StarkConfig.edit)
            data.append(StarkConfig.delete)
            data.insert(0,StarkConfig.checkbox)

        return data




    # def changelist_view(self, request, *args, **kwargs):
    #     return HttpResponse('列表')

    #2.显示是否添加按钮

    show_add_btn = True

    def get_show_add_btn(self):
        return self.show_add_btn


    #3.使model_form_class是可配置的
    model_form_class = None
    def get_model_form_class(self):
        if self.model_form_class:
            return self.model_form_class

        #ModelForm提供的错误信息显示
        from django.forms import ModelForm
        #方式一 通过自己写
        class TestModelForm(ModelForm):
            class Meta:
                model = self.model_class
                fields = "__all__"

        #方式二 通过type创建
        # meta = type('Meta', (object,), {'model': self.model_class, 'fields': '__all__'})
        # TestModelForm = type('TestModelForm', (ModelForm,), {'Meta': meta})

        return TestModelForm

    def __init__(self,model_class,site):
        self.model_class = model_class
        self.site = site

        self.request = None
        self._query_param_key = "_listfilter"


#############  URL相关 ##########
    def wrap(self,view_func):
        def inner(request,*args,**kwargs):
            self.request = request
            return view_func(request,*args,**kwargs)
        return inner
    def get_urls(self):
        app_model_name = (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        url_patterns = [
            url(r'^$', self.wrap(self.changelist_view), name='%s_%s_changelist' % app_model_name),
            url(r'^add/$', self.wrap(self.add_view), name='%s_%s_add' % app_model_name),
            url(r'^(\d+)/delete/$', self.wrap(self.delete_view), name='%s_%s_delete' % app_model_name),
            url(r'^(\d+)/change/$',self.wrap(self.change_view), name='%s_%s_change' % app_model_name),
        ]

        url_patterns.extend(self.extra_url())
        return url_patterns
        #hasattr  以字符串的形式，操作对象相关的属性
       # hasattr(obj, attr):用于检查obj是否有一个名称为attr的属性，返回一个布尔值。

    #getattr   得到这个对象的属性或方法

    #isinstance() :-判断一个对象是否是已知的类型
    # eg:>>>a = 2
		# >>> isinstance (a,int)
		# True
		# >>> isinstance (a,str)
		# False
		# >>> isinstance (a,(str,int,list))    # 是元组中的一个返回 True
		# True
    def extra_url(self):
        return []
    @property
    def urls(self):
        return self.get_urls()
    def get_change_url(self,nid):
        name = "stark:%s_%s_change" % (self.model_class._meta.app_label,self.model_class._meta.model_name,)
        edit_url = reverse(name,args=(nid,))
        return edit_url
    def get_list_url(self):
        name = "stark:%s_%s_changelist" % (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        edit_url = reverse(name)
        return edit_url
    def get_add_url(self):
        name = "stark:%s_%s_add" % (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        edit_url = reverse(name)
        return edit_url
    def get_delete_url(self,nid):
        name = "stark:%s_%s_delete" % (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        edit_url = reverse(name,args=(nid,))
        return edit_url

######################  处理请求的方法###########

    #列表页面
    def changelist_view(self,request,*args,**kwargs):

        cl = ChangeList(self)

        #处理表头
        head_list = []
        for field_name in self.get_list_display():
            if isinstance(field_name,str):

                # 根据类和字段名称，获取字段对象的verbose_name
                verbose_name = self.model_class._meta.get_field(field_name).verbose_name

            else:
                verbose_name = field_name(self,is_header=True)

            head_list.append(verbose_name)


        #处理分页
        from utils.pager import Pagination
        current_page = request.GET.get('page',1)
        total_count = self.model_class.objects.all().count()


        page_obj = Pagination(current_page,total_count,request.path_info,request.GET,per_page_count=4,max_pager_count=5)



        #处理表中的数据
        #list_display = [checkbox, 'id', 'name', edit]
        data_list = self.model_class.objects.all()[page_obj.start:page_obj.end]
        new_data_list = []
        for row in data_list:
                # row是 UserInfo(id=1,name='小花')
                # row.id,row.name,

            temp = []
            for field_name in self.get_list_display():
                if isinstance(field_name,str):
                    val = getattr(row,field_name)
                else:
                    val = field_name(self,row)
                temp.append(val)
            new_data_list.append(temp)


        return render(request,'stark/changelist.html',
                      {"page_obj":page_obj,
                       'data_list':new_data_list,
                       'head_list':head_list,
                       'add_url':self.get_add_url(),
                       'show_add_btn':self.get_show_add_btn()
                       })

    #添加页面
    def add_view(self, request, *args, **kwargs):

        model_form_class=self.get_model_form_class()

        if request.method == "GET":
            form = model_form_class()
            return render(request,'stark/add_view.html',{'form':form})

        else:
            form = model_form_class(request.POST)
            if form.is_valid():
                form.save()
                return redirect(self.get_list_url())

            return render(request,'stark/add_view.html',{'form':form})

    #修改页面
    def change_view(self, request, nid, *args, **kwargs):

        obj = self.model_class.objects.filter(pk=nid).first()
        if not obj:
            return redirect(self.get_list_url())

        model_form_class = self.get_model_form_class()

        #如果是get请求，则应该显示标签 + 默认值
        if request.method == 'GET':
            form =  model_form_class(instance=obj)
            return render(request,'stark/change_view.html',{'form':form})
        else:
            #instanc=obj  ---对那个对象，拿条数据进行修改
            form = model_form_class(instance=obj,data=request.POST)
            if form.is_valid():#表示合法
                form.save()
                list_query_str = request.GET.get(self._query_param_key)
                list_url = "%s?%s" %(self.get_list_url(),list_query_str,)

                return redirect(list_url)
            return render(request,'stark/change_view.html',{'form':form})


        #return HttpResponse('修改')

    #删除页面
    def delete_view(self, request, nid, *args, **kwargs):
        self.model_class.objects.filter(pk=nid).delete()
        return redirect(self.get_list_url())




#StarkSite类：是一个容器，用于放置处理请求的对应关系
class StarkSite(object):
    def __init__(self):
        """
        {
            models.UserInfo:
        }
        """
        self._registry = {}

    def register(self, model_class, stark_config_class=None):
        if not stark_config_class:
            stark_config_class = StarkConfig
        self._registry[model_class] = stark_config_class(model_class, self)

    def get_urls(self):
        url_pattern = []

        for model_class, stark_config_obj in self._registry.items():
            app_name = model_class._meta.app_label
            model_name = model_class._meta.model_name

            curd_url = url(r'^%s/%s/' % (app_name, model_name), (stark_config_obj.urls, None, None))
            url_pattern.append(curd_url)

        return url_pattern

    @property
    def urls(self):
        return (self.get_urls(), None, 'stark')

site = StarkSite()














