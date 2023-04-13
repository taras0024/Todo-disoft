from django.db import models
from django.utils.translation import gettext_lazy as _


class Status(models.TextChoices):
    NEW = ('NEW', _('New'))
    IN_PROGRES = ('IN_PROGRES', _('In progres'))
    DONE = ('DONE', _('Done'))
