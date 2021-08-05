from django.db import models
from tango_center.models import Article


class Comment(models.Model):
    user = models.ForeignKey("tango_auth.TangoUser", verbose_name='user', on_delete=models.DO_NOTHING)
    article = models.ForeignKey(Article, verbose_name='article', on_delete=models.DO_NOTHING)
    text = models.TextField(verbose_name='article content')
    create_time = models.DateTimeField('create_date', auto_now_add=True)

    parent = models.ForeignKey('self', default=None, blank=True, null=True,
                               verbose_name='refer', on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name_plural = verbose_name = 'comment'
        ordering = ['-create_time']
        app_label = 'tango_comments'

    def __unicode__(self):
        return self.article.title + '_' + str(self.pk)

    __str__ = __unicode__
