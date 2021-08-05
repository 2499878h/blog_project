from django.contrib import admin
from tango_center.models import Article, Category, Carousel, Nav


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('status', 'create_time')
    list_display = ('name', 'parent', 'rank', 'status')
    fields = ('name', 'parent', 'rank', 'status')


class ArticleAdmin(admin.ModelAdmin):
    search_fields = ('title', 'summary')
    list_filter = ('status', 'category', 'is_top',
                   'create_time', 'update_time', 'is_top')
    list_display = ('title', 'category', 'author',
                    'status', 'is_top', 'update_time')
    fieldsets = (
        ('base info', {
            'fields': ('title', 'img',
                       'category', 'tags', 'author',
                       'is_top', 'rank', 'status')
            }),
        ('content', {
            'fields': ('content',)
            }),
        ('summary', {
            'fields': ('summary',)
            }),
        ('date', {
            'fields': ('pub_time',)
            }),
    )


class NavAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'url', 'status', 'create_time')
    list_filter = ('status', 'create_time')
    fields = ('name', 'url', 'status')


class CarouselAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title', 'article', 'img', 'create_time')
    list_filter = ('create_time',)
    fields = ('title', 'article', 'img', 'summary')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Nav, NavAdmin)
admin.site.register(Carousel, CarouselAdmin)
