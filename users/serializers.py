from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email']
        read_only_fields = ('email', 'name')

# Before It was used to Register Users
    """ 
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)  # Automatically hashes password
        return user
    """

class UserRegisterationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        # Creating user using create_user method
        user = CustomUser.objects.create_user(**validated_data)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer class to authenticate users with email and password.
    """

    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")



