from django.urls import path
from .views import *
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token


router = routers.DefaultRouter()

# Registro todas las urls
router.register("elements", ElementsViewSet, "elements")
router.register("elementsEcommerce", ProductosEcommerceAPIView, "elementsEcommerce")
router.register(
    "ecommercePaginacion", ecommercePaginacionAPIView, "ecommercePaginacion"
)
router.register(
    "ecommercePaginacion", ecommercePaginacionAPIView, "ecommercePaginacion"
)
router.register("category", CategoriaViewSet, "category")
router.register("users", UsersViewSet, "users")
router.register("course", CourseViewSet, "course")
router.register("laboratory", LaboratorioViewSet, "laboratory")
router.register("location", LocationViewSet, "location")
router.register("box", BoxViewSet, "box")
router.register("especialidad", SpecialityViewSet, "especialidad")
router.register("token", TokenViewSet, "token")
router.register("log", LogViewSet, "log")
# router.register("notification", NotificationViewSet, "notification")


urlpatterns = [
    path(
        "elementos_por_especialidad/<str:nombre_especialidad>/",
        boxes_por_especialidad,
        name="elementos_por_especialidad",
    ),
    path(
        "categories_por_especialidad/<str:nombre_especialidad>/",
        categories_por_especialidad,
        name="categories_por_especialidad",
    ),
    path(
        "elementos_por_especialidad/<str:nombre_especialidad>/",
        boxes_por_especialidad,
        name="elementos_por_especialidad",
    ),
    path(
        "categories_por_especialidad/<str:nombre_especialidad>/",
        categories_por_especialidad,
        name="categories_por_especialidad",
    ),
    path("logPost/<int:user_id>/", CambioLog, name="logPost"),
    path(
        "notificacionesLeidas/<int:user_id>/",
        notificacionesLeidasViewSet,
        name="notificacionesLeidas",
    ),
    path("usersFiltro/<str:name>/", UsersFiltros, name="users"),
    path(
        "desaprobadoPost/<int:user_id>/<str:date_in>/",
        CambioDesaprobado,
        name="desaprobado",
    ),
    path("aprobadoPost/<int:user_id>/<str:date_in>/", CambioAprobado, name="aprobado"),
    path("devueltoPost/<int:user_id>/<str:date_in>/", CambioDevuelto, name="devuelto"),
    path("budgetlog/<int:budget_id>/", BudgetLogViewSet, name="budgetlog"),
    path("budgetlog/create/", BudgetLogCreateView.as_view(), name="create-budget-log"),
    path("budgetlog/create/", BudgetLogCreateView.as_view(), name="create-budget-log"),
    path("budget/", BudgetViewSet, name="budgetList"),
    path("budget/<int:budget_id>/update_name/", update_budget_name),
    path("cantCarrito/<int:user_id>/", cantCarrito, name="cantCarrito"),
    path(
        "cantNotificaciones/<int:user_id>/",
        cantNotificaciones,
        name="cantNotificaciones",
    ),
    path(
        "cantNotificaciones/<int:user_id>/",
        cantNotificaciones,
        name="cantNotificaciones",
    ),
    path("budget/<int:budget_id>/", BudgetViewSet, name="budgetDetail"),
    path(
        "budgetSpeciality/<str:speciality_name>/",
        BudgetSpecialityViewSet,
        name="budgetSpeciality",
    ),
    path(
        "budgetSpeciality/<str:speciality_name>/",
        BudgetSpecialityViewSet,
        name="budgetSpeciality",
    ),
    path("carrito/<int:user_id>/", carrito, name="carrito"),
    path("vencidos/<int:user_id>/", VencidosAPIView, name="vencidos"),
    path("pendientes/<int:user_id>/", PendientesAPIView, name="pendientes"),
    path(
        "presatmosActuales/<int:user_id>/",
        PrestamosActualesView,
        name="prestamosActuales",
    ),
    path(
        "prestamosHistorial/<int:user_id>/",
        PrestamoVerAPIView,
        name="prestamosHistorial",
    ),
    path("stock/<int:element_id>/", get_stock, name="stock"),
    path("allPrestamos/", AllPrestamos, name="allPrestamos"),
    path(
        "filtroCategoria/<str:category_id>/",
        elementos_por_categoria,
        name="filtroCategoria",
    ),
    path(
        "filtroStatusPrestamos/<str:status>/<int:user_id>/",
        FiltroStatusPrestamo,
        name="FiltroPrestamosStatus",
    ),
    path(
        "filtroStatusPrestamos/<str:status>/",
        FiltroStatusPrestamo,
        name="FiltroPrestamosStatusSinUserID",
    ),
    path("filtroDatePrestamos", FiltroDatePrestamo, name="FiltroPrestamosDate"),
    path(
        "PrestamosAgrupadosSinPaginacion",
        PrestamosSinPaginacion,
        name="FiltroPrestamosDate",
    ),
    path(
        "filtroComponentesPrestamos",
        FiltroComponentesPrestamo,
        name="FiltroPrestamosComponentes",
    ),
    path("pendientes/<int:user_id>/", PrestamoPendientesAPIView, name="pendientes"),
    path("logCantidad/<int:log_id>/", update_log_quantity, name="logCantidad"),
    path("notificaciones/<int:user_id>/", NotificacionesAPIView, name="notificaciones"),
    path(
        "buscadorPrestamo/<str:search>/",
        BuscadorPrestamosAPIView,
        name="buscadorPrestamo",
    ),
    path(
        "estadisticas/maspedido/",
        MostRequestedElementView.as_view(),
        name="most_requested_element",
    ),
    path("estadisticas/aprobado/", LogStatisticsView.as_view(), name="aprobado"),
    path("estadisticas/lender/", LenderStatisticsView.as_view(), name="lender"),
    path("estadisticas/borrower/", BorrowerStatisticsView.as_view(), name="borrower"),
    path("estadisticas/date/", DateStatisticsView.as_view(), name="date"),
    path("estadisticas/vencidos/", VencidoStatisticsView.as_view(), name="vencido"),
    path(
        "estadisticas/mayordeudor/",
        LenderVencidosStatisticsView.as_view(),
        name="mayordeudor",
    ),
    path(
        "estadisticas/box_mas_logs_rotos/",
        BoxMasLogsRotos.as_view(),
        name="box_mas_logs_rotos",
    ),
    path("estadisticas/avgDate/", DateAvgView.as_view(), name="avg/date"),
] + router.urls
