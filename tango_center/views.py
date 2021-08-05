from django import template
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.template import loader
from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from tango_center.models import Article, Category, Carousel, Nav
from django.conf import settings
import json


class BaseMixin(object):
    def get_context_data(self, *args, **kwargs):
        context = super(BaseMixin, self).get_context_data(**kwargs)
        try:
            # website title
            if 'website_title' not in context:
                context['website_title'] = settings.WEBSITE_TITLE

            context['website_welcome'] = settings.WEBSITE_WELCOME
            # hot article
            context['hot_article_list'] = \
                Article.objects.order_by("-view_times")[0:10]
            # nav
            context['nav_list'] = Nav.objects.filter(status=0)

            colors = ['primary', 'success', 'info', 'warning', 'danger']
            for index, link in enumerate(context['links']):
                link.color = colors[index % len(colors)]

        except Exception as e:
            print(e)

        return context


class IndexView(BaseMixin, ListView):
    template_name = 'blog/index.html'
    context_object_name = 'article_list'
    paginate_by = settings.PAGE_NUM

    def get_context_data(self, **kwargs):
        # carousel
        kwargs['carousel_page_list'] = Carousel.objects.all()
        return super(IndexView, self).get_context_data(**kwargs)

    def get_queryset(self):
        article_list = Article.objects.filter(status=0)
        return article_list


class ArticleView(BaseMixin, DetailView):
    queryset = Article.objects.filter(Q(status=0) | Q(status=1))
    template_name = 'blog/article.html'
    context_object_name = 'article'
    slug_field = 'title'

    def get(self, request, *args, **kwargs):
        # count read times
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        self.cur_user_ip = ip

        title = self.kwargs.get('slug')

        # add view tiems
        article = self.queryset.get(title=title)
        article.view_times += 1
        article.save()

        return super(ArticleView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # comments
        title = self.kwargs.get('slug', '')
        kwargs['comment_list'] = \
            self.queryset.get(title=title).comment_set.all()

        article = self.queryset.get(title=title)
        kwargs['website_title'] = article.title

        return super(ArticleView, self).get_context_data(**kwargs)


class AllView(BaseMixin, ListView):
    template_name = 'blog/all.html'
    context_object_name = 'article_list'

    def get_context_data(self, **kwargs):
        kwargs['category_list'] = Category.objects.all()
        kwargs['PAGE_NUM'] = settings.PAGE_NUM
        return super(AllView, self).get_context_data(**kwargs)

    def get_queryset(self):
        article_list = Article.objects.filter(
            status=0
        ).order_by("-pub_time")[0:settings.PAGE_NUM]
        return article_list

    def post(self, request, *args, **kwargs):
        val = self.request.POST.get("val", "")
        sort = self.request.POST.get("sort", "time")
        start = self.request.POST.get("start", 0)
        end = self.request.POST.get("end", settings.PAGE_NUM)

        start = int(start)
        end = int(end)

        if sort == "time":
            sort = "-pub_time"
        elif sort == "recommend":
            sort = "-view_times"
        else:
            sort = "-pub_time"

        if val == "all":
            article_list = \
                Article.objects.filter(status=0).order_by(sort)[start:end+1]
        else:
            try:
                article_list = Category.objects.get(
                                   name=val
                               ).article_set.filter(
                                   status=0
                               ).order_by(sort)[start:end+1]
            except Category.DoesNotExist:
                raise PermissionDenied

        isend = len(article_list) != (end-start+1)

        article_list = article_list[0:end-start]

        html = ""
        for article in article_list:
            html += template.loader.get_template(
                'blog/include/all_post.html'
            ).render({'post': article})

        mydict = {"html": html, "isend": isend}
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )


class SearchView(BaseMixin, ListView):
    template_name = 'blog/search.html'
    context_object_name = 'article_list'
    paginate_by = settings.PAGE_NUM

    def get_context_data(self, **kwargs):
        kwargs['s'] = self.request.GET.get('s', '')
        return super(SearchView, self).get_context_data(**kwargs)

    def get_queryset(self):
        # find by key word
        s = self.request.GET.get('s', '')
        # find in title summary or tags
        article_list = Article.objects.only(
            'title', 'summary', 'tags'
        ).filter(
            Q(title__icontains=s) |
            Q(summary__icontains=s) |
            Q(tags__icontains=s),
            status=0
        )
        return article_list


class TagView(BaseMixin, ListView):
    template_name = 'blog/tag.html'
    context_object_name = 'article_list'
    paginate_by = settings.PAGE_NUM

    def get_queryset(self):
        tag = self.kwargs.get('tag', '')
        article_list = \
            Article.objects.only('tags').filter(tags__icontains=tag, status=0)

        return article_list


class CategoryView(BaseMixin, ListView):
    template_name = 'blog/category.html'
    context_object_name = 'article_list'
    paginate_by = settings.PAGE_NUM

    def get_queryset(self):
        category = self.kwargs.get('category', '')
        try:
            article_list = \
                Category.objects.get(name=category).article_set.all()
        except Category.DoesNotExist:
            raise Http404

        return article_list


class UserView(BaseMixin, TemplateView):
    # template_name = 'blog/user.html'

    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return render(request, 'blog/login.html')

        slug = self.kwargs.get('slug')

        if slug == 'changeAvatar':
            self.template_name = 'blog/user_changeAvatar.html'
        elif slug == 'changepassword':
            self.template_name = 'blog/user_changepassword.html'

        return super(UserView, self).get(request, *args, **kwargs)



