# -*- coding: utf-8 -*-
"""
Implement 'create_superuser' Django management command.
"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


User = get_user_model()


class Command(BaseCommand):
    """
    A management command which creates default superuser.
    """
    help = 'Create default superuser'

    def handle(self, *args, **kwargs):
        User.objects.create_superuser(
            first_name='Admin',
            last_name='Super',
            email='super-admin@example.com',
            password='super-admin123',
        )
