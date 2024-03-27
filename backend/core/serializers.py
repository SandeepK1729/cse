from rest_framework_simplejwt.serializers   import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens        import RefreshToken
from rest_framework                         import serializers


from .models import User 

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
    
    def validate(self, attrs):
        data = super().validate(attrs)

        # Customize your response here
        # data.update({'user': {
        #     'name': self.user.get_full_name(),
        #     'email': self.user.email,
        #     'userId': self.user.id,
        # }})

        return data

class UserSerializer(serializers.ModelSerializer):
    """User serializer for user model"""
    
    token          = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model   = User
        fields  = [
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
            'gender',
            'date_joined',
            'token',
        ]
        
        write_only_fields = ['password']
        extra_kwargs = {
            'username'      : {'required': True},
            'password'      : {'required': True},
            'first_name'    : {'required': True},
            'last_name'     : {'required': True},
            
            'email'         : {'required': False},
            'gender'        : {'required': False},

            'date_joined'   : {'read_only': True},
            'token'         : {'read_only': True},
        }

    def get_token(self, obj):
        """get token

        Args:
            obj (User): user object

        Returns:
            JSON: access token and refresh token
        """
        user = self.user if hasattr(self, 'user') else obj

        refresh = RefreshToken.for_user(user)
        return {
            'refresh' : str(refresh),
            'access'  : str(refresh.access_token),
        }

    def create(self, validated_data):
        """create user

        Args:
            validated_data (JSON): contains user data

        Returns:
            User: created user
        """
        user = User.objects.create_user(**validated_data)
        user.save()
        self.user = user
        return user
    
    def update(self, instance, validated_data):
        """update user

        Args:
            instance (User): user instance from database
            validated_data (JSON): contains user updated data
        
        Returns:
            User: updated user
        """
        user = super().update(instance, validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
