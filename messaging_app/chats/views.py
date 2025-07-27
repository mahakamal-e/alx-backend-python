from rest_framework import viewsets, filters
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework import status
"""
This file defines viewsets for conversations and messages.
It uses Django REST Framework's ModelViewSet to automatically provide 
`list`, `create`, `retrieve`, `update`, and `destroy` actions.
"""

class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, creating, and retrieving conversations.
    Supports search filter on 'topic'.
    """
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['topic']
    
    def get_queryset(self):
        """Return only conversations,
        where the current user is a participant"""
        user = self.request.user
        return Conversation.objects.filter(participants=user)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for sending and retrieving messages.
    Supports filtering by conversation ID.
    """
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['conversation__id']
    
    def get_queryset(self):
        """Get messages where the user is a participant of the conversation"""
        user = self.request.user
        return Message.objects.filter(conversation__participants=user)
