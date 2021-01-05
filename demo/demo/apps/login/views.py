from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.http import HttpResponse
from . import models
import paramiko
from django.db import connection
import pymysql
# Create your views here.
from django.views import View
#登录逻辑判断
def login(request):
    if request.method == 'GET':

        return render(request, 'login.html')
    else :
        # add = models.Yonghu.objects.create(yonghu_id='wanghao',yonghu_secret='Www.1.com')
        # add.save()
        yonghu_id = request.POST.get('yonghu_id')
        yonghu_secret = request.POST.get('yonghu_secret')
        print('1')
        try:
            yonghu = models.Yonghu.objects.get(yonghu_id=yonghu_id)

            if yonghu:
                if yonghu.yonghu_secret == yonghu_secret:

                    return redirect('/index/')
                else:
                    return HttpResponse('密码错误')
        except:
            pass
            return HttpResponse('帐号不存在')



def index(request):
    return render(request, 'index.html')
#注册页面
def register(request):
    if request.method == 'GET':

        return render(request, 'register.html')
    else:
        yonghu_id = request.POST.get('yonghu_id')
        yonghu_secret = request.POST.get('yonghu_secret')
        add = models.Yonghu.objects.create(yonghu_id=yonghu_id,yonghu_secret=yonghu_secret)
        add.save()
        return render(request, 'login.html')
#测试
def abc(request):
    return render(request, '1.html')
#获取svn资产
def svn_asset(request):
    # 实例化SSHClient
    client = paramiko.SSHClient()

    # 自动添加策略，保存服务器的主机名和密钥信息，如果不添加，那么不再本地know_hosts文件中记录的主机将无法连接
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # 连接SSH服务端，以用户名和密码进行认证
    client.connect(hostname='192.168.1.97', port=22, username='root', password='hlyunwei!@#456')

    # 打开一个Channel并执行命令
    stdin, stdout, stderr = client.exec_command(
    "awk '{print $2}' /data/src/svn_info.txt")  # stdout 为正确输出，stderr为错误输出，同时是有1个变量有值
    # 获取svn信息
    svn_name = (str(stdout.read(), encoding='utf-8')).split('\n')

    stdin, stdout, stderr = client.exec_command(
        "awk '{print $4}' /data/src/svn_info.txt")
    path = (str(stdout.read(), encoding='utf-8')).split('\n')
    # print (path)
    stdin, stdout, stderr = client.exec_command(
         "awk '{print $19}' /data/src/svn_info.txt")
    last_change_person= (str(stdout.read(), encoding='utf-8')).split('\n')
    stdin, stdout, stderr = client.exec_command(
         "awk '{print $27}' /data/src/svn_info.txt")
    last_change_date = (str(stdout.read(), encoding='utf-8')).split('\n')

    for (i,j,k,n) in zip(svn_name,path,last_change_person,last_change_date):
        add = models.svn_asset.objects.create(svn_name=i,path=j,last_change_person=k,last_change_date=n)
        add.save()


    # 关闭SSHClient
    client.close()
    return HttpResponse('添加svn数据成功')



#清空svn资产数据库
def truncate (request):
    with connection.cursor() as cursor:
        cursor.execute("truncate table login_svn_asset")
    return HttpResponse('清空数据表成功')

def svn_list(request):

    # 创建连接对象
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='Www.1.com', db='test')
    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # 执行sql语句
    cursor.execute(
        'select id,svn_name,path,last_change_person,last_change_date from login_svn_asset ')
    # 获取查询到的所有数据
    svn_list = cursor.fetchall()
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()
    # 返回模板和数据
    return render(request, 'svn_list.html', {'svn_list': svn_list})


