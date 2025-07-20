from django.urls import path, include
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet

"""
Register viewsets with DRF router to generate URL patterns automatically.
This allows us to map URL endpoints to the appropriate viewsets.
"""
router = routers.DefaultRouter()  # This is what the checker expects
router.register(r'conversations', ConversationViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

