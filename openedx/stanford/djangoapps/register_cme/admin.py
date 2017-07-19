# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html

from .models import ExtraInfo


class ExtraInfoAdmin(admin.ModelAdmin):
    """
    Admin interface for ExtraInfo model.
    """
    list_display = (
        'user',
        'get_email',
        'last_name',
        'first_name',
    )
    search_fields = (
        'user__username',
        'user__email',
        'last_name',
        'first_name',
    )

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email address'

    class Meta(object):
        model = ExtraInfo


class NewUserAdmin(UserAdmin):
    """
    Modifies admin interface for User model to display additional ExtraInfo link.
    """
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'has_extra_info',
    )

    def has_extra_info(self, obj):
        if hasattr(obj, 'extrainfo'):
            return format_html(
                '<a href="/admin/register_cme/extrainfo/{extrainfo_id}">ExtraInfo</a>',
                extrainfo_id=obj.extrainfo.id,
            )
        else:
            return ''
    has_extra_info.short_description = 'ExtraInfo'
    has_extra_info.allow_tags = True

admin.site.register(ExtraInfo, ExtraInfoAdmin)
admin.site.unregister(User)
admin.site.register(User, NewUserAdmin)
