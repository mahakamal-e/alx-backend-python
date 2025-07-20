from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

"""
This viewset handles listing and creating conversations.
It extends ModelViewSet to automatically provide 'list', 'create', 'retrieve', 'update', 'destroy'.
"""
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    """
    Custom action to allow adding a message to a specific conversation.
    This creates a new message for the given conversation ID.
    """
    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        try:
            conversation = self.get_object()
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation not found."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['conversation'] = conversation.id

        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
This viewset handles listing and creating messages.
You can optionally filter messages by conversation ID.
"""
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    """
    Override get_queryset to optionally filter by conversation ID (passed as a query parameter).
    Example: /api/messages/?conversation=1
    """
    def get_queryset(self):
        queryset = super().get_queryset()
        conversation_id = self.request.query_params.get('conversation')
        if conversation_id:
            queryset = queryset.filter(conversation_id=conversation_id)
        return queryset