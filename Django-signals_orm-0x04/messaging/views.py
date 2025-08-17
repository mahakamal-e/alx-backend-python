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


root_messages = Message.objects.filter(
    parent_message__isnull=True,
).filter(
    models.Q(sender=request.user) | models.Q(receiver=request.user)
)
