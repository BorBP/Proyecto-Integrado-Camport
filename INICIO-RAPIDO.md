# 🚀 INICIO RÁPIDO - CAMPORT

Sistema de monitoreo de ganado en tiempo real con telemetría GPS y signos vitales.

---

## ⚡ Inicio Rápido (3 Pasos)

### 1️⃣ Iniciar el Backend (Django + WebSocket)

```powershell
# En la terminal 1
.\start-backend.ps1
```

O manualmente:
```bash
cd backend
python manage.py runserver
```

**Listo cuando veas:** `Starting ASGI/Daphne version 4.1.0 development server at http://127.0.0.1:8000/`

---

### 2️⃣ Iniciar el Frontend (React)

```powershell
# En la terminal 2
.\start-frontend.ps1
```

O manualmente:
```bash
cd frontend
npm start
```

**Listo cuando veas:** `Compiled successfully!` y `Local: http://localhost:3000`

---

### 3️⃣ Iniciar el Simulador V8

```powershell
# En la terminal 3
.\start-simulator.ps1 v8
```

O manualmente:
```bash
cd backend
python manage.py simulate_collars_v8
```

**Listo cuando veas:** `✓ Conectado a WebSocket` y estadísticas de animales

---

## 🌐 Acceder al Sistema

Una vez iniciados los 3 servicios:

- **Frontend (Usuario):** http://localhost:3000
- **Backend API:** http://localhost:8000/api/
- **Admin Django:** http://localhost:8000/admin/

### Credenciales de Prueba

| Usuario | Email | Contraseña | Rol |
|---------|-------|------------|-----|
| admin | admin@ganado.com | admin123 | Administrador |
| trabajador | trabajador@ganado.com | trabajador123 | Usuario |

---

## 📊 Verificar que Funciona

### En el Frontend (http://localhost:3000)

Deberías ver:

1. ✅ **Mapa** con 6 animales moviéndose en tiempo real
2. ✅ **Alertas** apareciendo cuando hay anomalías
3. ✅ **Panel lateral** con lista de animales
4. ✅ **Geocercas** dibujadas en el mapa

### En la Consola del Simulador

Deberías ver cada 2-5 segundos:

```
━━━ ESTADÍSTICAS CICLO #X ━━━
✅ BOVINO-001: Temp=38.1°C | BPM=62 | Pos=(lat, lng)
✅ BOVINO-002🐑: Temp=39.1°C | BPM=77 | Pos=(lat, lng)
...
❤️⚡ ALERTA: OVINO-001 - FIEBRE: 40.1°C
```

### En la Consola del Backend

Deberías ver:

```
📡 Telemetría recibida: BOVINO-001 - Pos:(...) Temp:38.1°C BPM:62
🔄 Enviando al frontend: BOVINO-001 - Pos:(...)
🌡️🔥 ALERTA CREADA EN BD: Fiebre detectada: 40.1°C
```

---

## 🛑 Detener el Sistema

```powershell
.\stop-all.ps1
```

O presiona `Ctrl+C` en cada una de las 3 terminales.

---

## 🔧 Comandos Útiles

### Ver Estado de la Base de Datos

```bash
cd backend
python utils/diagnostico_sistema.py
```

Muestra:
- Total de animales y sus geocercas
- Registros de telemetría
- Alertas pendientes y resueltas
- Estado general del sistema

### Limpiar Datos de Telemetría

```bash
cd backend
python manage.py shell -c "from api.models import Telemetria; Telemetria.objects.all().delete(); print('Telemetría limpiada')"
```

### Poblar Base de Datos (Primera vez)

```bash
cd backend
python populate_db.py
```

Crea:
- 2 usuarios (admin y trabajador)
- 6 animales (2 bovinos, 2 ovinos, 2 equinos)
- 3 geocercas
- Datos de prueba

---

## 🎮 Versiones del Simulador

El sistema incluye 3 versiones del simulador:

### V6 - Gravedad de Centroide
```powershell
.\start-simulator.ps1 v6
```
- Movimiento con atracción al centro (20%)
- Sistema de fugas aleatorias

### V7 - Random Walk Natural
```powershell
.\start-simulator.ps1 v7
```
- Random Walk puro (sin gravedad)
- Oveja negra con tendencia a escapar

### V8 - Signos Vitales Realistas ⭐ **RECOMENDADO**
```powershell
.\start-simulator.ps1 v8
```
- **Signos vitales con variación gradual**
- **Intervalos independientes** (Movimiento: 3s, Temp: 5s, BPM: 2s)
- **Alertas inteligentes** (solo con geocerca)
- **Sistema de cooldown** anti-spam

---

## 🏗️ Estructura del Proyecto

```
CAMPORT/
├── backend/                    # Django + WebSocket
│   ├── api/                   # API REST y WebSocket
│   │   ├── models.py          # Modelos de datos
│   │   ├── views.py           # Endpoints API
│   │   ├── consumers.py       # WebSocket handlers
│   │   └── management/        # Comandos de Django
│   │       └── commands/      # Simuladores
│   ├── utils/                 # Scripts de utilidad
│   ├── populate_db.py         # Poblar datos iniciales
│   └── manage.py              # Django CLI
│
├── frontend/                   # React App
│   ├── src/
│   │   ├── components/        # Componentes React
│   │   ├── context/           # Estado global
│   │   └── services/          # API y WebSocket
│   └── package.json
│
├── start-backend.ps1          # Iniciar backend
├── start-frontend.ps1         # Iniciar frontend
├── start-simulator.ps1        # Iniciar simulador
└── stop-all.ps1               # Detener todo
```

---

## ❓ Solución de Problemas

### El simulador dice "Animal matching query does not exist"

**Problema:** No hay animales en la base de datos

**Solución:**
```bash
cd backend
python populate_db.py
```

### El frontend no se conecta al backend

**Problema:** Backend no está ejecutándose

**Solución:**
1. Verifica que el backend esté en puerto 8000
2. Revisa el archivo `frontend/src/services/api.js` para la URL correcta

### No veo animales moviéndose en el mapa

**Problema:** El simulador no está enviando datos

**Solución:**
1. Asegúrate de que el simulador esté ejecutándose (terminal 3)
2. Verifica que veas logs de "Telemetría recibida" en el backend
3. Revisa la consola del navegador (F12) para errores de WebSocket

### El puerto 8000 ya está en uso

**Problema:** Otro proceso está usando el puerto

**Solución:**
```powershell
# Encontrar el proceso
netstat -ano | findstr :8000

# Matar el proceso (reemplaza PID con el número que obtuviste)
taskkill /PID <PID> /F
```

---

## 📚 Documentación Adicional

- **[README.md](README.md)** - Documentación general del proyecto
- **[DOCUMENTACION-COMPLETA.md](DOCUMENTACION-COMPLETA.md)** - Guía técnica completa
- **[REPORTE-PRUEBA-SISTEMA-COMPLETO.md](REPORTE-PRUEBA-SISTEMA-COMPLETO.md)** - Reporte de pruebas del sistema

---

## 🎯 Próximos Pasos

1. ✅ Familiarízate con la interfaz navegando por el mapa
2. ✅ Prueba marcar alertas como leídas/resueltas
3. ✅ Experimenta con diferentes versiones del simulador
4. ✅ Revisa el código para entender el flujo de datos
5. ✅ Personaliza las geocercas desde el admin panel

---

**¿Listo para empezar? ¡Ejecuta los 3 comandos y tendrás el sistema funcionando en menos de 2 minutos! 🚀**
