# 🚀 Guía de Inicio Rápido - CAMPORT V6.0

## ✅ Verificación Previa

Antes de iniciar, ejecuta el diagnóstico:

```powershell
.\diagnostico.ps1
```

**Debe mostrar:** ✅ "Sistema completamente configurado y listo!"

---

## 🎯 Inicio del Sistema (3 Pasos)

### Paso 1: Iniciar Backend

**Terminal 1:**
```powershell
.\start-backend.ps1
```

**Verás:**
```
🚀 Iniciando Backend Django...
📡 Backend estará disponible en: http://localhost:8000
Starting ASGI/Daphne version 4.1.0 development server...
```

✅ **Listo cuando veas:** "Starting ASGI/Daphne... at http://127.0.0.1:8000/"

---

### Paso 2: Iniciar Frontend

**Terminal 2 (nueva terminal):**
```powershell
.\start-frontend.ps1
```

**Verás:**
```
⚛️  Iniciando Frontend React...
Compiled successfully!
You can now view frontend in the browser.
  Local: http://localhost:3000
```

✅ **Listo cuando veas:** "Compiled successfully!"

Se abrirá automáticamente en tu navegador.

---

### Paso 3: Iniciar Simulador (Opcional)

**Terminal 3 (nueva terminal):**
```powershell
.\start-simulator.ps1
```

**Verás:**
```
🐄 Iniciando Simulador CAMPORT V6.0...
🧲 Gravedad de centroide: 20% atracción
=====================================================================================
📡 CICLO #1 - Consultando estado EN VIVO del rebaño...
  🟢 [1/5] BOVINO-001: (-38.845, -72.298) | Dist:0.0001° | T:38.5°C FC:74lpm
```

✅ **Listo cuando veas:** "CICLO #1" y datos de animales

---

## 🌐 Acceder al Sistema

1. **Abre tu navegador** en: http://localhost:3000

2. **Login con:**
   - Usuario: `admin`
   - Contraseña: `admin123`

3. **Verás:**
   - 🗺️ Mapa interactivo
   - 🐄 5 animales en el mapa
   - 📊 Panel lateral con lista de animales
   - 🔔 Campana de notificaciones

---

## ✨ Qué Hacer Ahora

### Explorar Dashboard
- Click en un animal del mapa para ver detalles
- Observa las actualizaciones en tiempo real
- Revisa las alertas en la campana 🔔

### Probar Panel de Admin
- Click en "Panel de Administración"
- Pestaña "Usuarios": Ver/crear usuarios
- Pestaña "Ganado": Ver/editar animales
- Pestaña "Geocercas": Ver perímetro

### Ver Simulador en Acción
- Observa cómo los animales se mueven cada 20 segundos
- Los animales tienden naturalmente al centro (gravedad)
- Cada ~60 segundos puede haber una "fuga"

---

## 🛑 Detener el Sistema

**Para detener cada servicio:**

Presiona `Ctrl+C` en cada terminal

**Orden recomendado:**
1. Terminal 3 (Simulador) - Ctrl+C
2. Terminal 2 (Frontend) - Ctrl+C
3. Terminal 1 (Backend) - Ctrl+C

---

## 🆘 Problemas Comunes

### ❌ "Puerto ya en uso"

**Backend (puerto 8000):**
```powershell
# Ver proceso
netstat -ano | findstr :8000
# Matar proceso (reemplaza PID)
taskkill /PID <PID> /F
```

**Frontend (puerto 3000):**
```powershell
# Ver proceso
netstat -ano | findstr :3000
# Matar proceso (reemplaza PID)
taskkill /PID <PID> /F
```

---

### ❌ "No se puede activar venv"

**Solución:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### ❌ Backend no conecta

**Verificar:**
```powershell
# Probar manualmente
cd backend
.\venv\Scripts\Activate.ps1
python manage.py runserver
```

---

### ❌ Frontend muestra error

**Reinstalar dependencias:**
```powershell
cd frontend
Remove-Item -Recurse -Force node_modules
npm install
```

---

## 📖 Más Información

- **Documentación completa:** [DOCUMENTACION.md](DOCUMENTACION.md)
- **Estructura del proyecto:** [ESTRUCTURA.md](ESTRUCTURA.md)
- **Diagnóstico del sistema:** `.\diagnostico.ps1`

---

## 🎯 Checklist de Inicio

- [ ] Ejecuté `.\diagnostico.ps1` → Todo OK
- [ ] Terminal 1: `.\start-backend.ps1` → Corriendo
- [ ] Terminal 2: `.\start-frontend.ps1` → Corriendo
- [ ] Terminal 3: `.\start-simulator.ps1` → Corriendo
- [ ] Navegador en http://localhost:3000
- [ ] Login exitoso con admin/admin123
- [ ] Veo el mapa con 5 animales
- [ ] Los animales se actualizan cada 20 seg

---

**¡Sistema listo! Disfruta explorando CAMPORT V6.0** 🐄🚀

**Para ayuda detallada:** [DOCUMENTACION.md](DOCUMENTACION.md)
