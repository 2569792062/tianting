from django.shortcuts import render, redirect, HttpResponse
from tiantingapp.models import *
from django.views import View
# 邮箱激活模块
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from tianting import settings
from itsdangerous import SignatureExpired
# 发送邮件模块
from django.core.mail import send_mail
import json
# 图片验证码模块
from io import BytesIO
from tiantingapp.check_code import create_validate_code
# 导入自定义登录装饰器
from tiantingapp.timos import *
# 导入登录类视图模块
from django.utils.decorators import method_decorator
import random
# 导入阿里云接口文件
from tiantingapp import aliyunsms, restful
from django.core.cache import cache


# Create your views here.


# 发送短信
def send_sms(request):
    # 接口地址:/duanxin/send_sms/?phone=xxxx
    # 1 获取手机
    phone = request.GET.get('phone')
    print('手机:' + phone)
    # 2 生成6位随机码
    code = aliyunsms.get_code(6, False)
    # 3 缓存到redis
    cache.set(phone, code, 5*60)  # 300s有效
    print('是否写入redis成功:', cache. has_key(phone))
    print('打印code:', cache.get(phone))
    # 4 发短信
    result = aliyunsms.send_sms(phone, code)
    print(result)
    return HttpResponse(result)


# 短信验证
def check_sms(request):
    # /duanxin/check_sms/?phone=xxx&code=xx
    # 1 后去电话和code
    phone = request.GET.get('phone')
    code = request.GET.get('code')
    # 2 获取Resis中code
    cache_code = cache.get(phone)
    # 3 判断
    if code == cache_code:
        return restful.ok("OK", data=None)
    else:
        return restful.page_error("False", data=None)


# 注册ajax验证接口
def gain(request):
    # 获取用户名
    uname = request.GET['code']
    users = Touch.objects.filter(t_name=uname)
    if users:
        # 已经被注册,不能用了
        return HttpResponse(json.dumps({'result': 'false'}))
    else:
        return HttpResponse(json.dumps({'result': 'ok'}))


# 激活函数
class ActiveView(View):
    def get(self, request, token):
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            user_id = info['confirm']
            print(333, user_id)
            user = Touch.objects.get(id=user_id)
            user.t_vat = 1
            user.save()
            return redirect('login')
        except SignatureExpired as e:
            return HttpResponse("激活链接已过期")


# 注册
class RegDetailView(View):

    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        use = request.POST.get('username')
        psd = request.POST.get('password')
        ema = request.POST.get('email')
        iph = request.POST.get('iphone')
        if Touch.objects.filter(t_name=use):
            return render(request, 'register.html', {'err': '用户名已存在！'})
        else:
            if Touch.objects.filter(t_mail=ema):
                return render(request, 'register.html', {'err': '邮箱已存在！'})
            else:
                if Touch.objects.filter(t_iphone=iph):
                    return render(request, 'register.html', {'err': '手机号已存在！'})
                else:
                    # 封神榜随机数
                    fsb = len(Gods.objects.all())
                    # 角色表随机数
                    jsb = len(Role.objects.all())
                    fs = random.randint(1, fsb)
                    js = random.randint(1, jsb)
                    users = Touch.objects.create(t_name=use, t_pass=psd, t_mail=ema, t_iphone=iph, t_vat=0, tf_id_id=1, tc_id_id=9, tg_id_id=fs, tr_id_id=js)
                    cz = Touch.objects.filter(t_name=use)
                    for tt in cz:
                        oi = tt.id
                        si = tt.tr_id_id
                        qi = Role.objects.filter(id=si)
                        for vv in qi:
                            zi = vv.id
                            di = vv.r_jury
                            wi = vv.r_name
                            Ation.objects.create(a_name=use, a_names=wi, ar_id_id=js, at_id_id=oi)
                            Menu.objects.create(m_name=wi, m_handle=di, m_care=12, mi_id_id=1, mr_id_id=zi)
                    if users:
                        serializer = Serializer(settings.SECRET_KEY, 3600)
                        info = {'confirm': users.id}
                        token = serializer.dumps(info)
                        token = token.decode()

                        subject = '天庭欢迎你！'
                        message = '恭喜你应劫而生，成为天庭一员！'
                        sender = settings.EMAIL_FROM
                        receiver = [ema]

                        html_message = '''<h1>%s 恭喜你成为天庭外门一份子</h1><br/><h3>请你在1小时内点击以下链接进行账户激 活</h3><a href="http://127.0.0.1:8000/active/%s">http://127.0.0.1:8000/active/%s</a> ''' % (use, token, token)
                        send_mail(subject, message, sender, receiver, html_message=html_message)

                        request.session["username"] = use
                        return render(request, 'login.html')
                    else:
                        return render(request, 'register.html')


