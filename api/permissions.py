from rest_framework.permissions import BasePermission

from ecoke.models import Brand


# class IsOwner(BasePermission):
#     """Custom permission class to allow only brand owners to edit them."""
#
#     def has_object_permission(self, request, view, obj):
#         """Return True id permission is granted to the brand owner."""
#         if isinstance(obj, Brand);
#             return obj.owner = request.user
#         return obj.owner == request.user
