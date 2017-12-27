import json
from django.utils.safestring import mark_safe
from django.conf.urls import url
from django.urls import reverse
from django.shortcuts import HttpResponse,redirect,render
from crm import models
from stark.service import v1


class StudentConfig(v1.StarkConfig):

    def extra_url(self):
        app_model_name = (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        patterns = [
            url(r'^(\d+)/sv/$', self.wrap(self.scores_view), name="%s_%s_sv" % app_model_name),
            url(r'^chart/$', self.wrap(self.scores_chart), name="%s_%s_chart" % app_model_name),
        ]
        return patterns

    def scores_view(self,request,sid):
        print(sid)
        obj=models.Student.objects.filter(id=sid).first()
        if not obj:
            return HttpResponse('亲，没有您要找的人哟！')
        class_list = obj.class_list.all()
        return render(request,'scores_view.html',{'class_list':class_list,"sid":sid})


    def scores_chart(self,request):

        ret = {'status':False,'data':None,'msg':None}
        try:

            cid = request.GET.get('cid')
            sid = request.GET.get('sid')

            record_list = models.StudyRecord.objects.filter(student_id=sid,course_record__class_obj_id=cid).order_by('course_record_id')

            data = []
            for row in record_list:
                day = "day%s" %row.course_record.day_num
                data.append([day,row.score])
            ret['data'] = data

            ret['status'] = True
        except Exception as e:
            ret['msg'] = "获取失败"

        return HttpResponse(json.dumps(ret))





    def display_scores(self,obj=None,is_header=False):
        if is_header:
            return '查看成绩'

        surls = reverse("stark:crm_student_sv", args=(obj.pk,))  #注意：这个(obj.pk,),pk后边一定要加逗号，不然会报错，俺已经吃了这个标点的两次亏了
        return mark_safe("<a href='%s'>点击查看</a>" %surls)

    list_display = ['username','emergency_contract','date',display_scores]