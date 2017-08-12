class UrlMiddleware:
    def process_view(self, request,view_name,view_args,view_kwargs):

        if request.path not in ['/user/register/',
                                '/user/register_handle/',
                                '/user/check_user_name/',
                                '/user/login/',
                                '/user/islogin/',
                                '/user/login_handle-/',
                                '/user/login_handle/',
                                '/user/verify_code/',
                                '/user/logout/',]:

            request.session['url_path'] = request.get_full_path()