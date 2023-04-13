# -*- coding: utf-8 -*-
from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from db.todo.models import TodoStatus, Todo, Photo, Comment


@admin.register(TodoStatus)
class TodoStatusAdmin(admin.ModelAdmin):
    list_display = ('status',)


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 0


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'status', 'author',)
    ordering = ('-created_at',)
    readonly_fields = ('status',)
    inlines = (PhotoInline,)

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        user = request.user
        form.base_fields['author'].initial = user
        return form


@admin.register(Comment)
class CommentModelAdmin(MPTTModelAdmin):
    mptt_level_indent = 30
    list_display = ('id', 'todo', 'author', 'text', 'created_at',)

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        user = request.user
        form.base_fields['author'].initial = user
        return form
