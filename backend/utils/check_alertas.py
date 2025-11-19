import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ganadoproject.settings')
django.setup()

from api.models import Alerta, Animal

print("\n\033[1m\033[96m" + "="*80 + "\033[0m")
print("\033[1m\033[96m" + "VERIFICACIÓN DE ALERTAS EN BASE DE DATOS".center(80) + "\033[0m")
print("\033[1m\033[96m" + "="*80 + "\033[0m\n")

# Total de alertas
total_alertas = Alerta.objects.count()
alertas_activas = Alerta.objects.filter(resuelta=False).count()
alertas_resueltas = Alerta.objects.filter(resuelta=True).count()

print(f"\033[1mTotal de alertas:\033[0m {total_alertas}")
print(f"\033[92mAlertas activas:\033[0m {alertas_activas}")
print(f"\033[93mAlertas resueltas:\033[0m {alertas_resueltas}")

# Últimas alertas
print(f"\n\033[1m\033[96mÚltimas 15 alertas:\033[0m\n")
alertas = Alerta.objects.all().order_by('-timestamp')[:15]

for alerta in alertas:
    estado = "✓ RESUELTA" if alerta.resuelta else "⚠ ACTIVA"
    color = "\033[92m" if alerta.resuelta else "\033[91m"
    
    print(f"{color}{estado}\033[0m - {alerta.animal.display_id}: {alerta.tipo_alerta}")
    print(f"  Mensaje: {alerta.mensaje}")
    print(f"  Fecha: {alerta.timestamp}")
    if alerta.valor_registrado:
        print(f"  Valor: {alerta.valor_registrado}")
    print()

# Distribución por tipo
print("\n\033[1m\033[96mDistribución por tipo de alerta:\033[0m\n")
tipos = Alerta.objects.values_list('tipo_alerta', flat=True)
from collections import Counter
distribucion = Counter(tipos)

for tipo, count in distribucion.items():
    print(f"  {tipo}: {count}")

# Distribución por animal
print("\n\033[1m\033[96mDistribución por animal:\033[0m\n")
for animal in Animal.objects.all():
    count = animal.alertas.count()
    if count > 0:
        print(f"  {animal.display_id}: {count} alertas")

print("\n\033[1m\033[96m" + "="*80 + "\033[0m\n")
