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

