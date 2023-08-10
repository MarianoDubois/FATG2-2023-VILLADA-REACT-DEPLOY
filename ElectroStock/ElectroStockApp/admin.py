from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin
from django.contrib.auth.admin import UserAdmin

# Register your models here.

admin.site.site_header = "Stock"
admin.site.index_title = "Stock"
admin.site.site_title = "Stock"


# Las clases pra importar y exportar
class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "description",
            "category",
        )
        export_order = (
            "id",
            "name",
            "description",
            "category",
        )


# Los filtros y busquedas
class CategoryAdmin(ImportExportActionModelAdmin):
    resource_classes = [CategoryResource]


class ElementAdmin(ImportExportActionModelAdmin):
    list_display = (
        'id',
        "name",
        "price_usd",
        "category",
        "ecommerce",
    )
    list_filter = (
        "category",
        "ecommerce",
    )
    search_fields = [
        "name",
        "price_usd",
        "category",
        "ecommerce",
    ]

class CustomUserAdmin(ImportExportActionModelAdmin, UserAdmin):
    list_display = (
        "username",
        "email",
        "course",
        "grupo",
        "especialidad",
    )

    def especialidad(self, obj):
        return ", ".join([specialty.name for specialty in obj.specialties.all()])

    def grupo(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])

    list_filter = (
        "groups",
        "course__grade",
        "specialties__name",
    )



class LaboratoryAdmin(ImportExportActionModelAdmin):
    list_display = ("name", "speciality")
    search_fields = [
        "name",
        "speciality",
    ]



class LogyAdmin(ImportExportActionModelAdmin):

    list_display = (
        "status",
        "quantity",
        "observation",
        "dateIn",
        "dateOut",
        "borrower",
        "lender",
        "box",
    )
    list_filter = ("status", "borrower__username", "dateIn", "dateOut")
    search_fields = [
        "status",
        "quantity",
        "observation",
        "dateIn",
        "dateOut",
        "borrower__username",
        "lender__username",
    ]


from django.contrib import admin


class BoxAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = (
        "name",
        "minimumStock",
        "responsable",
        "element",
        "location",
        "get_logs",
        "get_approved_element_count",
        "get_pendient",
        "current_stock",
    )
    list_filter = (
        "location",
        "responsable",
    )
    search_fields = [
        "get_responsable_username",
        "minimumStock",
        "name",
        "element",
        "location",
    ]

    def responsable(self, obj):
        return obj.responsable.username

    def get_logs(self, obj):
        approved_element_count = Log.objects.filter(box=obj, status="COM").aggregate(
            total=models.Sum("quantity")
        )["total"]
        return approved_element_count if approved_element_count is not None else 0

    get_logs.short_description = "Stock"

    def get_pendient(self, obj):
        approved_element_count = Log.objects.filter(box=obj, status="PED").aggregate(
            total=models.Sum("quantity")
        )["total"]
        return approved_element_count if approved_element_count is not None else 0

    get_pendient.short_description = "Pedidos"

    def get_approved_element_count(self, obj):
        approved_element_count = Log.objects.filter(box=obj, status="AP").aggregate(
            total=models.Sum("quantity")
        )["total"]
        return approved_element_count if approved_element_count is not None else 0

    get_approved_element_count.short_description = "Prestados"

    def current_stock(self, obj):
        total_com = Log.objects.filter(box=obj, status="COM").aggregate(
            total=models.Sum("quantity")
        )["total"]
        total_ar = Log.objects.filter(box=obj, status="AP").aggregate(
            total=models.Sum("quantity")
        )["total"]
        total_ped = Log.objects.filter(box=obj, status="PED").aggregate(
            total=models.Sum("quantity")
        )["total"]
        if total_com is None:
            total_com = 0
        if total_ar is None:
            total_ar = 0
        if total_ped is None:
            total_ped = 0

        current_stock = total_com - total_ar - total_ped
        return current_stock

    current_stock.short_description = "Stock Actual"


class CourseAdmin(ImportExportActionModelAdmin):
    pass


class LocationAdmin(ImportExportActionModelAdmin):
    list_display = ("name", "laboratoy")
    search_fields = [
        "name",
        "laboratoy",
    ]


# analizar cuales sirven y cuales no
admin.site.register(Element, ElementAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Laboratory, LaboratoryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Box, BoxAdmin)
admin.site.register(Log, LogyAdmin)
admin.site.register(Speciality)
