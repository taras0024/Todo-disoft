from django.db.models import Prefetch
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.base.views import BaseApiViewSet
from db.todo.models import Todo, Photo, Comment
from db.users.models import User
from .filters import TodoFilterSerializer
from .serializers import (
    ListTodoSerializer,
    DetailTodoSerializer,
    WriteTodoPhotoSerializer,
    WriteTodoSerializer,
    WriteCommentSerializer,
    UpdateTodoSerializer
)


class TodoViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  BaseApiViewSet):
    queryset = Todo.objects.prefetch_related(
        Prefetch('author', queryset=User.objects.all()),
        Prefetch('assigned', queryset=User.objects.all()),
        Prefetch('photos', queryset=Photo.objects.all()),
    )
    permission_classes = [IsAuthenticated, ]
    serializer_class = ListTodoSerializer
    serializer_classes = {
        'create': WriteTodoSerializer,
        'list': ListTodoSerializer,
        'retrieve': DetailTodoSerializer,
        'update': UpdateTodoSerializer,
        'partial_update': UpdateTodoSerializer,
        'photo': WriteTodoPhotoSerializer,
        'comment': WriteCommentSerializer,
    }
    filter_serializer_class = TodoFilterSerializer

    @extend_schema(
        operation_id='upload_file',
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'file': {
                        'type': 'string',
                        'format': 'binary'
                    }
                }
            }
        },
    )
    @action(methods=['post'], detail=True, url_path='add-photo', url_name='photo')
    def photo(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        Photo.objects.create(
            todo=self.get_object(),
            file=serializer.validated_data['file']
        )
        return Response(status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True, url_path='add-comment', url_name='comment')
    def comment(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        Comment.objects.create(
            todo=self.get_object(),
            author=self.request.user,
            **serializer.validated_data
        )
        return Response(status=status.HTTP_201_CREATED)

    @extend_schema(parameters=[OpenApiParameter('status', type=str), ])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance and request.user and instance.author != request.user:
            raise ValidationError({
                'author': 'You are not the author of this todo.'
            })
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
