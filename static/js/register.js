$(function () {
    $('#usr').change(function () {
        console.log('名字:'+$(this).val());
        var th = $(this);
        var uname = $(this).val();
        var URL = 'http://127.0.0.1:8000/gain';
        var data = 'code='+uname;
        doAjax(th,data,URL)
    });
    $('#pwd').change(function () {
        console.log('名字:'+$(this).val());
        var th = $(this);
        var pwd = $(this).val();
        var URL = 'http://127.0.0.1:8000/gain';
        var data = 'code='+pwd;
        doAjax(th,data,URL)
    });
    $('#email').change(function () {
        console.log('名字:'+$(this).val());
        var th = $(this);
        var email = $(this).val();
        var URL = 'http://127.0.0.1:8000/gain';
        var data = 'code='+email;
        doAjax(th,data,URL);
    });
    $('#iphone').change(function () {
        console.log('名字:'+$(this).val());
        var th = $(this);
        var iphone = $(this).val();
        var URL = 'http://127.0.0.1:8000/gain';
        var data = 'code='+iphone;
        doAjax(th,data,URL);
    });
    $('#cpwd').blur(function () {
        var cpwd = $(this).val();
        var pwd = $('#pwd').val();
        if(pwd == cpwd){
            $('#pwd2').html('两次密码一致！').removeClass('green').addClass('red')
        }else{
            $('#pwd2').html('两次密码不同，请重新输入！').removeClass('green').addClass('red')
        }
    });
    // 调用工具类
    function doAjax(th,data,URL) {
            console.log(URL);
            console.log(666, data);
            console.log(33,th[0].id);
            // 开始传入后台
            $.ajax({
                type: 'get',
                url: URL,
                data:data,
                dataType: "json",
                success: function (dws) {
                    // 网络传输返回永远为字符串，不是字典不能操作！
                    console.log(dws.result);
                    if(th[0].id == 'usr'){
                        if (dws.result == 'ok') {
                        $('#usr1').html('用户名可以使用！').removeClass('red').addClass('green')
                    } else {
                        $('#usr1').html('用户名已被占用！').removeClass('green').addClass('red')
                    }
                    }
                    else if(th[0].id == 'pwd'){
                        var pwd = th.val();
                        // var re_pwd = /^.*(?=.{2,})(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*? ]).*$/;
                        var re_pwd = /(?=.{6,12})(?=.*[a-z])(?=.*[A-Z])(?=.*\d).*/;
                        if (re_pwd.test(pwd)==false){
                            $('#pwd1').html('密码强度太低！').removeClass('green').addClass('red');
                        }else {
                            if (dws.result == 'ok') {
                                $('#pwd1').html('密码符合要求！').removeClass('red').addClass('green');
                            }else {
                            $('#pwd1').html('密码强度太低！').removeClass('green').addClass('red')
                        }
                        }
                    }
                    else if(th[0].id == 'cpwd'){
                        var cpwd = th.val();
                        var re_cpwd = /(?=.{6,12})(?=.*[a-z])(?=.*[A-Z])(?=.*\d).*/;
                        if (re_cpwd.test(cpwd)==false){
                            $('#pwd2').html('密码强度太低！').removeClass('green').addClass('red');
                        }else {
                            if (dws.result == 'ok') {
                                $('#pwd2').html('密码符合要求！').removeClass('red').addClass('green');
                            }else {
                            $('#pwd2').html('密码强度太低！').removeClass('green').addClass('red')
                        }
                        }
                    }
                    else if(th[0].id == 'email'){
                        var email = th.val();
                        var re_email = /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/
                        if (re_email.test(email)==false){
                            $('#email1').html('邮箱格式不正确！').removeClass('green').addClass('red');
                        }else {
                            if (dws.result == 'ok') {
                                $('#email1').html('邮箱格式正确！').removeClass('red').addClass('green');
                            }else {
                            $('#email1').html('邮箱已存在！').removeClass('green').addClass('red')
                        }
                        }
                    }
                    else if(th[0].id == 'iphone'){
                        var iphone = th.val();
                        // var re_iphone = /1\d{10}/;
                        var re_iphone =  /^1[34578]\d{9}$/;
                        if (re_iphone.test(iphone)==false){
                            $('#iphone1').html('手机号位数不正确！').removeClass('green').addClass('red');
                        }else {
                            if (dws.result == 'ok') {
                                $('#iphone1').html('手机号正确！').removeClass('red').addClass('green');
                            }else {
                            $('#iphone1').html('手机号已被注册！').removeClass('green').addClass('red')
                        }
                        }
                    }
                    },
                error:function(msg){
                    console.log(msg );
                    console.log('状态码:'+msg.status );
                }
            })
            }
            //提交事件
        	$('form').submit(function(event) {
        	flag = true;
        	//alert('点提交了....');
        	//如果一个不合法 flag=false.自动不跳转
        	$("form :input.layui-input").each(function(){
        		if($(this).val()==''){
        			flag = false;
        			}
        		})
        		if(flag==false){
        			alert('请全部输入！')
        		}
        		return flag;
        	});
        });


