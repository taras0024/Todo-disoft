from rest_framework import serializers

from api.base.fields import ManyPrimaryKeyRelatedField
from db.base.constants import Status
from db.todo.models import Todo, TodoStatus, Comment, Photo
from db.users.models import User
from service.tasks.email_tasks import send_email


class WriteCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text', 'parent',)


class ReadCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'parent', 'children', 'created_at',)


class ReadPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('id', 'file',)


class WriteTodoPhotoSerializer(serializers.Serializer):
    file = serializers.ImageField(required=True)


class ListTodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'description', 'status',)


class DetailTodoSerializer(ListTodoSerializer):
    comments = ReadCommentSerializer(many=True, read_only=True)
    photos = ReadPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Todo
        fields = (
            'id', 'title', 'description', 'status', 'author', 'assigned', 'comments', 'photos',
        )


class WriteTodoSerializer(serializers.ModelSerializer):
    assigned = ManyPrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
        allow_empty=True,
    )

    class Meta:
        model = Todo
        fields = ('id', 'title', 'description', 'status', 'assigned')

    def validate_status(self, value):
        value = value.upper()
        statuses = TodoStatus.objects.all().values_list('status', flat=True)
        if value not in statuses:
            raise serializers.ValidationError({
                'status': 'Not valid status. Valid statuses: [%s]' % ', '.join(statuses)
            })
        return value

    def create(self, validated_data):
        assigned = validated_data.pop('assigned', None)
        validated_data['author'] = self.context['user']

        instance = super().create(validated_data)
        if assigned:
            instance.assigned.set(assigned)
            send_email.apply_async(args=[instance.id])

        return instance


class UpdateTodoSerializer(WriteTodoSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'description', 'status', 'assigned',)

    def validate_status(self, value):
        value = super().validate_status(value)

        user = self.context['user']
        if not (self.instance and user):
            return value

        if user.is_superuser:
            return value

        if self.instance.assigned.filter(id=user.id).exists() and value in (Status.NEW, Status.DONE):
            raise serializers.ValidationError({
                'status': 'You are not allowed to change status of this todo.'
            })
        return value

    def validate(self, attrs):
        attrs = super().validate(attrs)
        user = self.context['user']
        if not (self.instance and user):
            return attrs

        if user.is_superuser:
            return attrs

        if self.instance.author != user:
            raise serializers.ValidationError({
                'author': 'You are not the author of this todo.'
            })
        return attrs

    def update(self, instance, validated_data):
        assigned = validated_data.pop('assigned', None)
        validated_data['author'] = self.context['user']

        instance = super().update(instance, validated_data)
        instance.refresh_from_db()

        if assigned:
            instance.assigned.set(assigned)
            send_email.apply_async(args=[instance.id])

        return instance
