from .permissions import IsStaffEditorPermission
from rest_framework import permissions


class IsStaffEditorPermissionMixins():
    permission_classes = [permissions.IsAdminUser,IsStaffEditorPermission]