from rest_framework.response import Response
from rest_framework.decorators import api_view
from ElectroStockApp import models
from .serializers import *
from rest_framework import viewsets, permissions, generics
from django.db.models import (
    Sum,
    Value,
    IntegerField,
    Q,
    Case,
    When,
    F,
    FloatField,
)
from django.shortcuts import get_object_or_404
import json
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions
from cryptography.fernet import Fernet
from django.utils import timezone
from dateutil.parser import parse as dateparse
from pytz import timezone, utc
from django.db.models.functions import TruncDate
from django.db.models import ExpressionWrapper, F, DurationField, Avg
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Count, Q
from collections import defaultdict
from django.contrib.auth import get_user_model, get_user
from django.contrib.auth.models import Group


# View para tomar el stock actual segun el id que mandas por la url
@api_view(["GET", "POST"])
def get_stock(request, element_id):
    if request.method == "GET":
        if element_id is not None:
            boxes = models.Box.objects.filter(element__id=element_id)
            box_ids = [box.id for box in boxes]

            total_com = models.Log.objects.filter(
                box__id__in=box_ids, status="COM"
            ).aggregate(total=Sum("quantity"))["total"]
            total_ped = models.Log.objects.filter(
                box__id__in=box_ids, status="PED"
            ).aggregate(total=Sum("quantity"))["total"]
            total_rot = models.Log.objects.filter(
                box__id__in=box_ids, status="ROT"
            ).aggregate(total=Sum("quantity"))["total"]
            total_ap = models.Log.objects.filter(
                box__id__in=box_ids, status="AP"
            ).aggregate(total=Sum("quantity"))["total"]

            if total_com is None:
                total_com = 0
            if total_ped is None:
                total_ped = 0
            if total_ap is None:
                total_ap = 0
            if total_rot is None:
                total_rot = 0

            current_stock = total_com - total_ped - total_ap - total_rot

            queryset = models.Log.objects.filter(box__id__in=box_ids, status="COM")
            queryset = queryset.annotate(
                current_stock=Value(current_stock, output_field=IntegerField())
            )

            serializer = StockSerializer(queryset, many=True)  # Serializar los datos

            return Response(serializer.data)  # Devolver la respuesta serializada

        return Response(
            []
        )  # Si no se proporciona el parámetro 'element_id', devolver una lista vacía como respuesta


class CustomPagination(PageNumberPagination):
    page_size = 10  # Cantidad de elementos por página
    page_size_query_param = "page_size"
    max_page_size = 100


from rest_framework.authentication import BasicAuthentication


class ElementsViewSet(viewsets.ModelViewSet):
    queryset = models.Element.objects.filter()
    permission_classes = [
        permissions.AllowAny
    ]  # permission_classes = [permissions.IsAuthenticated] Fix Rapido para morales
    # authentication_classes = [BasicAuthentication]
    serializer_class = ElementSerializer




class TokenViewSet(viewsets.ModelViewSet):
    queryset = models.TokenSignup.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = TokenSerializer




class ProductosEcommerceAPIView(viewsets.ModelViewSet):
    queryset = models.Element.objects.filter(ecommerce=True)
    permission_classes = [permissions.AllowAny]
    serializer_class = ElementEcommerceSerializer2


class ecommercePaginacionAPIView(viewsets.ModelViewSet):
    queryset = models.Element.objects.filter(ecommerce=True)
    permission_classes = [permissions.AllowAny]
    serializer_class = ElementEcommerceSerializer2
    pagination_class = CustomPagination

    @action(detail=False, methods=["GET"])
    def search(self, request):
        search_query = request.query_params.get("search", "")
        queryset = models.Element.objects.filter(
            ecommerce=True, name__icontains=search_query
        )
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


from PIL import Image
from io import BytesIO
from django.conf import settings
import os
import datetime

BASE_DIR = settings.BASE_DIR
carpeta_guardado = os.path.join(BASE_DIR, "img-prod/img-logs")

def combinar_imagenes(nombre_archivo, imagen1, imagen2=None, imagen3=None, imagen4=None):
    try:
        # Cargar las imágenes disponibles
        img1 = Image.open(imagen1.lstrip("/"))
        img2 = Image.open(imagen2.lstrip("/")) if imagen2 else None
        img3 = Image.open(imagen3.lstrip("/")) if imagen3 else None
        img4 = Image.open(imagen4.lstrip("/")) if imagen4 else None
        print('imagen 1', img1,'imagen 2', img2,'imagen 3', img3,'imagen 4', img4)
        # Obtener el tamaño de la imagen principal (img1)
        width, height = img1.size

        # Ajustar el tamaño de la nueva imagen según la cantidad de imágenes
        if img2 and img3 and img4:
            nueva_imagen = Image.new("RGB", (width * 2, height * 2))
            nueva_imagen.paste(img1, (0, 0))
            nueva_imagen.paste(img2.resize((width, height)), (width, 0))
            nueva_imagen.paste(img3.resize((width, height)), (0, height))
            nueva_imagen.paste(img4.resize((width, height)), (width, height))
        elif img2:
            nueva_imagen = Image.new("RGB", (width * 2, height))
            nueva_imagen.paste(img1, (0, 0))
            nueva_imagen.paste(img2.resize((width, height)), (width, 0))
        else:
            nueva_imagen = Image.new("RGB", (width, height))
            nueva_imagen.paste(img1, (0, 0))

        # Guardar la nueva imagen en bytes
        ruta_guardado = os.path.join(carpeta_guardado, nombre_archivo)
        print("Ruta de guardado:", ruta_guardado)
        nueva_imagen.save(ruta_guardado, format="JPEG")

        # Obtener el camino relativo
        ruta_relativa = os.path.relpath(ruta_guardado, BASE_DIR)
        print("Guardado exitoso.")

        return ruta_relativa

    except Exception as e:
        print("Error al combinar imágenes:", str(e))
        return None

import os
from django.conf import settings
from django.core.files.storage import default_storage


def obtener_imagen_primer_log(primer_log_prueba):
    try:
        if (
            primer_log_prueba.box
            and primer_log_prueba.box.element
            and primer_log_prueba.box.element.image
            and primer_log_prueba.box.element.image.file
        ):
            imagen_path = default_storage.path(
                primer_log_prueba.box.element.image.file.name
            )
            print("Ruta de la imagen primer log:", imagen_path)
            if default_storage.exists(primer_log_prueba.box.element.image.file.name):
                print("La imagen existe.")

                # Obtener el camino relativo
                ruta_relativa = os.path.relpath(imagen_path, BASE_DIR)

                return ruta_relativa
            else:
                print("La imagen NO existe.")
    except FileNotFoundError:
        print("Archivo no encontrado:", primer_log_prueba.box.element.image.file.name)
    return None


def obtener_imagenes_elementos(elementos):
    imagenes = []
    for elemento in elementos:
        box = elemento["box"]
        if "image" in box and box["image"]:
            imagenes.append(box["image"])
            print(box["image"])
    return imagenes


from collections import defaultdict




@api_view(["GET", "POST"])
def AllPrestamos(request):
    pagination_class = CustomPagination()

    if request.method == "GET":
        valid_statuses = [
            models.Log.Status.APROBADO,
            models.Log.Status.PEDIDO,
            models.Log.Status.DESAPROBADO,
            models.Log.Status.VENCIDO,
            models.Log.Status.DEVUELTO,
            models.Log.Status.DEVUELTOTARDIO,
        ]

        queryset = models.Log.objects.filter(status__in=valid_statuses).order_by("-dateIn")

        if queryset.exists():
            # Agrupar logs por fecha y hora de creación
            grouped_logs = defaultdict(list)

            for log in queryset:
                creation_date = (
                    log.dateIn.strftime("%Y-%m-%dT%H:%M") if log.dateIn else None
                )
                log_data = LogSerializer(log).data
                log_data["dateIn"] = creation_date
                grouped_logs[creation_date].append(log_data)

            response_data = []

            for creation_date, logs_data in grouped_logs.items():
                primer_log = logs_data[0]
                primer_log_prueba = models.Log.objects.get(id=primer_log.get("id", ""))

                dateIn_primer_log_prueba = (
                    primer_log_prueba.dateIn.strftime("%Y-%m-%d %H:%M")
                    if primer_log_prueba.dateIn
                    else None
                )
                dateOut_primer_log = (
                    primer_log.get("dateOut", "") if primer_log else None
                )

                imagen_primer_log = None
                imagen_primer_log = obtener_imagen_primer_log(primer_log_prueba)
                imagen_combinada = None
                nombre_archivo = (
                    f"imagen_combinada_{creation_date}_{datetime.datetime.now}.jpg"
                )
                # print("ACA ", logs_data)
                if imagen_primer_log:
                    imagenes_elementos = obtener_imagenes_elementos(logs_data)
                    imagenes_elementos_filtradas = [
                        imagen
                        for imagen in imagenes_elementos[:4]
                        if imagen is not None
                    ]
                    imagen_combinada = combinar_imagenes(
                        nombre_archivo, *imagenes_elementos_filtradas
                    )

                    primer_log["imagen_combinada"] = imagen_combinada

                count_logs = len(logs_data) if logs_data else 0

                response_data.append(
                    {
                        "dateOut": dateOut_primer_log,
                        "id_user": primer_log["borrower"]["id"]
                            if primer_log
                            else None,
                        "usuario": primer_log["borrower"]["username"]
                        if primer_log
                        else None,
                        "nombre": primer_log["borrower"]["first_name"]
                        if primer_log
                        else None,
                        "apellido": primer_log["borrower"]["last_name"]
                        if primer_log
                        else None,
                        "estado": primer_log["status"] if primer_log else None,
                        "dateIn": dateIn_primer_log_prueba,
                        "imagen": imagen_combinada,
                        "count": count_logs,
                        "lista": logs_data,
                    }
                )

            # Aplicar paginación
            paginated_response = pagination_class.paginate_queryset(
                response_data, request
            )
            return pagination_class.get_paginated_response(paginated_response)

        else:
            return Response("No se encontraron logs para este usuario.")

    if request.method == "POST":
        return Response({"message": "Post completado"})



