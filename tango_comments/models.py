# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from tango_center.models import Article


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='user', on_delete=models.DO_NOTHING)
    article = models.ForeignKey(Article, verbose_name='article', on_delete=models.DO_NOTHING)
    text = models.TextField(verbose_name='article content')
    create_time = models.DateTimeField('create_date', auto_now_add=True)

    parent = models.ForeignKey('self', default=None, blank=True, null=True,
                               verbose_name='refer', on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name_plural = verbose_name = 'comment'
        ordering = ['-create_time']
        app_label = 'comments manage'

    def __unicode__(self):
        return self.article.title + '_' + str(self.pk)

    __str__ = __unicode__
