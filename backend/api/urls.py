from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (UserViewSet, AnimalViewSet, TelemetriaViewSet,
                    GeocercaViewSet, AlertaViewSet, AlertaUsuarioViewSet, ReporteViewSet, simulate_emergency)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'animales', AnimalViewSet)
router.register(r'telemetria', TelemetriaViewSet)
router.register(r'geocercas', GeocercaViewSet)
router.register(r'alertas', AlertaViewSet)
router.register(r'alertas-usuario', AlertaUsuarioViewSet, basename='alerta-usuario')
router.register(r'reportes', ReporteViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('simulate_emergency/<str:collar_id>/<str:emergency_type>/', simulate_emergency, name='simulate_emergency'),
]
