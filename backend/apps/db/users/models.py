# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.timezone import now as timezone_now
from django.utils.translation import gettext_lazy as _

from db.users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'

    first_name = models.CharField(
        verbose_name=_('first name'),
        max_length=32,
    )

    last_name = models.CharField(
        verbose_name=_('last name'),
        max_length=32,
    )

    patronymic = models.CharField(
        verbose_name=_('patronymic'),
        max_length=32,
        blank=True,
    )

    email = models.EmailField(
        verbose_name=_('email'),
        max_length=64,
        unique=True,
    )

    date_joined = models.DateTimeField(
        verbose_name=_('date joined'),
        default=timezone_now,
    )

    last_login = models.DateTimeField(
        verbose_name=_('last login'),
        default=timezone_now,
    )

    is_staff = models.BooleanField(
        verbose_name=_('website stuff status'),
        help_text=_('Designates whether the user can visit this admin panel.'),
        default=False,
    )

    is_active = models.BooleanField(
        verbose_name=_('active'),
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'),
        default=True,
    )

    objects = UserManager()

    @property
    def username(self):
        return self.get_username()

    def get_full_name(self):
        """
        This method is needed by Django.
        """
        return f'{self.last_name} {self.first_name} {self.patronymic}'

    @property
    def full_name(self):
        return self.get_full_name()

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """
        Returns a bool of whether the raw_password was correct.
        Handles hashing formats behind the scenes.
        """

        def setter(raw_password):
            self.set_password(raw_password)
            self.save(update_fields=['password'])

        return check_password(raw_password, self.password, setter)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
