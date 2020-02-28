"""tianting URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, include
from tiantingapp.views import *
from django.conf.urls import url

urlpatterns = [
    # path('admin/', admin.site.urls),
    # 登录
    path('login/', LoginDetailView.as_view(), name='login'),
    # 登录图文验证
    path('check_code/', check_code, name='check_code'),
    # 注册
    path('reg/', RegDetailView.as_view(), name='reg'),
    # 注册Ajax验证
    path('gain/', gain),
    # 邮箱激活
    url(r"^active/(?P<token>.*)$", ActiveView.as_view(), name="active"),
    # 首页
    # path('index/', IndexDetailView.as_view(), name='index'),
    path('', IndexDetailView.as_view(), name='index'),
    # 会员列表
    path('memli/', MemDetailView.as_view(), name='memli'),
    # 更改页面
    path('ater/', AiterDetailView.as_view(), name='ater'),
    # 查询页面
    path('refe/', ReferDetailView.as_view(), name='refe'),
    # 会员删除
    path('memdel/', MedDetailView.as_view(), name='memdel'),
    # 增加人数
    path('zeng/', FortDetailView.as_view(), name='zeng'),
    # 订单列表
    path('orderli/', OrderDetailView.as_view(), name='orderli'),
    # 管理员列表
    path('lists/', ListsDetailView.as_view(), name='lists'),
    # 角色管理
    path('role/', RoleDetailView.as_view(), name='role'),
    # 权限分类
    path('cate/', CateDetailView.as_view(), name='cate'),
    # 权限管理
    path('rule/', RuleDetailView.as_view(), name='rule'),
    # 拆线图
    path('echart1/', Ech1DetailView.as_view(), name='echart1'),
    # 柱状图
    path('echart2/', Ech2DetailView.as_view(), name='echart2'),
    # 地图
    path('echart3/', Ech3DetailView.as_view(), name='echart3'),
    # 饼图
    path('echart4/', Ech4DetailView.as_view(), name='echart4'),
    # 雷达图
    path('echart5/', Ech5DetailView.as_view(), name='echart5'),
    # K线图
    path('echart6/', Ech6DetailView.as_view(), name='echart6'),
    # 热力图
    path('echart7/', Ech7DetailView.as_view(), name='echart7'),
    # 仪表图
    path('echart8/', Ech8DetailView.as_view(), name='echart8'),
    # 欢迎页面，九重天
    path('welcome/', WelDetailView.as_view(), name='welcome'),
    # 个人信息
    path('alter/', AlterDetailView.as_view(), name='alter'),
    # 增加角色
    path('part/', PartDetailView.as_view(), name='part'),
    path('send_sms/', send_sms, name='sms'),
    path('check_sms/', check_sms, name='sms1'),
]
