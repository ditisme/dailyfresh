/**
 * Created by python on 17-8-1.
 */
    $(function () {

        $('.name_input').blur(function () {
           $.get('/user/login_handle_'+$('.name_input').val()+'/', function (data) {
               if(data.result == 'False'){
                   $('.name_input').next().html('该用户名不存在')
                   $('.name_input').next().show();
               }
               else {
                   $('.name_input').next().hide();
               }
           })
        })

        $('.pass_input').blur(function () {
            $.get('/user/login_handle_'+$('.name_input').val()+'-'+$('.pass_input').val()+'/',
                function (data) {
                    if(data.pwd_result == 'False'){
                        $('.pass_input').next().html('密码错误')
                        $('.pass_input').next().show();
                    }
                    else {
                        $('.pass_input').next().hide();
                    }
                })
        })

    })

