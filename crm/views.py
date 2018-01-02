from django.shortcuts import HttpResponse,render,redirect
from rbac import models
from rbac.service.init_permission import init_permission




def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        user = models.User.objects.filter(username=user,password=pwd).first()

        if user:
            #表示已登录
            request.session['user_info'] = {'user_id':user.id,'uid':user.userinfo.id,'name':user.userinfo.name}
            #权限写入session中
            init_permission(user,request)

            #跳转
            return redirect('/index/')
        return render(request,'index.html')


def index(request):
    return render(request,'index.html')



