from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import User, Animal, Telemetria, Geocerca, Alerta, AlertaUsuario
from .serializers import (UserSerializer, AnimalSerializer, TelemetriaSerializer,
                          GeocercaSerializer, AlertaSerializer, AlertaUsuarioSerializer)

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
    queryset = Geocerca.objects.filter(activa=True)
    serializer_class = GeocercaSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(creado_por=self.request.user)

    @action(detail=False, methods=['get'])
    def activa(self, request):
        geocerca = self.queryset.first()
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

class AlertaUsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = AlertaUsuarioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AlertaUsuario.objects.filter(usuario=self.request.user)

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
