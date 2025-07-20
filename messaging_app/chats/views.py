from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.shortcuts import get_object_or_404


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and creating conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # فقط المحادثات اللي فيها المستخدم الحالي
        return self.queryset.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with specified participant IDs.
        JSON Format: {"participant_ids": ["user_id_1", "user_id_2", ...]}
        """
        participant_ids = request.data.get("participant_ids", [])
        if not participant_ids:
            return Response({"error": "You must provide participant_ids."}, status=400)

        # Add the current user to the conversation
        participant_ids.append(str(request.user.user_id))

        # Get users
        from chats.models import User  # Avoid circular import
        participants = User.objects.filter(user_id__in=participant_ids)

        # Create conversation
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and sending messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(conversation__participants=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Send a message to an existing conversation.
        JSON Format: {"conversation_id": "uuid", "message_body": "your text"}
        """
        conversation_id = request.data.get("conversation_id")
        message_body = request.data.get("message_body")

        if not conversation_id or not message_body:
            return Response({"error": "conversation_id and message_body are required."}, status=400)

        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)

        if request.user not in conversation.participants.all():
            return Response({"error": "You are not a participant in this conversation."}, status=403)

        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            message_body=message_body
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
