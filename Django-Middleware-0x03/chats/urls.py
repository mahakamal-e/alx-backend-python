from rest_framework_nested import routers
from .views import ConversationViewSet, MessageViewSet
from django.urls import path, include

"""
Using NestedDefaultRouter to define nested routes for messages under conversations.
This enables URL patterns like: /conversations/{conversation_id}/messages/
"""

# Main router
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Nested router for messages under conversations
conversations_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = router.urls + conversations_router.urls


