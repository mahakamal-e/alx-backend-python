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
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['topic']


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for sending and retrieving messages.
    Supports filtering by conversation ID.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['conversation__id']