from rest_framework import serializers
from ElectroStockApp import models
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum


# Serializer para heredar de categorias
class CategoriaPadreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = "__all__"


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TokenSignup
        fields = ["id", "name"]


# Para ver y editar categorias
class CategoriaSerializer(serializers.ModelSerializer):
    category = CategoriaPadreSerializer()

    class Meta:
        model = models.Category
        fields = "__all__"


# Para ver y editar todos los elementos
class ElementSerializer(serializers.ModelSerializer):
    category = CategoriaSerializer()

    class Meta:
        model = models.Element
        fields = "__all__"


# Para todos los cursos
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = "__all__"


# Para todos los grupos
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Group
        fields = "__all__"


# Para ver y editar todos los datos del especialidad
class SpecialitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Speciality
        fields = "__all__"


# Para todos los usuarios
class UsersSerializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField(many=True)
    course = CourseSerializer()
    specialties = serializers.StringRelatedField(many=True)

    class Meta:
        model = models.CustomUser
        fields = "__all__"


# Solo para la previsualizacion de los elementos en el ecommerce
class ElementEcommerceSerializer(serializers.ModelSerializer):
    current_stock = serializers.IntegerField()

    class Meta:
        model = models.Element
        fields = ("id", "name", "description", "image", "category", "current_stock")
        read_only_fields = (
            "id",
            "name",
            "description",
            "image",
            "category",
            "current_stock",
        )
        queryset = models.Element.objects.filter(ecommerce=True)


# Para ver y editar todos los datos del laboratorio
class LaboratorySerializer(serializers.ModelSerializer):
    speciality = SpecialitySerializer()

    class Meta:
        model = models.Laboratory
        fields = "__all__"


# Para ver y editar todos los datos de la location
class LocationSerializer(serializers.ModelSerializer):
    laboratoy = LaboratorySerializer()

    class Meta:
        model = models.Location
        fields = "__all__"


# Serializer de los boxes completos
class BoxSerializer(serializers.ModelSerializer):
    element = ElementSerializer()
    location = LocationSerializer()

    class Meta:
        model = models.Box
        fields = "__all__"


class BoxSerializerPrueba(serializers.ModelSerializer):
    current_stock = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = models.Box
        fields = (
            "id",
            "element",
            "location",
            "minimumStock",
            "name",
            "responsable",
            "current_stock",
            "image",
        )

    def get_current_stock(self, instance):
        # Realiza el cálculo del current_stock para la instancia actual (instance)
        element_id = instance.id  # Id del elemento actual

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

        return current_stock

    def get_image(self, instance):
        try:
            element_id = instance.id
            element = models.Element.objects.get(id=element_id)
            if element.image:
                image_url = element.image.url
                return image_url
            return None
        except ObjectDoesNotExist:
            return None


# Serializer de  los prestamos completmos
class LogSerializer(serializers.ModelSerializer):
    box = BoxSerializerPrueba()
    borrower = UsersSerializer()
    lender = UsersSerializer()

    class Meta:
        model = models.Log
        fields = (
            "id",
            "box",
            "borrower",
            "lender",
            "status",
            "quantity",
            "observation",
            "dateIn",
            "dateOut",
        )


# Serializer de  los prestamos completmos
class LogCambio(serializers.ModelSerializer):
    class Meta:
        model = models.Log
        fields = (
            "id",
            "box",
            "borrower",
            "lender",
            "status",
            "quantity",
            "observation",
            "dateIn",
            "dateOut",
        )


# Se pasa el stock actual de los productos
class StockSerializer(serializers.Serializer):
    current_stock = serializers.IntegerField()

    class Meta:
        model = models.Log
        fields = "current_stock"


# Serializer para la estaditica del porcentaje de prestamos aprobados
class LogStatisticsSerializer(serializers.Serializer):
    total_logs = serializers.IntegerField()
    approved_logs = serializers.IntegerField()
    rejected_logs = serializers.IntegerField()
    approval_rate = serializers.SerializerMethodField()

    def get_approval_rate(self, obj):
        if obj["total_logs"] > 0:
            return (
                round(obj["approved_logs"] / obj["rejected_logs"] * 100, 2)
                if obj["rejected_logs"] != 0
                else 100
            )
        return 0


