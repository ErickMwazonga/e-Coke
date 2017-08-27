from django.contrib.auth import get_user_model
#DRF imports
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    UpdateAPIView,
    RetrieveUpdateAPIView
)
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
)
# App imports
from .pagination import UserPageNumberPagination
from .serializers import (
    UserCreateSerializer,
    UserRetrieveSerializer,
    UserListSerializer,
    UserLoginSerializer,
)

User = get_user_model()

class UserCreateAPIView(CreateAPIView):
    queryset            = User.objects.all()
    serializer_class    = UserCreateSerializer
    permission_classes  = [IsAuthenticated]


class UserListAPIView(ListAPIView):
    queryset             = User.objects.all()
    serializer_class     = UserListSerializer
    filter_backends      = [SearchFilter, OrderingFilter]
    search_fields        = ['username']
    pagination_class     = UserPageNumberPagination


class UserRetrieveAPIView(RetrieveAPIView):
    queryset            = User.objects.all()
    serializer_class    = UserRetrieveSerializer


class UserUpdateAPIView(RetrieveUpdateAPIView):
    queryset             = User.objects.all()
    serializer_class     = UserListSerializer
    permission_classes   = [IsAuthenticated]


class UserDeleteAPIView(DestroyAPIView):
    queryset            = User.objects.all()
    serializer_class    = UserListSerializer
    permission_classes  = [IsAuthenticated]


class UserLoginAPIView(APIView):
    permission_classes  = [AllowAny]
    serializer_class    = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data         = request.data
        serializer   = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
