from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def delete_user(request):
    user = request.user
    if request.method == "POST":
        user.delete()
        return JsonResponse({"message": "Your account and all associated data have been deleted."})
    return JsonResponse({"error": "Method not allowed."}, status=400)


def threaded_conversations(request):
    root_messages = Message.objects.filter(parent_message__isnull=True) \
        .select_related('sender', 'receiver') \
        .prefetch_related('replies__sender', 'replies__receiver')

    def build_thread(msg):
        return {
            "id": msg.id,
            "sender": msg.sender.username,
            "receiver": msg.receiver.username,
            "content": msg.content,
            "timestamp": msg.timestamp,
            "replies": [build_thread(r) for r in msg.replies.all()]
        }

    data = [build_thread(msg) for msg in root_messages]
    return JsonResponse(data, safe=False)
