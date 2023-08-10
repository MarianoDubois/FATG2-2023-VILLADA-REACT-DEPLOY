from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, Group, Permission
from .especialidad import *

if not Group.objects.filter(name="Alumno").exists():
    alumno_group = Group.objects.create(name="Alumno")
    alumno_group.permissions.add()

if not Group.objects.filter(name="Profesor").exists():
    profesor_group = Group.objects.create(name="Profesor")
    profesor_group.permissions.add()


class Course(models.Model):
    grade = models.IntegerField()

    def __str__(self):
        return str(self.grade)

    class Meta:
        verbose_name_plural = "Cursos"
        verbose_name = "Curso"

class Speciality(models.Model): 
    name = models.CharField(max_length=40)
    def __str__(self):
        return self.name 

    class Meta:
        verbose_name_plural = "Especialidades"
        verbose_name = "Especialidad"
        
class CustomUser(AbstractUser, PermissionsMixin):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    specialties = models.ManyToManyField(Speciality, null=True, blank=True)

    # Se agrega related_name a la clave foránea de groups
    groups = models.ManyToManyField(
        Group, verbose_name=("groups"), blank=True, related_name="CustomUser"
    )

    # Se agrega related_name a la clave foránea de user_permissions
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=("user permissions"),
        blank=True,
        related_name="CustomUser",
    )


class Category(models.Model):  # ✅
    name = models.CharField(max_length=40,null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='child_categories',null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categorias"
        verbose_name = "Categoria"


class Element(models.Model):  
    name = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)
    price_usd = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, help_text='Ingrese el precio en dolares'
    )
    image = models.ImageField(upload_to="img-prod/", blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True, blank=True)
    ecommerce = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Elementos"
        verbose_name = "Elemento"

class Laboratory(models.Model):
    name = models.CharField(max_length=30)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Laboratorios"
        verbose_name = "Laboratorio"


class Location(models.Model):
    name = models.CharField(max_length=30)
    laboratoy = models.ForeignKey(Laboratory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Ubicaciones"
        verbose_name = "Ubicacion"


class Box(models.Model):
    responsable = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    minimumStock = models.IntegerField()
    name = models.CharField(max_length=30)
    element = models.ForeignKey(Element, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Boxes"
        verbose_name = "Box"
        


class Log(models.Model):
    class Status(models.TextChoices):
        APROBADO = "AP", "Aprobado"
        DESAPROBADO = "DAP", "Desaprobado"
        CARRITO = "CAR", "Carrito"
        PEDIDO = "PED", "Pedido"
        COMPRADO= 'COM', 'Comprado'
        DEVUELTO= 'DEV', 'Devuelto'

    status = models.CharField(
        max_length=30, choices=Status.choices, default=Status.DESAPROBADO
    )
    quantity = models.IntegerField()
    borrower = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='borrowed_logs', null=True, blank=True)
    lender = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='lender_logs', null=True, blank=True)
    box = models.ForeignKey(Box, on_delete=models.CASCADE)
    observation = models.CharField(max_length=100, null=True, blank=True)
    dateIn = models.DateTimeField(null=True)
    dateOut = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.status
    

    class Meta:
        verbose_name_plural = "Prestamos"
        verbose_name = "Prestamo"




