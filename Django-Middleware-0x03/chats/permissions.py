from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - Must be authenticated
    - Must be a participant in the conversation for all actions
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Explicit authentication check
        if not user.is_authenticated:
            return False

        # Determine conversation object
        conversation = getattr(obj, 'conversation', obj)

        # Check participation
        is_participant = user in conversation.participants.all()

        # Extra check: allow modification only if participant
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return is_participant

        # Read (GET) also requires participant
        return is_participant
