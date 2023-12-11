from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from ElectroStockApp.models import CustomUser, Speciality


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        # ...
        return token

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'password2', 'course', 'email')  # Agrega 'email' aquí

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username']
        )
        user.email = "pepito1234@gmail.com"
        user.set_password(validated_data['password'])
        user.is_staff = False

        # Ahora, puedes obtener las especialidades del validated_data
        specialties = validated_data.get('specialties', [])  

        user.save()

        # Agrega las especialidades al usuario si las has proporcionado
        for speciality in specialties:
            user.specialties.add(speciality)

        return user
