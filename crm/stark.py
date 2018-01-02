from stark.service import v1
from . import models
from django.utils.safestring import mark_safe
from django.conf.urls import url
from django.shortcuts import redirect,render,HttpResponse

from django.forms import ModelForm

class BasePermission(object):

    """
    根据权限信息，确定是否显示页面的添加，编辑，以及删除按钮
    """
    def get_show_add_btn(self):
        code_list = self.request.permission_code_list
        if "add" in code_list:
            return True

    def get_edit_link(self):
        code_list = self.request.permission_code_list
        if "edit" in code_list:
            return super(SchoolConfig,self).get_edit_link()
        else:
            return []

    def get_list_display(self):
        code_list = self.request.permission_code_list
        data = []
        if self.list_display:
            data.extend(self.list_display)
            if "del" in code_list:
                data.append(v1.StarkConfig.delete)
            data.insert(0,v1.StarkConfig.checkbox)
        return data



class DepartmentConfig(BasePermission,v1.StarkConfig):
    list_display = ['title','code']
    # def get_list_display(self):
    #     result = []
    #     result.extend(self.list_display)
    #     result.append(v1.StarkConfig.edit)
    #     result.append(v1.StarkConfig.delete)
    #     result.insert(0,v1.StarkConfig.checkbox)
    #     return result

    edit_link = ['title',]
v1.site.register(models.Department,DepartmentConfig)




class UserInfoConfig(BasePermission,v1.StarkConfig):

    #模糊查询
    show_search_form = True
    search_fields = ['name__contains', 'email__contains',]


    list_display = [ 'name', 'username', 'email','depart',]

    edit_link = ['name']

    comb_filter = [

        v1.FilterOption('depart'),

    ]



v1.site.register(models.UserInfo,UserInfoConfig)




class CourseConfig(BasePermission,v1.StarkConfig):
    list_display = ['name']
    edit_link = ['name']

v1.site.register(models.Course,CourseConfig)



class SchoolConfig(BasePermission,v1.StarkConfig):
    list_display = ['title']
    edit_link = ['title',]

v1.site.register(models.School,SchoolConfig)



class ClassListConfig(BasePermission,v1.StarkConfig):

    def course_semester(self,obj=None,is_header=False):
        if is_header:
            return '班级'

        return "%s(%s期)" %(obj.course.name,obj.semester,)


    def display_teachers(self,obj=None,is_header=False):
        if is_header:
            return '任课老师'

        html = []
        teacher_list = obj.teachers.all()
        for tea in teacher_list:
            html.append(tea.name)

        return "".join(html)



    def num(self,obj=None,is_header=False):
        if is_header:
            return '人数'

        return 50


    list_display = ['school',course_semester,'price','start_date','graduate_date',num,display_teachers,'tutor']
    edit_link = [course_semester,]

v1.site.register(models.ClassList,ClassListConfig)



from crm.configs.customer import CustomerConfig

v1.site.register(models.Customer,CustomerConfig)


# 跟进记录
class ConsultRecordConfig(BasePermission,v1.StarkConfig):

    list_display = ['customer','consultant','date']

    comb_filter = [
        v1.FilterOption('customer')
    ]

    def changelist_view(self,request,*args,**kwargs):

        customer = request.GET.get('customer')

        current_login_user_id = 1   #是自己的id为12

        ct = models.Customer.objects.filter(consultant=current_login_user_id,id=customer).count()
        if not ct:
            return HttpResponse('别抢客户呀。。。')
        return super(ConsultRecordConfig,self).changelist_view(request,*args,**kwargs)

v1.site.register(models.ConsultRecord,ConsultRecordConfig)





class PaymentRecordConfig(BasePermission,v1.StarkConfig):


    list_display = ['customer','class_list','consultant']

v1.site.register(models.PaymentRecord,PaymentRecordConfig)




from crm.configs.student import StudentConfig


v1.site.register(models.Student,StudentConfig)




