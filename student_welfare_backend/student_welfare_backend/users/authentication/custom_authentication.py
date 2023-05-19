from datetime import timedelta
from django.utils import timezone
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        authenticated_user = super().authenticate(request)
        if authenticated_user is not None and self.token_should_refresh(authenticated_user[1]):
            self.refresh_token(request, authenticated_user[1])

        return authenticated_user

    def token_should_refresh(self, token):
        # Check if token is about to expire in the next 5 minutes
        return token['exp'] - timezone.now().timestamp() < 300

    def refresh_token(self, request, token):
        refresh_token = RefreshToken(token)
        access_token = str(refresh_token.access_token)
        # Set the new access token in the request's Authorization header
        request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