# 图文验证码
def check_code(request):
    stream = BytesIO()
    img, code = create_validate_code()
    img.save(stream, 'PNG')
    request.session['valid_code'] = code
    print(2, code)
    return HttpResponse(stream.getvalue())


# 登录
class LoginDetailView(View):

    def get(self, request):
        stream = BytesIO()
        img, code = create_validate_code()
        img.save(stream, 'PNG')
        request.session['valid_code'] = code
        return render(request, 'login.html', {'stream': stream.getvalue()})

    def post(self, request):
        li = []
        dic = {}
        use = request.POST.get('username')
        psd = request.POST.get('password')
        code = request.POST.get('check_code')
        if Touch.objects.filter(t_name=use, t_pass=psd):
            if code.upper() == request.session.get('valid_code').upper():
                request.session["username"] = use
                request.session.set_expiry(600)
                gg = request.session.get('username')
                f = Ation.objects.filter(a_name=gg).values('ar_id__menu__m_care')
                for x in f:
                    for u in x['ar_id__menu__m_care']:
                        cc = Icm.objects.filter(ii_id=u)
                        for q in cc:
                            li.append(q)

                dic['ff'] = li
                dic['uss'] = gg
                return render(request, 'index.html', dic)
            else:
                return render(request, 'login.html', {'err': '验证码错误！'})
        else:
            return render(request, 'login.html', {'err': '口令或暗语错误！'})


# 首页
@method_decorator(login_required, name='get')
class IndexDetailView(View):

    def get(self, request):
        gg = request.session.get('username')
        return render(request, 'index.html', {'uss': gg})

    def post(self, request):

        # li = []
        # dic = {}
        gg = request.session.get('username')
        # f = Ation.objects.filter(a_name=gg).values('ar_id__menu__m_care')
        # for x in f:
        #     for u in x['ar_id__menu__m_care']:
        #         cc = Icm.objects.filter(ii_id=u)
        #         for q in cc:
        #             li.append(q)
        #
        # dic['ff'] = li
        # dic['uss'] = gg
        # return render(request, 'index.html', dic)
        return render(request, 'index.html', {'uss': gg})


# 权限分类
class CateDetailView(View):

    def get(self, request):
        return render(request, 'admin-cate.html')

    def post(self, request):
        return render(request, 'admin-cate.html')


# 修改密码
class AlterDetailView(View):

    def get(self, request):
        return render(request, 'admin-password.html')

    def post(self, request):
        gg = request.session.get('username')
        usr = request.POST.get('username')
        old = request.POST.get('oldpass')
        new = request.POST.get('newpass')
        rep = request.POST.get('repass')
        # 拿到手机号
        phone = request.POST.get('phone')
        code = request.POST.get('smscode')
        # 2 获取Resis中code
        cache_code = cache.get(phone)
        if usr and old and new and rep and phone and code:
            if gg == usr:
                if Touch.objects.filter(t_name=usr, t_pass=old):
                    if new == rep:
                        if code == cache_code:
                            Touch.objects.filter(t_name=usr).update(t_pass=new)
                            return redirect('login')
                        else:
                            return render(request, 'admin-password.html', {'err': '验证码失败！'})
                    else:
                        return render(request, 'admin-password.html', {'err': '两次输入密码不一致！'})
                else:
                    return render(request, 'admin-password.html', {'err': '用户名或密码错误！'})
            else:
                return render(request, 'admin-password.html', {'err': '只能更改当前账号信息！'})
        else:
            return render(request, 'admin-password.html', {'err': '请正确输入！'})


