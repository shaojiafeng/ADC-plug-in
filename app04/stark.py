from stark.service import v1
from . import models

class RoleConfig(v1.StarkConfig):
    list_display = ['id','title']

v1.site.register(models.Role,RoleConfig)



class DepartmentConfig(v1.StarkConfig):
    list_display = ['id','caption']

v1.site.register(models.Department,DepartmentConfig)




class UserInfoConfig(v1.StarkConfig):


    #让性别显示的是汉字
    def display_gender(self,obj=None,is_header = False):
        if is_header:
            return '性别'

        return obj.get_gender_display()

    #显示部门
    def display_depart(self,obj=None,is_header=False):
        if is_header:
            return '部门'
        return obj.depart.caption

    #显示角色
    def display_roles(self,obj=None,is_header=False):
        if is_header:
            return '角色'

        html = []
        role_list = obj.roles.all()
        for role in role_list:
            html.append(role.title)

        return ",".join(html)

    list_display = ['id','name','email',display_gender,display_depart,display_roles]

    comb_filter = [
        v1.FilterOption('gender', is_choice=True),
        v1.FilterOption('depart'),
        #v1.FilterOption('depart'),如果不加condition={'id__gt': 2}  ---condition 表示对显示的数据进行筛选
        v1.FilterOption('roles', True),
    ]




    def multi_del(self,request):
        # print(request.POST)
        pk_list = request.POST.getlist('pk')
        # print(pk_list)
        self.model_class.objects.filter(id__in=pk_list).delete()


    multi_del.short_desc = "批量删除"

    def multi_init(self,request):
        pk_list = request.POST.getlist('pk')

    multi_init.short_desc = "初始化"

    actions = [multi_del,multi_init]



v1.site.register(models.UserInfo,UserInfoConfig)