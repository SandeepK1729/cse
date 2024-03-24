from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Customize the token response"""
    @classmethod
    def get_token(cls, user):
        """get token

        Args:
            user (User): authenticated user

        Returns:
            JSON: contains access, refresh token and user name and email
        """
        token = super().get_token(user)

        # Add custom claims
        token['name']   = user.get_full_name()
        token['email']  = user.email
        token['userId'] = user.id

        return token

