import logging
from datetime import datetime, timedelta
from collections import defaultdict
from django.http import HttpResponseForbidden

# ============================
# Configure logging to file
# ============================
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('requests.log')
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


# ============================================
# 1) RequestLoggingMiddleware
# Logs every incoming request with timestamp, user and path
# ============================================
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        # Django will pass the next middleware or view function here
        self.get_response = get_response

    def __call__(self, request):
        # Identify the user (Anonymous if not authenticated)
        user = request.user if request.user.is_authenticated else 'Anonymous'

        # Prepare log message
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"

        # Write to requests.log
        logger.info(log_message)

        # Continue to next middleware or view
        response = self.get_response(request)
        return response


# ============================================
# 2) RestrictAccessByTimeMiddleware
# Restricts access to the application outside of allowed hours
# Allowed hours: 6 AM to 9 PM
# ============================================
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour

        # If time is outside 6 AM - 9 PM → Block
        if current_hour < 6 or current_hour >= 21:
            return HttpResponseForbidden(
                "Access to the messaging app is restricted at this time."
            )

        return self.get_response(request)


# ============================================
# 3) OffensiveLanguageMiddleware
# Limits number of POST requests (messages) per IP to 5 per minute
# ============================================
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Store request timestamps per IP: {ip: [datetime, datetime, ...]}
        self.requests_per_ip = defaultdict(list)

    def __call__(self, request):
        # Apply only to POST requests (sending messages)
        if request.method == "POST":
            ip = self.get_client_ip(request)
            now = datetime.now()

            # Remove timestamps older than 1 minute
            self.requests_per_ip[ip] = [
                t for t in self.requests_per_ip[ip] if now - t < timedelta(minutes=1)
            ]

            # If 5 or more requests in last minute → Block
            if len(self.requests_per_ip[ip]) >= 5:
                return HttpResponseForbidden("Message limit exceeded. Try again later.")

            # Record current request time
            self.requests_per_ip[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        """
        Get client's real IP address (works behind proxies as well).
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')


# ============================================
# 4) RolePermissionMiddleware
# Restricts access unless the user role is 'admin' or 'moderator'
# ============================================
class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        # Ensure user is authenticated
        if user.is_authenticated:
            # Assume user model has a 'role' attribute
            role = getattr(user, 'role', None)
            if role not in ['admin', 'moderator']:
                return HttpResponseForbidden(
                    "You do not have permission to perform this action."
                )
        else:
            return HttpResponseForbidden("Authentication required.")

        return self.get_response(request)
