from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password

# 1. Modelo de Usuario Extendido
class User(AbstractUser):
    RUT = models.CharField(max_length=12, unique=True)
    domicilio = models.CharField(max_length=255)
    SEXO_CHOICES = [('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')]
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    fecha_nacimiento = models.DateField()
    
    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$')):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

# 2. Modelo del Ganado (Animal)
class Animal(models.Model):
    TIPO_ANIMAL_CHOICES = [
        ('OVINO', 'Ovinos'),
        ('BOVINO', 'Bovinos'),
        ('EQUINO', 'Equinos'),
    ]
    SEXO_ANIMAL_CHOICES = [('M', 'Macho'), ('H', 'Hembra')]

    collar_id = models.CharField(max_length=50, unique=True, primary_key=True)
    display_id = models.CharField(max_length=50, unique=True, editable=False, blank=True)
    tipo_animal = models.CharField(max_length=10, choices=TIPO_ANIMAL_CHOICES)
    raza = models.CharField(max_length=100)
    edad = models.PositiveIntegerField()
    peso_kg = models.FloatField()
    sexo = models.CharField(max_length=1, choices=SEXO_ANIMAL_CHOICES)
    color = models.CharField(max_length=50)
    geocerca = models.ForeignKey('Geocerca', on_delete=models.SET_NULL, null=True, blank=True, related_name='animales')
    agregado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='ganado_agregado')

    def save(self, *args, **kwargs):
        # Generar display_id si no existe
        if not self.display_id:
            # Obtener el último número para este tipo de animal
            last_animal = Animal.objects.filter(
                tipo_animal=self.tipo_animal
            ).order_by('-display_id').first()
            
            if last_animal and last_animal.display_id:
                # Extraer el número del último display_id
                try:
                    last_number = int(last_animal.display_id.split('-')[1])
                    new_number = last_number + 1
                except (IndexError, ValueError):
                    new_number = 1
            else:
                new_number = 1
            
            # Generar el nuevo display_id
            self.display_id = f"{self.tipo_animal}-{new_number:03d}"
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tipo_animal} ({self.display_id or self.collar_id})"

# 3. Modelo de Datos de Telemetría
class Telemetria(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='telemetria')
    timestamp = models.DateTimeField(auto_now_add=True)
    latitud = models.FloatField()
    longitud = models.FloatField()
    temperatura_corporal = models.FloatField()
    frecuencia_cardiaca = models.PositiveIntegerField()
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['animal', '-timestamp']),
        ]

    def __str__(self):
        return f"Telemetría de {self.animal.collar_id} a las {self.timestamp}"

# 4. Modelo de Geocerca
class Geocerca(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    coordenadas = models.JSONField()
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

# 5. Modelo de Alertas
class Alerta(models.Model):
    TIPO_ALERTA_CHOICES = [
        ('TEMPERATURA', 'Temperatura Anormal'),
        ('FRECUENCIA', 'Frecuencia Cardíaca Anormal'),
        ('PERIMETRO', 'Fuera de Perímetro'),
    ]
    
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='alertas')
    tipo_alerta = models.CharField(max_length=20, choices=TIPO_ALERTA_CHOICES)
    mensaje = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    resuelta = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.tipo_alerta} - {self.animal.collar_id}"

# 6. Modelo de Alertas por Usuario
class AlertaUsuario(models.Model):
    alerta = models.ForeignKey(Alerta, on_delete=models.CASCADE, related_name='usuarios_notificados')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alertas_recibidas')
    leido = models.BooleanField(default=False)
    fecha_lectura = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('alerta', 'usuario')

    def __str__(self):
        return f"Alerta {self.alerta.id} para {self.usuario.username}"
