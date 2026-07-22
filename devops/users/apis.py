from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from drf_spectacular.utils import extend_schema

from devops.users.models import BaseUser
from django.core.validators import MinLengthValidator
from .validators import number_validator, letter_validator, special_char_validator

class RegisterAPI(APIView):
    
        
    class InputRegisterSerializer(serializers.Serializer):
        email = serializers.CharField(max_length=255)

        password = serializers.CharField(
            validators=[
                MinLengthValidator(limit_value=10),
                number_validator,
                letter_validator,
                special_char_validator
            ]
        )
        confirm_password = serializers.CharField(max_length=255)
        
    
    def validate_email(self, email):
        if BaseUser.objects.filter(email=email):
            raise serializers.ValidationError("Email Already Taken")
    
    def validate(self, data):
        if not data.get("password") or not data.get("confirm_password"):
            raise serializers.ValidationError("Please fill password and confirm password")
        
        if data.get("password") != data.get("confirm_password"):
            raise serializers.ValidationError("Confirm password is not equal to password")
            
            
    
    class OutPutRegisterSerializer(serializers.ModelSerializer):
        class Meta:
            model= BaseUser
            fields = ("email")
            
    @extend_schema(request=InputRegisterSerializer, responses=OutPutRegisterSerializer)
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            query = create_user(
                email=serializer.validated_data.get("email"),
                password=serializer.validated_data.get("password"),
                )
        except Exception as ex:
            return Response(
                f"Database Error {ex}",
                status=status.HTTP_400_BAD_REQUEST
            )
            
        return Response(self.OutPutRegisterSerializer(query, context={"request":request}).data)

        
    
