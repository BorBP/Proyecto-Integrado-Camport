# 🚀 Guía de Inicio Rápido

## ✅ Prerrequisitos Instalados

- ✓ Python 3.12
- ✓ Node.js y npm
- ✓ Backend configurado con Django
- ✓ Frontend configurado con React
- ✓ Base de datos poblada con datos de prueba

## 🎯 Iniciar la Aplicación

### Opción 1: Usando Scripts PowerShell (Recomendado)

Abre **3 terminales PowerShell** en la carpeta raíz del proyecto:

**Terminal 1 - Backend:**
```powershell
.\start-backend.ps1
```

**Terminal 2 - Simulador (Opcional pero recomendado):**
```powershell
.\start-simulator.ps1
```

**Terminal 3 - Frontend:**
```powershell
.\start-frontend.ps1
```

### Opción 2: Comandos Manuales

**Terminal 1 - Backend:**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python manage.py runserver
```

**Terminal 2 - Simulador:**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python simulator.py
```

**Terminal 3 - Frontend:**
```powershell
cd frontend
npm start
```

## 🌐 Acceder a la Aplicación

1. El frontend se abrirá automáticamente en: **http://localhost:3000**
2. Backend API disponible en: **http://localhost:8000/api**
3. Panel de administración Django: **http://localhost:8000/admin**

## 👤 Credenciales de Prueba

### Administrador
- **Usuario:** `admin`
- **Contraseña:** `admin123`
- **Permisos:** Acceso completo al dashboard y panel admin

### Trabajador
- **Usuario:** `trabajador`
- **Contraseña:** `trabajador123`
- **Permisos:** Solo acceso al dashboard de monitoreo

## 🎮 Cómo Usar la Aplicación

### 1. Login
- Ingresa con cualquiera de las credenciales de arriba
- El sistema te redirigirá al dashboard

### 2. Dashboard de Monitoreo
- **Mapa en tiempo real** con animales marcados (🐑 🐄 🐎)
- **Panel lateral** con lista de animales y sus datos vitales
- **Campana de notificaciones** para alertas
- Los datos se actualizan automáticamente si el simulador está activo

### 3. Panel de Administración (Solo Admin)
- Clic en tu nombre de usuario → "Dashboard" te llevará de vuelta al mapa
- O visita directamente: **http://localhost:3000/admin**

**Pestañas disponibles:**
- **👥 Usuarios:** CRUD completo de usuarios del sistema
- **🐄 Ganado:** CRUD completo de animales
- **🗺️ Geocerca:** Visualización del perímetro configurado

### 4. Sistema de Alertas

El sistema genera alertas automáticas cuando:
- 🌡️ **Temperatura anormal:** < 37.5°C o > 40°C
- ❤️ **Frecuencia cardíaca anormal:** < 40 lpm o > 120 lpm
- 🗺️ **Fuera de perímetro:** Animal sale de la geocerca

Las alertas aparecen en la campana 🔔 en tiempo real.

## 🧪 Probar Alertas Manualmente

Puedes simular emergencias usando la API REST:

```bash
# Simular fiebre
curl -X POST http://localhost:8000/api/simulate_emergency/OVINO-001/fiebre/

# Simular animal fuera de perímetro
curl -X POST http://localhost:8000/api/simulate_emergency/BOVINO-001/perimetro/

# Simular taquicardia
curl -X POST http://localhost:8000/api/simulate_emergency/EQUINO-001/taquicardia/

# Simular hipotermia
curl -X POST http://localhost:8000/api/simulate_emergency/OVINO-002/hipotermia/
```

## 📊 Animales Disponibles

El sistema incluye 5 animales de prueba:

1. **OVINO-001** - Oveja Suffolk
2. **OVINO-002** - Oveja Merino
3. **BOVINO-001** - Vaca Angus
4. **BOVINO-002** - Vaca Hereford
5. **EQUINO-001** - Caballo Criollo

## 🔧 Si Algo Sale Mal

### Backend no inicia
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python manage.py migrate
python populate_db.py
```

### Frontend no inicia
```powershell
cd frontend
npm install
npm start
```

### WebSocket no conecta
- Asegúrate de que el backend esté corriendo
- Verifica que no haya otro proceso usando el puerto 8000

### Sin datos en el mapa
- Inicia el simulador (start-simulator.ps1)
- O crea telemetría manualmente vía API

## 📚 Más Información

Ver **README.md** para documentación completa de:
- Arquitectura del sistema
- API endpoints
- Configuración avanzada
- Tecnologías utilizadas

## ✨ Funcionalidades Destacadas

✅ Monitoreo en tiempo real con WebSockets
✅ Mapa interactivo con OpenStreetMap
✅ Sistema de alertas automáticas
✅ Gestión completa de usuarios y ganado (Admin)
✅ Geocercas configurables
✅ Dashboard responsive
✅ Autenticación JWT
✅ API RESTful completa

## 🎉 ¡Listo!

La aplicación está completamente funcional. Explora las diferentes funcionalidades y disfruta del monitoreo de ganado en tiempo real! 🐄🗺️