# Serializer para la estadistica para el mayor usuario que hace prestamos
class LenderStatisticsSerializer(serializers.Serializer):
    lender__username = serializers.CharField()
    total_lender_logs = serializers.IntegerField()

    class Meta:
        fields = ("lender__username", "total_lender_logs")


# Serializer para el usuario que mas aprueba prestamos
class BorrowerStatisticsSerializer(serializers.Serializer):
    borrower__username = serializers.CharField()
    total_borrower_logs = serializers.IntegerField()

    class Meta:
        fields = ("borrower__username", "total_borrower_logs")


# Serializer para la estadistica de los dias con mayor prestamos
class DateStatisticsSerializer(serializers.ModelSerializer):
    total_datein_logs = serializers.IntegerField()

    class Meta:
        model = models.Log  # Asigna el modelo correcto aquí
        fields = ("dateIn", "total_datein_logs")


# Serializer para la estadistica de la taza de vencidos
class VencidoStatisticsSerializer(serializers.Serializer):
    total_logs = serializers.IntegerField()
    approved_logs = serializers.IntegerField()
    expired_logs = serializers.IntegerField()
    tardio_logs = serializers.IntegerField()
    expired_rate = serializers.SerializerMethodField()
    vencido_percentage = serializers.FloatField()

    def get_expired_rate(self, obj):
        if obj["total_logs"] > 0:
            return (
                round(
                    (obj["approved_logs"] / (obj["expired_logs"] + obj["tardio_logs"]))
                    * 100
                    // 2
                )
                if obj["tardio_logs"] != 0 or obj["expired_logs"] != 0
                else 1
            )
        return 0


# Serializer estadistica deudor
class LenderVencidosStatisticsSerializer(serializers.Serializer):
    lender__username = serializers.CharField()
    vencidos_count = serializers.IntegerField()


class BudgetSerializer(serializers.ModelSerializer):
    speciality = SpecialitySerializer()

    class Meta:
        model = models.Budget
        fields = "__all__"


class BudgetSerializer2(serializers.ModelSerializer):
    speciality = serializers.PrimaryKeyRelatedField(
        queryset=models.Speciality.objects.all()
    )

    class Meta:
        model = models.Budget
        fields = "__all__"


class BudgetLogSerializer(serializers.ModelSerializer):
    element = ElementSerializer()
    budget = BudgetSerializer()

    class Meta:
        model = models.BudgetLog
        fields = "__all__"


class BudgetLogCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BudgetLog
        fields = "__all__"


class BoxMasLogsRotostSerializer(serializers.ModelSerializer):
    box_nombre = serializers.CharField(
        source="name"
    )  # Asociar el campo "name" del modelo con "box_nombre"
    cantidad_logs_rotos = serializers.IntegerField(
        source="total_productos_rotos"
    )  # Asociar el campo "num_logs_rotos" del modelo con "cantidad_logs_rotos"

    class Meta:
        model = models.Box
        fields = ("box_nombre", "cantidad_logs_rotos")


class ElementEcommerceSerializer2(serializers.ModelSerializer):
    class Meta:
        model = models.Element
        fields = ("id", "name", "description", "image", "category")

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Realiza el cálculo del current_stock en la vista
        element_id = instance.id  # Id del elemento
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

        # Agrega el campo current_stock al resultado
        data["current_stock"] = current_stock

        return data


class NotificationSerializer(serializers.ModelSerializer):
    user_sender = UsersSerializer()
    user_revoker = groups = serializers.StringRelatedField(many=True)

    class Meta:
        model = models.Notification
        fields = "__all__"


class OnlyPkLogSerializer(serializers.ModelSerializer):
    box_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Box.objects.all(), source="box", write_only=True
    )
    borrower_id = serializers.PrimaryKeyRelatedField(
        queryset=models.get_user_model().objects.all(),
        source="borrower",
        write_only=True,
    )
    lender_id = serializers.PrimaryKeyRelatedField(
        queryset=models.get_user_model().objects.all(), source="lender", write_only=True
    )

    class Meta:
        model = models.Log
        fields = (
            "id",
            "borrower",
            "lender",
            "status",
            "quantity",
            "observation",
            "dateIn",
            "dateOut",
            "box_id",  # Agrega los campos write_only
            "borrower_id",  # Agrega los campos write_only
            "lender_id",  # Agrega los campos write_only
        )
