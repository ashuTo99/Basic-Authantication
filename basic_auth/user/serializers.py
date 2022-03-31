from dataclasses import fields
from rest_framework import serializers
from .models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email','password', 'confirm_password', )
        

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            confirm_password = validated_data['confirm_password']
        )
        user.set_password(validated_data['password'])

        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email','password','confirm_password')


class LoginUserSerializer(serializers.Serializer):
    email = serializers.CharField(allow_blank=False)
    password = serializers.CharField(allow_blank=False)

    class Meta:
        fields = ['email', 'password']


    # Validate request data
    def validate(self, data):
        email = data.get('email', '')
        password = data.get('password', '')
        user = User.objects.get(email=email)
        if user is None:
            raise serializers.ValidationError({'emai':'this email is not valid'})
        elif password != '' or password is not None:
            if user is None or not check_password(password, user.password):
                raise serializers.ValidationError({"Password": "Wrong Credentials."})
        return data