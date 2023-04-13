from rest_framework.viewsets import ReadOnlyModelViewSet

from db.users.models import User
from .serializers import UserSerializer


class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
