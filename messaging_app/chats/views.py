from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter  # <-- custom filter for sender/date filtering

"""
This file defines viewsets for conversations and messages.
It uses Django REST Framework's ModelViewSet to automatically provide 
`list`, `create`, `retrieve`, `update`, and `destroy` actions.
Custom permissions are applied to restrict access only to participants.
"""

class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, creating, and retrieving conversations.
    Supports search filter on 'topic'.
    """
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['topic']
    # Apply custom permission
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        """Return only conversations where the current user is a participant"""
        user = self.request.user
        return Conversation.objects.filter(participants=user)

    def retrieve(self, request, *args, **kwargs):
        """
        Explicit check: Ensure the user is part of the conversation before retrieving
        Uses conversation_id and returns HTTP_403_FORBIDDEN if not allowed
        """
        conversation_id = kwargs.get('pk')  # explicitly mention conversation_id
        conversation = Conversation.objects.get(pk=conversation_id)

        # User must be participant
        if request.user not in conversation.participants.all():
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        return super().retrieve(request, *args, **kwargs)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for sending and retrieving messages.
    Supports filtering by conversation ID and additional filters (sender/date range).
    """
    pagination_class = MessagePagination
    serializer_class = MessageSerializer

    # Add filtering and searching
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['conversation__id']
    filterset_class = MessageFilter  # <-- custom filter for advanced filtering

    # Apply custom permission
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        """Get messages where the user is a participant of the conversation"""
        user = self.request.user
        return Message.objects.filter(conversation__participants=user)
