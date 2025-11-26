from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import User, Animal, Telemetria, Geocerca, Alerta, AlertaUsuario, Reporte
from .serializers import (UserSerializer, AnimalSerializer, TelemetriaSerializer,
                          GeocercaSerializer, AlertaSerializer, AlertaUsuarioSerializer, ReporteSerializer)
import csv
import io

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Optimizar consultas usando prefetch_related para evitar N+1 queries
        return Animal.objects.prefetch_related('telemetria').all()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(agregado_por=self.request.user)

    @action(detail=True, methods=['get'])
    def telemetria_reciente(self, request, pk=None):
        animal = self.get_object()
        telemetria = animal.telemetria.first()
        if telemetria:
            serializer = TelemetriaSerializer(telemetria)
            return Response(serializer.data)
        return Response({'detail': 'No hay datos de telemetría'}, status=status.HTTP_404_NOT_FOUND)

class TelemetriaViewSet(viewsets.ModelViewSet):
    queryset = Telemetria.objects.all()
    serializer_class = TelemetriaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Telemetria.objects.all()
        animal_id = self.request.query_params.get('animal', None)
        if animal_id:
            queryset = queryset.filter(animal_id=animal_id)
        return queryset

class GeocercaViewSet(viewsets.ModelViewSet):
    queryset = Geocerca.objects.all()
    serializer_class = GeocercaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retornar todas las geocercas, con opción de filtrar por activa
        queryset = Geocerca.objects.all()
        activa = self.request.query_params.get('activa', None)
        if activa is not None:
            queryset = queryset.filter(activa=activa.lower() == 'true')
        return queryset

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(creado_por=self.request.user)

    @action(detail=False, methods=['get'])
    def activa(self, request):
        geocerca = Geocerca.objects.filter(activa=True).first()
        if geocerca:
            serializer = self.get_serializer(geocerca)
            return Response(serializer.data)
        return Response({'detail': 'No hay geocerca activa'}, status=status.HTTP_404_NOT_FOUND)

class AlertaViewSet(viewsets.ModelViewSet):
    queryset = Alerta.objects.all()
    serializer_class = AlertaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Alerta.objects.all()
        resuelta = self.request.query_params.get('resuelta', None)
        if resuelta is not None:
            queryset = queryset.filter(resuelta=resuelta.lower() == 'true')
        return queryset
    
    @action(detail=True, methods=['post'])
    def resolver(self, request, pk=None):
        """Marca una alerta como resuelta y la mueve a reportes"""
        alerta = self.get_object()
        alerta.resuelta = True
        alerta.fecha_resolucion = timezone.now()
        alerta.save()
        
        # Crear reporte si no existe
        if not hasattr(alerta, 'reporte'):
            Reporte.objects.create(
                alerta=alerta,
                generado_por=request.user,
                observaciones=request.data.get('observaciones', '')
            )
        
        serializer = self.get_serializer(alerta)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def activas(self, request):
        """Obtiene solo las alertas activas (no resueltas)"""
        alertas = self.get_queryset().filter(resuelta=False)
        serializer = self.get_serializer(alertas, many=True)
        return Response(serializer.data)

class AlertaUsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = AlertaUsuarioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AlertaUsuario.objects.filter(usuario=self.request.user, eliminada=False)

    @action(detail=True, methods=['post'])
    def marcar_leido(self, request, pk=None):
        alerta_usuario = self.get_object()
        alerta_usuario.leido = True
        alerta_usuario.fecha_lectura = timezone.now()
        alerta_usuario.save()
        serializer = self.get_serializer(alerta_usuario)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def no_leidas(self, request):
        no_leidas = self.get_queryset().filter(leido=False)
        serializer = self.get_serializer(no_leidas, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def eliminar(self, request, pk=None):
        """Elimina una alerta (marca como eliminada sin borrar el registro)"""
        alerta_usuario = self.get_object()
        alerta_usuario.eliminada = True
        alerta_usuario.save()
        return Response({'status': 'Alerta eliminada'})
    
    @action(detail=True, methods=['post'])
    def resolver_y_reportar(self, request, pk=None):
        """Marca la alerta como leída, resuelta y la mueve a reportes"""
        alerta_usuario = self.get_object()
        alerta_usuario.leido = True
        alerta_usuario.fecha_lectura = timezone.now()
        alerta_usuario.save()
        
        # Resolver la alerta
        alerta = alerta_usuario.alerta
        alerta.resuelta = True
        alerta.fecha_resolucion = timezone.now()
        alerta.save()
        
        # Crear reporte si no existe
        if not hasattr(alerta, 'reporte'):
            Reporte.objects.create(
                alerta=alerta,
                generado_por=request.user,
                observaciones=request.data.get('observaciones', '')
            )
        
        return Response({'status': 'Alerta resuelta y enviada a reportes'})

class ReporteViewSet(viewsets.ModelViewSet):
    serializer_class = ReporteSerializer
    permission_classes = [IsAuthenticated]
    queryset = Reporte.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(generado_por=self.request.user)
    
    @action(detail=False, methods=['get'])
    def exportar_csv(self, request):
        """Exporta todos los reportes en formato CSV"""
        reportes = Reporte.objects.all().select_related('alerta', 'alerta__animal', 'generado_por')
        
        # Crear archivo CSV en memoria con encoding UTF-8
        output = io.StringIO()
        # Agregar BOM para que Excel reconozca UTF-8
        output.write('\ufeff')
        # Usar punto y coma como delimitador para Excel
        writer = csv.writer(output, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        
        # Encabezados
        writer.writerow([
            'ID Reporte',
            'Collar ID',
            'Display ID',
            'Tipo Animal',
            'Tipo Alerta',
            'Mensaje',
            'Valor Registrado',
            'Fecha Alerta',
            'Fecha Resolución',
            'Fecha Generación',
            'Generado Por',
            'Observaciones',
            'Exportado'
        ])
        
        # Datos
        for reporte in reportes:
            writer.writerow([
                reporte.id,
                reporte.alerta.animal.collar_id,
                reporte.alerta.animal.display_id or '',
                reporte.alerta.animal.tipo_animal,
                reporte.alerta.tipo_alerta,
                reporte.alerta.mensaje,
                reporte.alerta.valor_registrado if reporte.alerta.valor_registrado else '',
                reporte.alerta.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                reporte.alerta.fecha_resolucion.strftime('%Y-%m-%d %H:%M:%S') if reporte.alerta.fecha_resolucion else '',
                reporte.fecha_generacion.strftime('%Y-%m-%d %H:%M:%S'),
                reporte.generado_por.username if reporte.generado_por else '',
                reporte.observaciones or '',
                'Sí' if reporte.exportado else 'No'
            ])
        
        # Marcar reportes como exportados
        reportes.update(exportado=True, fecha_exportacion=timezone.now())
        
        # Crear respuesta HTTP con charset UTF-8
        output.seek(0)
        response = HttpResponse(output.getvalue(), content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="reportes_camport_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        return response
    
    @action(detail=False, methods=['post'])
    def exportar_csv_filtrado(self, request):
        """Exporta reportes filtrados en formato CSV"""
        # Filtros opcionales
        fecha_desde = request.data.get('fecha_desde')
        fecha_hasta = request.data.get('fecha_hasta')
        tipo_alerta = request.data.get('tipo_alerta')
        animal_id = request.data.get('animal_id')
        
        reportes = Reporte.objects.all().select_related('alerta', 'alerta__animal', 'generado_por')
        
        if fecha_desde:
            reportes = reportes.filter(fecha_generacion__gte=fecha_desde)
        if fecha_hasta:
            reportes = reportes.filter(fecha_generacion__lte=fecha_hasta)
        if tipo_alerta:
            reportes = reportes.filter(alerta__tipo_alerta=tipo_alerta)
        if animal_id:
            reportes = reportes.filter(alerta__animal__collar_id=animal_id)
        
        # Crear archivo CSV en memoria con encoding UTF-8
        output = io.StringIO()
        # Agregar BOM para que Excel reconozca UTF-8
        output.write('\ufeff')
        # Usar punto y coma como delimitador para Excel
        writer = csv.writer(output, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        
        # Encabezados
        writer.writerow([
            'ID Reporte',
            'Collar ID',
            'Display ID',
            'Tipo Animal',
            'Tipo Alerta',
            'Mensaje',
            'Valor Registrado',
            'Fecha Alerta',
            'Fecha Resolución',
            'Fecha Generación',
            'Generado Por',
            'Observaciones',
            'Exportado'
        ])
        
        # Datos
        for reporte in reportes:
            writer.writerow([
                reporte.id,
                reporte.alerta.animal.collar_id,
                reporte.alerta.animal.display_id or '',
                reporte.alerta.animal.tipo_animal,
                reporte.alerta.tipo_alerta,
                reporte.alerta.mensaje,
                reporte.alerta.valor_registrado if reporte.alerta.valor_registrado else '',
                reporte.alerta.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                reporte.alerta.fecha_resolucion.strftime('%Y-%m-%d %H:%M:%S') if reporte.alerta.fecha_resolucion else '',
                reporte.fecha_generacion.strftime('%Y-%m-%d %H:%M:%S'),
                reporte.generado_por.username if reporte.generado_por else '',
                reporte.observaciones or '',
                'Sí' if reporte.exportado else 'No'
            ])
        
        # Marcar reportes como exportados
        reportes.update(exportado=True, fecha_exportacion=timezone.now())
        
        # Crear respuesta HTTP con charset UTF-8
        output.seek(0)
        response = HttpResponse(output.getvalue(), content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="reportes_camport_filtrado_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        return response

@api_view(['POST'])
@permission_classes([AllowAny])
def simulate_emergency(request, collar_id, emergency_type):
    """
    URL Secreta para simular emergencias en demos
    """
    try:
        animal = get_object_or_404(Animal, collar_id=collar_id)
        
        # Obtener última telemetría
        last_telemetria = animal.telemetria.first()
        if not last_telemetria:
            return Response({'error': 'No hay telemetría previa'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Modificar datos según tipo de emergencia
        if emergency_type == 'fiebre':
            temperatura = 41.5
            frecuencia = last_telemetria.frecuencia_cardiaca
            lat = last_telemetria.latitud
            lng = last_telemetria.longitud
        elif emergency_type == 'hipotermia':
            temperatura = 36.0
            frecuencia = last_telemetria.frecuencia_cardiaca
            lat = last_telemetria.latitud
            lng = last_telemetria.longitud
        elif emergency_type == 'taquicardia':
            temperatura = last_telemetria.temperatura_corporal
            frecuencia = 150
            lat = last_telemetria.latitud
            lng = last_telemetria.longitud
        elif emergency_type == 'perimetro':
            temperatura = last_telemetria.temperatura_corporal
            frecuencia = last_telemetria.frecuencia_cardiaca
            # Mover fuera del perímetro (asumiendo coordenadas iniciales)
            lat = last_telemetria.latitud + 0.01
            lng = last_telemetria.longitud + 0.01
        else:
            return Response({'error': 'Tipo de emergencia no válido'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Crear nueva telemetría con datos anómalos
        telemetria = Telemetria.objects.create(
            animal=animal,
            latitud=lat,
            longitud=lng,
            temperatura_corporal=temperatura,
            frecuencia_cardiaca=frecuencia
        )
        
        return Response({
            'success': True,
            'message': f'Emergencia {emergency_type} simulada para {collar_id}',
            'telemetria': TelemetriaSerializer(telemetria).data
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
