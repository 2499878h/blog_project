from django.shortcuts import render

# Create your views here.
import datetime
from django.http import HttpResponse
from django.views.generic import View
from django.core.exceptions import PermissionDenied
from tango_comments.models import Comment
from tango_center.models import Article

ArticleModel = Article


class CommentControl(View):
    def post(self, request, *args, **kwargs):
        # get user info
        user = self.request.user
        # get comments
        text = self.request.POST.get("comment", "")
        # whether login
        if not user.is_authenticated:
            return HttpResponse("please login!", status=403)

        title = self.kwargs.get('slug', '')
        try:
            article = ArticleModel.objects.get(title=title)
        except ArticleModel.DoesNotExist:
            raise PermissionDenied

        # save comments
        parent = None

        if not text:
            return HttpResponse("please input cotent！", status=403)

        comment = Comment.objects.create(
                user=user,
                article=article,
                text=text,
                parent=parent
                )

        try:
            img = comment.user.img
        except Exception as e:
            img = "http://vmaig.qiniudn.com/image/tx/tx-default.jpg"

        print_comment = "<p>review：{}</p>".format(text)
        if parent:
            print_comment = "<div class=\"comment-quote\">\
                                  <p>\
                                      <a>@{}</a>\
                                      {}\
                                  </p>\
                              </div>".format(
                                  parent.user.username,
                                  parent.text
                              ) + print_comment
        # response
        html = "<li>\
                    <div class=\"vmaig-comment-tx\">\
                        <img src={} width=\"40\"></img>\
                    </div>\
                    <div class=\"vmaig-comment-content\">\
                        <a><h1>{}</h1></a>\
                        {}\
                        <p>{}</p>\
                    </div>\
                </li>".format(
                    img,
                    comment.user.username,
                    print_comment,
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )

        return HttpResponse(html)
