from django.db import models
from django.urls import reverse


STATUS = {
        0: 'normal',
        1: 'draft',
        2: 'delete',
}


class Nav(models.Model):
    name = models.CharField(max_length=40, verbose_name='nav content')
    url = models.CharField(max_length=200, blank=True, null=True,
                           verbose_name='redirect url')

    status = models.IntegerField(default=0, choices=STATUS.items(),
                                 verbose_name='status')
    create_time = models.DateTimeField('create_time', auto_now_add=True)

    class Meta:
        verbose_name_plural = verbose_name = "nav"
        ordering = ['-create_time']
        app_label = "tango_center"

    def __unicode__(self):
        return self.name

    __str__ = __unicode__


class Category(models.Model):
    name = models.CharField(max_length=40, verbose_name='name')
    parent = models.ForeignKey('self', default=None, blank=True, null=True,
                               verbose_name='parent category', on_delete=models.DO_NOTHING)
    rank = models.IntegerField(default=0, verbose_name='order')
    status = models.IntegerField(default=0, choices=STATUS.items(),
                                 verbose_name='status')

    create_time = models.DateTimeField('create_date', auto_now_add=True)

    class Meta:
        verbose_name_plural = verbose_name = 'category'
        ordering = ['rank', '-create_time']
        app_label = "tango_center"

    def get_absolute_url(self):
        return reverse('category-detail-view', args=(self.name,))

    def __unicode__(self):
        if self.parent:
            return '%s-->%s' % (self.parent, self.name)
        else:
            return '%s' % (self.name)

    __str__ = __unicode__


class Article(models.Model):
    author = models.ForeignKey("tango_auth.TangoUser", verbose_name='author', on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category, verbose_name='category', on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=100, verbose_name='title')
    img = models.CharField(max_length=200,
                           default='/static/img/article/avatar.jpg')
    tags = models.CharField(max_length=200, null=True, blank=True,
                            verbose_name='tag', help_text='segment by comma')
    summary = models.TextField(verbose_name='summary')
    content = models.TextField(verbose_name='content')
    view_times = models.IntegerField(default=0)
    zan_times = models.IntegerField(default=0)

    is_top = models.BooleanField(default=False, verbose_name='top')
    rank = models.IntegerField(default=0, verbose_name='order')
    status = models.IntegerField(default=0, choices=STATUS.items(),
                                 verbose_name='status')
    pub_time = models.DateTimeField(default=False, verbose_name='pub_date')
    create_time = models.DateTimeField('create_time', auto_now_add=True)
    update_time = models.DateTimeField('update_time', auto_now=True)

    def get_absolute_url(self):
        return reverse('article-detail-view', args=(self.title,))

    def get_tags(self):
        tags_list = (self.tags or "").split(',')
        while '' in tags_list:
            tags_list.remove('')

        return tags_list

    class Meta:
        verbose_name_plural = verbose_name = 'article'
        ordering = ['rank', '-is_top', '-pub_time', '-create_time']
        app_label = 'tango_center'

    def __unicode__(self):
            return self.title

    __str__ = __unicode__


class Carousel(models.Model):
    title = models.CharField(max_length=100, verbose_name='title')
    summary = models.TextField(blank=True, null=True, verbose_name='summary')
    img = models.CharField(max_length=200, verbose_name='img',
                           default='/static/img/carousel/avatar.jpg')
    article = models.ForeignKey(Article, verbose_name='article', on_delete=models.DO_NOTHING)
    create_time = models.DateTimeField('create_date', auto_now_add=True)

    class Meta:
        verbose_name_plural = verbose_name = 'carousel'
        ordering = ['-create_time']
        app_label = 'tango_center'