@api_view(["GET", "POST"])
def PrestamoVerAPIView(request, user_id):
    pagination_class = CustomPagination()

    if request.method == "GET":
        valid_statuses = [
            models.Log.Status.APROBADO,
            models.Log.Status.PEDIDO,
            models.Log.Status.DESAPROBADO,
            models.Log.Status.VENCIDO,
            models.Log.Status.DEVUELTO,
            models.Log.Status.DEVUELTOTARDIO,
        ]

        queryset = models.Log.objects.filter(lender=user_id, status__in=valid_statuses).order_by("-dateIn")

        if queryset.exists():
            # Agrupar logs por fecha y hora de creación
            grouped_logs = defaultdict(list)

            for log in queryset:
                creation_date = (
                    log.dateIn.strftime("%Y-%m-%dT%H:%M") if log.dateIn else None
                )
                log_data = LogSerializer(log).data
                log_data["dateIn"] = creation_date
                grouped_logs[creation_date].append(log_data)

            response_data = []

            for creation_date, logs_data in grouped_logs.items():
                primer_log = logs_data[0]
                primer_log_prueba = models.Log.objects.get(id=primer_log.get("id", ""))

                dateIn_primer_log_prueba = (
                    primer_log_prueba.dateIn.strftime("%Y-%m-%d %H:%M")
                    if primer_log_prueba.dateIn
                    else None
                )
                dateOut_primer_log = (
                    primer_log.get("dateOut", "") if primer_log else None
                )

                imagen_primer_log = None
                imagen_primer_log = obtener_imagen_primer_log(primer_log_prueba)
                imagen_combinada = None
                nombre_archivo = (
                    f"imagen_combinada_{creation_date}_{datetime.datetime.now}.jpg"
                )
                # print("ACA ", logs_data)
                if imagen_primer_log:
                    imagenes_elementos = obtener_imagenes_elementos(logs_data)
                    imagenes_elementos_filtradas = [
                        imagen
                        for imagen in imagenes_elementos[:4]
                        if imagen is not None
                    ]
                    imagen_combinada = combinar_imagenes(
                        nombre_archivo, *imagenes_elementos_filtradas
                    )

                    primer_log["imagen_combinada"] = imagen_combinada

                count_logs = len(logs_data) if logs_data else 0

                response_data.append(
                    {
                        "dateOut": dateOut_primer_log,
                        "id_user": primer_log["borrower"]["id"]
                            if primer_log
                            else None,
                        "usuario": primer_log["borrower"]["username"]
                        if primer_log
                        else None,
                        "nombre": primer_log["borrower"]["first_name"]
                        if primer_log
                        else None,
                        "apellido": primer_log["borrower"]["last_name"]
                        if primer_log
                        else None,
                        "estado": primer_log["status"] if primer_log else None,
                        "dateIn": dateIn_primer_log_prueba,
                        "imagen": imagen_combinada,
                        "count": count_logs,
                        "lista": logs_data,
                    }
                )

            # Aplicar paginación
            paginated_response = pagination_class.paginate_queryset(
                response_data, request
            )
            return pagination_class.get_paginated_response(paginated_response)

        else:
            return Response("No se encontraron logs para este usuario.")

    if request.method == "POST":
        return Response({"message": "Post completado"})


@api_view(["GET", "POST"])
def PrestamoPendientesAPIView(request, user_id):
    if request.method == "GET":
        valid_statuses = [
            models.Log.Status.PEDIDO,
        ]

        queryset = models.Log.objects.filter(lender=user_id, status__in=valid_statuses).order_by("-dateIn")

        serializer = LogSerializer(queryset, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        return Response({"message": "Post completado"})

    return Response(status=405)


# View para las categorias
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CategoriaSerializer


# View para los usuarios
from validate_email_address import validate_email
from rest_framework.decorators import action
from rest_framework.response import Response
import dns.resolver


# View para los usuarios
class UsersViewSet(viewsets.ModelViewSet):
    queryset = models.CustomUser.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UsersSerializer

    # Método personalizado para actualizar el email mediante PUT
    @action(detail=True, methods=["put"])
    def update_email(self, request, pk=None):
        user = self.get_object()
        new_email = request.data.get("email", None)

        if new_email is not None:
            try:
                # Validar el correo electrónico con verificación de registros MX usando dnspython
                result = dns.resolver.resolve(new_email.split("@")[1], "MX")
                is_valid = bool(result)

                if is_valid:
                    user.email = new_email
                    user.save()
                    serializer = self.get_serializer(user)
                    return Response(serializer.data)
                else:
                    return Response(
                        {
                            "error": 'El campo "email" no es una dirección de correo electrónico válida'
                        },
                        status=400,
                    )
            except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN) as e:
                return Response({"error": f"Error de validación: {e}"}, status=400)
            except Exception as e:
                return Response(
                    {"error": f"Error desconocido de validación: {e}"}, status=400
                )
        else:
            return Response({"error": 'El campo "email" es requerido'}, status=400)


class LogViewSet(viewsets.ModelViewSet):
    queryset = models.Log.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = OnlyPkLogSerializer


# View para los cursos
class CourseViewSet(viewsets.ModelViewSet):
    queryset = models.Course.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CourseSerializer


# View para los laboratorios
class LaboratorioViewSet(viewsets.ModelViewSet):
    queryset = models.Laboratory.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = LaboratorySerializer


# View para las ubicaciones
class LocationViewSet(viewsets.ModelViewSet):
    queryset = models.Location.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = LocationSerializer


# View para los boxes
class BoxViewSet(viewsets.ModelViewSet):
    queryset = models.Box.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = BoxSerializer


# View para las especialidades
class SpecialityViewSet(viewsets.ModelViewSet):
    queryset = models.Speciality.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = SpecialitySerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = models.Notification.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = NotificationSerializer


# View para tomar el stock actual segun el id que mandas por la url
@api_view(["GET", "POST"])
def get_stock(request, element_id):
    if request.method == "GET":
        if element_id is not None:
            boxes = models.Box.objects.filter(element__id=element_id)
            box_ids = [box.id for box in boxes]

            total_com = models.Log.objects.filter(
                box__id__in=box_ids, status="COM"
            ).aggregate(total=Sum("quantity"))["total"]
            total_ped = models.Log.objects.filter(
                box__id__in=box_ids, status="PED"
            ).aggregate(total=Sum("quantity"))["total"]
            total_rot = models.Log.objects.filter(
                box__id__in=box_ids, status="ROT"
            ).aggregate(total=Sum("quantity"))["total"]
            total_ap = models.Log.objects.filter(
                box__id__in=box_ids, status="AP"
            ).aggregate(total=Sum("quantity"))["total"]

            if total_com is None:
                total_com = 0
            if total_ped is None:
                total_ped = 0
            if total_ap is None:
                total_ap = 0
            if total_rot is None:
                total_rot = 0

            current_stock = total_com - total_ped - total_ap - total_rot

            queryset = models.Log.objects.filter(box__id__in=box_ids, status="COM")
            queryset = queryset.annotate(
                current_stock=Value(current_stock, output_field=IntegerField())
            )

            serializer = StockSerializer(queryset, many=True)  # Serializar los datos

            return Response(serializer.data)  # Devolver la respuesta serializada

        return Response(
            []
        )  # Si no se proporciona el parámetro 'element_id', devolver una lista vacía como respuesta


