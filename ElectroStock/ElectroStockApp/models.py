# ElectroStockApp/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models.signals import post_save


# Creo el grupo alumno
if not Group.objects.filter(name="Alumno").exists():
    alumno_group = Group.objects.create(name="Alumno")
    alumno_group.permissions.add()

# Creo el grupo profesor
if not Group.objects.filter(name="Profesor").exists():
    profesor_group = Group.objects.create(name="Profesor")
    profesor_group.permissions.add()

if not Group.objects.filter(name="Jefe de area").exists():
    profesor_group = Group.objects.create(name="Jefe de area")
    profesor_group.permissions.add()

if not Group.objects.filter(name="Ayudante del Stock").exists():
    profesor_group = Group.objects.create(name="Ayudante del Stock")
    profesor_group.permissions.add()

if not Group.objects.filter(name="Ayudante del Presupuesto").exists():
    profesor_group = Group.objects.create(name="Ayudante del Presupuesto")
    profesor_group.permissions.add()


class Course(models.Model):
    grade = models.IntegerField(verbose_name="Año")

    def __str__(self):
        return str(self.grade)

    class Meta:
        verbose_name_plural = "Cursos"
        verbose_name = "Curso"


class Speciality(models.Model):
    name = models.CharField(max_length=40, verbose_name="Nombre")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Especialidades"
        verbose_name = "Especialidad"


class CustomUser(AbstractUser):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    specialties = models.ManyToManyField(Speciality, blank=True)

    groups = models.ManyToManyField(
        Group, verbose_name=("groups"), blank=True, related_name="custom_users"
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=("user permissions"),
        blank=True,
        related_name="custom_users",
    )

    def send_notification(
        self, type_of_notification, target_users=None, target_groups=None
    ):
        notification = Notification.objects.create(
            user_sender=self, type_of_notification=type_of_notification
        )

        if target_users:
            notification.user_revoker.add(*target_users)

        if target_groups:
            users_in_groups = (
                get_user_model().objects.filter(groups__in=target_groups).distinct()
            )
            notification.user_revoker.add(*users_in_groups)

        return notification


class Notification(models.Model):
    class NotificationType(models.TextChoices):
        HELLO = "HW", "Hello World"
        CUSTOM = "CS", "Custom"
        PEDIDO = "PD", "Pedido"
        APROBADO = "AP", "Aprobado"
        DESAPROBADO = "DP", "Desaprobado"
        DEVUELTO = "DV", "Devuelto"

    class NotificationStatus(models.TextChoices):
        UNREAD = "unread", "No leída"
        READ = "read", "Leída"

    user_sender = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        related_name="sent_notifications",
        on_delete=models.CASCADE,
    )
    user_revoker = models.ManyToManyField(
        get_user_model(),
        verbose_name=("destinatarios"),
        blank=True,
        related_name="notifications_revoked",
    )
    status = models.CharField(
        max_length=10,
        choices=NotificationStatus.choices,
        default=NotificationStatus.UNREAD,
        verbose_name="Estado",
    )
    type_of_notification = models.CharField(
        max_length=2,
        choices=NotificationType.choices,
        default=NotificationType.CUSTOM,
        verbose_name="Tipo de notificación",
    )
    message = models.TextField(null=True, blank=True, verbose_name="Mensaje")
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Notificaciones"
        verbose_name = "Notificación"

    def __str__(self):
        return self.message


class Category(models.Model):
    name = models.CharField(max_length=40, null=True, blank=True, verbose_name="Nombre")
    description = models.TextField(null=True, blank=True, verbose_name="Descripcion")
    category = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="child_categories",
        null=True,
        blank=True,
        verbose_name="Categoria",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categorias"
        verbose_name = "Categoria"


class Element(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nombre")
    description = models.TextField(null=True, blank=True, verbose_name="Descripcion")
    image = models.ImageField(upload_to="img-prod/", blank=True, verbose_name="Foto")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Categoria",
    )
    ecommerce = models.BooleanField(default=True, verbose_name="Prestable")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Elementos"
        verbose_name = "Elemento"


