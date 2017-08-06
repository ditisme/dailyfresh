/**
 * Created by python on 17-8-1.
 */
    $(function () {

        var error_name = false;
        var error_verify = true;


         $('.name_input').blur(function () {
           $.get('/user/login_handle-/', {'user_name':$('.name_input').val(),'verify':$('.verify_input').val()}, function (data) {
               if(data.name_result == 0){
                   $('.name_input').next().html('该用户名不存在')
                   $('.name_input').next().show();
                   error_name = true;
               }
               else {
                   $('.name_input').next().hide();
                   error_name = false;
               }
           })
        })



        $('#change').css('cursor','pointer').click(function () {
            $('.verify_img').attr('src',$('.verify_img').attr('src')+1)
        })

        $('.verify_input').blur(function () {
             $.get('/user/login_handle-/', {'user_name':$('.name_input').val(),'verify':$('.verify_input').val()}, function (data) {
                  if(data.verify_result == 'false'){
                      $('.verify_error').show();
                      error_verify = true;
                      $('.verify_img').attr('src',$('.verify_img').attr('src')+1)
                  }
                  else {
                      $('.verify_error').hide();
                      error_verify = false;
                  }
            })
        })


        $('.name_input').click(function () {
            $('.pwd_error').hide();
        })

        $('.pass_input').click(function () {
            $('.pwd_error').hide();
        })

        $('.form_input').submit(function () {
            return  (error_name == false && error_verify == false);
            // if(error_password == false && error_name == false && error_verify ==false){
            //     return true;
            // }
            // else {
            //     return false;
            // }

        })


    })