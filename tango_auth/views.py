from django.http import HttpResponse, Http404
from django.views.generic import View
from django.conf import settings
from django.core.mail import send_mail
from django.core.exceptions import PermissionDenied
from django.contrib import auth
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode

from PIL import Image
import os
import json
import base64
import logging

from tango_auth.forms import TangoUserCreationForm, TangoPasswordRestForm
from tango_auth.models import TangoUser

logger = logging.getLogger(__name__)


class UserControl(View):

    def post(self, request, *args, **kwargs):
        # Get what to do with the user
        slug = self.kwargs.get('slug')

        if slug == 'login':
            return self.login(request)
        elif slug == "logout":
            return self.logout(request)
        elif slug == "changepassword":
            return self.changepassword(request)
        elif slug == "forgetpassword":
            return self.forgetpassword(request)
        elif slug == "register":
            return self.register(request)
        elif slug == "changeAvatar":
            return self.changeAvatar(request)
        elif slug == "resetpassword":
            return self.resetpassword(request)

        raise PermissionDenied

    def get(self, request, *args, **kwargs):
        raise Http404

    def login(self, request):
        password = request.POST.get("password", "")
        username = request.POST.get("username", "")
        user = auth.authenticate(username=username, password=password)

        errors = []

        if user is not None:
            auth.login(request, user)
        else:
            errors.append("error username or password")

        mydict = {"errors": errors}
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )

    def logout(self, request):
        if not request.user.is_authenticated:
            raise PermissionDenied
        else:
            auth.logout(request)
            return HttpResponse('OK')

    def register(self, request):
        username = self.request.POST.get("username", "")
        password1 = self.request.POST.get("password1", "")
        password2 = self.request.POST.get("password2", "")
        email = self.request.POST.get("email", "")

        form = TangoUserCreationForm(request.POST)

        errors = []
        # valid form data
        if form.is_valid():
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
            title = "Welcome to {} ！".format(site_name)
            message = "".join([
                "Hello, {} \n\n".format(username),
                "Remember：\n",
                "username：{}\n".format(username),
                "email：{}\n".format(email),
                "site：http://{}\n\n".format(domain),
            ])
            from_email = None
            try:
                send_mail(title, message, from_email, [email])
            except Exception as e:
                return HttpResponse("send email fail!\n", status=500)

            new_user = form.save()
            user = auth.authenticate(username=username, password=password2)
            auth.login(request, user)

        else:
            for k, v in form.errors.items():
                # error info
                errors.append(v.as_text())
        mydict = {"errors": errors}
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )

    def changepassword(self, request):
        if not request.user.is_authenticated:
            logger.error('[UserControl]user have not login')
            raise PermissionDenied

        form = PasswordChangeForm(request.user, request.POST)

        errors = []
        # valid form
        if form.is_valid():
            user = form.save()
            auth.logout(request)
        else:
            for k, v in form.errors.items():
                errors.append(v.as_text())

        mydict = {"errors": errors}
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )

    def forgetpassword(self, request):
        username = self.request.POST.get("username", "")
        email = self.request.POST.get("email", "")

        form = TangoPasswordRestForm(request.POST)

        errors = []

        if form.is_valid():
            token_generator = default_token_generator
            from_email = None
            opts = {
                    'token_generator': token_generator,
                    'from_email': from_email,
                    'request': request,
                   }
            user = form.save(**opts)

        else:
            for k, v in form.errors.items():
                errors.append(v.as_text())

        mydict = {"errors": errors}
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )

    def resetpassword(self, request):
        uidb64 = self.request.POST.get("uidb64", "")
        token = self.request.POST.get("token", "")
        password1 = self.request.POST.get("password1", "")
        password2 = self.request.POST.get("password2", "")

        try:
            uid = urlsafe_base64_decode(uidb64)
            user = TangoUser._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, TangoUser.DoesNotExist):
            user = None

        token_generator = default_token_generator

        if user is not None and token_generator.check_token(user, token):
            form = SetPasswordForm(user, request.POST)
            errors = []
            if form.is_valid():
                user = form.save()
            else:
                for k, v in form.errors.items():
                    errors.append(v.as_text())

            mydict = {"errors": errors}
            return HttpResponse(
                json.dumps(mydict),
                content_type="application/json"
            )
        else:
            return HttpResponse(
                "reset error",
                status=403
            )

    def changeAvatar(self, request):
        if not request.user.is_authenticated:
            raise PermissionDenied

        # save avatar
        data = request.POST['Avatar']
        if not data:
            return HttpResponse("update avatar error", status=500)

        imgData = base64.b64decode(data)

        filename = "Avatar_100x100_{}.jpg".format(request.user.id)
        filedir = "tango_auth/static/Avatar/"
        static_root = getattr(settings, 'STATIC_ROOT', None)
        debug = getattr(settings, 'DEBUG', None)
        if static_root and not debug:
            filedir = os.path.join(static_root, 'Avatar')
        if not os.path.exists(filedir):
            os.makedirs(filedir)

        path = os.path.join(filedir, filename)

        file = open(path, "wb+")
        file.write(imgData)
        file.flush()
        file.close()

        # change size
        im = Image.open(path)
        out = im.convert('RGB').resize((100, 100), Image.ANTIALIAS)
        out.save(path)

        request.user.img = "/static/Avatar/"+filename
        request.user.save()

        # Verify upload is wrong
        if not os.path.exists(path):
  
            return HttpResponse("Upload avatar error", status=500)

        return HttpResponse("The avatar uploaded successfully!\n(Note that there is a 10-minute cache)")

