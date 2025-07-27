"""
Custom authentication setup for messaging_app
"""

from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    """
    Extend JWTAuthentication if we want custom behavior (optional).
    For now, just use default JWT authentication.
    """
    pass
