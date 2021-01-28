from django_elasticsearch_dsl_drf.pagination import (
    PageNumberPagination as BasePageNumberPagination,
)


# https://django-elasticsearch-dsl-drf.readthedocs.io/en/latest/advanced_usage_examples.html?highlight=size#customisations
class PageNumberPagination(BasePageNumberPagination):
    """Custom page number pagination."""

    max_page_size = 1000
    page_size_query_param = "page_size"

    def get_paginated_response_context(self, data):
        __data = super().get_paginated_response_context(data)
        __data.append(("current_page", int(self.request.query_params.get("page", 1))))
        __data.append(("page_size", self.get_page_size(self.request)))
        __data.append(("ordering", self.request.query_params.get("ordering", "")))

        return sorted(__data)
