from django.urls import path, include, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from tasks import views
from .views import (
    RegistrarInicioFinMantenimientoView, 
    RegistrarInicioFinActividadView, 
    ObservacionMantenimientoView, 
    ObservacionActividadView,
    ObservacionDetailView,
    login,
    register,

)
from django.conf import settings
from django.conf.urls.static import static

# Crea una instancia de DefaultRouter
router = DefaultRouter()

# Registra las rutas
router.register(r'mantenimiento', views.MantenimientoViewSet, basename='mantenimiento')
router.register(r'actividad', views.ActividadViewSet, basename='actividad')
# Define urlpatterns
urlpatterns = [
    path('api/v1/', include(router.urls)),  # Incluye las rutas del DefaultRouter
    path('api/v1/mantenimientos/cargar/', 
         views.CargarMantenimientosView.as_view(), 
         name='cargar_mantenimientos'),
    
    # Rutas para mantenimientos
    path('api/v1/mantenimientos/<int:mantenimiento_id>/inicio-fin/', 
         RegistrarInicioFinMantenimientoView.as_view(), 
         name='registrar_inicio_fin_mantenimiento'),
    
    # Rutas para actividades
    path('api/v1/actividades/<int:actividad_id>/inicio-fin/', 
         RegistrarInicioFinActividadView.as_view(), 
         name='registrar_inicio_fin_actividad'),

    path('api/v1/actividades/crear/', 
         views.CrearActividadesView.as_view(), 
         name='crear_actividades'),
     
    # Rutas para observaciones
    path('api/v1/mantenimientos/<int:mantenimiento_id>/observaciones/', 
         ObservacionMantenimientoView.as_view(), 
         name='observaciones_mantenimiento'),
    path('api/v1/actividades/<int:actividad_id>/observaciones/', 
         ObservacionActividadView.as_view(), 
         name='agregar_observacion_actividad'),  # Ruta para agregar observaciones
    path('api/v1/actividades/<int:actividad_id>/observaciones/<int:observacion_id>/', 
         ObservacionActividadView.as_view(), 
         name='editar_observacion_actividad'),  # Ruta para editar observaciones
    path('api/v1/observaciones/<int:observacion_id>/', 
         ObservacionDetailView.as_view(), 
         name='editar_observacion'),
     re_path('login', views.login),
     re_path('register', views.register),
     

]

# Configuración para archivos media en modo debug
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)