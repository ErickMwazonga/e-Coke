from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination
)

# class BrandLimitOffsetPagination(LimitOffsetPagination):
#     default_limit = 3
#     max_limit = 10


class BrandPageNumberPagination(PageNumberPagination):
    page_size = 5
