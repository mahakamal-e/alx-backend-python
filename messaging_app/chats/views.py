from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .permissions import IsParticipantOfConversation
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, creating, and retrieving conversations.
    Only participants can view or modify conversations.
    """
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['topic']
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        """Return only conversations where the current user is a participant."""
        user = self.request.user
        return Conversation.objects.filter(participants=user)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for sending and retrieving messages.
    Only participants of a conversation can access its messages.
    """
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['conversation__id']
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        """Return only messages from conversations where the user is a participant."""
        user = self.request.user
        return Message.objects.filter(conversation__participants=user)
