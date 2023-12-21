from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Contact

class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = (
            'name', 'email', 'content'
        )

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['id'] = user.id
        token['email'] = user.email

        return token
