from rest_framework import permissions
from .models import Conversation

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to ensure:
    - The user is authenticated (handled globally, but double-check here).
    - The user is a participant in the conversation they are trying to access.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the authenticated user is part of the conversation.
        Works for Message and Conversation objects.
        """
        # If object is a Message, get its conversation
        if hasattr(obj, 'conversation'):
            conversation = obj.conversation
        else:
            conversation = obj

        return request.user in conversation.participants.all()
