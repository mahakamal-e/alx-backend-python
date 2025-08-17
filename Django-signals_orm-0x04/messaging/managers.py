from django.db import models


class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        # Filter unread messages for a specific user and fetch only needed fields
        return self.filter(receiver=user, read=False).only('id', 'sender', 'content', 'timestamp')
