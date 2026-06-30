from rest_framework_simplejwt.authentication import JWTAuthentication


class TokenUser:
    # minimal user object returned after token verification — no DB lookup needed
    is_authenticated = True


class ServiceJWTAuthentication(JWTAuthentication):
    # override get_user to skip DB lookup — only verify token signature
    # each service has its own DB with no users table, so we can't look up the user
    def get_user(self, validated_token):
        return TokenUser()