# 管理员列表
class ListsDetailView(View):

    def get(self, request):
        dic = {}
        li = []
        jiu = Cloud.objects.all()
        you = Gods.objects.all()
        dic['jiu'] = jiu
        dic['you'] = you
        gg = request.session.get('username')
        qi = Touch.objects.filter(t_name=gg)

        gaga = Evil.objects.all()

        for yi in gaga:
            li.append(yi.e_take)

        for cc in qi:
            ei = Gods.objects.filter(id=cc.tg_id_id)
            for vv in ei:
                if vv.g_name == '玉皇大帝':
                    dic['yhdd'] = 'yhdd'
                    return render(request, 'admin-list.html', dic)
                elif vv.g_name in li:
                    hei = Evil.objects.filter(e_take=vv.g_name)
                    dic['hei'] = hei
                    return render(request, 'admin-list.html', dic)
                else:
                    dic['yss'] = '只对内部人员开放!!'
                    return render(request, 'admin-list.html', dic)

    def post(self, request):
        dic = {}
        gg = request.session.get('username')
        jiu = Cloud.objects.all()
        you = Gods.objects.all()

        dic['you'] = you
        dic['jiu'] = jiu

        # 地域
        di = request.POST.get('contrller')
        # 性别
        sex = request.POST.get('contrllers')
        # 发送的内容
        nei = request.POST.get('nr')
        nei2 = request.POST.get('nr2')
        # 某个人
        haha = request.POST.getlist('yy[]')
        print('我是哈哈哈', haha)
        qi = Touch.objects.filter(t_name=gg)
        for cc in qi:
            ei = Gods.objects.filter(id=cc.tg_id_id)
            for vv in ei:
                if vv.g_name == '玉皇大帝':
                    if nei or nei2 == '':
                        dic['yhdd'] = 'yhdd'
                        dic['err'] = '请输入内容！'
                        return render(request, 'admin-list.html', dic)
                    else:
                        if di and sex and nei:
                            vi = Gods.objects.filter(gc_id_id=di)
                            for xx in vi:
                                if xx.g_sex == sex:
                                    Evil.objects.create(e_name='玉皇大帝', e_take=xx.g_name, e_det=nei, e_note='无')
                                    dic['yhdd'] = 'yhdd'
                                    dic['err'] = '传音成功！'
                                    return render(request, 'admin-list.html', dic)
                                else:
                                    dic['yhdd'] = 'yhdd'
                                    dic['err'] = '此重天中没有该性别'
                                    return render(request, 'admin-list.html', dic)

                        elif di and nei:
                            vi = Gods.objects.filter(gc_id_id=di)
                            for ss in vi:
                                Evil.objects.create(e_name='玉皇大帝', e_take=ss.g_name, e_det=nei, e_note='无')
                                dic['yhdd'] = 'yhdd'
                                dic['err'] = '传音成功！'
                                return render(request, 'admin-list.html', dic)
                        elif sex and nei:
                            vi = Gods.objects.filter(g_sex=sex)
                            for ss in vi:
                                Evil.objects.create(e_name='玉皇大帝', e_take=ss.g_name, e_det=nei, e_note='无')
                                dic['yhdd'] = 'yhdd'
                                dic['err'] = '传音成功！'
                                return render(request, 'admin-list.html', dic)
                        elif haha and nei2:
                            print(9999)
                            for tt in haha:
                                vi = Gods.objects.filter(id=tt)
                                for ss in vi:
                                    Evil.objects.create(e_name='玉皇大帝', e_take=ss.g_name, e_det=nei2, e_note='无')
                                    dic['yhdd'] = 'yhdd'
                                    dic['err'] = '传音成功！'
                                    return render(request, 'admin-list.html', dic)
                        else:
                            dic['err'] = '请正确输入！'
                            return render(request, 'admin-list.html', dic)
                else:
                    dic['yss'] = '只对内部人员开放'
                    return render(request, 'admin-list.html', dic)


