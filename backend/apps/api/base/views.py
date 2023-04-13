from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from .pagination import ResponsePagePagination


class BaseApiViewSet(GenericViewSet):
    pagination_class = ResponsePagePagination
    serializer_classes = {}
    authentication_classes = (JWTAuthentication,)

    filter_serializer_class = None
    filter_serializer_map = {}

    def get_serializer_class(self):
        print(self.action)
        if self.action in self.serializer_classes:
            return self.serializer_classes[self.action]
        return self.serializer_class

    def get_serializer_context(self):
        return {**super().get_serializer_context(), "user": self.request.user}

    def get_filter_serializer_class(self):
        if (
                isinstance(getattr(self, "filter_serializer_map", None), dict)
                and getattr(self, 'action', None)
                and self.filter_serializer_map.get(self.action)
        ):
            return self.filter_serializer_map[self.action]
        return self.filter_serializer_class

    def filter_by_query_params(self, queryset):
        context = self.get_serializer_context()
        filter_serializer = self.get_filter_serializer_class()(data=self.request.query_params, context=context)
        if not filter_serializer.is_valid(raise_exception=True):
            return queryset
        filter_values = filter_serializer.validated_data

        if filter_values.get("db_query"):
            queryset = queryset.filter(filter_values["db_query"])

        if filter_values.get("db_filters"):
            queryset = queryset.filter(filter_values["db_filters"])

        if filter_values.get("db_extra"):
            queryset = queryset.extra(**filter_values["db_extra"])

        return queryset

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        if self.get_filter_serializer_class() is not None:
            queryset = self.filter_by_query_params(queryset)

        return queryset
