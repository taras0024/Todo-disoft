# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = (
        'id', 'email', 'last_name', 'first_name', 'patronymic', 'date_joined',
    )
    list_filter = ()

    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        (_('Permissions'),
         {
             'fields': (
                 'is_superuser',
             ),
         }),
        (_('Full name'), {
            'fields': ('last_name', 'first_name', 'patronymic',)
        }),
    )

    add_fieldsets = (
        (None, {
            'fields': ('email', 'password1', 'password2',),
        }),
        (_('Full name'), {
            'fields': ('last_name', 'first_name', 'patronymic',)
        }),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
