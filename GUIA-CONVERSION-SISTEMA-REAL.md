# 🚀 GUÍA COMPLETA: CONVERSIÓN DE CAMPORT SIMULADO A SISTEMA REAL CON HARDWARE

**Documento:** Guía de Migración a Sistema de Producción  
**Proyecto:** CAMPORT - Sistema de Monitoreo de Ganado  
**Versión:** 1.0  
**Fecha:** Noviembre 2025  
**Autor:** Sistema CAMPORT

---

## 📋 TABLA DE CONTENIDOS

1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Arquitectura del Sistema Real](#arquitectura-del-sistema-real)
3. [Cambios en el Software](#cambios-en-el-software)
4. [Hardware Necesario](#hardware-necesario)
5. [Costos Detallados (CLP)](#costos-detallados-clp)
6. [Plan de Implementación](#plan-de-implementación)
7. [Código de Ejemplo](#código-de-ejemplo)
8. [Proveedores en Chile](#proveedores-en-chile)
9. [Consideraciones Técnicas](#consideraciones-técnicas)
10. [Mantenimiento y Operación](#mantenimiento-y-operación)

---

## 1. RESUMEN EJECUTIVO

### 1.1 Estado Actual del Proyecto

**✅ Ya tienes implementado (~80% del sistema):**

- Backend Django robusto con API REST
- Sistema de WebSocket para tiempo real
- Modelos de datos correctos (Animal, Telemetría, Alertas, Geocercas)
- Frontend React funcional con mapas
- Sistema de alertas inteligente con cooldown
- Gestión de geocercas con validación geométrica
- Panel de administración completo

**❌ Necesitas agregar (~20% restante):**

- Receptor de datos desde hardware real (collares GPS)
- Protocolo de comunicación IoT (MQTT/LoRaWAN)
- Sistema de gestión de dispositivos físicos
- Módulo de monitoreo de salud de dispositivos
- Sistema de respaldo y recuperación ante fallos
- Optimizaciones para producción
- Infraestructura de red para comunicación con collares

---

### 1.2 Ventajas de tu Base Actual

1. **Arquitectura sólida**: WebSocket ya implementado para tiempo real
2. **Modelos de datos correctos**: Fácil agregar campos de hardware
3. **Sistema de alertas**: Solo necesita conectar con datos reales
4. **Frontend listo**: Solo cambiar fuente de datos
5. **Geocercas funcionando**: Algoritmo ya validado

---

## 2. ARQUITECTURA DEL SISTEMA REAL

### 2.1 Diagrama de Arquitectura Completa


```
┌─────────────────────────────────────────────────────────────────────────┐
│                    CAPA 1: DISPOSITIVOS IoT (CAMPO)                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  🐄 COLLARES GPS (En los animales)          📡 GATEWAYS (Torres/Postes) │
│  ├─ Módulo GPS (ubicación)                  ├─ Receptor LoRa/LoRaWAN    │
│  ├─ Sensor Temperatura                      ├─ Módulo 4G/LTE            │
│  ├─ Sensor Frecuencia Cardíaca              ├─ Procesador Edge (RPi)    │
│  ├─ Acelerómetro (actividad)                ├─ Batería + Solar          │
│  ├─ Batería Li-Ion + Panel Solar            └─ Conexión Internet        │
│  └─ Transmisor LoRa/4G/NB-IoT                                           │
│                                                                           │
│  Cantidad: 1 por animal                      Cantidad: 1 cada 5km        │
│  Costo: ~.000 CLP c/u                     Costo: ~.000 CLP c/u    │
│                                                                           │
└────────────────┬─────────────────────────────────────┬──────────────────┘
                 │                                     │
                 │ Protocolo: LoRaWAN, NB-IoT, 4G     │
                 ▼                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    CAPA 2: COMUNICACIÓN (RED)                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  📡 MQTT Broker (Mosquitto/HiveMQ)                                       │
│  ├─ Topics organizados por granja/animal                                │
│  ├─ Autenticación TLS/SSL                                               │
│  ├─ Certificados X.509 para dispositivos                                │
│  └─ QoS 1 o 2 para mensajes críticos                                    │
│                                                                           │
│  🔐 Capa de Seguridad                                                    │
│  ├─ Firewall para conexiones                                            │
│  ├─ VPN para acceso remoto                                              │
│  ├─ Encriptación end-to-end                                             │
│  └─ Autenticación de dispositivos                                       │
│                                                                           │
│  Costo servidor: ~.200.000 CLP (one-time)                             │
│                                                                           │
└────────────────┬────────────────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│              CAPA 3: PROCESAMIENTO (TU BACKEND ACTUAL)                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  🐍 Django Application (Base ya implementada)                            │
│  ├─ API REST (Django REST Framework) ✅ Ya existe                       │
│  ├─ WebSocket (Django Channels) ✅ Ya existe                            │
│  ├─ 🆕 MQTT Client - Recibir datos de collares reales                   │
│  ├─ 🆕 Procesamiento de telemetría en tiempo real                       │
│  ├─ Sistema de Alertas ✅ Ya existe (mejorar umbrales)                  │
│  └─ 🆕 Gestión de dispositivos y salud del sistema                      │
│                                                                           │
│  🔄 Servicios Adicionales (A implementar)                                │
│  ├─ Celery - Tareas asíncronas y programadas                            │
│  ├─ Redis - Cache y message broker                                      │
│  ├─ PostgreSQL + TimescaleDB - Base de datos serie temporal             │
│  └─ Elasticsearch - Logs y búsqueda (opcional)                          │
│                                                                           │
│  Costo mensual cloud: ~.000-150.000 CLP                              │
│  O servidor local: ~.000 CLP (one-time)                             │
│                                                                           │
└────────────────┬────────────────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                  CAPA 4: PRESENTACIÓN (USUARIOS)                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  💻 Web App (React) ✅ Ya existe                                        │
│  📱 Mobile App (React Native/Flutter) 🆕 A desarrollar                  │
│  🖥️ Desktop App (Electron) 🆕 Opcional                                 │
│  📊 Dashboard Analytics (Grafana) 🆕 Para administradores               │
│                                                                           │
│  Costo desarrollo app móvil: ~.000.000-5.000.000 CLP                  │
│                                                                           │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Flujo de Datos en Tiempo Real

```
[Collar GPS en animal]
    │
    │ Cada 30-60 segundos
    │ Envía: GPS, Temp, BPM, Batería
    ▼
[Gateway LoRa/4G]
    │
    │ Retransmite vía 4G/Internet
    ▼
[MQTT Broker]
    │
    │ Publica en topic: farm/XXX/animal/YYY/telemetry
    ▼
[Django MQTT Client] 🆕 A IMPLEMENTAR
    │
    │ Suscrito a topics, recibe mensaje
    ▼
[Procesamiento Backend]
    ├─ Validar datos
    ├─ Guardar en BD (PostgreSQL)
    ├─ Verificar alertas (temp, BPM, geofence)
    └─ Enviar vía WebSocket a frontend
    ▼
[Frontend React] ✅ YA EXISTE
    │
    └─ Actualiza mapa, alertas, gráficos en tiempo real
```

---

## 3. CAMBIOS EN EL SOFTWARE

### 3.1 Nuevos Modelos de Base de Datos

**Archivo:** `backend/api/models.py`

#### 3.1.1 Modelo de Dispositivo Collar

```python
from django.db import models
from django.utils import timezone

class DispositivoCollar(models.Model):
    """"""
    Gestión de collares físicos instalados en los animales.
    Reemplaza/complementa el concepto de collar_id virtual.
    """"""
    
    # Identificación
    collar_id = models.CharField(max_length=50, unique=True, primary_key=True)
    numero_serie = models.CharField(max_length=100, unique=True)
    fabricante = models.CharField(max_length=100, default='CAMPORT')
    modelo = models.CharField(max_length=100, default='CAMPORT-V1')
    version_firmware = models.CharField(max_length=20, default='1.0.0')
    
    # Relación con animal (puede cambiar con el tiempo)
    animal_actual = models.OneToOneField(
        'Animal', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='dispositivo_activo'
    )
    
    # Estado operativo
    activo = models.BooleanField(default=True)
    en_mantenimiento = models.BooleanField(default=False)
    fecha_instalacion = models.DateField()
    fecha_activacion = models.DateTimeField(auto_now_add=True)
    
    # Salud del dispositivo
    bateria_porcentaje = models.IntegerField(default=100)
    voltaje_bateria = models.FloatField(null=True, blank=True)
    ultimo_ping = models.DateTimeField(default=timezone.now)
    ultima_telemetria = models.DateTimeField(null=True, blank=True)
    
    # Configuración
    intervalo_envio_segundos = models.IntegerField(default=60)
    modo_ahorro_energia = models.BooleanField(default=False)
    umbral_bateria_baja = models.IntegerField(default=20)
    umbral_bateria_critica = models.IntegerField(default=10)
    
    # Estadísticas
    total_mensajes_enviados = models.BigIntegerField(default=0)
    total_mensajes_fallidos = models.IntegerField(default=0)
    ultimo_error = models.TextField(null=True, blank=True)
    fecha_ultimo_error = models.DateTimeField(null=True, blank=True)
    
    # Mantenimiento
    fecha_ultimo_mantenimiento = models.DateField(null=True, blank=True)
    proxima_revision = models.DateField(null=True, blank=True)
    notas_mantenimiento = models.TextField(blank=True)
    
    # Información de red
    imei = models.CharField(max_length=20, null=True, blank=True)  # Para 4G
    deveui = models.CharField(max_length=20, null=True, blank=True)  # Para LoRaWAN
    rssi_promedio = models.IntegerField(null=True, blank=True)  # Señal
    snr_promedio = models.FloatField(null=True, blank=True)  # Signal-to-Noise
    
    class Meta:
        verbose_name = "Dispositivo Collar"
        verbose_name_plural = "Dispositivos Collares"
        ordering = ['-ultimo_ping']
    
    def __str__(self):
        animal_info = f" - {self.animal_actual.display_id}" if self.animal_actual else ""
        return f"{self.collar_id}{animal_info}"
    
    @property
    def esta_online(self):
        """"""Dispositivo online si envió datos en últimos 10 minutos""""""
        from datetime import timedelta
        limite = timezone.now() - timedelta(minutes=10)
        return self.ultimo_ping >= limite
    
    @property
    def necesita_mantenimiento(self):
        """"""Verifica si necesita mantenimiento""""""
        if not self.proxima_revision:
            return False
        return timezone.now().date() >= self.proxima_revision
    
    def registrar_ping(self, bateria=None, rssi=None):
        """"""Actualizar último ping y estadísticas""""""
        self.ultimo_ping = timezone.now()
        if bateria is not None:
            self.bateria_porcentaje = bateria
        if rssi is not None:
            # Calcular promedio móvil
            if self.rssi_promedio is None:
                self.rssi_promedio = rssi
            else:
                self.rssi_promedio = int((self.rssi_promedio * 0.8) + (rssi * 0.2))
        self.save(update_fields=['ultimo_ping', 'bateria_porcentaje', 'rssi_promedio'])
```

#### 3.1.2 Modelo de Gateway (Antenas Receptoras)

```python
class Gateway(models.Model):
    """"""
    Antenas/Gateways que reciben señales de los collares.
    Puede ser torre LoRa o punto de acceso 4G.
    """"""
    
    # Identificación
    gateway_id = models.CharField(max_length=50, unique=True, primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    
    # Ubicación física
    latitud = models.FloatField()
    longitud = models.FloatField()
    altitud = models.FloatField(null=True, blank=True, help_text="Metros sobre nivel del mar")
    direccion = models.CharField(max_length=255, blank=True)
    
    # Estado operativo
    activo = models.BooleanField(default=True)
    en_mantenimiento = models.BooleanField(default=False)
    ultimo_heartbeat = models.DateTimeField(default=timezone.now)
    
    # Configuración de red
    ip_address = models.GenericIPAddressField()
    puerto = models.IntegerField(default=1883)
    tipo_conexion = models.CharField(max_length=20, choices=[
        ('LORA', 'LoRaWAN'),
        ('4G', '4G/LTE'),
        ('WIFI', 'WiFi'),
        ('ETH', 'Ethernet'),
        ('NBIOT', 'NB-IoT')
    ], default='LORA')
    
    # Para LoRaWAN
    gateway_eui = models.CharField(max_length=20, null=True, blank=True)
    frecuencia_mhz = models.FloatField(null=True, blank=True, default=915.0)  # 915 MHz Chile
    
    # Métricas operativas
    collares_en_rango = models.IntegerField(default=0)
    mensajes_procesados_hoy = models.IntegerField(default=0)
    mensajes_fallidos_hoy = models.IntegerField(default=0)
    uptime_porcentaje = models.FloatField(default=100.0)
    
    # Cobertura estimada
    radio_cobertura_km = models.FloatField(default=5.0, help_text="Radio de cobertura en km")
    
    # Instalación
    fecha_instalacion = models.DateField()
    instalado_por = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name = "Gateway"
        verbose_name_plural = "Gateways"
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} ({self.gateway_id})"
    
    @property
    def esta_online(self):
        """"""Gateway online si heartbeat en últimos 5 minutos""""""
        from datetime import timedelta
        limite = timezone.now() - timedelta(minutes=5)
        return self.ultimo_heartbeat >= limite
    
    def actualizar_estadisticas(self, exito=True):
        """"""Actualizar contadores de mensajes""""""
        if exito:
            self.mensajes_procesados_hoy += 1
        else:
            self.mensajes_fallidos_hoy += 1
        self.save(update_fields=['mensajes_procesados_hoy', 'mensajes_fallidos_hoy'])
```

#### 3.1.3 Modelo de Log de Dispositivos

```python
class LogDispositivo(models.Model):
    """"""
    Registro de eventos importantes de dispositivos.
    Útil para debugging y auditoría.
    """"""
    
    dispositivo = models.ForeignKey(
        DispositivoCollar, 
        on_delete=models.CASCADE,
        related_name='logs'
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    
    tipo_evento = models.CharField(max_length=20, choices=[
        ('ONLINE', 'Dispositivo Online'),
        ('OFFLINE', 'Dispositivo Offline'),
        ('LOW_BAT', 'Batería Baja'),
        ('CRIT_BAT', 'Batería Crítica'),
        ('ERROR', 'Error de Sistema'),
        ('MAINT', 'Mantenimiento Realizado'),
        ('UPDATE', 'Actualización Firmware'),
        ('INSTALL', 'Instalación en Animal'),
        ('REMOVE', 'Remoción de Animal'),
        ('CONFIG', 'Cambio de Configuración'),
        ('GPS_LOSS', 'Pérdida de señal GPS'),
        ('WEAK_SIG', 'Señal débil'),
    ])
    
    nivel = models.CharField(max_length=10, choices=[
        ('DEBUG', 'Debug'),
        ('INFO', 'Info'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
        ('CRITICAL', 'Critical')
    ], default='INFO')
    
    mensaje = models.TextField()
    detalles = models.JSONField(null=True, blank=True)
    
    # Usuario que realizó acción (si aplica)
    usuario = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = "Log de Dispositivo"
        verbose_name_plural = "Logs de Dispositivos"
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['dispositivo', '-timestamp']),
            models.Index(fields=['tipo_evento', '-timestamp']),
            models.Index(fields=['nivel', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.dispositivo.collar_id} - {self.tipo_evento} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
```

#### 3.1.4 Modificar Modelo Telemetría

Agregar campos de calidad de datos del hardware:

```python
# En el modelo Telemetria existente, agregar:

class Telemetria(models.Model):
    # ... campos existentes ...
    
    # NUEVOS CAMPOS PARA HARDWARE REAL:
    
    # Calidad de GPS
    satelites_gps = models.IntegerField(null=True, blank=True, help_text="Número de satélites")
    hdop = models.FloatField(null=True, blank=True, help_text="Horizontal Dilution of Precision")
    altitud = models.FloatField(null=True, blank=True, help_text="Metros sobre nivel del mar")
    velocidad_kmh = models.FloatField(null=True, blank=True, help_text="Velocidad de movimiento")
    
    # Estado del dispositivo
    bateria_porcentaje = models.IntegerField(null=True, blank=True)
    voltaje_bateria = models.FloatField(null=True, blank=True)
    temperatura_dispositivo = models.FloatField(null=True, blank=True, help_text="Temp del collar, no del animal")
    
    # Calidad de señal
    rssi = models.IntegerField(null=True, blank=True, help_text="Received Signal Strength Indicator")
    snr = models.FloatField(null=True, blank=True, help_text="Signal-to-Noise Ratio")
    
    # Datos de actividad (si el collar tiene acelerómetro)
    nivel_actividad = models.IntegerField(null=True, blank=True, help_text="0-10, 0=inmóvil, 10=muy activo")
    esta_rumiando = models.BooleanField(null=True, blank=True)
    
    # Metadatos
    gateway_receptor = models.ForeignKey(
        'Gateway', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        help_text="Gateway que recibió este mensaje"
    )
    latencia_ms = models.IntegerField(null=True, blank=True, help_text="Tiempo desde collar hasta servidor")
    
    # Control de calidad
    datos_validados = models.BooleanField(default=True, help_text="Si los datos pasaron validación")
    anomalia_detectada = models.BooleanField(default=False)
    nota_anomalia = models.TextField(blank=True)
```

---

### 3.2 Servicio MQTT Listener (Nuevo)

**Archivo:** `backend/api/management/commands/mqtt_listener.py`

Este reemplaza al simulador actual:

```python
""""""
Management command para escuchar datos reales de collares vía MQTT.
Este servicio corre 24/7 escuchando el broker MQTT.

Uso:
    python manage.py mqtt_listener
""""""

import paho.mqtt.client as mqtt
import json
import time
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from api.models import Animal, Telemetria, DispositivoCollar, Gateway, LogDispositivo, Alerta

class Command(BaseCommand):
    help = 'Escucha datos reales de collares vía MQTT'

    def __init__(self):
        super().__init__()
        self.channel_layer = get_channel_layer()
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 10

    def add_arguments(self, parser):
        parser.add_argument(
            '--broker',
            type=str,
            default=settings.MQTT_BROKER,
            help='Dirección del broker MQTT'
        )
        parser.add_argument(
            '--port',
            type=int,
            default=settings.MQTT_PORT,
            help='Puerto del broker MQTT'
        )

    def on_connect(self, client, userdata, flags, rc):
        """"""Callback cuando se conecta al broker""""""
        if rc == 0:
            self.stdout.write(self.style.SUCCESS('✓ Conectado al broker MQTT'))
            self.reconnect_attempts = 0
            
            # Suscribirse a todos los topics de telemetría
            topics = [
                ("farm/+/animal/+/telemetry", 1),  # QoS 1
                ("farm/+/animal/+/status", 1),
                ("farm/+/gateway/+/health", 0)
            ]
            
            for topic, qos in topics:
                client.subscribe(topic, qos)
                self.stdout.write(f"  Suscrito a: {topic} (QoS {qos})")
        else:
            self.stderr.write(f'✗ Error de conexión: código {rc}')
            self.handle_reconnect()

    def on_disconnect(self, client, userdata, rc):
        """"""Callback cuando se desconecta del broker""""""
        if rc != 0:
            self.stderr.write(f'✗ Desconexión inesperada: código {rc}')
            self.handle_reconnect()

    def handle_reconnect(self):
        """"""Manejo de reconexión con backoff exponencial""""""
        if self.reconnect_attempts < self.max_reconnect_attempts:
            self.reconnect_attempts += 1
            wait_time = min(60, 2 ** self.reconnect_attempts)
            self.stdout.write(f'Reintentando en {wait_time} segundos...')
            time.sleep(wait_time)
        else:
            self.stderr.write('✗ Máximo de reintentos alcanzado')
            raise Exception('No se pudo reconectar al broker MQTT')

    def on_message(self, client, userdata, msg):
        """"""Callback cuando llega un mensaje MQTT""""""
        try:
            topic_parts = msg.topic.split('/')
            
            # Parsear topic: farm/{farm_id}/animal/{collar_id}/telemetry
            if len(topic_parts) >= 5:
                farm_id = topic_parts[1]
                resource_type = topic_parts[2]  # 'animal' o 'gateway'
                resource_id = topic_parts[3]
                message_type = topic_parts[4]  # 'telemetry', 'status', 'health'
                
                # Decodificar payload JSON
                data = json.loads(msg.payload.decode('utf-8'))
                
                # Procesar según tipo de mensaje
                if resource_type == 'animal' and message_type == 'telemetry':
                    self.process_telemetry(resource_id, data)
                elif resource_type == 'animal' and message_type == 'status':
                    self.process_device_status(resource_id, data)
                elif resource_type == 'gateway' and message_type == 'health':
                    self.process_gateway_health(resource_id, data)
                    
        except json.JSONDecodeError as e:
            self.stderr.write(f'✗ Error parseando JSON: {e}')
        except Exception as e:
            self.stderr.write(f'✗ Error procesando mensaje: {e}')
            import traceback
            traceback.print_exc()

    def process_telemetry(self, collar_id, data):
        """"""
        Procesar datos de telemetría de un collar.
        Este es el corazón del sistema real.
        """"""
        try:
            # 1. Verificar que el dispositivo existe
            try:
                dispositivo = DispositivoCollar.objects.get(collar_id=collar_id)
            except DispositivoCollar.DoesNotExist:
                self.stderr.write(f'✗ Dispositivo {collar_id} no registrado')
                return
            
            # 2. Verificar que está asignado a un animal
            if not dispositivo.animal_actual:
                self.stderr.write(f'⚠ Dispositivo {collar_id} no asignado a ningún animal')
                return
            
            animal = dispositivo.animal_actual
            
            # 3. Validar datos recibidos
            required_fields = ['gps', 'sensors', 'status', 'timestamp']
            if not all(field in data for field in required_fields):
                self.stderr.write(f'✗ Datos incompletos de {collar_id}')
                return
            
            # 4. Extraer y validar datos GPS
            gps_data = data['gps']
            if not self.validate_gps(gps_data):
                self.stderr.write(f'⚠ GPS inválido de {collar_id}')
                # Aún así guardamos los datos de sensores
            
            # 5. Crear registro de telemetría
            telemetria = Telemetria.objects.create(
                animal=animal,
                
                # GPS
                latitud=gps_data.get('lat', 0),
                longitud=gps_data.get('lng', 0),
                altitud=gps_data.get('altitude'),
                satelites_gps=gps_data.get('satellites', 0),
                hdop=gps_data.get('hdop'),
                velocidad_kmh=gps_data.get('speed', 0),
                
                # Sensores vitales
                temperatura_corporal=data['sensors'].get('temperature', 0),
                frecuencia_cardiaca=data['sensors'].get('heart_rate', 0),
                nivel_actividad=data['sensors'].get('activity_level', 0),
                esta_rumiando=data['sensors'].get('ruminating', False),
                
                # Estado del dispositivo
                bateria_porcentaje=data['status'].get('battery', 0),
                voltaje_bateria=data['status'].get('voltage'),
                temperatura_dispositivo=data['status'].get('device_temp'),
                rssi=data['status'].get('rssi'),
                snr=data['status'].get('snr'),
                
                # Metadatos
                gateway_receptor_id=data.get('gateway_id'),
                datos_validados=self.validate_gps(gps_data),
            )
            
            # 6. Actualizar estado del dispositivo
            dispositivo.registrar_ping(
                bateria=data['status'].get('battery'),
                rssi=data['status'].get('rssi')
            )
            dispositivo.ultima_telemetria = telemetria.timestamp
            dispositivo.total_mensajes_enviados += 1
            dispositivo.save()
            
            # 7. Verificar alertas (reutilizar lógica actual del consumer)
            alertas = self.check_alerts_for_telemetry(telemetria)
            
            # 8. Enviar por WebSocket al frontend (igual que ahora)
            async_to_sync(self.channel_layer.group_send)(
                "telemetria",
                {
                    "type": "telemetria_update",
                    "data": {
                        "collar_id": collar_id,
                        "tipo_animal": animal.tipo_animal,
                        "latitud": float(telemetria.latitud),
                        "longitud": float(telemetria.longitud),
                        "temperatura_corporal": float(telemetria.temperatura_corporal),
                        "frecuencia_cardiaca": int(telemetria.frecuencia_cardiaca),
                        "bateria": data['status'].get('battery', 100),
                        "timestamp": telemetria.timestamp.isoformat(),
                        "alertas": alertas
                    }
                }
            )
            
            # 9. Log
            self.stdout.write(
                self.style.SUCCESS(
                    f'📡 Telemetría: {collar_id} | '
                    f'Pos:({telemetria.latitud:.5f},{telemetria.longitud:.5f}) | '
                    f'Temp:{telemetria.temperatura_corporal}°C | '
                    f'BPM:{telemetria.frecuencia_cardiaca} | '
                    f'Bat:{data["status"].get("battery", 0)}% | '
                    f'Alertas:{len(alertas)}'
                )
            )
            
            # 10. Verificar batería baja
            if data['status'].get('battery', 100) < dispositivo.umbral_bateria_baja:
                self.crear_alerta_bateria_baja(dispositivo, data['status'].get('battery'))
                
        except Exception as e:
            self.stderr.write(f'✗ Error procesando telemetría de {collar_id}: {e}')
            import traceback
            traceback.print_exc()

    def validate_gps(self, gps_data):
        """"""Validar que los datos GPS sean razonables""""""
        lat = gps_data.get('lat', 0)
        lng = gps_data.get('lng', 0)
        satellites = gps_data.get('satellites', 0)
        
        # Validaciones básicas
        if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
            return False
        
        # Chile está entre latitudes -17 y -56
        if not (-56 <= lat <= -17):
            return False
        
        # Chile está entre longitudes -66 y -75
        if not (-75 <= lng <= -66):
            return False
        
        # Mínimo 4 satélites para GPS confiable
        if satellites < 4:
            return False
        
        return True

    def check_alerts_for_telemetry(self, telemetria):
        """"""
        Verificar alertas (reutilizar lógica del consumer actual).
        Retorna lista de alertas generadas.
        """"""
        from api.consumers import TelemetriaConsumer
        
        # Crear instancia temporal del consumer para usar su lógica
        consumer = TelemetriaConsumer()
        
        # Preparar datos en formato que espera el consumer
        telemetria_data = {
            'collar_id': telemetria.animal.collar_id,
            'latitud': float(telemetria.latitud),
            'longitud': float(telemetria.longitud),
            'temperatura_corporal': float(telemetria.temperatura_corporal),
            'frecuencia_cardiaca': int(telemetria.frecuencia_cardiaca)
        }
        
        # Llamar al método de verificación de alertas
        # (Este es sync_to_async porque check_alerts es @database_sync_to_async)
        from asgiref.sync import async_to_sync
        alertas = async_to_sync(consumer.check_alerts)(telemetria_data)
        
        return alertas

    def process_device_status(self, collar_id, data):
        """"""Procesar mensajes de estado del dispositivo""""""
        try:
            dispositivo = DispositivoCollar.objects.get(collar_id=collar_id)
            
            # Actualizar firmware version si cambió
            if 'firmware_version' in data:
                if dispositivo.version_firmware != data['firmware_version']:
                    old_version = dispositivo.version_firmware
                    dispositivo.version_firmware = data['firmware_version']
                    dispositivo.save()
                    
                    # Log de actualización
                    LogDispositivo.objects.create(
                        dispositivo=dispositivo,
                        tipo_evento='UPDATE',
                        nivel='INFO',
                        mensaje=f'Firmware actualizado de {old_version} a {data["firmware_version"]}'
                    )
            
            # Registrar errores si los hay
            if data.get('error'):
                dispositivo.ultimo_error = data['error']
                dispositivo.fecha_ultimo_error = datetime.now()
                dispositivo.save()
                
                LogDispositivo.objects.create(
                    dispositivo=dispositivo,
                    tipo_evento='ERROR',
                    nivel='ERROR',
                    mensaje=f'Error reportado: {data["error"]}',
                    detalles=data
                )
                
        except DispositivoCollar.DoesNotExist:
            self.stderr.write(f'✗ Dispositivo {collar_id} no encontrado')

    def process_gateway_health(self, gateway_id, data):
        """"""Procesar health check de gateways""""""
        try:
            gateway = Gateway.objects.get(gateway_id=gateway_id)
            gateway.ultimo_heartbeat = datetime.now()
            
            if 'collars_in_range' in data:
                gateway.collares_en_rango = data['collars_in_range']
            
            if 'uptime' in data:
                # Calcular porcentaje de uptime
                gateway.uptime_porcentaje = (data['uptime'] / 86400) * 100  # uptime en segundos
            
            gateway.save()
            
            self.stdout.write(f'💚 Gateway {gateway_id} health OK')
            
        except Gateway.DoesNotExist:
            self.stderr.write(f'✗ Gateway {gateway_id} no encontrado')

    def crear_alerta_bateria_baja(self, dispositivo, bateria):
        """"""Crear alerta de batería baja""""""
        nivel = 'CRIT_BAT' if bateria < dispositivo.umbral_bateria_critica else 'LOW_BAT'
        
        # Log
        LogDispositivo.objects.create(
            dispositivo=dispositivo,
            tipo_evento=nivel,
            nivel='WARNING' if nivel == 'LOW_BAT' else 'CRITICAL',
            mensaje=f'Batería {"crítica" if nivel == "CRIT_BAT" else "baja"}: {bateria}%'
        )
        
        # Alerta al usuario
        if dispositivo.animal_actual:
            Alerta.objects.create(
                animal=dispositivo.animal_actual,
                tipo_alerta='DISPOSITIVO',
                mensaje=f'Batería {"crítica" if nivel == "CRIT_BAT" else "baja"} en collar {dispositivo.collar_id}: {bateria}%',
                valor_registrado=bateria
            )

    def handle(self, *args, **options):
        """"""Punto de entrada del comando""""""
        broker = options['broker']
        port = options['port']
        
        self.stdout.write('═' * 60)
        self.stdout.write('  CAMPORT - MQTT Listener para Collares Reales')
        self.stdout.write('═' * 60)
        self.stdout.write(f'Broker: {broker}:{port}')
        self.stdout.write('Presiona Ctrl+C para detener')
        self.stdout.write('═' * 60)
        self.stdout.write('')
        
        # Configurar cliente MQTT
        client = mqtt.Client(client_id=f"camport_backend_{int(time.time())}")
        
        # Callbacks
        client.on_connect = self.on_connect
        client.on_disconnect = self.on_disconnect
        client.on_message = self.on_message
        
        # Autenticación
        if hasattr(settings, 'MQTT_USERNAME') and settings.MQTT_USERNAME:
            client.username_pw_set(settings.MQTT_USERNAME, settings.MQTT_PASSWORD)
        
        # TLS/SSL para producción
        if hasattr(settings, 'MQTT_USE_TLS') and settings.MQTT_USE_TLS:
            client.tls_set()
        
        # Conectar
        try:
            client.connect(broker, port, keepalive=60)
            
            # Loop forever (bloquea hasta Ctrl+C)
            client.loop_forever()
            
        except KeyboardInterrupt:
            self.stdout.write('\n\n✓ Deteniendo listener MQTT...')
            client.disconnect()
            self.stdout.write('✓ Desconectado del broker')
        except Exception as e:
            self.stderr.write(f'\n✗ Error fatal: {e}')
            raise
```

---

### 3.3 Configuración de Settings

**Archivo:** `backend/ganadoproject/settings_production.py`

```python
""""""
Configuración para ambiente de producción con hardware real.
Usar: python manage.py runserver --settings=ganadoproject.settings_production
""""""

from .settings import *
import os

# Seguridad
DEBUG = False
ALLOWED_HOSTS = [
    'camport.tu-dominio.cl',
    'www.camport.tu-dominio.cl',
    '200.123.45.67',  # IP pública del servidor
    'localhost',
    '127.0.0.1',
]

# Base de Datos PostgreSQL + TimescaleDB
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'camport_production',
        'USER': 'camport_user',
        'PASSWORD': os.environ.get('DB_PASSWORD', 'CAMBIAR_EN_PRODUCCION'),
        'HOST': 'localhost',
        'PORT': '5432',
        'CONN_MAX_AGE': 600,  # Conexiones persistentes
        'OPTIONS': {
            'options': '-c search_path=public,timescaledb'
        }
    }
}

# Redis para cache y Celery
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'camport',
        'TIMEOUT': 300,  # 5 minutos default
    }
}

# Configuración MQTT
MQTT_BROKER = os.environ.get('MQTT_BROKER', 'mqtt.camport.cl')
MQTT_PORT = int(os.environ.get('MQTT_PORT', 8883))  # 8883 para TLS
MQTT_USERNAME = os.environ.get('MQTT_USERNAME', 'camport')
MQTT_PASSWORD = os.environ.get('MQTT_PASSWORD', 'CAMBIAR_EN_PRODUCCION')
MQTT_USE_TLS = True
MQTT_TLS_INSECURE = False  # Validar certificados en producción

# Celery Configuration
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'America/Santiago'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutos máximo por tarea

# Logging mejorado
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file_django': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/camport/django.log',
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'file_mqtt': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/camport/mqtt.log',
            'maxBytes': 1024*1024*10,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'file_celery': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/camport/celery.log',
            'maxBytes': 1024*1024*10,
            'backupCount': 5,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file_django'],
            'level': 'INFO',
            'propagate': True,
        },
        'mqtt': {
            'handlers': ['console', 'file_mqtt'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'celery': {
            'handlers': ['console', 'file_celery'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Seguridad HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 año
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# CORS para frontend en dominio diferente
CORS_ALLOWED_ORIGINS = [
    "https://app.camport.cl",
    "https://www.camport.cl",
]

# Email para alertas críticas
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
DEFAULT_FROM_EMAIL = 'alertas@camport.cl'
SERVER_EMAIL = 'servidor@camport.cl'

# Administradores (reciben emails de errores)
ADMINS = [
    ('Admin CAMPORT', 'admin@camport.cl'),
]

# Managers (reciben emails de broken links)
MANAGERS = ADMINS
```

---
