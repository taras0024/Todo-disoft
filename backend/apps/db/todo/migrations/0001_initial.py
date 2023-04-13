# Generated by Django 4.2 on 2023-04-13 10:18

from django.conf import settings
from django.contrib.auth.management import create_permissions
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import service.uploads
from db.base.constants import Status


def set_default_status(apps, schema_editor):
    # Need for creating permission before migration
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, verbosity=0)

    TodoStatus = apps.get_model('todo', 'TodoStatus')
    db_alias = schema_editor.connection.alias

    defaults = []
    for status in Status:
        defaults.append(TodoStatus(status=status))

    TodoStatus.objects.using(db_alias).bulk_create(defaults)


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TodoStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=64, unique=True)),
            ],
            options={
                'verbose_name': 'Status',
                'verbose_name_plural': 'Statuses',
            },
        ),
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('status', models.CharField(default='NEW', max_length=255)),
                ('assigned',
                 models.ManyToManyField(blank=True, related_name='assigned_todos', to=settings.AUTH_USER_MODEL)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='todo',
                                             to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Todo',
                'verbose_name_plural': 'Todos',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(upload_to=service.uploads.photo_uploads)),
                ('todo',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='todo.todo')),
            ],
            options={
                'verbose_name': 'Photo',
                'verbose_name_plural': 'Photos',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('text', models.TextField()),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments',
                                             to=settings.AUTH_USER_MODEL)),
                ('parent',
                 mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                            related_name='children', to='todo.comment')),
                ('todo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments',
                                           to='todo.todo')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
        ),
        migrations.RunPython(set_default_status),
    ]
