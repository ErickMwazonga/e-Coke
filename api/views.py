#DRF imports
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    UpdateAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)
from rest_framework.permissions import (
    IsAuthenticated,
)
# App imports
from ecoke.models import Brand
from .pagination import BrandPageNumberPagination
from .serializers import (
    BrandCreateSerializer,
    BrandRetrieveSerializer,
    BrandListSerializer,
    BrandDetailsSerializer,
)

# from .permissions import IsOwner


class BrandCreateAPIView(CreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandCreateSerializer


class BrandListAPIView(ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['collector_name', 'respondent_name', 'respondent_city', 'date_of_collection']
    pagination_class = BrandPageNumberPagination


class BrandRetrieveAPIView(RetrieveAPIView):
    queryset  = Brand.objects.all()
    serializer_class = BrandRetrieveSerializer


class BrandUpdateAPIView(RetrieveUpdateAPIView):
    queryset  = Brand.objects.all()
    serializer_class  = BrandListSerializer


class BrandDeleteAPIView(DestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandListSerializer


class BrandDetailsView(RetrieveUpdateDestroyAPIView):
    """This class handles GET, PUT, PATCH and DELETE requests."""
    queryset = Brand.objects.all()
    serializer_class = BrandDetailsSerializer
    permission_classes = (
            IsAuthenticated,
            # IsOwner
        )
