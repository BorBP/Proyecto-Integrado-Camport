# 🐄 CAMPORT - Sistema de Monitoreo de Ganado en Tiempo Real

**Versión:** 8.0  
**Estado:** ✅ FUNCIONANDO  
**Fecha:** Noviembre 2025

Sistema fullstack para monitoreo de ganado con geolocalización GPS, telemetría de signos vitales y alertas inteligentes en tiempo real.

---

## 🚀 Inicio Rápido

### Ver **[INICIO-RAPIDO.md](INICIO-RAPIDO.md)** para comenzar en 2 minutos

O ejecuta estos 3 comandos en 3 terminales diferentes:

```powershell
# Terminal 1: Backend
.\start-backend.ps1

# Terminal 2: Frontend  
.\start-frontend.ps1

# Terminal 3: Simulador
.\start-simulator.ps1 v8
```

**Acceso:**
- 🌐 Frontend: http://localhost:3000
- 🔐 Usuario: `admin` / Contraseña: `admin123`

---

## 📚 Documentación

| Archivo | Descripción |
|---------|-------------|
| **[INICIO-RAPIDO.md](INICIO-RAPIDO.md)** | ⚡ Guía de inicio rápido (2 minutos) |
| **[DOCUMENTACION-COMPLETA.md](DOCUMENTACION-COMPLETA.md)** | 📖 Documentación técnica completa |
| **[REPORTE-PRUEBA-SISTEMA-COMPLETO.md](REPORTE-PRUEBA-SISTEMA-COMPLETO.md)** | 📊 Reporte de pruebas del sistema |
| **[RESUMEN-EJECUTIVO.md](RESUMEN-EJECUTIVO.md)** | 📋 Resumen ejecutivo del proyecto |

---

## ✨ Características Principales

## ✨ Características Principales

### 🗺️ Monitoreo en Tiempo Real
- **Mapa interactivo** con OpenStreetMap
- **6 animales** monitoreados simultáneamente
- **Actualización automática** de posiciones (cada 3 segundos)
- **3 geocercas** activas con validación geométrica

### 🚨 Sistema de Alertas Inteligente
- **Temperatura:** Fiebre (>40°C) | Hipotermia (<37.5°C)
- **Frecuencia Cardíaca:** Agitación (>100 BPM) | Bajo estímulo (<50 BPM)  
- **Perímetro:** Detección de fuga en tiempo real
- **Cooldown anti-spam:** Vitales (180s) | Perímetro (60s)

### 📊 Telemetría Avanzada
- **Intervalos independientes** por tipo de dato
- **Variación gradual y realista** de signos vitales
- **Almacenamiento histórico** completo
- **Panel de administración** para gestión

### 🔧 Tecnologías

**Backend:**
- Django 5.0.3 + Django REST Framework
- WebSocket (Channels 4.0 + Daphne)
- Shapely 2.0.2 (geometría)
- SQLite / PostgreSQL

**Frontend:**
- React 18
- Leaflet + React Leaflet
- WebSocket con reconexión automática
- Context API para estado global

**Simulador V8:**
- Python asyncio
- Intervalos independientes
- Signos vitales realistas
- Sistema de oveja negra

---

## 🏗️ Estructura del Proyecto

```
CAMPORT/
├── backend/                      # Django + WebSocket
│   ├── api/                     # API REST y modelos
│   │   ├── models.py            # Animal, Telemetria, Alerta, etc.
│   │   ├── views.py             # Endpoints API
│   │   ├── consumers.py         # WebSocket handlers
│   │   └── management/commands/ # Simuladores V6, V7, V8
│   ├── utils/                   # Scripts de utilidad
│   ├── populate_db.py           # Datos iniciales
│   └── manage.py
│
├── frontend/                     # React App
│   ├── src/
│   │   ├── components/          # Mapa, Dashboard, Admin
│   │   ├── context/             # Estado global
│   │   └── services/            # API y WebSocket
│   └── package.json
│
├── start-backend.ps1            # Iniciar backend
├── start-frontend.ps1           # Iniciar frontend
├── start-simulator.ps1          # Iniciar simulador (V6/V7/V8)
├── stop-all.ps1                 # Detener todo
│
├── INICIO-RAPIDO.md             # Guía de inicio rápido
├── DOCUMENTACION-COMPLETA.md    # Documentación técnica
└── README.md                    # Este archivo
```

