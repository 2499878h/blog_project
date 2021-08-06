from django import template
register = template.Library()


@register.filter
def change_url(title):
    title = title.replace(' ', '_')
    return title