@api_view(["GET", "POST"])
def carrito(request, user_id):
    if request.method == "GET":
        queryset = models.Log.objects.filter(
            lender=user_id, status=models.Log.Status.CARRITO
        )
        serializer = LogSerializer(queryset, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        return Response({"message": "Elemento agregado al carrito"})

    return Response(status=405)


@api_view(["GET"])
def UsersFiltros(request, name):
    if request.method == "GET":
        queryset = models.CustomUser.objects.filter(username=name)
        serializer = UsersSerializer(queryset, many=True)
        return Response(serializer.data)

    return Response(status=405)


@api_view(["GET", "POST"])
def VencidosAPIView(request, user_id):
    if request.method == "GET":
        queryset = models.Log.objects.filter(
            lender=user_id, status=models.Log.Status.VENCIDO
        )
        serializer = LogSerializer(queryset, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        return Response({"message": "Post completado"})

    return Response(status=405)


@api_view(["GET", "POST"])
def cantCarrito(request, user_id):
    if request.method == "GET":
        queryset = models.Log.objects.filter(
            lender=user_id, status=models.Log.Status.CARRITO
        )

        # Contar la cantidad de elementos en el carrito
        count = queryset.count()

        return Response({count})

    if request.method == "POST":
        return Response({"message": "Post completado"})

    return Response(status=405)


@api_view(["GET", "POST"])
def cantNotificaciones(request, user_id):
    if request.method == "GET":
        queryset = models.Notification.objects.filter(
            user_revoker=user_id, status=models.Notification.NotificationStatus.UNREAD
        )

        # Contar la cantidad de elementos en el carrito
        count = queryset.count()

        return Response({count})

    if request.method == "POST":
        return Response({"message": "Post completado"})

    return Response(status=405)


@api_view(["GET", "POST"])
def PrestamosActualesView(request, user_id):
    pagination_class = CustomPagination()

    if request.method == "GET":
        valid_statuses = [
            models.Log.Status.APROBADO,
            models.Log.Status.VENCIDO,
        ]

        queryset = models.Log.objects.filter(lender=user_id, status__in=valid_statuses)

        serializer = LogSerializer(queryset, many=True)

        # Aplicar paginación
        paginated_response = pagination_class.paginate_queryset(
            serializer.data, request
        )
        return pagination_class.get_paginated_response(paginated_response)

    if request.method == "POST":
        return Response({"message": "Post completado"})

    return Response(status=405)


from django.utils.timezone import now
import datetime


# View para las estadisticas de los productos mas pedidos
class MostRequestedElementView(generics.ListAPIView):
    serializer_class = ElementSerializer

    def get_queryset(self):
        current_year = datetime.datetime.now().year
        queryset = (
            models.Element.objects.filter(
                box__log__status=models.Log.Status.APROBADO,
                box__log__dateIn__year=current_year,
            )
            .annotate(
                num_borrowed_logs=Count(
                    "box__log", filter=Q(box__log__status=models.Log.Status.APROBADO)
                )
            )
            .order_by("-num_borrowed_logs")[:5]
        )

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = []

        current_year = (
            datetime.datetime.now().year
        )  # Agregar esta línea para definir la variable current_year

        for item in serializer.data:
            element_data = item.copy()
            element_id = item["id"]
            num_borrowed_logs = models.Log.objects.filter(
                box__element_id=element_id, status="AP", dateIn__year=current_year
            ).count()
            element_data["num_borrowed_logs"] = num_borrowed_logs
            response_data.append(element_data)

        return Response(response_data)


# view para la estaditica del porcentaje de prestamos aprobados
class LogStatisticsView(generics.ListAPIView):
    serializer_class = LogStatisticsSerializer

    def get_queryset(self):
        current_year = datetime.datetime.now().year
        queryset = models.Log.objects.filter(dateIn__year=current_year)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        statistics = queryset.aggregate(
            total_logs=Count("id"),
            approved_logs=Sum(
                Case(When(status="AP", then=1), default=0, output_field=IntegerField())
            ),
            rejected_logs=Sum(
                Case(When(status="DAP", then=1), default=0, output_field=IntegerField())
            ),
        )

        serializer = self.get_serializer(
            [statistics], many=True
        )  # Use the LogStatisticsSerializer
        return Response(serializer.data)


# view para la estadistica para el mayor usuario que hace prestamos
class LenderStatisticsView(generics.ListAPIView):
    serializer_class = LenderStatisticsSerializer

    def get_queryset(self):
        current_year = datetime.datetime.now().year
        queryset = (
            models.Log.objects.filter(dateIn__year=current_year)
            .values("lender__username")
            .annotate(total_lender_logs=Count("lender"))
            .order_by("-total_lender_logs")
        )
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        lender_statistics = serializer.data if serializer.data else None
        return Response(lender_statistics)


# view para el usuario que mas aprueba prestamos
class BorrowerStatisticsView(generics.ListAPIView):
    serializer_class = BorrowerStatisticsSerializer

    def get_queryset(self):
        current_year = datetime.datetime.now().year
        queryset = (
            models.Log.objects.filter(dateIn__year=current_year)
            .values("borrower__username")
            .annotate(total_borrower_logs=Count("borrower"))
            .order_by("-total_borrower_logs")
        )
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        borrower_statistics = serializer.data if serializer.data else None
        return Response(borrower_statistics)


# view para la estadistica de los dias con mayor prestamos
class DateStatisticsView(generics.ListAPIView):
    serializer_class = DateStatisticsSerializer

    def get_queryset(self):
        current_year = datetime.datetime.now().year
        queryset = (
            models.Log.objects.filter(dateIn__year=current_year)
            .values("dateIn")
            .annotate(total_datein_logs=Count("dateIn"))
            .order_by("-total_datein_logs")[:1]
        )
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        date_statistics = serializer.data if serializer.data else None
        return Response(date_statistics)


class DateAvgView(APIView):
    def get(self, request, format=None):
        # Filtra los registros por los estados AP, DAP, DEV, VEN y TAR
        current_year = datetime.datetime.now().year
        queryset = models.Log.objects.filter(
            dateIn__year=current_year,
            status__in=["AP", "DAP", "DEV", "VEN", "TAR"],
            dateOut__isnull=False,
        )

        # Agrega una anotación para calcular la duración solo si dateOut no es nulo
        queryset = queryset.annotate(
            duration=ExpressionWrapper(
                F("dateOut") - F("dateIn"), output_field=DurationField()
            )
        )

        # Filtra los registros con duración no nula
        queryset = queryset.exclude(duration=None)

        # Imprime los valores de duration en la queryset
        for log in queryset:
            print(f"Log ID: {log.id}, Duration: {log.duration}")

        average_duration_timedelta = queryset.aggregate(avg_duration=Avg("duration"))[
            "avg_duration"
        ]

        # Verifica si el resultado es None antes de realizar la conversión
        if average_duration_timedelta is not None:
            # Extrae los componentes de días, horas, minutos y segundos
            days = average_duration_timedelta.days
            seconds = average_duration_timedelta.seconds

            hours, remainder = divmod(seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            average_duration_str = f"{days} días"
        else:
            average_duration_str = "N/A"  # Si no hay resultados

        return Response({"average_duration": average_duration_str})


# View para la estadística de la taza de vencidos
class VencidoStatisticsView(generics.ListAPIView):
    serializer_class = VencidoStatisticsSerializer

    def get_queryset(self):
        current_year = datetime.datetime.now().year
        queryset = models.Log.objects.filter(dateIn__year=current_year)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        statistics = queryset.aggregate(
            total_logs=Count("id"),
            approved_logs=Sum(
                Case(When(status="AP", then=1), default=0, output_field=FloatField())
            ),
            expired_logs=Sum(
                Case(When(status="VEN", then=1), default=0, output_field=FloatField())
            ),
            tardio_logs=Sum(
                Case(When(status="TAR", then=1), default=0, output_field=FloatField())
            ),
        )

        # Calcula el porcentaje de registros vencidos
        total_logs = statistics["total_logs"]
        expired_logs = statistics["expired_logs"]
        print(total_logs)
        print(expired_logs)
        vencido_percentage = (
            ((expired_logs * 100) / total_logs) if total_logs > 0 else 0
        )

        # Agrega el porcentaje correcto al diccionario de estadísticas
        statistics["vencido_percentage"] = vencido_percentage

        serializer = self.get_serializer([statistics], many=True)
        return Response(serializer.data)


# View mandar mayores deudoreszz
class LenderVencidosStatisticsView(generics.ListAPIView):
    serializer_class = LenderVencidosStatisticsSerializer

    def get_queryset(self):
        current_year = datetime.datetime.now().year
        queryset = (
            models.Log.objects.filter(
                Q(status="VEN") | Q(status="TAR"), dateIn__year=current_year
            )
            .values("lender__username")
            .annotate(vencidos_count=Count("lender"))
            .order_by("-vencidos_count")
        )
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        lender_statistics = serializer.data if serializer.data else None
        return Response(lender_statistics)


class BoxMasLogsRotos(generics.ListAPIView):
    serializer_class = BoxMasLogsRotostSerializer

    def get_queryset(self):
        queryset = (
            models.Box.objects.filter(log__status="ROT")
            .annotate(total_productos_rotos=Sum("log__quantity"))
            .order_by("-total_productos_rotos")
        )

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": 'No hay boxes con logs con status "ROTO".'},
                status=status.HTTP_404_NOT_FOUND,
            )


@api_view(["GET"])
def elementos_por_categoria(request, category_id):
    pagination_class = CustomPagination()
    # pagination_class.page_size = 10  # Número de elementos por página

    # Obtener la categoría correspondiente o devolver un error 404 si no existe
    categoria = get_object_or_404(models.Category, name=category_id)

    # Obtener todos los elementos que pertenecen a la categoría
    elementos = models.Element.objects.filter(category=categoria)
    if elementos.exists():
        # Paginar los elementos
        paginated_elements = pagination_class.paginate_queryset(elementos, request)
    if elementos.exists():
        # Paginar los elementos
        paginated_elements = pagination_class.paginate_queryset(elementos, request)

        elementos_con_stock = []
        elementos_con_stock = []

        if paginated_elements is not None:
            for elemento in paginated_elements:
                element_id = elemento.id
        if paginated_elements is not None:
            for elemento in paginated_elements:
                element_id = elemento.id

                boxes = models.Box.objects.filter(element__id=element_id)
                box_ids = [box.id for box in boxes]
                boxes = models.Box.objects.filter(element__id=element_id)
                box_ids = [box.id for box in boxes]

                total_com = models.Log.objects.filter(
                    box__id__in=box_ids, status="COM"
                ).aggregate(total=Sum("quantity"))["total"]
                total_ped = models.Log.objects.filter(
                    box__id__in=box_ids, status="PED"
                ).aggregate(total=Sum("quantity"))["total"]
                total_rot = models.Log.objects.filter(
                    box__id__in=box_ids, status="ROT"
                ).aggregate(total=Sum("quantity"))["total"]
                total_ap = models.Log.objects.filter(
                    box__id__in=box_ids, status="AP"
                ).aggregate(total=Sum("quantity"))["total"]
                total_com = models.Log.objects.filter(
                    box__id__in=box_ids, status="COM"
                ).aggregate(total=Sum("quantity"))["total"]
                total_ped = models.Log.objects.filter(
                    box__id__in=box_ids, status="PED"
                ).aggregate(total=Sum("quantity"))["total"]
                total_rot = models.Log.objects.filter(
                    box__id__in=box_ids, status="ROT"
                ).aggregate(total=Sum("quantity"))["total"]
                total_ap = models.Log.objects.filter(
                    box__id__in=box_ids, status="AP"
                ).aggregate(total=Sum("quantity"))["total"]

                if total_com is None:
                    total_com = 0
                if total_ped is None:
                    total_ped = 0
                if total_ap is None:
                    total_ap = 0
                if total_rot is None:
                    total_rot = 0
                if total_com is None:
                    total_com = 0
                if total_ped is None:
                    total_ped = 0
                if total_ap is None:
                    total_ap = 0
                if total_rot is None:
                    total_rot = 0

                current_stock = total_com - total_ped - total_ap - total_rot
                current_stock = total_com - total_ped - total_ap - total_rot

                elemento_con_stock = {
                    "id": elemento.id,
                    "name": elemento.name,
                    "description": elemento.description,
                    "image": elemento.image,
                    "category": elemento.category,
                    "current_stock": current_stock,
                }
                elemento_con_stock = {
                    "id": elemento.id,
                    "name": elemento.name,
                    "description": elemento.description,
                    "image": elemento.image,
                    "category": elemento.category,
                    "current_stock": current_stock,
                }

                elementos_con_stock.append(elemento_con_stock)
                elementos_con_stock.append(elemento_con_stock)

        serializer = ElementEcommerceSerializer(elementos_con_stock, many=True)
        serializer = ElementEcommerceSerializer(elementos_con_stock, many=True)

        return pagination_class.get_paginated_response(serializer.data)
    else:
        # La categoría no tiene elementos, verificar si tiene categorías hijas con elementos
        categorias_hijas = categoria.child_categories.all()
        elementos_categorias_hijas = models.Element.objects.filter(
            category__in=categorias_hijas
        )

        if elementos_categorias_hijas.exists():
            # Devolver elementos de categorías hijas
            paginated_elements_hijas = pagination_class.paginate_queryset(
                elementos_categorias_hijas, request
            )

            elementos_con_stock_hijas = []

            if paginated_elements_hijas is not None:
                for elemento_hija in paginated_elements_hijas:
                    elemento_hija_id = elemento_hija.id

                    boxes = models.Box.objects.filter(element__id=elemento_hija_id)
                    box_ids = [box.id for box in boxes]

                    total_com = models.Log.objects.filter(
                        box__id__in=box_ids, status="COM"
                    ).aggregate(total=Sum("quantity"))["total"]
                    total_ped = models.Log.objects.filter(
                        box__id__in=box_ids, status="PED"
                    ).aggregate(total=Sum("quantity"))["total"]
                    total_rot = models.Log.objects.filter(
                        box__id__in=box_ids, status="ROT"
                    ).aggregate(total=Sum("quantity"))["total"]
                    total_ap = models.Log.objects.filter(
                        box__id__in=box_ids, status="AP"
                    ).aggregate(total=Sum("quantity"))["total"]

                    if total_com is None:
                        total_com = 0
                    if total_ped is None:
                        total_ped = 0
                    if total_ap is None:
                        total_ap = 0
                    if total_rot is None:
                        total_rot = 0

                    current_stock = total_com - total_ped - total_ap - total_rot

                    elemento_con_stock = {
                        "id": elemento_hija_id,
                        "name": elemento_hija.name,
                        "description": elemento_hija.description,
                        "image": elemento_hija.image,
                        "category": elemento_hija.category,
                        "current_stock": current_stock,
                    }

                    elementos_con_stock_hijas.append(elemento_con_stock)

                serializer_hijas = ElementEcommerceSerializer(
                    elementos_con_stock_hijas, many=True
                )
                return pagination_class.get_paginated_response(serializer_hijas.data)
        else:
            # La categoría no tiene elementos ni categorías hijas con elementos, devolver respuesta vacía
            return Response([])


from django.utils.dateparse import parse_datetime
from dateutil.parser import parse as dateparse
from pytz import timezone, utc


@api_view(["GET", "PUT"])
def CambioAprobado(request, user_id, date_in):
    if request.method == "GET":
        valid_statuses = [models.Log.Status.PEDIDO]
        queryset = models.Log.objects.filter(lender=user_id, status__in=valid_statuses)

        if queryset.exists():
            # Agrupar logs por fecha y hora de creación
            grouped_logs = defaultdict(list)

            for log in queryset:
                creation_date = (
                    log.dateIn.strftime("%Y-%m-%d %H:%M") if log.dateIn else None
                )
                log_data = LogSerializer(log).data
                log_data["dateIn"] = creation_date
                grouped_logs[creation_date].append(log_data)

            # Verificar si hay logs para la fecha proporcionada y cambiar su estado a APROBADO
            logs_to_approve = grouped_logs.get(date_in, [])

            if logs_to_approve:
                # Recopilar los IDs de los logs aprobados
                log_ids_to_approve = [log["id"] for log in logs_to_approve]

                # Obtener las instancias de los logs aprobados por sus IDs
                logs_instances_to_approve = models.Log.objects.filter(
                    id__in=log_ids_to_approve
                )

                # Aquí asumo que estás intentando serializar las instancias, no los datos serializados
                serializer = LogSerializer(logs_instances_to_approve, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    "No se encontraron logs para esta fecha y este usuario."
                )

        else:
            return Response(
                "No se encontraron logs para este usuario con status APROBADO o PEDIDO."
            )

    if request.method == "PUT":
        valid_statuses = [models.Log.Status.PEDIDO]
        queryset = models.Log.objects.filter(lender=user_id, status__in=valid_statuses)

        if queryset.exists():
            # Agrupar logs por fecha y hora de creación
            grouped_logs = defaultdict(list)

            for log in queryset:
                creation_date = (
                    log.dateIn.strftime("%Y-%m-%d %H:%M") if log.dateIn else None
                )
                log_data = LogSerializer(log).data
                log_data["dateIn"] = creation_date
                grouped_logs[creation_date].append(log_data)

            # Verificar si hay logs para la fecha proporcionada y cambiar su estado a APROBADO
            logs_to_approve = grouped_logs.get(date_in, [])
            print("creacion_date ", creation_date, "date_in ", date_in)
            if creation_date == date_in:
                # Recopilar los IDs de los logs aprobados
                log_ids_to_approve = [log["id"] for log in logs_to_approve]

                # Obtener las instancias de los logs aprobados por sus IDs
                logs_instances_to_approve = models.Log.objects.filter(
                    id__in=log_ids_to_approve
                )
                logs_instances_to_approve.update(status=models.Log.Status.APROBADO)

                # Aquí asumo que estás intentando serializar las instancias, no los datos serializados
                serializer = LogSerializer(logs_instances_to_approve, many=True)
                create_notification_aprobado(user_id, date_in)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    "No se encontraron logs para esta fecha y este usuario."
                )

        else:
            return Response(
                "No se encontraron logs para este usuario con status APROBADO o PEDIDO."
            )


@api_view(["GET", "PUT"])
def CambioDesaprobado(request, user_id, date_in):
    if request.method == "GET":
        valid_statuses = [models.Log.Status.PEDIDO]
        queryset = models.Log.objects.filter(lender=user_id, status__in=valid_statuses)

        if queryset.exists():
            # Agrupar logs por fecha y hora de creación
            grouped_logs = defaultdict(list)

            for log in queryset:
                creation_date = (
                    log.dateIn.strftime("%Y-%m-%d %H:%M") if log.dateIn else None
                )
                log_data = LogSerializer(log).data
                log_data["dateIn"] = creation_date
                grouped_logs[creation_date].append(log_data)

            # Verificar si hay logs para la fecha proporcionada y cambiar su estado a APROBADO
            logs_to_approve = grouped_logs.get(date_in, [])
            print("creacion_date ", creation_date, "date_in ", date_in)
            if creation_date == date_in:
                # Recopilar los IDs de los logs aprobados
                log_ids_to_approve = [log["id"] for log in logs_to_approve]

                # Obtener las instancias de los logs aprobados por sus IDs
                logs_instances_to_approve = models.Log.objects.filter(
                    id__in=log_ids_to_approve
                )

                # Aquí asumo que estás intentando serializar las instancias, no los datos serializados
                serializer = LogSerializer(logs_instances_to_approve, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    "No se encontraron logs para esta fecha y este usuario."
                )

        else:
            return Response(
                "No se encontraron logs para este usuario con status APROBADO o PEDIDO."
            )

    if request.method == "PUT":
        valid_statuses = [models.Log.Status.PEDIDO]
        queryset = models.Log.objects.filter(lender=user_id, status__in=valid_statuses)

        if queryset.exists():
            # Agrupar logs por fecha y hora de creación
            grouped_logs = defaultdict(list)

            for log in queryset:
                creation_date = (
                    log.dateIn.strftime("%Y-%m-%d %H:%M") if log.dateIn else None
                )
                log_data = LogSerializer(log).data
                log_data["dateIn"] = creation_date
                grouped_logs[creation_date].append(log_data)

            # Verificar si hay logs para la fecha proporcionada y cambiar su estado a APROBADO
            logs_to_approve = grouped_logs.get(date_in, [])
            print("creacion_date ", creation_date, "date_in ", date_in)
            if creation_date == date_in:
                # Recopilar los IDs de los logs aprobados
                log_ids_to_approve = [log["id"] for log in logs_to_approve]

                # Obtener las instancias de los logs aprobados por sus IDs
                logs_instances_to_approve = models.Log.objects.filter(
                    id__in=log_ids_to_approve
                )
                logs_instances_to_approve.update(status=models.Log.Status.DESAPROBADO)
                create_notification_desaprobado(user_id, date_in)
                # Aquí asumo que estás intentando serializar las instancias, no los datos serializados
                serializer = LogSerializer(logs_instances_to_approve, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    "No se encontraron logs para esta fecha y este usuario."
                )

        else:
            return Response(
                "No se encontraron logs para este usuario con status DESAPROBADO o PEDIDO."
            )


@api_view(["GET", "POST", "PUT"])
def notificacionesLeidasViewSet(request, user_id):
    if request.method == "GET":
        # Agregar código para manejar la solicitud GET si es necesario
        queryset = models.Notification.objects.filter(user_revoker=user_id)
        serializer = NotificationSerializer(queryset, many=True)
        return Response(serializer.data)

    if request.method == "PUT":
        # Agregar código para manejar la solicitud PUT
        notificaciones = models.Notification.objects.filter(
            user_revoker=user_id, status=models.Notification.NotificationStatus.UNREAD
        )
        new_status = models.Notification.NotificationStatus.READ
        for notificacion in notificaciones:
            notificacion.status = new_status
            notificacion.save()

        serializer = NotificationSerializer(notificaciones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET", "POST", "PUT"])
def CambioLog(request, user_id):
    if request.method == "GET":
        # Agregar código para manejar la solicitud GET si es necesario
        queryset = models.Log.objects.filter(
            lender=user_id, status=models.Log.Status.CARRITO
        )
        serializer = LogSerializer(queryset, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        # Obtener el usuario existente (puedes usar get_object_or_404 para manejar si no existe)
        user = get_object_or_404(models.CustomUser, id=user_id)

        # Verificar si ya existe un Log con el mismo "box" y estado "CARRITO"
        box = request.data.get("box")
        if models.Log.objects.filter(
            box=box, status=models.Log.Status.CARRITO
        ).exists():
            return Response(
                {"message": "Ya existe un Log con el mismo box en estado CARRITO"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Crear un nuevo registro Log asociado al usuario
        serializer = LogCambio(data=request.data)
        if serializer.is_valid():
            serializer.save(lender=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "PUT":
        # Agregar código para manejar la solicitud PUT
        logs_carrito = models.Log.objects.filter(
            lender=user_id, status=models.Log.Status.CARRITO
        )
        new_status = models.Log.Status.PEDIDO
        new_dateout = request.data.get("dateout", None)
        count = 0
        for log in logs_carrito:
            count += 1
            log.status = new_status
            if new_dateout is not None:
                log.dateOut = new_dateout
            log.save()
        serializer = LogSerializer(logs_carrito, many=True)
        create_notification_pedido(user_id, count)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
def NotificacionesAPIView(request, user_id):
    if request.method == "GET":
        queryset = models.Notification.objects.filter(user_revoker=user_id)
        notifications = queryset.all()

        # Formatear el timestamp en el formato deseado
        formatted_notifications = []
        for notification in notifications:
            notification.timestamp = notification.timestamp.strftime("%Y-%m-%d %H:%M")
            formatted_notifications.append(notification)

        serializer = NotificationSerializer(formatted_notifications, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        return Response({"message": "Notificaciones agregada"})

    return Response(status=405)


@api_view(["GET"])
def boxes_por_especialidad(request, nombre_especialidad):
    # Obtén la especialidad especificada en la URL
    especialidad = get_object_or_404(models.Speciality, name=nombre_especialidad)

    # Filtrar boxes por la especialidad y obtener los elementos dentro de cada box
    boxes = models.Box.objects.filter(
        location__laboratoy__speciality=especialidad
    ).prefetch_related("element")

    # Crear una lista de elementos en el formato deseado
    elementos_por_especialidad = []
    for box in boxes:
        elemento = {
            "id": box.element.id,
            "name": box.element.name,
            "description": box.element.description,
            "price_usd": box.element.price_usd,
            "image": None if not box.element.image else box.element.image.url,
            "ecommerce": box.element.ecommerce,
            "category": box.element.category.id if box.element.category else None,
        }
        elementos_por_especialidad.append(elemento)

    return Response(elementos_por_especialidad)


@api_view(["GET"])
def categories_por_especialidad(request, nombre_especialidad, date):
    # Obtén la especialidad especificada en la URL
    especialidad = get_object_or_404(models.Speciality, name=nombre_especialidad)

    # Filtrar cajas (boxes) por la especialidad y obtener las categorías únicas de los elementos
    categorias = models.Category.objects.filter(
        element__box__location__laboratoy__speciality=especialidad
    ).distinct()

    # Crear una lista de categorías en el formato deseado
    categorias_por_especialidad = []
    for categoria in categorias:
        categoria_info = {
            "id": categoria.id,
            "category": categoria.category.name if categoria.category else None,
            "name": categoria.name,
            "description": categoria.description,
            # Puedes agregar más campos de la categoría si es necesario
        }
        categorias_por_especialidad.append(categoria_info)

    return Response(categorias_por_especialidad)


@api_view(["GET", "POST", "DELETE", "PUT"])
def BudgetLogViewSet(request, budget_id):
    if request.method == "GET":
        try:
            # Obtiene todos los BudgetLog relacionados con el budget especificado
            queryset = models.BudgetLog.objects.filter(budget=budget_id)

            # Serializa los resultados incluyendo información del budget relacionado
            serializer = BudgetLogSerializer(
                queryset, many=True, context={"request": request}
            )

            # Construye la respuesta que incluye información del budget
            response_data = {
                "budget_id": budget_id,
                "budget_details": BudgetSerializer(
                    models.Budget.objects.get(id=budget_id)
                ).data,
                "budget_logs": serializer.data,
            }

            return Response(response_data)
        except models.Budget.DoesNotExist:
            return Response(
                {"message": "Presupuesto no encontrado"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except models.BudgetLog.DoesNotExist:
            return Response(
                {
                    "message": "No se encontraron registros de BudgetLog para este presupuesto"
                },
                status=status.HTTP_404_NOT_FOUND,
            )

    if request.method == "POST":
        return Response({"message": "Notificaciones agregada"})

    if request.method == "DELETE":
        try:
            print(request.data)

            queryset = models.BudgetLog.objects.get(id=budget_id)
            queryset.delete()
            return Response({"message": "Log eliminado"})
        except models.BudgetLog.DoesNotExist:
            return Response(
                {f"message": "Log no encontrado {request.log_id}"},
                status=status.HTTP_404_NOT_FOUND,
            )
    if request.method == "PUT":
        # Actualiza el estado del presupuesto a "COMPRADO".
        queryset = models.BudgetLog.objects.get(id=budget_id)
        serializer = BudgetLogSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data)
    return Response(status=405)


@api_view(["GET", "POST"])
def BudgetSpecialityViewSet(request, speciality_name):
    if request.method == "GET":
        queryset = models.Budget.objects.filter(speciality__name=speciality_name)

        serializer = BudgetSerializer(queryset, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        return Response({"message": "Notificaciones agregada"})

    return Response(status=405)

@api_view(["PUT"])
def update_budget_name(request, budget_id=None):
    try:
        # Obtén el presupuesto actual
        budget = models.Budget.objects.get(id=budget_id)

        # Actualiza el nombre del presupuesto
        new_name = request.data.get('name', '')
        budget.name = new_name
        budget.save()

        return Response({"message": f"Nombre del presupuesto actualizado a {new_name}"})
    except models.Budget.DoesNotExist:
        return Response({"error": "Presupuesto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

@api_view(["GET", "POST", "DELETE", "PUT"])
def BudgetViewSet(request, budget_id=None):
    if request.method == "GET":
        queryset = models.Budget.objects.all()

        serializer = BudgetSerializer(queryset, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        # Deserializa los datos de la solicitud POST
        serializer = BudgetSerializer2(data=request.data)

        # Verifica si los datos son válidos
        if serializer.is_valid():
            # Guarda el nuevo objeto Budget en la base de datos
            serializer.save()

            # Devuelve una respuesta con los datos del objeto creado
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Devuelve una respuesta con errores de validación si los datos no son válidos
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        # Check if the budget_id is provided
        if budget_id is not None:
            try:
                # Get the budget instance
                budget_instance = models.Budget.objects.get(id=budget_id)
                budget_instance.delete()  # Delete the budget instance

                return Response(
                    {"message": "Budget deleted successfully"},
                    status=status.HTTP_204_NO_CONTENT,
                )
            except models.Budget.DoesNotExist:
                return Response(
                    {"message": "Budget not found"}, status=status.HTTP_404_NOT_FOUND
                )

    if request.method == "PUT":
        try:
            # Obtén el presupuesto actual
            budget = models.Budget.objects.get(id=budget_id)

            # Serializa y valida los datos del presupuesto actualizado
            budget_serializer = BudgetSerializer(
                budget, data=request.data, partial=True
            )
            if not budget_serializer.is_valid():
                return Response(
                    budget_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

            # Guarda el presupuesto actualizado

            print(budget_serializer)
            budget_serializer.save()
            budget.status = "COMPLETADO"
            budget.save()
            # Obtiene todos los elementos asociados al presupuesto
            budget_logs = models.BudgetLog.objects.filter(budget=budget)

            # Itera sobre los elementos del presupuesto
            for budget_log in budget_logs:
                element = budget_log.element
                quantity = budget_log.quantity

                if element is None:
                    # Si el elemento es nulo, crea uno nuevo con el nombre del BudgetLog
                    new_element = models.Element.objects.create(name=budget_log.name)

                    # Actualiza el BudgetLog con el nuevo elemento creado
                    budget_log.element = new_element
                    budget_log.save()
                location_instance, _ = models.Location.objects.get_or_create(
                    name="Depósito"
                )
                # Verifica si el Box existe, si no, créalo
                box, created = models.Box.objects.get_or_create(
                    element=budget_log.element,
                    defaults={
                        "name": f"Caja para {budget_log.element.name}",
                        "minimumStock": 1,
                        "location": location_instance,
                    },
                )

                # Ahora, necesitas obtener la instancia de Location basándote en 'Depósito'
                # Aquí asumo que 'Depósito' es un nombre de ubicación que está en el modelo Location

                # Asigna la ubicación al Box
                box.location = location_instance
                box.save()

                # Crea un nuevo Log para el elemento y la cantidad correspondiente
                models.Log.objects.create(
                    status=models.Log.Status.COMPRADO,
                    quantity=quantity,
                    borrower=None,  # Puedes cambiar esto según tus necesidades
                    lender=None,  # Puedes cambiar esto según tus necesidades
                    box=box,
                    observation=f"Compra de {quantity} {budget_log.element.name} para el presupuesto {budget.name}",
                )

            return Response(budget_serializer.data)
        except models.Budget.DoesNotExist:
            return Response(
                {"error": "Presupuesto no encontrado"}, status=status.HTTP_404_NOT_FOUND
            )

    return Response(
        {"error": "Método no permitido"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
    )


def check_stock_sufficiency(element_id, new_quantity):
    boxes = models.Box.objects.filter(element__id=element_id)
    box_ids = [box.id for box in boxes]

    total_com = models.Log.objects.filter(box__id__in=box_ids, status="COM").aggregate(
        total=Sum("quantity")
    )["total"]
    total_ped = models.Log.objects.filter(box__id__in=box_ids, status="PED").aggregate(
        total=Sum("quantity")
    )["total"]
    total_rot = models.Log.objects.filter(box__id__in=box_ids, status="ROT").aggregate(
        total=Sum("quantity")
    )["total"]
    total_ap = models.Log.objects.filter(box__id__in=box_ids, status="AP").aggregate(
        total=Sum("quantity")
    )["total"]

    if total_com is None:
        total_com = 0
    if total_ped is None:
        total_ped = 0
    if total_ap is None:
        total_ap = 0
    if total_rot is None:
        total_rot = 0

    current_stock = total_com - total_ped - total_ap - total_rot

    return current_stock >= new_quantity


@api_view(["PUT"])
def update_log_quantity(request, log_id):
    try:
        # Buscar el registro Log por ID
        log = models.Log.objects.get(pk=log_id)

        if request.method == "PUT":
            # Obtener la nueva cantidad desde la solicitud
            new_quantity = request.data.get("quantity")
            new_observation = request.data.get("observation")

            # Verificar si hay suficiente stock antes de actualizar
            enough_stock = check_stock_sufficiency(log.box.element.id, new_quantity)

            if enough_stock:
                # Actualizar la cantidad del registro Log si hay suficiente stock
                log.quantity = new_quantity
                log.observation = new_observation
                log.save()

                # Devolver una respuesta exitosa
                return Response(
                    {"message": "Cantidad del registro actualizada correctamente"}
                )
            else:
                return Response(
                    {"message": "No hay suficiente stock disponible"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

    except models.Log.DoesNotExist:
        return Response(
            {"message": "El registro Log no existe"}, status=status.HTTP_404_NOT_FOUND
        )

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class BudgetLogCreateView(generics.CreateAPIView):
    queryset = models.BudgetLog.objects.all()
    serializer_class = BudgetLogCreateSerializer


@api_view(["GET", "PUT"])
def CambioDevuelto(request, user_id, date_in):
    if request.method == "GET":
        valid_statuses = [models.Log.Status.APROBADO, models.Log.Status.VENCIDO]
        queryset = models.Log.objects.filter(lender=user_id, status__in=valid_statuses)

        if queryset.exists():
            # Agrupar logs por fecha y hora de creación
            grouped_logs = defaultdict(list)

            for log in queryset:
                creation_date = (
                    log.dateIn.strftime("%Y-%m-%d %H:%M") if log.dateIn else None
                )
                log_data = LogSerializer(log).data
                log_data["dateIn"] = creation_date
                grouped_logs[creation_date].append(log_data)

            # Verificar si hay logs para la fecha proporcionada y cambiar su estado a APROBADO
            logs_to_approve = grouped_logs.get(date_in, [])
            print("creacion_date ", creation_date, "date_in ", date_in)
            if creation_date == date_in:
                # Recopilar los IDs de los logs aprobados
                log_ids_to_approve = [log["id"] for log in logs_to_approve]

                # Obtener las instancias de los logs aprobados por sus IDs
                logs_instances_to_approve = models.Log.objects.filter(
                    id__in=log_ids_to_approve
                )

                # Aquí asumo que estás intentando serializar las instancias, no los datos serializados
                serializer = LogSerializer(logs_instances_to_approve, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    "No se encontraron logs para esta fecha y este usuario."
                )

        else:
            return Response(
                "No se encontraron logs para este usuario con status APROBADO o PEDIDO."
            )
    if request.method == "PUT":
        valid_statuses = [models.Log.Status.APROBADO, models.Log.Status.VENCIDO]
        queryset = models.Log.objects.filter(lender=user_id, status__in=valid_statuses)

        if queryset.exists():
            # Agrupar logs por fecha y hora de creación
            grouped_logs = defaultdict(list)
            creation_date = None
            for log in queryset:
                creation_date = (
                    log.dateIn.strftime("%Y-%m-%d %H:%M") if log.dateIn else None
                )
                log_data = LogSerializer(log).data
                log_data["dateIn"] = creation_date
                grouped_logs[creation_date].append(log_data)

            # Verificar si hay logs para la fecha proporcionada y cambiar su estado a APROBADO o DEVUELTOTARDIO
            logs_to_approve = grouped_logs.get(date_in, [])
            # rint("creacion_date ", creation_date, "date_in ", date_in)
            logs_instances_to_approve = []
            logs_instances_to_return_late = []
            if creation_date == date_in:
                # Recopilar los IDs de los logs aprobados y vencidos
                log_ids_to_approve = [
                    log["id"]
                    for log in logs_to_approve
                    if log["status"] == models.Log.Status.APROBADO
                ]
                log_ids_to_return_late = [
                    log["id"]
                    for log in logs_to_approve
                    if log["status"] == models.Log.Status.VENCIDO
                ]

                # Obtener las instancias de los logs aprobados y vencidos por sus IDs y actualizar sus estados
                if log_ids_to_approve:
                    logs_instances_to_approve = models.Log.objects.filter(
                        id__in=log_ids_to_approve
                    )
                    logs_instances_to_approve.update(status=models.Log.Status.DEVUELTO)
                    statusDevolucionTardia = False
                    create_notification_devuelto(
                        user_id, date_in, statusDevolucionTardia
                    )
                if log_ids_to_return_late:
                    logs_instances_to_return_late = models.Log.objects.filter(
                        id__in=log_ids_to_return_late
                    )
                    logs_instances_to_return_late.update(
                        status=models.Log.Status.DEVUELTOTARDIO
                    )
                    statusDevolucionTardia = True
                    create_notification_devuelto(
                        user_id, date_in, statusDevolucionTardia
                    )

                # Aquí asumo que estás intentando serializar las instancias, no los datos serializados
                serializer_approve = LogSerializer(logs_instances_to_approve, many=True)
                serializer_return_late = LogSerializer(
                    logs_instances_to_return_late, many=True
                )

                return Response(
                    {
                        "logs_aprobados": serializer_approve.data,
                        "logs_devueltotardio": serializer_return_late.data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    "No se encontraron logs para esta fecha y este usuario."
                )
        else:
            return Response(
                "No se encontraron logs para este usuario con status APROBADO o VENCIDO."
            )


@api_view(["GET", "POST"])
def PendientesAPIView(request, user_id):
    if request.method == "GET":
        queryset = models.Log.objects.filter(
            lender=user_id, status=models.Log.Status.PEDIDO
        )
        serializer = LogSerializer(queryset, many=True)

        # Agrupar logs por fecha y hora de creación
        grouped_logs = defaultdict(list)
        for log in queryset:
            creation_date = log.dateIn.strftime(
                "%Y-%m-%dT%H:%M:%S.%f%z"
            )  # Formatear fecha y hora
            log_data = LogSerializer(log).data
            log_data[
                "dateIn"
            ] = creation_date  # Actualizar la clave 'dateIn' al string formateado
            grouped_logs[creation_date].append(log_data)

        return Response(grouped_logs)

    if request.method == "POST":
        return Response({"message": "Post completado"})

    return Response(status=405)


# A PARTIR DE ACA COSAS DE NOTIFICACIONES Y PRESTAMOS
# CambioAprobado
def create_notification_aprobado(user, date_in):
    notificacion = models.Notification.objects.create(
        user_sender=None,
        type_of_notification=models.Notification.NotificationType.APROBADO,
        message=f"Tu solicitud de préstamo con fecha {date_in} ha sido aprobada.",
    )
    notificacion.user_revoker.add(user)
    return notificacion


#


def create_notification_pedido(user_id, quantity):
    user = models.CustomUser.objects.get(id=user_id)
    profesor_group = Group.objects.get(name="Profesor")
    detalles_pedido = (
        f"Pedido Enviado de {user.username} :\n"
        f"Cantidad de Elementos: {quantity}\n"
        f"Observaciones"
    )

    notificacion = models.Notification.objects.create(
        user_sender=user,
        type_of_notification=models.Notification.NotificationType.PEDIDO,
        message=detalles_pedido,
    )
    profesor_group_users = get_user_model().objects.filter(groups=profesor_group)
    notificacion.user_revoker.add(*profesor_group_users)
    return notificacion


# CambioDesaprobado


def create_notification_desaprobado(user, date_in):
    notificacion = models.Notification.objects.create(
        user_sender=None,
        type_of_notification=models.Notification.NotificationType.DESAPROBADO,
        message=f"Tu solicitud de préstamo con fecha {date_in} ha sido desaprobada.",
    )
    notificacion.user_revoker.add(user)
    return notificacion


# CambioDevuelto
def create_notification_devuelto(user_id, dateIn, statusDevolucionTardia):
    user = models.CustomUser.objects.get(id=user_id)
    notificacion_prestador = models.Notification.objects.create(
        user_sender=None,
        type_of_notification=models.Notification.NotificationType.DEVUELTO,
        message=f"Tu préstamo de la fecha {dateIn} ha sido devuelto con exito.",
    )
    notificacion_prestador.user_revoker.add(user)

    profesor_group = Group.objects.get(name="Profesor")
    if statusDevolucionTardia:
        detalles_devuelto = (
            f"Se devolvio El prestamo de {user.username} pedido en la fecha {dateIn}:\n"
            "El pedido Se devolvio con demora"  # Descontar los dias para ver con cuantos dias de demora
        )
    else:
        detalles_devuelto = (
            f"Se devolvio El prestamo de {user.username} pedido en la fecha {dateIn}:\n"
            "El pedido se devolvio en tiempo y forma"  # Descontar los dias para ver con cuantos dias de demora
        )
    notificacion_profesores = models.Notification.objects.create(
        user_sender=user,
        type_of_notification=models.Notification.NotificationType.DEVUELTO,
        message=detalles_devuelto,
    )
    profesor_group_users = get_user_model().objects.filter(groups=profesor_group)
    notificacion_profesores.user_revoker.add(*profesor_group_users)
    return notificacion_profesores






@api_view(["GET"])
def FiltroStatusPrestamo(request, status, user_id=None):
    pagination_class = CustomPagination()

    if request.method == "GET":
        valid_statuses = [
            models.Log.Status.APROBADO,
            models.Log.Status.PEDIDO,
            models.Log.Status.DESAPROBADO,
            models.Log.Status.VENCIDO,
            models.Log.Status.DEVUELTOTARDIO,
            models.Log.Status.DEVUELTO,
        ]

        if status not in valid_statuses:
            return Response(f"El estado '{status}' no es válido.", status=400)
        if user_id:
            queryset = models.Log.objects.filter(lender=user_id, status=status).order_by("-dateIn")
        else:
            queryset = models.Log.objects.filter(status=status).order_by("-dateIn")

        if queryset.exists():
            # Agrupar logs por fecha y hora de creación
            grouped_logs = defaultdict(list)

            for log in queryset:
                creation_date = (
                    log.dateIn.strftime("%Y-%m-%dT%H:%M") if log.dateIn else None
                )
                log_data = LogSerializer(log).data
                log_data["dateIn"] = creation_date
                grouped_logs[creation_date].append(log_data)

            response_data = []

            for creation_date, logs_data in grouped_logs.items():
                primer_log = logs_data[0]
                primer_log_prueba = models.Log.objects.get(id=primer_log.get("id", ""))

                dateIn_primer_log_prueba = (
                    primer_log_prueba.dateIn.strftime("%Y-%m-%d %H:%M")
                    if primer_log_prueba.dateIn
                    else None
                )
                dateOut_primer_log = (
                    primer_log.get("dateOut", "") if primer_log else None
                )

                imagen_primer_log = None
                imagen_primer_log = obtener_imagen_primer_log(primer_log_prueba)
                imagen_combinada = None
                nombre_archivo = (
                    f"imagen_combinada_{creation_date}_{datetime.datetime.now}.jpg"
                )
                print("ACA ", logs_data)
                if imagen_primer_log:
                    imagenes_elementos = obtener_imagenes_elementos(logs_data)
                    imagenes_elementos_filtradas = [
                        imagen
                        for imagen in imagenes_elementos[:4]
                        if imagen is not None
                    ]
                    imagen_combinada = combinar_imagenes(
                        nombre_archivo, *imagenes_elementos_filtradas
                    )

                    primer_log["imagen_combinada"] = imagen_combinada

                count_logs = len(logs_data) if logs_data else 0

                response_data.append(
                    {
                        "dateOut": dateOut_primer_log,
                        "id_user": primer_log["borrower"]["id"]
                            if primer_log
                            else None,
                        "usuario": primer_log["borrower"]["username"]
                        if primer_log
                        else None,
                        "nombre": primer_log["borrower"]["first_name"]
                        if primer_log
                        else None,
                        "apellido": primer_log["borrower"]["last_name"]
                        if primer_log
                        else None,
                        "estado": primer_log["status"] if primer_log else None,
                        "dateIn": dateIn_primer_log_prueba,
                        "imagen": imagen_combinada,
                        "count": count_logs,
                        "lista": logs_data,
                    }
                )

            # Aplicar paginación
            paginated_response = pagination_class.paginate_queryset(
                response_data, request
            )
            return pagination_class.get_paginated_response(paginated_response)

        else:
            return Response("No se encontraron logs para este usuario.")


@api_view(["GET"])
def FiltroDatePrestamo(request):
    pagination_class = CustomPagination()

    if request.method == "GET":
        valid_statuses = [
            models.Log.Status.APROBADO,
            models.Log.Status.PEDIDO,
            models.Log.Status.DESAPROBADO,
            models.Log.Status.VENCIDO,
            models.Log.Status.DEVUELTOTARDIO,
        ]

        queryset = models.Log.objects.filter(
             status__in=valid_statuses
        ).order_by("dateIn")
            
        if queryset.exists():
            # Agrupar logs por fecha y hora de creación
            grouped_logs = defaultdict(list)

            for log in queryset:
                creation_date = (
                    log.dateIn.strftime("%Y-%m-%dT%H:%M") if log.dateIn else None
                )
                log_data = LogSerializer(log).data
                log_data["dateIn"] = creation_date
                grouped_logs[creation_date].append(log_data)

            response_data = []

            for creation_date, logs_data in grouped_logs.items():
                primer_log = logs_data[0]
                primer_log_prueba = models.Log.objects.get(id=primer_log.get("id", ""))

                dateIn_primer_log_prueba = (
                    primer_log_prueba.dateIn.strftime("%Y-%m-%d %H:%M")
                    if primer_log_prueba.dateIn
                    else None
                )
                dateOut_primer_log = (
                    primer_log.get("dateOut", "") if primer_log else None
                )

                imagen_primer_log = None
                imagen_primer_log = obtener_imagen_primer_log(primer_log_prueba)
                imagen_combinada = None
                nombre_archivo = (
                    f"imagen_combinada_{creation_date}_{datetime.datetime.now}.jpg"
                )
                print("ACA ", logs_data)
                if imagen_primer_log:
                    imagenes_elementos = obtener_imagenes_elementos(logs_data)
                    imagenes_elementos_filtradas = [
                        imagen
                        for imagen in imagenes_elementos[:4]
                        if imagen is not None
                    ]
                    imagen_combinada = combinar_imagenes(
                        nombre_archivo, *imagenes_elementos_filtradas
                    )

                    primer_log["imagen_combinada"] = imagen_combinada

                count_logs = len(logs_data) if logs_data else 0

                response_data.append(
                    {
                        "dateOut": dateOut_primer_log,
                        "id_user": primer_log["borrower"]["id"]
                            if primer_log
                            else None,
                        "usuario": primer_log["borrower"]["username"]
                        if primer_log
                        else None,
                        "nombre": primer_log["borrower"]["first_name"]
                        if primer_log
                        else None,
                        "apellido": primer_log["borrower"]["last_name"]
                        if primer_log
                        else None,
                        "estado": primer_log["status"] if primer_log else None,
                        "dateIn": dateIn_primer_log_prueba,
                        "imagen": imagen_combinada,
                        "count": count_logs,
                        "lista": logs_data,
                    }
                )

            # Aplicar paginación
            paginated_response = pagination_class.paginate_queryset(
                response_data, request
            )
            return pagination_class.get_paginated_response(paginated_response)

        else:
            return Response("No se encontraron logs para este usuario.")


@api_view(["GET"])
def FiltroComponentesPrestamo(request):
    pagination_class = CustomPagination()

    if request.method == "GET":
        valid_statuses = [
            models.Log.Status.APROBADO,
            models.Log.Status.PEDIDO,
            models.Log.Status.DESAPROBADO,
            models.Log.Status.VENCIDO,
            models.Log.Status.DEVUELTOTARDIO,
        ]

        queryset = models.Log.objects.filter(status__in=valid_statuses).order_by("-dateIn")

        if queryset.exists():
            # Agrupar logs por fecha y hora de creación
            grouped_logs = defaultdict(list)

            for log in queryset:
                creation_date = (
                    log.dateIn.strftime("%Y-%m-%dT%H:%M") if log.dateIn else None
                )
                log_data = LogSerializer(log).data
                log_data["dateIn"] = creation_date
                grouped_logs[creation_date].append(log_data)

            response_data = []

            for creation_date, logs_data in grouped_logs.items():
                primer_log = logs_data[0]
                primer_log_prueba = models.Log.objects.get(id=primer_log.get("id", ""))

                dateIn_primer_log_prueba = (
                    primer_log_prueba.dateIn.strftime("%Y-%m-%d %H:%M")
                    if primer_log_prueba.dateIn
                    else None
                )
                dateOut_primer_log = (
                    primer_log.get("dateOut", "") if primer_log else None
                )

                imagen_primer_log = None
                imagen_primer_log = obtener_imagen_primer_log(primer_log_prueba)
                imagen_combinada = None
                nombre_archivo = (
                    f"imagen_combinada_{creation_date}_{datetime.datetime.now}.jpg"
                )
                print("ACA ", logs_data)
                if imagen_primer_log:
                    imagenes_elementos = obtener_imagenes_elementos(logs_data)
                    imagenes_elementos_filtradas = [
                        imagen
                        for imagen in imagenes_elementos[:4]
                        if imagen is not None
                    ]
                    imagen_combinada = combinar_imagenes(
                        nombre_archivo, *imagenes_elementos_filtradas
                    )

                    primer_log["imagen_combinada"] = imagen_combinada

                count_logs = len(logs_data) if logs_data else 0

                response_data.append(
                    {
                        "dateOut": dateOut_primer_log,
                        "id_user": primer_log["borrower"]["id"]
                            if primer_log
                            else None,
                        "usuario": primer_log["borrower"]["username"]
                        if primer_log
                        else None,
                        "nombre": primer_log["borrower"]["first_name"]
                        if primer_log
                        else None,
                        "apellido": primer_log["borrower"]["last_name"]
                        if primer_log
                        else None,
                        "estado": primer_log["status"] if primer_log else None,
                        "dateIn": dateIn_primer_log_prueba,
                        "imagen": imagen_combinada,
                        "count": count_logs,
                        "lista": logs_data,
                    }
                )
            response_data = sorted(
                response_data, key=lambda x: x["count"], reverse=True
            )
            # Aplicar paginación
            paginated_response = pagination_class.paginate_queryset(
                response_data, request
            )
            return pagination_class.get_paginated_response(paginated_response)

        else:
            return Response("No se encontraron logs para este usuario.")


@api_view(["GET"])
def PrestamosSinPaginacion(request):
    if request.method == "GET":
        valid_statuses = [
            models.Log.Status.APROBADO,
            models.Log.Status.PEDIDO,
            models.Log.Status.DESAPROBADO,
            models.Log.Status.VENCIDO,
            models.Log.Status.DEVUELTOTARDIO,
        ]

        queryset = models.Log.objects.filter(status__in=valid_statuses).order_by("-dateIn")

        if queryset.exists():
            # Agrupar logs por fecha y hora de creación
            grouped_logs = defaultdict(list)

            for log in queryset:
                creation_date = (
                    log.dateIn.strftime("%Y-%m-%dT%H:%M") if log.dateIn else None
                )
                log_data = LogSerializer(log).data
                log_data["dateIn"] = creation_date
                grouped_logs[creation_date].append(log_data)

            response_data = []

            for creation_date, logs_data in grouped_logs.items():
                primer_log = logs_data[0]
                primer_log_prueba = models.Log.objects.get(id=primer_log.get("id", ""))

                dateIn_primer_log_prueba = (
                    primer_log_prueba.dateIn.strftime("%Y-%m-%d %H:%M")
                    if primer_log_prueba.dateIn
                    else None
                )
                dateOut_primer_log = (
                    primer_log.get("dateOut", "") if primer_log else None
                )

                imagen_primer_log = None
                imagen_primer_log = obtener_imagen_primer_log(primer_log_prueba)
                imagen_combinada = None
                nombre_archivo = (
                    f"imagen_combinada_{creation_date}_{datetime.datetime.now}.jpg"
                )
                print("ACA ", logs_data)
                if imagen_primer_log:
                    imagenes_elementos = obtener_imagenes_elementos(logs_data)
                    imagenes_elementos_filtradas = [
                        imagen
                        for imagen in imagenes_elementos[:4]
                        if imagen is not None
                    ]
                    imagen_combinada = combinar_imagenes(
                        nombre_archivo, *imagenes_elementos_filtradas
                    )

                    primer_log["imagen_combinada"] = imagen_combinada

                count_logs = len(logs_data) if logs_data else 0

                response_data.append(
                    {
                        "dateOut": dateOut_primer_log,
                        "id_user": primer_log["borrower"]["id"]
                            if primer_log
                            else None,
                        "usuario": primer_log["borrower"]["username"]
                        if primer_log
                        else None,
                        "nombre": primer_log["borrower"]["first_name"]
                        if primer_log
                        else None,
                        "apellido": primer_log["borrower"]["last_name"]
                        if primer_log
                        else None,
                        "estado": primer_log["status"] if primer_log else None,
                        "dateIn": dateIn_primer_log_prueba,
                        "imagen": imagen_combinada,
                        "count": count_logs,
                        "lista": logs_data,
                    }
                )

            return Response(response_data)

        else:
            return Response("No se encontraron logs para este usuario.")


@api_view(["GET", "POST"])
def BuscadorPrestamosAPIView(request, search):
    pagination_class = CustomPagination()

    if request.method == "GET":
        valid_statuses = [
            models.Log.Status.APROBADO,
            models.Log.Status.PEDIDO,
            models.Log.Status.DESAPROBADO,
            models.Log.Status.VENCIDO,
            models.Log.Status.DEVUELTO,
            models.Log.Status.DEVUELTOTARDIO,
        ]

        queryset = models.Log.objects.filter(status__in=valid_statuses).order_by("-dateIn")

        # Filtrar por término de búsqueda si se proporciona
        if search:
            queryset = queryset.filter(
                Q(borrower__username__icontains=search)
                | Q(borrower__first_name__icontains=search)
                | Q(borrower__last_name__icontains=search)
                | Q(status__icontains=search)
            )

        if queryset.exists():
            # Agrupar logs por fecha y hora de creación
            grouped_logs = defaultdict(list)

            for log in queryset:
                creation_date = (
                    log.dateIn.strftime("%Y-%m-%dT%H:%M") if log.dateIn else None
                )
                log_data = LogSerializer(log).data
                log_data["dateIn"] = creation_date
                grouped_logs[creation_date].append(log_data)

            response_data = []

            for creation_date, logs_data in grouped_logs.items():
                primer_log = logs_data[0]
                primer_log_prueba = models.Log.objects.get(id=primer_log.get("id", ""))

                dateIn_primer_log_prueba = (
                    primer_log_prueba.dateIn.strftime("%Y-%m-%d %H:%M")
                    if primer_log_prueba.dateIn
                    else None
                )
                dateOut_primer_log = (
                    primer_log.get("dateOut", "") if primer_log else None
                )

                imagen_primer_log = None
                imagen_primer_log = obtener_imagen_primer_log(primer_log_prueba)
                imagen_combinada = None
                nombre_archivo = (
                    f"imagen_combinada_{creation_date}_{datetime.datetime.now}.jpg"
                )
                print("ACA ", logs_data)
                if imagen_primer_log:
                    imagenes_elementos = obtener_imagenes_elementos(logs_data)
                    imagenes_elementos_filtradas = [
                        imagen
                        for imagen in imagenes_elementos[:4]
                        if imagen is not None
                    ]
                    imagen_combinada = combinar_imagenes(
                        nombre_archivo, *imagenes_elementos_filtradas
                    )

                    primer_log["imagen_combinada"] = imagen_combinada

                count_logs = len(logs_data) if logs_data else 0

                response_data.append(
                    {
                        "dateOut": dateOut_primer_log,
                        "id_user": primer_log["borrower"]["id"]
                            if primer_log
                            else None,
                        "usuario": primer_log["borrower"]["username"]
                        if primer_log
                        else None,
                        "nombre": primer_log["borrower"]["first_name"]
                        if primer_log
                        else None,
                        "apellido": primer_log["borrower"]["last_name"]
                        if primer_log
                        else None,
                        "estado": primer_log["status"] if primer_log else None,
                        "dateIn": dateIn_primer_log_prueba,
                        "imagen": imagen_combinada,
                        "count": count_logs,
                        "lista": logs_data,
                    }
                )

            # Aplicar paginación
            paginated_response = pagination_class.paginate_queryset(
                response_data, request
            )
            return pagination_class.get_paginated_response(paginated_response)

        else:
            return Response("No se encontraron logs para este usuario.")
