from django.db import models
from mptt.managers import TreeQuerySet


class CommentQuerySet(TreeQuerySet, models.query.QuerySet):
    pass


CommentManager = CommentQuerySet.as_manager()
