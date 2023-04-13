from django.db import models
from rest_framework import serializers

from db.todo.models import TodoStatus


class TodoFilterSerializer(serializers.Serializer):
    status = serializers.CharField(required=False)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        db_filters, extra_filters, query_filter = models.Q(), dict(), models.Q()

        status = (attrs.get('status') or '').upper()
        if status:
            if not TodoStatus.objects.filter(status=status).exists():
                raise serializers.ValidationError({
                    'status': 'Not valid status.'
                })
            db_filters |= models.Q(status=status)

        return {"db_filters": db_filters, "db_query": query_filter, "db_extra": extra_filters}
