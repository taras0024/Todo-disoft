# -*- coding: utf-8 -*-
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = (
    'UserManager',
)


class UserQuerySet(models.query.QuerySet):
    def create_user(self, first_name, last_name, email, password=None, **kwargs):
        required_fields = {'first_name': first_name, 'last_name': last_name, 'email': email}
        if not all(required_fields.values()):
            undefined_key = list(filter(lambda k: not required_fields[k], required_fields.keys()))[0]
            raise ValueError(_('Users must have %s' % undefined_key))

        def _extra_fields(model):
            field_names = [field.name for field in model._meta.fields]
            return dict(
                (key, value) for key, value in kwargs.items() if key in field_names
            )

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            **_extra_fields(self.model)
        )
        user.set_password(password)
        user.save(using=self._db)
        user.refresh_from_db(using=self._db)
        return user

    def create(self, **kwargs):
        return self.create_user(**kwargs)

    def create_superuser(self, first_name, last_name, email, password, **kwargs):
        return self.create_user(first_name, last_name, email, password, is_superuser=True, is_staff=True, **kwargs)


UserManager = type('UserManager', (models.Manager.from_queryset(UserQuerySet), BaseUserManager), {})