# 角色管理
class RoleDetailView(View):

    def get(self, request):
        return render(request, 'admin-role.html')

    def post(self, request):
        return render(request, 'admin-role.html')


# 权限管理
class RuleDetailView(View):

    def get(self, request):
        li = []
        ai = []
        dic = {}
        ic = Icm.objects.filter(i_url=None)
        for ee in ic:
            li.append(ee)
        ix = Power.objects.all()
        for xx in ix:
            ai.append(xx)
        dic['li'] = li
        dic['ai'] = ai
        return render(request, 'admin-rule.html', dic)

    def post(self, request):
        xm1 = request.session.get('xm1')
        name = request.POST.get('name')
        gg = request.session.get('username')
        li = []
        ai = []
        dic = {}
        ic = Icm.objects.filter(i_url=None)
        for ee in ic:
            li.append(ee)
        ix = Power.objects.all()
        for xx in ix:
            ai.append(xx)
        dic['li'] = li
        dic['ai'] = ai
        # 菜单id
        cd1 = request.POST.getlist('xx[]')
        # 权限id
        qx1 = request.POST.getlist('yy[]')
        uu = Touch.objects.filter(t_name=gg).values('tr_id__r_name')
        for x in uu:
            if x['tr_id__r_name'] == '帝王':
                if name:
                    xjs = Gods.objects.filter(g_name=xm1)
                    if xjs:
                        for qq in xjs:
                            zz = Touch.objects.filter(tg_id_id=qq.id)
                            for q in zz:
                                # 新角色名
                                Role.objects.filter(id=q.tr_id_id).update(r_name=name)

                                cd = ''.join(cd1)
                                qx = list(map(int, qx1))
                                qx2 = sum(qx)

                                ui = Role.objects.filter(id=q.tr_id_id)
                                # 用户角色表中的新角色名
                                for w in ui:
                                    io = Ation.objects.filter(ar_id_id=w.id)
                                    for oo in io:
                                        Menu.objects.filter(m_name=oo.a_names).update(m_name=name, m_handle=qx2, m_care=cd)
                                        Ation.objects.filter(ar_id_id=w.id).update(a_names=name)

                            dic['err'] = '修改成功！'
                            return render(request, 'admin-rule.html', dic)
                    else:
                        dic['err'] = '请输入已存在的角色名！'
                        return render(request, 'admin-rule.html', dic)
                else:
                    dic['err'] = '请输入角色名！'
                    return render(request, 'admin-rule.html', dic)
            else:
                return redirect('rule')


