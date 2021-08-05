from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from tango_auth.models import TangoUser
from tango_auth.forms import TangoUserCreationForm


class TangoUserAdmin(UserAdmin):
    add_form = TangoUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')
        }),
    )
    fieldsets = (
        ('base info', {'fields': ('username', 'password', 'email')}),
        ('authority', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('date', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.unregister(Group)
admin.site.register(TangoUser, TangoUserAdmin)
