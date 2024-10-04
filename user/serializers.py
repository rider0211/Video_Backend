import datetime
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Invitation
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils import timezone
from rest_framework import serializers
from tourplace.models import TourPlace
from tourplace.serializers import TourplaceSerializer

class UserRegUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True, required = True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'phone_number', 'usertype', 'status', 'tourplace', 'level', 'is_activate')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.usertype = validated_data.get('usertype', instance.usertype)
        instance.tourplace = validated_data.get('tourplace', instance.tourplace)
        instance.level = validated_data.get('level', instance.level)
        instance.is_activate = validated_data.get('is_activate', instance.is_activate)
        instance.save()
        return super().update(instance, validated_data)

class UserListSerializer(serializers.ModelSerializer):
    tourplace = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'usertype', 'status', 'tourplace', 'level', 'is_activate']
        read_only_fields = fields
    def get_tourplace(self, obj):
        tourplace_ids = obj.tourplace
        tourplaces = TourPlace.objects.filter(id__in=tourplace_ids)
        return TourplaceSerializer(tourplaces, many=True).data

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user:
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token
            return {
                'refresh': str(refresh),
                'access': str(access),
                'user_id': user.id,
                'usertype': user.usertype,
                'level': user.level,
                'username': user.username,
                'status' : user.status,
                'tourplace': user.tourplace,
                'user': user
            }
        else:
            raise serializers.ValidationError("Invalid email or password")
        
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)  # Exclude password from the serialized data

class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['email', 'token', 'invited_by', 'created_at']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user