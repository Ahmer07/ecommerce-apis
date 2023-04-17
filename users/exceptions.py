from rest_framework import exceptions


class PrivilegeException(exceptions.PermissionDenied):
    status_code = 403
    default_detail = "You are not allowed to perform requested operation"


class ValidationException(exceptions.ValidationError):
    status_code = 400
    default_detail = "Invalid data"
