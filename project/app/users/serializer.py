from dataclasses import fields

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User

user_fields = ('id', 'email', 'password', 'full_name', 'avatar', 'date_joined', 'is_active', 'is_staff', 'is_superuser', 'last_login')

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['username'] = user.username
        return token

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, min_length=6)
    full_name = serializers.CharField(required=True, min_length=6)

    class Meta:
        model = User
        fields = user_fields

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists!")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        user = self.context['request'].user

        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError("Incorrect old password!")

        if user.check_password(attrs['new_password']):
            raise serializers.ValidationError("New password must not be same as old password!")

        return attrs