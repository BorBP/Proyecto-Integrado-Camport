from django.contrib import admin
from .models import User, Animal, Telemetria, Geocerca, Alerta, AlertaUsuario, Reporte

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'RUT', 'is_staff', 'fecha_nacimiento']
    search_fields = ['username', 'email', 'RUT']
    list_filter = ['is_staff', 'sexo']

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ['collar_id', 'display_id', 'tipo_animal', 'raza', 'edad', 'sexo', 'geocerca', 'agregado_por']
    search_fields = ['collar_id', 'display_id', 'raza']
    list_filter = ['tipo_animal', 'sexo', 'geocerca']

@admin.register(Telemetria)
class TelemetriaAdmin(admin.ModelAdmin):
    list_display = ['animal', 'timestamp', 'latitud', 'longitud', 'temperatura_corporal', 'frecuencia_cardiaca']
    list_filter = ['animal', 'timestamp']
    date_hierarchy = 'timestamp'

@admin.register(Geocerca)
class GeocercaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'creado_por', 'fecha_creacion', 'activa']
    list_filter = ['activa', 'fecha_creacion']

@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ['animal', 'tipo_alerta', 'timestamp', 'valor_registrado', 'resuelta', 'fecha_resolucion']
    list_filter = ['tipo_alerta', 'resuelta', 'timestamp']
    date_hierarchy = 'timestamp'
    search_fields = ['animal__collar_id', 'animal__display_id', 'mensaje']

@admin.register(AlertaUsuario)
class AlertaUsuarioAdmin(admin.ModelAdmin):
    list_display = ['alerta', 'usuario', 'leido', 'fecha_lectura', 'eliminada']
    list_filter = ['leido', 'usuario', 'eliminada']
    
@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ['id', 'alerta', 'generado_por', 'fecha_generacion', 'exportado', 'fecha_exportacion']
    list_filter = ['exportado', 'fecha_generacion', 'generado_por']
    date_hierarchy = 'fecha_generacion'
    search_fields = ['alerta__animal__collar_id', 'alerta__animal__display_id', 'observaciones']
