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
    
    participants_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )

    messages = serializers.SerializerMethodField()
    topic = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'topic', 'participants', 'participants_ids', 'messages']

    def get_messages(self, obj):
        messages = obj.messages.all()
        return MessageSerializer(messages, many=True).data

    def validate_topic(self, value):
        if "forbidden" in value.lower():
            raise serializers.ValidationError("Topic contains forbidden word.")
        return value

    def create(self, validated_data):
        
        participants_ids = validated_data.pop('participants_ids', [])
        conversation = Conversation.objects.create(**validated_data)

        
        if participants_ids:
            users = User.objects.filter(user_id__in=participants_ids)
            conversation.participants.set(users)

        return conversation