# 新增角色
class PartDetailView(View):

    def get(self, request):
        li = []
        ai = []
        ti = []
        gi = []
        wei = []
        hao = []
        ww = 0
        dic = {}
        ic = Icm.objects.filter(i_url=None)
        gg = request.session.get('username')

        uu = Touch.objects.filter(t_name=gg).values('tr_id__r_name')
        for x in uu:
            if x['tr_id__r_name'] == '帝王':
                for ee in ic:
                    li.append(ee)
                ix = Power.objects.all()
                for xx in ix:
                    ai.append(xx)

                # 模块重组
                xxb = Touch.objects.all()
                for q in xxb:
                    zxc = Touch.objects.filter(id=q.id).values('tr_id__r_name')
                    # 模块
                    for asd in zxc:

                        aa = asd['tr_id__r_name']
                        ss = Menu.objects.filter(m_name=aa)

                        for dd in ss:
                            qqq = len(dd.m_care)
                            for ff in dd.m_care:
                                pp = Icm.objects.filter(id=ff)
                                for tt in pp:
                                    ww += 1
                                    if ww == qqq:
                                        ww = 0
                                        gi.append(tt.i_name)
                                        gi.append(333)
                                    else:
                                        gi.append(tt.i_name)
                for ccc in gi:
                    if ccc != 333:
                        wei.append(ccc)

                    else:
                        ggg = '<-->'.join(wei)
                        hao.append(ggg)
                        wei.clear()

                # 信息表展示
                xxb = Touch.objects.all()

                for q in xxb:
                    xxc = Touch.objects.filter(id=q.id).values('tg_id__g_name')
                    for w in xxc:
                        xxd = Touch.objects.filter(id=q.id).values('tg_id__gc_id__c_name')
                        for e in xxd:
                            xxe = Touch.objects.filter(id=q.id).values('tr_id__r_name')
                            for f in xxe:
                                xxf = Touch.objects.filter(id=q.id).values('tr_id__r_grade')
                                for g in xxf:
                                    dii = {
                                        'yh': q.t_name,
                                        'xm': w['tg_id__g_name'],
                                        'zy': e['tg_id__gc_id__c_name'],
                                        'jj': f['tr_id__r_name'],
                                        'wz': g['tr_id__r_grade'],
                                    }
                                    ti.append(dii)

                dic['hao'] = hao
                dic['li'] = li
                dic['ai'] = ai
                dic['ci'] = ti
                dic['dw'] = 'ss'
                return render(request, 'role-add.html', dic)
            else:
                # 模块重组
                xxb = Touch.objects.all()
                for q in xxb:
                    zxc = Touch.objects.filter(id=q.id).values('tr_id__r_name')
                    # 模块
                    for asd in zxc:

                        aa = asd['tr_id__r_name']
                        ss = Menu.objects.filter(m_name=aa)

                        for dd in ss:
                            qqq = len(dd.m_care)
                            for ff in dd.m_care:
                                pp = Icm.objects.filter(id=ff)
                                for tt in pp:
                                    ww += 1
                                    if ww == qqq:
                                        ww = 0
                                        gi.append(tt.i_name)
                                        gi.append(333)
                                    else:
                                        gi.append(tt.i_name)
                for ccc in gi:
                    if ccc != 333:
                        wei.append(ccc)

                    else:
                        ggg = '<-->'.join(wei)
                        hao.append(ggg)
                        wei.clear()

                # 信息表展示
                xxb = Touch.objects.all()

                for q in xxb:
                    xxc = Touch.objects.filter(id=q.id).values('tg_id__g_name')
                    for w in xxc:
                        xxd = Touch.objects.filter(id=q.id).values('tg_id__gc_id__c_name')
                        for e in xxd:
                            xxe = Touch.objects.filter(id=q.id).values('tr_id__r_name')
                            for f in xxe:
                                xxf = Touch.objects.filter(id=q.id).values('tr_id__r_grade')
                                for g in xxf:
                                    dii = {
                                        'yh': q.t_name,
                                        'xm': w['tg_id__g_name'],
                                        'zy': e['tg_id__gc_id__c_name'],
                                        'jj': f['tr_id__r_name'],
                                        'wz': g['tr_id__r_grade'],
                                    }
                                    ti.append(dii)

                dic['hao'] = hao
                dic['li'] = li
                dic['ai'] = ai
                dic['ci'] = ti
                return render(request, 'role-add.html', dic)

    def post(self, request):
        li = []
        ai = []
        ti = []
        dic = {}
        # 菜单id
        cd1 = request.POST.getlist('xx[]')
        # 权限id
        qx1 = request.POST.getlist('yy[]')
        # 角色名
        jsm = request.POST.get('name')
        xm1 = request.POST.get('xm1')
        ic = Icm.objects.filter(i_url=None)
        for ee in ic:
            li.append(ee)
        ix = Power.objects.all()
        for xx in ix:
            ai.append(xx)
        dic['li'] = li
        dic['ai'] = ai

        if cd1 and qx1:
            if jsm:
                cd = ''.join(cd1)
                qx = list(map(int, qx1))
                qx2 = sum(qx)
                Role.objects.create(r_name=jsm, r_grade='散仙', r_jury=qx2)
                sss = Role.objects.filter(r_name=jsm)
                for ii in sss:
                    Menu.objects.create(m_name=jsm, m_handle=qx2, m_care=cd, mi_id_id=1, mr_id_id=ii.id)
                    dic['err'] = '添加成功！'
                    return render(request, 'role-add.html', dic)
            else:
                dic['err'] = '请输入角色名！'
                return render(request, 'role-add.html', dic)
        elif xm1:
            request.session["xm1"] = xm1
            return redirect('rule')
        else:
            dic['err'] = '菜单和权限每种至少选择一个！'
            return render(request, 'role-add.html', dic)


