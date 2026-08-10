from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from drf_spectacular.utils import extend_schema

from devops.users.models import BaseUser, Profile
from django.core.validators import MinLengthValidator
from .validators import number_validator, letter_validator, special_char_validator
from devops.api.mixins import ApiAuthMixin
from devops.users.services import register
from devops.users.selectors import get_profile

from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache

class RegisterAPI(APIView):
    
        
    class InputRegisterSerializer(serializers.Serializer):
        email = serializers.EmailField(max_length=255)
        bio = serializers.CharField(max_length=1000, required=False)
        
        password = serializers.CharField(
            validators=[
                MinLengthValidator(limit_value=10),
                number_validator,
                letter_validator,
                special_char_validator,
                
            ]
        )
        confirm_password = serializers.CharField(max_length=255)
        
    
        def validate_email(self, email):
            if BaseUser.objects.filter(email=email):
                raise serializers.ValidationError("Email Already Taken")
            return email
        def validate(self, data):
            if not data.get("password") or not data.get("confirm_password"):
                raise serializers.ValidationError("Please fill password and confirm password")
            
            if data.get("password") != data.get("confirm_password"):
                raise serializers.ValidationError("Confirm password is not equal to password")
            return data
            
    
    class OutPutRegisterSerializer(serializers.ModelSerializer):
        token = serializers.SerializerMethodField("get_token")
        class Meta:
            model= BaseUser
            fields = ("email", "token", "created_at", "updated_at")
            
        def get_token(self, user):
            data = dict()
            
            token_class = RefreshToken
            refresh = token_class.for_user(user)
            
            data["refresh"] = str(refresh)
            data["access"] = str(refresh.access_token)
            
            return data

    @extend_schema(request=InputRegisterSerializer, responses=OutPutRegisterSerializer)
    def post(self, request):
        serializer = self.InputRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            query = register(
                email=serializer.validated_data.get("email"),
                password=serializer.validated_data.get("password"),
                bio=serializer.validated_data.get("bio"),
                
                )
        except Exception as ex:
            return Response(
                f"Database Error {ex}",
                status=status.HTTP_400_BAD_REQUEST
            )
            
        return Response(self.OutPutRegisterSerializer(query, context={"request":request}).data)

        
    


class ProfileAPI(ApiAuthMixin, APIView):
        
    class OutPutSerializer(serializers.ModelSerializer):
        class Meta:
            model= Profile
            fields = ("bio", "posts_count", "subscriber_count", "subscription_count")
        
        def to_representation(self, instance):
            rep = super().to_representation(instance)
            cache_profile = cache.get(f"profile_{instance.user}", {})
            if cache_profile:
                rep["posts_count"]        = cache_profile.get("posts_count")
                rep["subscriber_count"]   = cache_profile.get("subscribers_count")
                rep["subscription_count"] = cache_profile.get("subscriptions_count")
                
            return rep
    
    @extend_schema(responses=OutPutSerializer)
    def get(self, request):
        query = get_profile(request.user)
        return Response(self.OutPutSerializer(query, context={"request":request}).data)
        
        
    
