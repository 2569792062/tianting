from django.shortcuts import redirect


# 自定义登录判断装饰器
def login_required(view_func):
    def wrapper(request, *view_args, **view_kwargs):
        # 判断用户是否登录
        if request.session.has_key('islogin'):
            # 用户登录,返回相应页面
            return view_func(request, *view_args, **view_kwargs)
        else:
            # 用户没登录，返回登录页
            return redirect('/login')
    return wrapper

