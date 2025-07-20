from rest_framework import serializers
from .models import CustomUser, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for CustomUser model.
    Serializes user fields: id, username, email, and role.
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role']


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message model.
    Includes sender information using UserSerializer.
    """
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp']


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for Conversation model.
    Includes nested participants and messages.
    """
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'messages']

    def get_messages(self, obj):
        """
        Returns serialized messages related to the conversation.
        """
        messages = obj.message_set.all()
        return MessageSerializer(messages, many=True).data