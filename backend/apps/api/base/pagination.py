from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


def reformat_response(response_data,
                      response_type="OK",
                      response_detail=None,
                      update_response=False):
    response_results_data = OrderedDict([
        ("type", response_type),
        ("success", True),
        ("detail", response_detail or {}),
        ("results", response_data)
    ])

    if update_response:
        response_results_data.update(response_data)

    return response_results_data


class PagePagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000

    def get_page_size(self, request):
        if self.page_size_query_param and request.query_params.get(self.page_size_query_param):
            return super().get_page_size(request)
        view = request.parser_context.get('view', object)
        paginate_by = getattr(view, "paginate_by", None)
        if isinstance(paginate_by, int):
            return paginate_by
        return self.page_size


class ResponsePagePagination(PagePagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 200

    def get_paginated_response(self, data):
        """
        Need for reformat response in Mobile V2 API
        :param data: response data
        :return: Response
        """
        return Response(
            reformat_response(OrderedDict([
                ('page_number', self.page.number),
                ('page_size', self.page.paginator.per_page),
                ('total_pages_count', self.page.paginator.num_pages),
                ('total_items_count', self.page.paginator.count),
                ('next', self.get_next_link()),
                ('previous', self.get_previous_link()),
                ('data', data)
            ]))
        )
