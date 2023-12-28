from rest_framework.pagination import PageNumberPagination, _positive_int
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'size'

    def get_paginated_response(self, data):
        return Response({
            'total': self.page.paginator.count,
            'links_paginas': {
                'proxima': self.get_next_link(),
                'anterior': self.get_previous_link()
            },
            'resultados': data
        })

    def get_page_size(self, request):
        if self.page_size_query_param:
            try:
                request_page_size = request.query_params[self.page_size_query_param]
                if request_page_size == 'all':
                    return 7 ** 10

                return _positive_int(
                    request_page_size,
                    strict=True,
                    cutoff=self.max_page_size
                )
            except (KeyError, ValueError):
                pass

        return self.page_size