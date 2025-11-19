from rest_framework import serializers
from .models import User, Animal, Telemetria, Geocerca, Alerta, AlertaUsuario, Reporte

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'RUT', 
                  'domicilio', 'sexo', 'fecha_nacimiento', 'is_staff', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class AnimalSerializer(serializers.ModelSerializer):
    agregado_por_username = serializers.CharField(source='agregado_por.username', read_only=True)
    geocerca_nombre = serializers.CharField(source='geocerca.nombre', read_only=True)
    
    class Meta:
        model = Animal
        fields = ['collar_id', 'display_id', 'tipo_animal', 'raza', 'edad', 'peso_kg', 
                  'sexo', 'color', 'geocerca', 'geocerca_nombre', 'agregado_por', 'agregado_por_username']
        read_only_fields = ['agregado_por', 'display_id']

class TelemetriaSerializer(serializers.ModelSerializer):
    animal_tipo = serializers.CharField(source='animal.tipo_animal', read_only=True)
    
    class Meta:
        model = Telemetria
        fields = ['id', 'animal', 'animal_tipo', 'timestamp', 'latitud', 
                  'longitud', 'temperatura_corporal', 'frecuencia_cardiaca']
        read_only_fields = ['timestamp']

class GeocercaSerializer(serializers.ModelSerializer):
    creado_por_username = serializers.CharField(source='creado_por.username', read_only=True)
    animales_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Geocerca
        fields = ['id', 'nombre', 'coordenadas', 'creado_por', 
                  'creado_por_username', 'fecha_creacion', 'activa', 'animales_count']
        read_only_fields = ['creado_por', 'fecha_creacion']
    
    def get_animales_count(self, obj):
        return obj.animales.count()

class AlertaSerializer(serializers.ModelSerializer):
    animal_collar = serializers.CharField(source='animal.collar_id', read_only=True)
    animal_display_id = serializers.CharField(source='animal.display_id', read_only=True)
    animal_tipo = serializers.CharField(source='animal.tipo_animal', read_only=True)
    
    class Meta:
        model = Alerta
        fields = ['id', 'animal', 'animal_collar', 'animal_display_id', 'animal_tipo', 
                  'tipo_alerta', 'mensaje', 'timestamp', 'resuelta', 'fecha_resolucion', 'valor_registrado']
        read_only_fields = ['timestamp']

class AlertaUsuarioSerializer(serializers.ModelSerializer):
    alerta_detalle = AlertaSerializer(source='alerta', read_only=True)
    usuario_username = serializers.CharField(source='usuario.username', read_only=True)
    
    class Meta:
        model = AlertaUsuario
        fields = ['id', 'alerta', 'alerta_detalle', 'usuario', 
                  'usuario_username', 'leido', 'fecha_lectura', 'eliminada']
        read_only_fields = ['fecha_lectura']

class ReporteSerializer(serializers.ModelSerializer):
    alerta_detalle = AlertaSerializer(source='alerta', read_only=True)
    generado_por_username = serializers.CharField(source='generado_por.username', read_only=True)
    
    class Meta:
        model = Reporte
        fields = ['id', 'alerta', 'alerta_detalle', 'generado_por', 'generado_por_username',
                  'fecha_generacion', 'observaciones', 'exportado', 'fecha_exportacion']
        read_only_fields = ['fecha_generacion', 'generado_por']