# 拆线图
class Ech1DetailView(View):

    def get(self, request):
        return render(request, 'echarts1.html')

    def post(self, request):
        return render(request, 'echarts1.html')


# 柱状图
class Ech2DetailView(View):

    def get(self, request):
        return render(request, 'echarts2.html')

    def post(self, request):
        return render(request, 'echarts2.html')


# 地图
class Ech3DetailView(View):

    def get(self, request):
        return render(request, 'echarts3.html')

    def post(self, request):
        return render(request, 'echarts3.html')


# 饼图
class Ech4DetailView(View):

    def get(self, request):
        return render(request, 'echarts4.html')

    def post(self, request):
        return render(request, 'echarts4.html')


# 雷达图
class Ech5DetailView(View):

    def get(self, request):
        return render(request, 'echarts5.html')

    def post(self, request):
        return render(request, 'echarts5.html')


# K线图
class Ech6DetailView(View):

    def get(self, request):
        return render(request, 'echarts6.html')

    def post(self, request):
        return render(request, 'echarts6.html')


# 热力图
class Ech7DetailView(View):

    def get(self, request):
        return render(request, 'echarts7.html')

    def post(self, request):
        return render(request, 'echarts7.html')


# 仪表图
class Ech8DetailView(View):

    def get(self, request):
        return render(request, 'echarts8.html')

    def post(self, request):
        return render(request, 'echarts8.html')


# 羽化成仙
class MedDetailView(View):

    def get(self, request):
        li = []
        dic = {}
        xr = Gods.objects.filter(g_easy='是')
        for qwe in xr:
            li.append(qwe)
        gg = request.session.get('username')
        # 拿到操作权限
        cz = Ation.objects.filter(a_name=gg).values('ar_id__r_jury')
        li1 = [16, 8, 4, 2, 1]
        li2 = []

        for dd in cz:
            num = int(dd['ar_id__r_jury'])
            for i in li1:
                if i <= num:
                    li2.append(i)
                    num -= i
                else:
                    continue
        li3 = []
        for x in li2:
            qq = Power.objects.filter(primary_key=x)
            for yy in qq:
                li3.append(yy)
        dic['xr'] = li
        dic['qx'] = li3
        return render(request, 'member-del.html', dic)

    def post(self, request):
        li = []
        dic = {}
        li3 = []

        gg = request.session.get('username')
        # 拿到操作权限
        cz = Ation.objects.filter(a_name=gg).values('ar_id__r_jury')
        li1 = [16, 8, 4, 2, 1]
        li2 = []

        for dd in cz:
            num = int(dd['ar_id__r_jury'])
            for i in li1:
                if i <= num:
                    li2.append(i)
                    num -= i
                else:
                    continue
        for x in li2:
            qq = Power.objects.filter(primary_key=x)
            for yy in qq:
                li3.append(yy)
        # 前端获取的人名id
        ip1 = request.POST.get('ip1')
        # 前端获取的增删改查id
        ip2 = request.POST.get('ip2')
        ww = Power.objects.filter(primary_key=ip2)
        for zz in ww:
            if zz.primary_key == '1':
                return redirect('zeng')
            elif zz.primary_key == '2':
                Gods.objects.filter(id=ip1).delete()
                uu = Gods.objects.filter(g_easy='是')
                for rr in uu:
                    li.append(rr)
            elif zz.primary_key == '4':
                request.session["ip1"] = ip1
                request.session.set_expiry(600)
                return redirect('ater')
            elif zz.primary_key == '8':
                # return render(request, 'member-edit.html')
                return redirect('refe')
            else:
                pass
        dic['xr'] = li
        dic['qx'] = li3
        return render(request, 'member-del.html', dic)