class Laboratory(models.Model):
    name = models.CharField(max_length=30, verbose_name="Nombre")
    speciality = models.ForeignKey(
        Speciality,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Especialidad",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Laboratorios"
        verbose_name = "Laboratorio"


class Location(models.Model):
    name = models.CharField(max_length=30, verbose_name="Nombre")
    laboratoy = models.ForeignKey(
        Laboratory, on_delete=models.CASCADE, verbose_name="Laboratorio"
    )

    def __str__(self):
        return self.name if self.name else f"Location {self.id}"

    class Meta:
        verbose_name_plural = "Ubicaciones"
        verbose_name = "Ubicacion"


class TokenSignup(models.Model):
    name = models.CharField(max_length=30, verbose_name="Nombre")
    name = models.CharField(max_length=30, verbose_name="Nombre")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Tokens"
        verbose_name = "Token"


class Box(models.Model):
    responsable = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True
    )
    minimumStock = models.IntegerField(verbose_name="Stock Minimo")
    name = models.CharField(max_length=255, verbose_name="Nombre")
    element = models.ForeignKey(
        Element, on_delete=models.CASCADE, verbose_name="Elemento"
    )
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, verbose_name="Ubicacion"
    )

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
        ]
        verbose_name_plural = "Boxes"
        verbose_name = "Box"


class Log(models.Model):
    class Status(models.TextChoices):
        APROBADO = "AP", "Aprobado"
        DESAPROBADO = "DAP", "Desaprobado"
        CARRITO = "CAR", "Carrito"
        PEDIDO = "PED", "Pedido"
        COMPRADO = "COM", "Comprado"
        DEVUELTO = "DEV", "Devuelto"
        VENCIDO = "VEN", "Vencido"
        DEVUELTOTARDIO = "TAR", "Tardio"
        ROTO = "ROT", "Roto"

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.COMPRADO,
        verbose_name="Estado",
    )
    quantity = models.IntegerField(verbose_name="Cantidad")
    borrower = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="borrowed_logs",
        help_text="Si se ingresa como comprado poner nombre de tu usuario",
        null=True,
        blank=True,
        verbose_name="Prestador/Comprador",
    )
    lender = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="lender_logs",
        null=True,
        blank=True,
        verbose_name="Prestatario",
    )
    box = models.ForeignKey(Box, on_delete=models.CASCADE)
    observation = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Observaciones"
    )
    dateIn = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de ingreso"
    )  # si este campo da error revisar en la init
    dateOut = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de devolucion",
        help_text="No es necesario si se carga como comprado",
    )

    def __str__(self):
        return self.status

    @property
    def is_pedido(self):
        return self.status == self.Status.PEDIDO

    @property
    def is_aprobado(self):
        return self.status == self.Status.APROBADO

    @property
    def is_desaprobado(self):
        return self.status == self.Status.DESAPROBADO

    @property
    def is_devuelto(self):
        return self.status == self.Status.DEVUELTO

    # Conecta el método a la señal post_save del modelo Log

    class Meta:
        indexes = [
            models.Index(fields=["quantity", "status", "box"]),
        ]
        verbose_name_plural = "Prestamos y movimientos"
        verbose_name = "Prestamo y movimientos"


