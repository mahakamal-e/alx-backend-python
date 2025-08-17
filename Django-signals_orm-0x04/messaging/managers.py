from django.db import models


class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        # Filter unread messages for a specific user and select only necessary fields
        return self.filter(receiver=user, read=False).only('id', 'sender', 'content', 'timestamp')
