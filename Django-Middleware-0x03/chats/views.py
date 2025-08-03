from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter  # custom filter for sender/date filtering


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, creating, and retrieving conversations.
    Supports search filter on 'topic'.
    """
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['topic']
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        """Return only conversations where the current user is a participant"""
        user = self.request.user
        return Conversation.objects.filter(participants=user)

    def create(self, request, *args, **kwargs):
        """
        Create conversation and add participants:
        - Includes participants from request
        - Adds current user automatically
        """
        data = request.data.copy()

        # Participants from request (list of IDs)
        participants_ids = data.get("participants", [])

        # Ensure participants_ids is a list (convert if needed)
        if isinstance(participants_ids, str):
            import json
            participants_ids = json.loads(participants_ids)

        # Add current user if not already in list
        if str(request.user.user_id) not in participants_ids:
            participants_ids.append(str(request.user.user_id))

        # Create the conversation object with topic only
        serializer = self.get_serializer(data={"topic": data.get("topic", "")})
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save()

        # Add participants to conversation
        participants = User.objects.filter(user_id__in=participants_ids)
        conversation.participants.set(participants)

        # Return conversation with participants serialized
        return Response(self.get_serializer(conversation).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        """
        Ensure the user is part of the conversation before retrieving.
        """
        conversation_id = kwargs.get('pk')
        conversation = Conversation.objects.get(pk=conversation_id)

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
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['conversation__id']
    filterset_class = MessageFilter
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        """Get messages where the user is a participant of the conversation"""
        user = self.request.user
        return Message.objects.filter(conversation__participants=user)
