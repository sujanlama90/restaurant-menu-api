from rest_framework import serializers
from .models import CustomUser

class CustomerRegisterSerailizer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['id','first_name','last_name','username','email','phone','password','password1']

    def validate(self, data):
        if data['password'] != data['password1']:
            raise serializers.ValidationError('password and password1 doesnot match!!')
        return data
    
    def validate_email(self, value):
        value = value.strip().lower()

        if CustomUser.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "This email is already registered."
            )
        return value
    
    def create(self, validated_data):
        validated_data.pop('password1')
        return CustomUser.objects.create_user(**validated_data,role='CUSTOMER',
        is_staff=False,
        is_superuser=False,
        )

class StaffRegisterSerailizer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','username','email','phone','password','password1']

    def validate(self, data):
        if data['password'] != data['password1']:
            raise serializers.ValidationError('password and password1 doesnot match!!')
        return data

    def validate_email(self, value):
        value = value.strip().lower()

        if CustomUser.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "This email is already registered."
            )
        return value

    def create(self, validated_data):
        validated_data.pop('password1')
        return CustomUser.objects.create_user(**validated_data,role='STAFF',is_staff=False,
                                              is_active=False,
                                              is_superuser=False,)


class AdminSerailizer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','username','email','phone','password','password1']

    def validate(self, data):
        if data['password'] != data['password1']:
            raise serializers.ValidationError('password and password1 doesnot match!!')
        return data
    
    def validate_email(self, value):
        value = value.strip().lower()

        if CustomUser.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "This email is already registered."
            )
        return value

    def create(self, validated_data):
        validated_data.pop('password1')
        return CustomUser.objects.create_superuser(**validated_data,role='ADMIN',is_superuser=True)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id", "username", "first_name",
            "last_name", "email", "phone", "role"
        ]
        read_only_fields = ['id','role']

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'email',
            'role',
            'is_active',
        ]
        read_only_fields = ['id']