from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
import logging

# docker exec -it promoease-backend-backend-1 python test_views.py

# Get the custom User model
User = get_user_model()

# Setup logger for debugging and tracking requests
logger = logging.getLogger(__name__)

class RegisterView(generics.CreateAPIView):
    """
    API for user registration.
    Uses Django Rest Framework's `CreateAPIView`, which automatically handles:
    - Data validation (`serializer.is_valid()`)
    - Object creation (`serializer.save()`)
    - Returning an HTTP 201 response on success
    """
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        """
        Overrides the default `create()` method of `CreateAPIView`.
        - Logs request data for debugging
        - Calls the parent `create()` method to handle registration
        - Modifies the response to return a custom success message
        """
        logger.info(f"🛠 Register Request Data: {request.data}")
        response = super().create(request, *args, **kwargs)
        response.data = {"message": "User created successfully"}
        return response


class LoginView(APIView):
    """
    API for user authentication.
    - Accepts email & password as input
    - Returns access & refresh tokens if authentication is successful
    - Stores the access token in HttpOnly Secure Cookie
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handles user login requests.
        - Uses `LoginSerializer` to validate and authenticate the user
        - If successful, returns JWT access & refresh tokens
        - Stores access token in a secure HttpOnly cookie
        """
        logger.info(f"🛠 Login Request Data: {request.data}")
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens = serializer.validated_data  # Returns {'access': ..., 'refresh': ...}
        response = Response({"message": "Login successful"}, status=status.HTTP_200_OK)

        # Set JWT in HttpOnly Secure Cookie
        response.set_cookie(
            key=settings.SIMPLE_JWT["AUTH_COOKIE"],  # Cookie Name
            value=tokens["access"],  # Save access token
            httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],  # Secure Cookie
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],  # HTTPS-only
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],  # Cross-site protection
            max_age=60 * 60 * 24,  # Valid for 1 day
        )

        # Return the refresh token in the response (frontend can store it securely)
        return response


class LogoutView(APIView):
    """
    API for user logout.
    - Invalidates the refresh token
    - Deletes the access token from HttpOnly Cookie
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Handles user logout by blacklisting the refresh token.
        - Also removes JWT access token from HttpOnly Cookie.
        """
        response = Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)

        # Delete JWT access token from cookies
        response.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE"])

        # Blacklist the refresh token (optional, only if using blacklisting)
        refresh_token = request.data.get("refresh")
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception as e:
                logger.error(f"❌ Failed to blacklist refresh token: {e}")

        return response


class UserProfileView(APIView):
    """
    API to get the currently authenticated user's information.
    Requires the user to be logged in (JWT authentication).
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieves user profile details from the authenticated request.
        """
        user = request.user
        return Response({
            "email": user.email,
            "name": user.name,
            "role": user.role
        })