"""def create_notification_on_aprobado(sender, instance, **kwargs):
    print("Entering create_notification_on_aprobado")
    if instance.is_aprobado:
        print("HAY UN APROBADO!")
        # Crea y envía la notificación al usuario prestador
        notificacion = Notification.objects.create(
            user_sender=None,  # Sin remitente
            type_of_notification=Notification.NotificationType.APROBADO,
            message=f"Tu solicitud de préstamo ha sido aprobada: {instance.box.name}",
        )
        notificacion.user_revoker.add(instance.borrower)
    else:
        print("No es un APROBADO")


# ... (similar modifications for other signal functions)


def create_notification_on_pedido(sender, instance, **kwargs):
    if instance.is_pedido:
        # Obtén el grupo "Profesor"
        profesor_group = Group.objects.get(name="Profesor")

        # Crea y envía la notificación a todos los usuarios del grupo "Profesor"
        detalles_pedido = (
            f"Detalles del pedido:\n"
            f"Elemento: {instance.box.name}\n"
            f"Cantidad: {instance.quantity}\n"
            f"Observaciones: {instance.observation}"
        )

        notificacion = Notification.objects.create(
            user_sender=instance.borrower,  # Sin remitente
            type_of_notification=Notification.NotificationType.PEDIDO,
            message=detalles_pedido,
        )
        profesor_group_users = get_user_model().objects.filter(groups=profesor_group)
        notificacion.user_revoker.add(*profesor_group_users)


def create_notification_on_desaprobado(sender, instance, **kwargs):
    if instance.is_desaprobado:
        # Crea y envía la notificación al usuario prestador
        notificacion = Notification.objects.create(
            user_sender=None,  # Sin remitente
            type_of_notification=Notification.NotificationType.DESAPROBADO,
            message=f"Tu solicitud de préstamo ha sido desaprobada: {instance.box.name}",
        )
        notificacion.user_revoker.add(instance.borrower)


def create_notification_on_devuelto(sender, instance, **kwargs):
    if instance.is_devuelto:
        # Crea y envía la notificación al usuario prestador
        notificacion_prestador = Notification.objects.create(
            user_sender=None,  # Sin remitente
            type_of_notification=Notification.NotificationType.DEVUELTO,
            message=f"Tu préstamo ha sido devuelto: {instance.box.name}",
        )
        notificacion_prestador.user_revoker.add(instance.borrower)

        # Obtén el grupo "Profesor"
        profesor_group = Group.objects.get(name="Profesor")

        # Crea y envía la notificación a todos los usuarios del grupo "Profesor"
        detalles_devuelto = (
            f"Detalles del préstamo devuelto:\n"
            f"Elemento: {instance.box.name}\n"
            f"Cantidad: {instance.quantity}\n"
            f"Observaciones: {instance.observation}"
        )

        notificacion_profesores = Notification.objects.create(
            user_sender=None,  # Sin remitente
            type_of_notification=Notification.NotificationType.DEVUELTO,
            message=detalles_devuelto,
        )
        profesor_group_users = get_user_model().objects.filter(groups=profesor_group)
        notificacion_profesores.user_revoker.add(*profesor_group_users)


post_save.connect(create_notification_on_devuelto, sender=Log)
post_save.connect(create_notification_on_aprobado, sender=Log)
post_save.connect(create_notification_on_desaprobado, sender=Log)
post_save.connect(create_notification_on_pedido, sender=Log)

"""


class Budget(models.Model):
    class Status(models.TextChoices):
        COMPLETADO = "COMPLETADO", "Completado"
        PROGRESO = "PROGRESO", "Progreso"

    name = models.CharField(max_length=30, verbose_name="Nombre")
    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.PROGRESO,
        verbose_name="Estado",
    )
    speciality = models.ForeignKey(
        Speciality,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Especialidad",
    )

    class Meta:
        verbose_name_plural = "Presupuesto"
        verbose_name = "Presupuesto"


class BudgetLog(models.Model):
    class Status(models.TextChoices):
        COMPRADO = "COMPRADO", "Comprado"
        PENDIENTE = "PENDIENTE", "Pendiente"

    name = models.CharField(
        max_length=255, verbose_name="Nombre", null=True, blank=True
    )
    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.PENDIENTE,
        verbose_name="Estado",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Ingrese el precio en pesos",
        verbose_name="Precio",
    )
    element = models.ForeignKey(
        Element,
        on_delete=models.CASCADE,
        verbose_name="Elemento",
        null=True,
        blank=True,
    )
    budget = models.ForeignKey(
        Budget, on_delete=models.CASCADE, verbose_name="Presupuesto"
    )
    quantity = models.IntegerField(verbose_name="Cantidad")

    class Meta:
        verbose_name_plural = "Prestamos y movimientos del presupuesto"
        verbose_name = "Prestamos y movimientos del presupuesto"
