from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email']
        read_only_fields = ('email', 'name')


class UserRegisterSerialzer(serializers.ModelSerializer):
    '''
    Serializer class to register user with password confirmation logic
    '''
    password = serializers.CharField(write_only=True, min_length=8)
    conf_password = serializers.CharField(write_only=True, label="Confirmation Password")

    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email', 'password', 'conf_password']

    # Main Password Validation Logic (Commonly used in Sign Up Forms)
    def validate(self, user_data):
        if user_data['password'] != user_data['conf_password']:
            raise serializers.ValidationError("Passwords doesn't match!")
        return user_data


    def create(self, validated_data):
        # Example JSON data: {'username': 'john', 'email': 'john@example.com', 'password': '1234'}
        validated_data.pop('conf_password') # Remove the confirmation password before create new User
        user = CustomUser.objects.create_user(**validated_data) # Unpack the JSON Data to the model
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





"""class UserRegistrationSerializer(serializers.ModelSerializer):
    '''
    Old User Registration Serializer
    '''
    password = serializers.CharField(write_only=True, min_length=8)
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email', 'password']


    def create(self, validated_data):
        # Creating user using create_user method
        validated_data['password'] = make_password(validated_data['password'])
        user = CustomUser.objects.create(**validated_data)
        user.save()
        return user"""




