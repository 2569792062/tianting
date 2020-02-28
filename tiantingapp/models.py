from django.db import models

# Create your models here.


# 创建天庭表
class Fore(models.Model):
    # 天庭名称
    f_name = models.CharField(max_length=10)


# 创建九重天表
class Cloud(models.Model):
    # 九重天名称
    c_name = models.CharField(max_length=10)
    # 九重天要求
    c_quire = models.CharField(max_length=10)
    # 关联天庭表
    cf_id = models.ForeignKey('Fore', on_delete=models.CASCADE)


# 创建封神榜表
class Gods(models.Model):
    # 神仙名字
    g_name = models.CharField(max_length=10)
    # 神仙性别
    g_sex = models.CharField(max_length=10)
    # 岁数
    g_age = models.CharField(max_length=10)
    # 籍贯
    g_town = models.CharField(max_length=10)
    # 飞升与否
    g_easy = models.CharField(max_length=10)
    # 关联天庭表
    gf_id = models.ForeignKey('Fore', on_delete=models.CASCADE)
    # 关联九重天表
    gc_id = models.ForeignKey('Cloud', on_delete=models.CASCADE)


# 创建角色表
class Role(models.Model):
    # 角色名字
    r_name = models.CharField(max_length=10)
    # 修行等级
    r_grade = models.CharField(max_length=10)
    # 职位权限
    r_jury = models.CharField(max_length=20)


# 用户表
class Touch(models.Model):
    # 用户名
    t_name = models.CharField(max_length=20)
    # 密码
    t_pass = models.CharField(max_length=10)
    # 邮箱
    t_mail = models.CharField(max_length=20)
    # 手机号
    t_iphone = models.CharField(max_length=20)
    # 是否激活
    t_vat = models.BooleanField(default=False)
    # 关联天庭表
    tf_id = models.ForeignKey('Fore', on_delete=models.CASCADE)
    # 关联九重天表
    tc_id = models.ForeignKey('Cloud', on_delete=models.CASCADE)
    # 关联封神表
    tg_id = models.ForeignKey('Gods', on_delete=models.CASCADE)
    # 关联角色表
    tr_id = models.ForeignKey('Role', on_delete=models.CASCADE)


# 用户角色关系表
class Ation(models.Model):
    # 用户名字
    a_name = models.CharField(max_length=10)
    # 角色名字
    a_names = models.CharField(max_length=10)
    # 关联角色表
    ar_id = models.ForeignKey('Role', on_delete=models.CASCADE)
    # 关联用户表
    at_id = models.ForeignKey('Touch', on_delete=models.CASCADE)


# 模块定义表
class Icm(models.Model):
    # 模块名称
    i_name = models.CharField(max_length=10,)
    # 模块的url
    i_url = models.CharField(max_length=100, null=True)
    # 自己关联自己，设置级联
    ii_id = models.ForeignKey('Icm', on_delete=models.CASCADE, null=True)


# 角色模块关系表
class Menu(models.Model):
    # 角色名
    m_name = models.CharField(max_length=10)
    # 操作权限
    m_handle = models.CharField(max_length=6)
    # 菜单编号
    m_care = models.CharField(max_length=20)
    # 关联模块表
    mi_id = models.ForeignKey('Icm', on_delete=models.CASCADE)
    # 关联角色表
    mr_id = models.ForeignKey('Role', on_delete=models.CASCADE)


# 权限设置关系表
class Power(models.Model):
    # 权限id（主键）
    primary_key = models.CharField(max_length=10, primary_key=True)
    # 权限名字
    p_name = models.CharField(max_length=10)


# 功德表
class Quin(models.Model):
    # 神仙名字
    q_name = models.CharField(max_length=10)
    # 所犯的事
    q_thing = models.CharField(max_length=30)
    # 受到的处罚
    q_cti = models.CharField(max_length=10)
    # 关联封神榜表
    qg_id = models.ForeignKey('Gods', on_delete=models.CASCADE)


