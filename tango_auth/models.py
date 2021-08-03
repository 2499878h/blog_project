# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser


class TangoUser(AbstractUser):
    img = models.CharField(max_length=200, default='/static/Avatar/avatar.jpg',
                           verbose_name=u'Avatar address')
    intro = models.CharField(max_length=200, blank=True, null=True,
                             verbose_name=u'Introduction')

    class Meta(AbstractUser.Meta):
        app_label = "User Management"
