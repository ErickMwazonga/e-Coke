from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination
)

class UserPageNumberPagination(PageNumberPagination):
    page_size = 5