# 宝物表
class Sure(models.Model):
    # 宝物名字
    s_name = models.CharField(max_length=20)
    # 宝物介绍
    s_mend = models.CharField(max_length=50)
    # 宝物数量
    s_cou = models.CharField(max_length=10)
    # 佩戴要求
    s_adr = models.CharField(max_length=10)
    # 归属人
    s_exif = models.CharField(max_length=10)
    # 好感度
    s_favor = models.CharField(max_length=10)


# 蟠桃表
class Canned(models.Model):
    # 蟠桃名字
    c_name = models.CharField(max_length=10)
    # 蟠桃介绍
    c_mes = models.CharField(max_length=50)
    # 打理人
    c_dai = models.CharField(max_length=20)
    # 蟠桃寿命
    c_spa = models.CharField(max_length=10)
    # 蟠桃成长情况
    c_grow = models.CharField(max_length=10)
    # 蟠桃总数
    c_cou = models.CharField(max_length=10)


# 炼丹和神兵表
class Rwt(models.Model):
    # 名字
    r_name = models.CharField(max_length=10)
    # 介绍
    r_mes = models.CharField(max_length=50)
    # 数量
    r_spa = models.CharField(max_length=10)
    # 归属人
    r_grow = models.CharField(max_length=10)
    # 自己关联自己，设置级联
    rr_id = models.ForeignKey('Rwt', on_delete=models.CASCADE, null=True)


# 传送地点表
class Lite(models.Model):
    # 地点名称
    l_name = models.CharField(max_length=10)
    # 距离多远
    l_dist = models.CharField(max_length=10)
    # 所属势力
    l_fore = models.CharField(max_length=10)


# 灵田表
class Worn(models.Model):
    # 灵田名字
    w_name = models.CharField(max_length=10)
    # 耕种人
    w_bou = models.CharField(max_length=10)
    # 每亩产量
    w_yed = models.CharField(max_length=10)
    # 灵田效果
    w_ect = models.CharField(max_length=50)
    # 所占亩数
    w_acre = models.CharField(max_length=10)


# 喜结良缘表
class Yeah(models.Model):
    # 境界
    y_name = models.CharField(max_length=10)
    # 德行
    y_vxi = models.CharField(max_length=10)
    # 家世
    y_aes = models.CharField(max_length=10)
    # 缘分值
    y_evd = models.CharField(max_length=10)
    # 婚配与否
    y_fbe = models.CharField(max_length=10)
    # 关联封神表
    yg_id = models.ForeignKey('Gods', on_delete=models.CASCADE)


# 日志表
class Ory(models.Model):
    # 日志模块
    o_name = models.CharField(max_length=10)
    # 操作人
    o_arts = models.CharField(max_length=10)
    # 备注
    o_mark = models.CharField(max_length=20)
    # 执行操作
    o_exe = models.CharField(max_length=10)
    # 日期
    o_time = models.DateTimeField(auto_now_add=True)


# 进度表
class Dies(models.Model):
    # 操作人
    d_name = models.CharField(max_length=10)
    # 所做操作
    d_rate = models.CharField(max_length=10)
    # 相关进度
    d_dist = models.CharField(max_length=10)
    # 关联炼丹神兵表
    dr_id = models.ForeignKey('Rwt', on_delete=models.CASCADE, null=True)
    # 关联蟠桃成长进度表
    dc_id = models.ForeignKey('Canned', on_delete=models.CASCADE, null=True)


# 玉皇大帝命令表
class Evil(models.Model):
    # 发布命令者
    e_name = models.CharField(max_length=10)
    # 接受命令者
    e_take = models.CharField(max_length=10)
    # 内容
    e_det = models.CharField(max_length=30)
    # 注意事项
    e_note = models.CharField(max_length=20)
    # 发布时间
    e_time = models.DateTimeField(auto_now_add=True)






