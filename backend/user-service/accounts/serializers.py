from rest_framework import serializers
from accounts.models import User

# Handles incoming registration requests — validates and saves new user
class RegisterSerializer(serializers.ModelSerializer):
    # write_only ensures password is accepted but never returned in response
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        # Only these fields are accepted from the registration request
        fields = ['id', 'username', 'email', 'password', 'role', 'phone']

    # Overrides default create() to use create_user() which hashes the password
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            # role and phone are optional — defaults applied if not provided
            role=validated_data.get('role', 'staff'),
            phone=validated_data.get('phone', ''),
        )
        return user

# Handles outgoing user data in API responses — password excluded for security
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Only safe fields returned — no password, no internal Django fields
        fields = ['id', 'username', 'email', 'role', 'phone', 'created_at']