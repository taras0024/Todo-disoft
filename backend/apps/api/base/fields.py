from django.utils.translation import gettext_lazy as _
from rest_framework import relations


class ManyValuesRelatedField(relations.ManyRelatedField):
    default_error_messages = {
        'objects_does_not_exist': _('Invalid pk: {pk_values} - objects does not exist.'),
    }

    def __init__(self, pk_values_only: bool = False, **kwargs):
        self.pk_values_only = pk_values_only
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        if isinstance(data, str) or not hasattr(data, '__iter__'):
            self.fail('not_a_list', input_type=type(data).__name__)

        if not self.allow_empty and len(data) == 0:
            self.fail('empty')

        ids = list(self.child_relation.get_queryset().filter(pk__in=data).values_list('pk', flat=True))
        diff = set(data) - set(ids)

        if diff:
            self.fail('objects_does_not_exist', pk_values=list(diff))
        return ids if self.pk_values_only else list(self.child_relation.get_queryset().filter(pk__in=data))


class ManyPrimaryKeyRelatedField(relations.PrimaryKeyRelatedField):

    @classmethod
    def many_init(cls, *args, **kwargs):
        pk_values_only = kwargs.pop('pk_values_only', False)
        list_kwargs = {'child_relation': cls(*args, **kwargs)}
        for key in kwargs:
            if key in relations.MANY_RELATION_KWARGS:
                list_kwargs[key] = kwargs[key]
        return ManyValuesRelatedField(pk_values_only=pk_values_only, **list_kwargs)
