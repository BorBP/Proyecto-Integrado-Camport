# 🐄 CAMPORT - Sistema de Monitoreo de Ganado en Tiempo Real

**Versión:** V6.0 - Gravedad de Centroide  
**Estado:** ✅ Production Ready

Sistema fullstack completo para monitoreo de ganado con geolocalización en tiempo real, telemetría de signos vitales y alertas automáticas.

---

## 📚 Documentación

| Documento | Descripción |
|-----------|-------------|
| **[INICIO-RAPIDO.md](INICIO-RAPIDO.md)** | ⚡ Guía rápida para iniciar el sistema en 3 pasos |
| **[DOCUMENTACION.md](DOCUMENTACION.md)** | 📖 Documentación completa y detallada |
| **[ESTRUCTURA.md](ESTRUCTURA.md)** | 📁 Estructura del proyecto y archivos |
| **`diagnostico.ps1`** | 🔍 Script de diagnóstico del sistema |

---

## ⚡ Inicio Rápido (3 Pasos)

### 1. Verificar que todo esté instalado
```powershell
.\diagnostico.ps1
```

### 2. Iniciar el sistema (3 terminales)
```powershell
# Terminal 1
.\start-backend.ps1

# Terminal 2
.\start-frontend.ps1

# Terminal 3 (Opcional)
.\start-simulator.ps1
```

### 3. Acceder
- 🌐 **Frontend:** http://localhost:3000
- 👤 **Login:** `admin` / `admin123`

**📖 Ver guía completa:** [INICIO-RAPIDO.md](INICIO-RAPIDO.md)

---

## 🏗️ Arquitectura

### Backend
- **Framework:** Django 5.0 + Django REST Framework
- **Base de Datos:** SQLite
- **Tiempo Real:** Django Channels (WebSockets)
- **Autenticación:** JWT (Simple JWT)

### Frontend
- **Framework:** React 18
- **Enrutamiento:** React Router DOM
- **Mapas:** React Leaflet + OpenStreetMap
- **WebSockets:** ReconnectingWebSocket
- **Estado:** React Context API

## 🚀 Inicio Rápido

### 1. Verificar Sistema
```powershell
.\diagnostico.ps1
```

### 2. Iniciar Backend
```powershell
.\start-backend.ps1
```

### 3. Iniciar Frontend
```powershell
.\start-frontend.ps1
```

### 4. Iniciar Simulador (Opcional)
```powershell
.\start-simulator.ps1
```

### 5. Acceder al Sistema
- 🌐 Frontend: http://localhost:3000
- 🔧 Backend: http://localhost:8000
- 👤 Login: `admin` / `admin123`

---

## 📦 Instalación (Primera Vez)

### Backend
```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
python manage.py migrate
python populate_db.py
```

### Frontend
```bash
cd frontend
npm install
```

---

## 👤 Credenciales

- **Admin:** `admin` / `admin123`
- **Trabajador:** `trabajador` / `trabajador123`

---

## 🎯 Características Principales

✅ **Dashboard en Tiempo Real** - Mapa interactivo con OpenStreetMap  
✅ **Sistema de Alertas** - Notificaciones automáticas  
✅ **Geocercas Múltiples** - Perímetros configurables  
✅ **Telemetría en Vivo** - Temperatura, FC, ubicación  
✅ **Simulador V6.0** - Gravedad de centroide  
✅ **Panel de Administración** - Gestión completa  

---

## 📁 Estructura

```
Proyecto-Integrado-Camport/
├── backend/              # Django + Channels
├── frontend/             # React + Leaflet
├── start-backend.ps1     # Iniciar backend
├── start-frontend.ps1    # Iniciar frontend
├── start-simulator.ps1   # Iniciar simulador
├── diagnostico.ps1       # Diagnóstico del sistema
├── DOCUMENTACION.md      # 📖 Documentación completa
└── README.md             # Este archivo
```

---

## 🛠️ Solución de Problemas

**Sistema no inicia:**
```powershell
.\diagnostico.ps1  # Ejecutar diagnóstico
```

**Ver documentación completa:** [DOCUMENTACION.md](DOCUMENTACION.md)

---

## 📊 Tecnologías

**Backend:** Django 5.0, Channels, JWT, Shapely  
**Frontend:** React 18, Leaflet, Axios, WebSocket  
**Database:** SQLite  

---

**Versión:** V6.0 - Gravedad de Centroide  
**Estado:** ✅ Production Ready  
**Documentación Completa:** [DOCUMENTACION.md](DOCUMENTACION.md)
