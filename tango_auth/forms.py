from django import forms
from tango_auth.models import TangoUser
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
import base64
import logging


class TangoUserCreationForm(forms.ModelForm):

    # error message
    error_messages = {
        'duplicate_username': "user already create.",
        'password_mismatch': "password not equal.",
        'duplicate_email': u'email has been database.'
    }

    username = forms.RegexField(
        max_length=30,
        regex=r'^[\w.@+-]+$',
        error_messages={
            'invalid':  "only contain number、char@/./+/-/_",
            'required': "username is null"
        }
    )
    email = forms.EmailField(
        error_messages={
            'invalid':  "email error",
            'required': u'email null'}
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        error_messages={
            'required': "password null"
            }
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        error_messages={
            'required': "password null"
            }
    )

    class Meta:
        model = TangoUser
        fields = ("username", "email")

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            TangoUser._default_manager.get(username=username)
        except TangoUser.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages["duplicate_username"]
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                    self.error_messages["password_mismatch"]
            )
        return password2

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            TangoUser._default_manager.get(email=email)
        except TangoUser.DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages["duplicate_email"]
        )

    def save(self, commit=True):
        user = super(TangoUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class TangoPasswordRestForm(forms.Form):

    error_messages = {
        'email_error': "username or password error",
    }

    username = forms.RegexField(
        max_length=30,
        regex=r'^[\w.@+-]+$',
        error_messages={
            'invalid': "only contain number、char@/./+/-/_",
            'required': "username null"}
        )
    email = forms.EmailField(
        error_messages={
            'invalid':  "emaile error",
            'required': u'email null'}
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if username and email:
            try:
                self.user = TangoUser.objects.get(
                    username=username, email=email, is_active=True
                )
            except TangoUser.DoesNotExist:
                raise forms.ValidationError(
                    self.error_messages["email_error"]
                )

        return self.cleaned_data

    def save(self, from_email=None, request=None,
             token_generator=default_token_generator):
        email = self.cleaned_data['email']
        current_site = get_current_site(request)
        site_name = current_site.name
        domain = current_site.domain
        uid = base64.urlsafe_b64encode(
            force_bytes(self.user.pk)
        ).rstrip(b'\n=').decode('utf-8')
        token = token_generator.make_token(self.user)
        protocol = 'http'

        title = "reset {} password".format(site_name)
        message = "".join([
            "reset password by the site:\n\n",
            "{}://{}/resetpassword/{}/{}/\n\n".format(
                protocol, domain, uid, token
            )
        ])

        try:
            send_mail(title, message, from_email, [self.user.email])
        except Exception as e:
            pass