# 渡劫人数增加
class FortDetailView(View):

    def get(self, request):
        return render(request, 'zengren.html')

    def post(self, request):
        name = request.POST.get('sxm')
        sex = request.POST.get('sex')
        age = request.POST.get('age')
        jg = request.POST.get('jg')
        fsy = request.POST.get('fs')
        if name and sex and age and jg and fsy:
            if Gods.objects.filter(g_name=name):
                return render(request, 'zengren.html', {'err': '该人已经存在！'})
            else:
                if sex == '男' or '女':
                    if int(age) >= 0:
                        if '国' or '朝' or '虚无' in jg:
                            if fsy == '是' or '否':
                                Gods.objects.create(g_name=name, g_sex=sex, g_age=age, g_town=jg, g_easy=fsy, gf_id_id=1, gc_id_id=9)
                                return redirect('memdel')
                            else:
                                return render(request, 'zengren.html', {'请正确输入飞升选项！'})
                        else:
                            return render(request, 'zengren.html', {'err': '请正确输入籍贯！'})
                    else:
                        return render(request, 'zengren.html', {'err': '请正确输入年龄！'})
                else:
                    return render(request, 'zengren.html', {'err': '请正确输入男女！'})
        else:
            return render(request, 'zengren.html', {'err': '请全部输入！'})


# 渡劫飞升
class MemDetailView(View):

    def get(self, request):
        li = []
        dic = {}
        xr = Gods.objects.filter(g_easy='否')
        for qwe in xr:
            li.append(qwe)
        gg = request.session.get('username')
        # 拿到操作权限
        cz = Ation.objects.filter(a_name=gg).values('ar_id__r_jury')
        li1 = [16, 8, 4, 2, 1]
        li2 = []

        for dd in cz:
            num = int(dd['ar_id__r_jury'])
            for i in li1:
                if i <= num:
                    li2.append(i)
                    num -= i
                else:
                    continue
        li3 = []
        for x in li2:
            qq = Power.objects.filter(primary_key=x)
            for yy in qq:
                li3.append(yy)
        dic['xr'] = li
        dic['qx'] = li3
        return render(request, 'member-list.html', dic)

    def post(self, request):
        li = []
        dic = {}
        li3 = []

        gg = request.session.get('username')
        # 拿到操作权限
        cz = Ation.objects.filter(a_name=gg).values('ar_id__r_jury')
        li1 = [16, 8, 4, 2, 1]
        li2 = []

        for dd in cz:
            num = int(dd['ar_id__r_jury'])
            for i in li1:
                if i <= num:
                    li2.append(i)
                    num -= i
                else:
                    continue

        for x in li2:
            qq = Power.objects.filter(primary_key=x)
            for yy in qq:
                li3.append(yy)
        # 前端获取的人名id
        ip1 = request.POST.get('ip1')
        # 前端获取的增删改查id
        ip2 = request.POST.get('ip2')
        ww = Power.objects.filter(primary_key=ip2)
        for zz in ww:
            if zz.primary_key == '1':
                Gods.objects.filter(id=ip1).update(g_easy='是')
                uu = Gods.objects.filter(g_easy='否')
                for rr in uu:
                    li.append(rr)
            elif zz.primary_key == '2':
                Gods.objects.filter(id=ip1).delete()
                uu = Gods.objects.filter(g_easy='否')
                for rr in uu:
                    li.append(rr)
            elif zz.primary_key == '4':
                request.session["ip1"] = ip1
                request.session.set_expiry(600)
                return redirect('ater')
            elif zz.primary_key == '8':
                # return render(request, 'member-edit.html')
                return redirect('refe')
            else:
                pass
        dic['xr'] = li
        dic['qx'] = li3
        return render(request, 'member-list.html', dic)