#老师上课记录
class CourseRecordConfig(BasePermission,v1.StarkConfig):

    def extra_url(self):
        app_model_name = (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        url_list = [
            url(r'^(\d+)/score_list/$', self.wrap(self.score_list), name="%s_%s_score_list" % app_model_name),
        ]
        return url_list

    def score_list(self,request,record_id):
        """
        自定义录入
        :param request:
        :param record_id:老师上课记录ID
        :return:
        """
        if request.method == "GET":
            # 方式一
            # study_record_list = models.StudyRecord.objects.filter(course_record_id=record_id)
            # score_choices = models.StudyRecord.score_choices
            # return render(request,'score_list.html',{'study_record_list':study_record_list,'score_choices':score_choices})
            # 方式二
            from django.forms import Form
            from django.forms import fields
            from django.forms import widgets

            # class TempForm(Form):
                #此方法不能动态生成
            #     score = fields.ChoiceField(choices=models.StudyRecord.score_choices)
            #     homework_note = fields.CharField(widget=widgets.Textarea())
            data = []
            study_record_list = models.StudyRecord.objects.filter(course_record_id=record_id)
            for obj in study_record_list:
                # obj是对象
                #自己创建Form，可以动态生成字典形式的数据
                TempForm = type('TempForm',(Form,),{
                    'score_%s' %obj.pk : fields.ChoiceField(choices=models.StudyRecord.score_choices),
                    'homework_note_%s' %obj.pk : fields.CharField(widget=widgets.Textarea())
                })
                data.append({'obj':obj,'form':TempForm(initial={'score_%s' %obj.pk:obj.score,'homework_note_%s' %obj.pk:obj.homework_note})})
            return render(request, 'score_list.html',{'data': data})
        else:
            data_dict = {}
            for key,value in request.POST.items():
                if key == "csrfmiddlewaretoken":
                    continue
                name,nid = key.rsplit('_',1)
                if nid in data_dict:
                    data_dict[nid][name] = value
                else:
                    data_dict[nid] = {name:value}

            for nid,update_dict in data_dict.items():
                models.StudyRecord.objects.filter(id=nid).update(**update_dict)

            return redirect(request.path_info)


    def kaoqin(self,obj=None,is_header=False):
        if is_header:
            return '考勤'
        return mark_safe("<a href='/stark/crm/studyrecord/?course_record=%s'>考勤管理</a>" %obj.pk)

    def display_score_list(self,obj=None,is_header=False):
        if is_header:
            return '成绩录入'

        from django.urls import reverse
        rurl = reverse("stark:crm_courserecord_score_list",args=(obj.pk,))

        return mark_safe("<a href='%s'>成绩录入</a>" %rurl)


    list_display = ['class_obj','day_num',kaoqin,display_score_list]

    def multi_init(self,request):
        """
        自定义执行批量初始化方法
        :param request:
        :return:
        """

        #拿到上课记录的id列表
        pk_list=request.POST.getlist('pk')

        #上课记录的对象
        record_list = models.CourseRecord.objects.filter(id__in=pk_list)
        for record in record_list:
            #record.class_obj  关联的班级
            exists=models.StudyRecord.objects.filter(course_record=record).exists()
            if exists:
                continue

            student_list = models.Student.objects.filter(class_list=record.class_obj)
            bulk_list = []
            for student in student_list:
                #为每个学生创建一天的学习记录
                bulk_list.append(models.StudyRecord(student=student,course_record=record))
            models.StudyRecord.objects.bulk_create(bulk_list)


        #actions可以有返回值
        #return redirect('http://www.baidu.com')


    multi_init.short_desc = '学生初始化'
    actions = [multi_init]
    show_actions = True


v1.site.register(models.CourseRecord,CourseRecordConfig)




#学生学习记录
class StudyRecordConfig(BasePermission,v1.StarkConfig):

    def display_record(self,obj=None,is_header=False):
        if is_header:
            return '出勤'
        return obj.get_record_display()

    list_display = ['course_record','student',display_record]
    comb_filter = [
        v1.FilterOption('course_record')
    ]

    def actions_checked(self,request):
        pk_list = request.POST.getlist('pk')
        models.StudyRecord.objects.filter(id__in=pk_list).update(record='checked2a@W@1')
    actions_checked.short_desc = '签到'


    def actions_vacate(self,request):
        pk_list = request.POST.getlist('pk')
        models.StudyRecord.objects.filter(id__in=pk_list).update(record='vacate')
    actions_vacate.short_desc = '请假'


    def actions_late(self,request):
        pk_list = request.POST.getlist('pk')
        models.StudyRecord.objects.filter(id__in=pk_list).update(record='late')
    actions_late.short_desc = '迟到'


    def actions_noshow(self,request):
        pk_list=request.POST.getlist('pk')
        models.StudyRecord.objects.filter(id__in=pk_list).update(record='noshow')
    actions_noshow.short_desc = '缺勤'


    def actions_leave_early(self,request):
        pk_list = request.POST.getlist('pk')
        models.StudyRecord.objects.filter(id__in=pk_list).update(record='leave_early')
    actions_leave_early.short_desc = '早退'


    actions = [actions_checked,actions_vacate,actions_late,actions_noshow,actions_leave_early]
    show_actions = True

    show_add_btn = False

v1.site.register(models.StudyRecord,StudyRecordConfig)