from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'role']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()
    topic = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'topic', 'participants', 'messages']

    def get_messages(self, obj):
        messages = obj.messages.all()  # use related_name 'messages' instead of message_set
        return MessageSerializer(messages, many=True).data

    def validate_topic(self, value):
        if "forbidden" in value.lower():
            raise serializers.ValidationError("Topic contains forbidden word.")
        return value
