# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel, MPTTModelBase

from db.base.constants import Status
from db.base.models import DateTimeModelMixin
from db.todo.managers import CommentManager
from service.uploads import photo_uploads


class TodoStatus(models.Model):
    status = models.CharField(
        max_length=64,
        unique=True,
    )

    class Meta:
        verbose_name = _('Status')
        verbose_name_plural = _('Statuses')

    def save(self, *args, **kwargs):
        self.status = self.status.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.status


class Todo(DateTimeModelMixin):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=255, default=Status.NEW)
    author = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='todo',
    )
    assigned = models.ManyToManyField(
        'users.User',
        related_name='assigned_todos',
        blank=True,
    )

    def __str__(self):
        return f'{self.id}-{self.title}'

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('Todo')
        verbose_name_plural = _('Todos')


class Photo(models.Model):
    file = models.ImageField(upload_to=photo_uploads)
    todo = models.ForeignKey(
        'todo.Todo',
        on_delete=models.CASCADE,
        related_name='photos',
    )

    class Meta:
        verbose_name = _('Photo')
        verbose_name_plural = _('Photos')


class Comment(DateTimeModelMixin, MPTTModel, metaclass=MPTTModelBase):
    text = models.TextField()
    todo = models.ForeignKey(
        'todo.Todo',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    author = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='comments',
    )

    objects = CommentManager

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

    def __str__(self):
        return f'{self.id}-{self.text}'
