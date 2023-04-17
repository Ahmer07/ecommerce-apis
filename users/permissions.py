from rest_framework.permissions import BasePermission
import pdb

class IsSuperAdmin(BasePermission):
    message = "You must be a super admin to perform requested operation"

    def has_permission(self, request, view):
        if  request.user.role == "super_admin":
            return True
        return False


class IsCustomer(BasePermission):
    message = "You must be a customer to perform requested operation"

    def has_permission(self, request, view):
        if  request.user.role == "customer":
            return True
        return False


class IsOwner(BasePermission):
    message = "You must be owner of resource to perform requested operation"

    def has_object_permission(self, request, view, obj):
        # pdb.set_trace()
        if obj.id == request.user.id:
            return True
        return False
