from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q


@login_required
def delete_user(request):
    user = request.user
    if request.method == "POST":
        user.delete()
        return JsonResponse({"message": "Your account and all associated data have been deleted."})
    return JsonResponse({"error": "Method not allowed."}, status=400)


@login_required
def threaded_conversations(request):
    # Fetch root messages (no parent) for current user
    root_messages = Message.objects.filter(
        parent_message__isnull=True
    ).filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).select_related('sender', 'receiver') \
     .prefetch_related('replies__sender', 'replies__receiver')

    # Recursive function to build nested thread
    def build_thread(message):
        return {
            "id": message.id,
            "sender": message.sender.username,
            "receiver": message.receiver.username,
            "content": message.content,
            "timestamp": message.timestamp,
            "replies": [build_thread(reply) for reply in message.replies.all()]
        }

    data = [build_thread(msg) for msg in root_messages]
    return JsonResponse(data, safe=False)