---

## 📦 Instalación Inicial

### Requisitos Previos
- Python 3.12+
- Node.js 16+
- Git

### Backend
```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1     # Windows
# source venv/bin/activate      # Linux/Mac
pip install -r requirements.txt
python manage.py migrate
python populate_db.py           # Crear datos de prueba
```

### Frontend
```bash
cd frontend
npm install
```

---

## 🎮 Versiones del Simulador

| Versión | Características | Comando |
|---------|----------------|---------|
| **V6** | Gravedad de centroide, fugas aleatorias | `.\start-simulator.ps1 v6` |
| **V7** | Random walk natural, oveja negra manual | `.\start-simulator.ps1 v7` |
| **V8** ⭐ | Signos vitales realistas, intervalos independientes | `.\start-simulator.ps1 v8` |

**Recomendado:** V8 por su realismo y funcionalidades avanzadas

---

## 👤 Usuarios del Sistema

| Usuario | Email | Contraseña | Rol |
|---------|-------|------------|-----|
| admin | admin@ganado.com | admin123 | Administrador |
| trabajador | trabajador@ganado.com | trabajador123 | Usuario |

---

## 🐄 Animales en el Sistema

1. **BOVINO-001** → Perimetro secundario
2. **BOVINO-002** 🐑 → Perímetro Principal (Oveja Negra)
3. **EQUINO-001** → Perímetro Principal  
4. **EQUINO-002** → home_dash
5. **OVINO-001** → Perimetro secundario
6. **OVINO-002** → Perimetro secundario

---

## 🔧 Utilidades

### Diagnóstico del Sistema
```bash
cd backend
python utils/diagnostico_sistema.py
```

Muestra el estado completo: animales, geocercas, telemetría, alertas.

### Limpiar Telemetría
```bash
cd backend
python manage.py shell -c "from api.models import Telemetria; Telemetria.objects.all().delete(); print('✓ Limpiado')"
```

### Limpiar Alertas
```bash
cd backend
python manage.py shell -c "from api.models import Alerta; Alerta.objects.all().delete(); print('✓ Limpiado')"
```

---

## 🛠️ Solución de Problemas

### Puerto 8000 ocupado
```powershell
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### No hay animales en la BD
```bash
cd backend
python populate_db.py
```

### WebSocket no conecta
1. Verificar que el backend esté en puerto 8000
2. Revisar logs del backend para errores
3. Verificar firewall/antivirus

### Animales no se mueven en el mapa
1. Asegurar que el simulador esté ejecutándose
2. Verificar logs: "Telemetría recibida" en backend
3. Revisar consola del navegador (F12)

Ver **[INICIO-RAPIDO.md](INICIO-RAPIDO.md)** para más soluciones.

---

## 📝 Comandos de Desarrollo

### Crear migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### Crear superusuario
```bash
python manage.py createsuperuser
```

### Acceder al shell de Django
```bash
python manage.py shell
```

### Ver rutas del frontend
```bash
cd frontend
npm run build    # Producción
```

---

## 📊 Métricas del Sistema

**Rendimiento validado:**
- ⚡ Actualización de posiciones cada 3s
- ⚡ Signos vitales cada 2-5s
- ⚡ Latencia WebSocket < 50ms
- ⚡ 100% de precisión geográfica

**Estado:**
- ✅ Sistema completamente funcional
- ✅ Flujo de datos verificado
- ✅ Alertas funcionando correctamente
- ✅ Broadcast a múltiples clientes

---

## 📄 Licencia

Proyecto Integrado CAMPORT  
Todos los derechos reservados © 2025

---

## 🎉 Estado del Proyecto

**✅ SISTEMA OPERATIVO Y FUNCIONAL**

El sistema ha sido probado exhaustivamente y está listo para:
- ✅ Monitoreo en tiempo real de ganado
- ✅ Generación y gestión de alertas
- ✅ Visualización geográfica precisa
- ✅ Gestión de múltiples geocercas
- ✅ Panel de administración completo

**Ver [REPORTE-PRUEBA-SISTEMA-COMPLETO.md](REPORTE-PRUEBA-SISTEMA-COMPLETO.md) para detalles de las pruebas**

---

**Última actualización:** Noviembre 2025  
**Versión:** 8.0
