from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
# from django.contrib.auth.models import User

from rest_framework import serializers

# custom models
from accounts.models import Owner

Owner._meta.get_field('email')._unique = True


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ('id', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ('id', 'email', 'password','account_type','first_name','last_name')
        extra_kwargs = {'password': {'write_only': True}}

    # def validate_password(self, value):
    #     try:
    #         password_validation.validate_password(value)
    #     except ValidationError as exc:
    #         raise serializers.ValidationError(str(exc))
    #     return value

    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        return value

    def create(self, validated_data):
        # user = Owner.objects.create_user(validated_data['email'], validated_data['password'])
        user = Owner.objects.create_user(**validated_data)

        return user

# Login Serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")