# 封神榜更改
class AiterDetailView(View):

    def get(self, request):
        return render(request, 'member-add.html')

    def post(self, request):
        ip1 = request.session.get('ip1')
        name = request.POST.get('name')
        sex = request.POST.get('sex')
        age = request.POST.get('age')
        jg = request.POST.get('jg')
        fsy = request.POST.get('fsyf')
        if name and sex and age and jg and fsy:
            if sex == '男' or '女':
                if int(age) >= 0:
                    if '国' or '朝' or '虚无' in jg:
                        if fsy == '是' or '否':
                            Gods.objects.filter(id=ip1).update(g_name=name, g_sex=sex, g_age=age, g_town=jg, g_easy=fsy)
                            return redirect('memli')
                        else:
                            return render(request, 'member-add.html', {'请正确输入飞升选项！'})
                    else:
                        return render(request, 'member-add.html', {'err': '请正确输入籍贯！'})
                else:
                    return render(request, 'member-add.html', {'err': '请正确输入年龄！'})
            else:
                return render(request, 'member-add.html', {'err': '请正确输入男女！'})
        else:
            return render(request, 'member-add.html', {'err': '请全部输入！'})


# 查询信息
class ReferDetailView(View):
    def get(self, request):
        return render(request, 'member-edit.html')

    def post(self, request):
        ai = []
        js = request.POST.get('jss')
        if Gods.objects.filter(g_name=js):
            kn1 = Gods.objects.filter(g_name=js)
            ai.append(kn1)
            return render(request, 'member-edit.html', {'ai': ai})
        elif Gods.objects.filter(pk=js):
            kn2 = Gods.objects.filter(pk=js)
            ai.append(kn2)
            return render(request, 'member-edit.html', {'ai': ai})
        else:
            return render(request, 'member-edit.html', {'err': '请正确输入！'})


# 百务具举
class OrderDetailView(View):

    def get(self, request):
        li = []
        dic = {}
        gg = request.session.get('username')
        uu = Touch.objects.filter(t_name=gg).values('tr_id__r_name')
        for x in uu:
            if x['tr_id__r_name'] == '帝王':
                dw = Ory.objects.filter(o_exe='上传奏折')
                for q in dw:
                    li.append(q)
                dic['dw'] = 'ww'
                dic['li'] = li
                return render(request, 'order-list.html', dic)
            else:
                return render(request, 'order-list.html')

    def post(self, request):
        li = []
        dic = {}
        gg = request.session.get('username')
        zz1 = request.POST.get('zz1')
        yd = request.POST.get('yd1')
        sc = request.POST.get('sc1')
        uu = Touch.objects.filter(t_name=gg).values('tr_id__r_name')
        rr = Touch.objects.filter(t_name=gg).values('tg_id__g_name')
        for x in uu:
            if x['tr_id__r_name'] == '帝王':
                if sc:
                    Ory.objects.filter(id=sc).delete()
                    ssc = Ory.objects.filter(o_exe='上传奏折')
                    for q in ssc:
                        li.append(q)
                    dic['dw'] = 'ww'
                    dic['li'] = li
                    dic['err'] = '删除成功！'
                    return render(request, 'order-list.html', dic)
                elif yd:
                    Ory.objects.filter(id=yd).update(o_exe='已读奏折')
                    ssc = Ory.objects.filter(o_exe='上传奏折')
                    for q in ssc:
                        li.append(q)
                    dic['dw'] = 'ww'
                    dic['li'] = li
                    dic['err'] = '操作成功！'
                    return render(request, 'order-list.html', dic)
                else:
                    return render(request, 'order-list.html')
            else:
                if zz1:
                    for ii in rr:
                        vv = ii['tg_id__g_name']
                        Ory.objects.create(o_name='百务具举', o_arts=vv, o_mark=zz1, o_exe='上传奏折')
                        return render(request, 'order-list.html', {'err': '上交成功！'})
                else:
                    return render(request, 'order-list.html', {'err': '请输入要上交的奏折内容！'})


# 欢迎页面，九重天展示
class WelDetailView(View):

    def get(self, request):
        ai = {}
        li = []
        cloud = Cloud.objects.all()
        for x in cloud:

            fs = Gods.objects.filter(gc_id=x.id)
            for y in fs:

                dic = {
                    'us': y.g_name,
                    'ss': x.c_name,
                    'su': x.c_quire
                }
                li.append(dic)

        ai['li'] = li
        return render(request, 'welcome.html', ai)

    def post(self, request):
        return render(request, 'welcome.html')

