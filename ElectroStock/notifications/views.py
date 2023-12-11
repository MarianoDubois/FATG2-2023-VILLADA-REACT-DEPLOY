from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import get_user_model, get_user
from django.contrib.auth.models import Group
from rest_framework.decorators import api_view
from rest_framework import viewsets, permissions, generics
from api.serializers import *


@api_view(["POST"])
def create_test_notification(request):
    try:
        # Obtén el ID del usuario destinatario desde los parámetros del POST
        usuario_destinatario_id = request.data.get("usuario_destinatario_id")
        usuario_destinatario = get_user_model().objects.get(pk=usuario_destinatario_id)

        # Obtén el tipo de notificación desde los parámetros del POST
        tipo_notificacion = request.data.get("tipo_notificacion")
        # Obtén el grupo "Profesor"
        profesor_group = Group.objects.get(name="Profesor")

        # Crea y envía la notificación
        notificacion = models.Notification.objects.create(
            user_sender=request.user,  # El remitente es el usuario autenticado
            type_of_notification=tipo_notificacion,
            message=request.data.get("mensaje"),
        )
        profesor_group_users = get_user_model().objects.filter(groups=profesor_group)
        # Agrega al usuario destinatario a la notificación
        notificacion.user_revoker.add(usuario_destinatario)

        # Agrega a los usuarios del grupo "Profesor" a la notificación
        notificacion.user_revoker.add(*profesor_group_users)

        return JsonResponse({"mensaje": "Notificación enviada exitosamente."})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
