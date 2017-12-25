from stark.service import v1
from . import models
from django.utils.safestring import mark_safe
from django.conf.urls import url
from django.shortcuts import redirect,render,HttpResponse
from django.forms import ModelForm



class DepartmentConfig(v1.StarkConfig):
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


# class UserInfoModelForm(ModelForm):
#     class Meta:
#         model = models.UserInfo
#         fields = ["username","password"]

class UserInfoConfig(v1.StarkConfig):

    #模糊查询
    show_search_form = True
    search_fields = ['name__contains', 'email__contains',]


    list_display = [ 'name', 'username', 'email','depart',]

    comb_filter = [

        v1.FilterOption('depart'),

    ]



    # model_form_class = UserInfoModelForm

v1.site.register(models.UserInfo,UserInfoConfig)




class CourseConfig(v1.StarkConfig):
    list_display = ['name']
    # edit_link = ['name']

v1.site.register(models.Course,CourseConfig)



class SchoolConfig(v1.StarkConfig):
    list_display = ['title']
    edit_link = ['title']

v1.site.register(models.School,SchoolConfig)


class ClassListConfig(v1.StarkConfig):

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



class CustomerConfig(v1.StarkConfig):
    def display_gender(self,obj=None,is_header=False):
        if is_header:
            return '性别'
        return obj.get_gender_display


    def display_education(self,obj=None,is_header=False):
        if is_header:
            return '学历'
        return obj.get_education_display

    def display_course(self,obj=None,is_header=False):
        if is_header:
            return '咨询课程'
        course_list = obj.course.all()
        html = []
        for item in course_list:
            # temp = "<a href='/stark/crm/customer/%s/%s/dc'>X</a>"%(obj.pk,item.pk,item.name)
            #href  中，第一个%s----obj.pk（当前的课程id），，，，第二个%s----item.pk(咨询课程的id)

            temp = "<a style='display:inline-block;padding:3px 5px;border:1px solid blue;margin:2px;' href='/stark/crm/customer/%s/%s/dc/'>%s X</a>" % (obj.pk, item.pk, item.name)

            html.append(temp)

        return mark_safe(" ".join(html))


    def display_status(self,obj=None,is_header=False):
        if is_header:
            return '状态'
        return obj.get_status_display()

    def record(self,obj=None,is_header=False):
        if is_header:
            return '跟进记录'
        return mark_safe("<a href='/stark/crm/consultrecord/?customer=%s'>查看跟进记录</a>" %(obj.pk))

    list_display = ['qq', 'name', display_gender, display_education,display_course,display_status,record]
    edit_link = ['qq']


    def delete_course(self,request,customer_id,course_id):
        """
               删除当前用户感兴趣的课程
               :param request:
               :param customer_id:
               :param course_id:
               :return:
               """
        customer_obj = self.model_class.objects.filter(pk=customer_id).first()
        customer_obj.course.remove(course_id)

        return redirect(self.get_list_url())

    #删除咨询课程的小标签
    def extra_url(self):

        app_model_name = (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        patterns = [
            url(r'^(\d+)/(\d+)/dc/$', self.wrap(self.delete_course), name="%s_%s_dc" %app_model_name),
        ]
        return patterns

v1.site.register(models.Customer,CustomerConfig)



class ConsultRecordConfig(v1.StarkConfig):
    #跟进记录
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







class PaymentRecordConfig(v1.StarkConfig):
    # def pay_type_choices(self,obj=None,is_header=False):
    #     if is_header:
    #         return '缴费类型选择'
    #     return obj.get_pay_type_choices_display



    list_display = ['customer','class_list','consultant']

v1.site.register(models.PaymentRecord,PaymentRecordConfig)




class StudentConfig(v1.StarkConfig):


    list_display = ['customer','username','emergency_contract','class_list','company','location','position','salary','welfare','date']
    edit_link = ['class_list']

v1.site.register(models.Student,StudentConfig)




class CourseRecordConfig(v1.StarkConfig):

    list_display = ['class_obj','day_num',]

v1.site.register(models.CourseRecord,CourseRecordConfig)




class StudyRecordConfig(v1.StarkConfig):
    def course_record(self,obj=None,is_header=False):
        if is_header:
            return '第几天课程'
        return obj.get_course_record_display()

    def student(self,obj=None,is_header=False):
        if is_header:
            return '学员'
        return obj.get_student_display()

    def record(self,obj=None,is_header=False):
        if is_header:
            return '上课记录'
        return obj.get_record_display()

    def score(self,obj=None,is_header=False):
        if is_header:
            return '本节成绩'
        return obj.get_score_display()




    list_display = [course_record,student,record,score,'date']
v1.site.register(models.StudyRecord,StudyRecordConfig)