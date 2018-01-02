from django.shortcuts import render,redirect,HttpResponse

# Create your views here.


HOST_LIST = []

for i in range(1,104):
    HOST_LIST.append("c%s.com" %i)

from utils.pager import Pagination
def hosts(request):

    pager_obj = Pagination(request.GET.get('page',1),len(HOST_LIST),request.path_info,request.GET)
    host_list = HOST_LIST[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html()

    list_condition = request.GET.urlencode()

    from django.http import QueryDict

    params = QueryDict(mutable=True)
    params['_list_filter'] = request.GET.urlencode()

    list_condition = params.urlencode()

    return render(request,'hosts.html',{'host_list':host_list,'page_html':html,'list_condition':list_condition})


USER_LIST = []

for s in range(1,302):
    USER_LIST.append('Shaojf%s' %s )


def users(request):
    pager_obj = Pagination(request.GET.get('page', 1), len(USER_LIST), request.path_info,request.GET)
    user_list = USER_LIST[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html()
    return render(request, 'users.html', {'user_list':user_list, 'page_html': html})



def edit_host(request,pk):
    if request.method == 'GET':
        return render(request,'edit_host.html')
    else:
        url = "/hosts/?%s" %(request.GET.get('_list_filter'))
        return redirect(url)

























    # current_page = int(request.GET.get('page'))
    #
    # per_page_count = 10
    #
    # start = (current_page - 1) * per_page_count
    # end = current_page * per_page_count
    # host_list = HOST_LIST[start:end]
    #
    #
    # total_count = len(HOST_LIST)
    #
    # max_page_num,div = divmod(total_count,per_page_count)
    # if div:
    #     max_page_num += 1
    #
    # page_html_list = []
    # for i in range(1,max_page_num + 1):
    #     if i == current_page:
    #         temp = '<a class="active" href="/hosts/?page=%s">%s</a>' % (i,i)
    #
    #     else:
    #         temp = '<a href="/hosts/?page=%s">%s</a>' % (i, i)
    #     page_html_list.append(temp)
    #
    # page_html = ''.join(page_html_list)
    # return render(request,'hosts.html',{'host_list':host_list,'page_html':page_html})



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