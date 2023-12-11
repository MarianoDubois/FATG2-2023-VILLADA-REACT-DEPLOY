from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from .serializer import MyTokenObtainPairSerializer, RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from ElectroStockApp.models import CustomUser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
import json
from django.contrib.auth.models import User
from django.urls import reverse
from ElectroStockApp import models
from api import serializers

@api_view(["GET"])
def UsersFiltros(request, name):
    if request.method == "GET":
        queryset = models.CustomUser.objects.filter(
            username=name
        )
        serializer = serializers.UsersSerializer(queryset, many=True)
        return Response(serializer.data)


    return Response(status=405)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Agregar el usuario al grupo de Profesor
        profesor_group = models.Group.objects.get(name="Profesor")
        user.groups.add(profesor_group)

        # Obtener las especialidades seleccionadas
        speciality_ids = request.data.get("selectedSpecialities", [])
        specialities = models.Speciality.objects.filter(pk__in=speciality_ids)
        user.specialties.set(specialities)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/auth/token/',
        '/auth/register/',
        '/auth/token/refresh/',
        '/auth/test/'
    ]
    return Response(routes)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def testEndPoint(request):
    if request.method == 'GET':
        data = f"Congratulation {request.user}, your API just responded to GET request"
        return Response({'response': data}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        try:
            body = request.body.decode('utf-8')
            data = json.loads(body)
            if 'text' not in data:
                return Response("Invalid JSON data", status.HTTP_400_BAD_REQUEST)
            text = data.get('text')
            data = f'Congratulation your API just responded to POST request with text: {text}'
            return Response({'response': data}, status=status.HTTP_200_OK)
        except json.JSONDecodeError:
            return Response("Invalid JSON data", status.HTTP_400_BAD_REQUEST)
    return Response("Invalid JSON data", status.HTTP_400_BAD_REQUEST)
