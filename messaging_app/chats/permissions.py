from rest_framework import permissions


class IsParticipant(permissions.BasePermission):
    """
    Only participants in the conversation are allowed to view its details.
    """
    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()
