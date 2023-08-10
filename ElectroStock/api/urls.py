from django.urls import path
from .views import *
from rest_framework import routers



router = routers.DefaultRouter()

#Registro todas las urls
router.register("elements", ElementsViewSet, "elements")
router.register("elementsEcommerce", ProductosEcommerceAPIView, "elementsEcommerce")
router.register("category", CategoriaViewSet, "category")
router.register('users', UsersViewSet, 'users')
router.register('course', CourseViewSet, 'course')
router.register('laboratory', LaboratorioViewSet, 'laboratory')
router.register('location', LocationViewSet, 'location')
router.register('box', BoxViewSet, 'box')
router.register('prestamos', PrestamoVerAPIView, 'prestamos')
router.register('especialidad', SpecialityViewSet, 'especialidad')

urlpatterns= [
     path("stock/<int:element_id>/", get_stock, name="stock"),
] + router.urls



