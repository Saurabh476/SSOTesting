from authlib.integrations.base_client import OAuthError
from authlib.integrations.django_client import OAuth
from authlib.oauth2.rfc6749 import OAuth2Token
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from djangoTutorial import settings
from users import views
from users.auth_backend import PasswordlessAuthBackend as plb
from django.contrib import messages
from django.contrib.auth import login

class OAuthMiddleware(MiddlewareMixin):

    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.oauth = OAuth()

    # def process_request(self, request):
    #     if settings.OAUTH_URL_WHITELISTS is not None:
    #         for w in settings.OAUTH_URL_WHITELISTS:
    #             # print('Inside 2.3 SSO',request.path)
    #             if request.path.startswith(w):
    #                 # print("******** function2.3 ***********")
    #                 # print(request.path_info)
    #                 # print(request.GET['code'])
    #                 print(self.get_response(request))
    #                 return self.get_response(request)

    #     def update_token(token, refresh_token, access_token):
    #         print(token,"this is update token")
    #         request.session['token'] = token
    #         return None
    #     print("Before sso client",request.path_info)
    #     sso_client = self.oauth.register(
    #         settings.OAUTH_CLIENT_NAME, overwrite=True, **settings.OAUTH_CLIENT, update_token=update_token
    #     )
    #     print('After SSO',request.path)
    #     if request.path.startswith('/profile'):
    #         self.clear_session(request)
    #         request.session['token'] = sso_client.authorize_access_token(request)
    #         print("******************request session******************")
    #         if self.get_current_user(sso_client, request) is not None:
    #             redirect_uri = request.session.pop('redirect_uri', None)
    #             if redirect_uri is not None:
    #                 return redirect(redirect_uri)
    #             return redirect(views.index)

    #     if request.session.get('token', None) is not None:
    #         current_user = self.get_current_user(sso_client, request)
    #         if current_user is not None:
    #             return self.get_response(request)

    #     # remember redirect URI for redirecting to the original URL.
    #     request.session['redirect_uri'] = request.path
    #     return sso_client.authorize_redirect(request, settings.OAUTH_CLIENT['redirect_uri'])

    # # fetch current login user info
    # # 1. check if it's in cache
    # # 2. fetch from remote API when it's not in cache
    # @staticmethod
    def update_token(token, refresh_token, access_token):
            request.session['token'] = token
            return None
    def process_request(self, request):
        if settings.OAUTH_URL_WHITELISTS is not None:
            for w in settings.OAUTH_URL_WHITELISTS:
                if request.path.startswith(w):
                    sso_client = self.oauth.register(
                        settings.OAUTH_CLIENT_NAME, overwrite=True, **settings.OAUTH_CLIENT, update_token=self.update_token
                    )
                    if request.path.startswith('/authenticate'):
                        self.clear_session(request)
                        request.session['token'] = sso_client.authorize_access_token(request)
                        if self.get_current_user(sso_client, request) is not None:
                            print(self.get_current_user(sso_client,request))
                            return self.get_response(request)


        print(request.path,'Path in oauth.process_request before if')
        if request.path.startswith('/login/'):
            print("***********INSIDE IF ******************",request.path)
                 

            print(request.path,'Path in oauth.process_request after if')
            # if request.path.startwith('/login/'):
            sso_client = self.oauth.register(settings.OAUTH_CLIENT_NAME, overwrite=True, **settings.OAUTH_CLIENT, update_token=self.update_token)
            # if request.path.startswith('/profile'):
            #     self.clear_session(request)
            #     request.session['token'] = sso_client.authorize_access_token(request)
            #     if self.get_current_user(sso_client, request) is not None:
            #         redirect_uri = request.session.pop('redirect_uri', None)
            #         if redirect_uri is not None:
            #             return redirect(redirect_uri)
            #         return redirect(views.index)

            if request.session.get('token', None) is not None:
                current_user = self.get_current_user(sso_client, request)
                print(current_user['login'], "This is current user --------------")
                if current_user is not None:
                    ###########################
                    plbObject = plb()
                    userRollNo = current_user['login']
                    user, studentProfile = plbObject.authenticate(rollnumber=userRollNo)
                    if user:
                        if user.is_active:
                            login(request,user)
                            messages.success(request,'***Login Successful*** \n LoggedInUserName: '+str(user)+'\n CSE-UserName: '+str(studentProfile.cseusername)+'\n FirstName: '+str(studentProfile.firstname)+'\n LastName: '+str(studentProfile.lastname)+'\n RollNumber: '+str(studentProfile.rollnumber)+'\n Section:'+str(studentProfile.section))
                            # messages.succes(request,'Username:')
                            return redirect('blog-home')
                    else:
                        message = "User Name: "+ str(username)+" is Incorrect"
                        return HttpResponse(message)
                    ###########################
                    messages.success(request,'Login Successful:')
                    return redirect('blog-home')
                    # return self.get_response(request)

            # remember redirect URI for redirecting to the original URL.
            request.session['redirect_uri'] = request.path
            return sso_client.authorize_redirect(request, settings.OAUTH_CLIENT['redirect_uri'])


        return self.get_response(request)
    # fetch current login user info
    # 1. check if it's in cache
    # 2. fetch from remote API when it's not in cache
    @staticmethod
    def get_current_user(sso_client, request):
        token = request.session.get('token', None)
        if token is None or 'access_token' not in token:
            return None

        if not OAuth2Token.from_dict(token).is_expired() and 'user' in request.session:
            return request.session['user']

        try:
            res = sso_client.get(settings.OAUTH_CLIENT['userinfo_endpoint'], token=OAuth2Token(token))
            if res.ok:
                request.session['user'] = res.json()
                return res.json()
        except OAuthError as e:
            print(e)
        return None

    @staticmethod
    def clear_session(request):
        try:
            del request.session['user']
            del request.session['token']
        except KeyError:
            pass

    def __del__(self):
        print('destroyed')
