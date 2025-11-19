# 📋 ESTRUCTURA Y ORGANIZACIÓN DEL PROYECTO CAMPORT

**Fecha de organización:** Noviembre 2025  
**Estado:** ✅ Limpio y organizado

---

## 📁 Estructura de Archivos

### 🗂️ Raíz del Proyecto

```
CAMPORT/
│
├── 📄 README.md                           # Documentación principal
├── 📄 INICIO-RAPIDO.md                    # Guía de inicio rápido (⚡ LEER PRIMERO)
├── 📄 DOCUMENTACION-COMPLETA.md           # Documentación técnica completa
├── 📄 REPORTE-PRUEBA-SISTEMA-COMPLETO.md  # Reporte de pruebas recientes
├── 📄 RESUMEN-EJECUTIVO.md                # Resumen del proyecto
├── 📄 .gitignore                          # Archivos ignorados por Git
│
├── 🔧 start-backend.ps1                   # Iniciar servidor Django
├── 🔧 start-frontend.ps1                  # Iniciar app React
├── 🔧 start-simulator.ps1                 # Iniciar simulador (v6/v7/v8)
├── 🔧 stop-all.ps1                        # Detener todos los servicios
│
├── 📂 backend/                            # Backend Django + API
├── 📂 frontend/                           # Frontend React
└── 📂 .git/                               # Control de versiones
```

---

## 🖥️ Backend (`backend/`)

```
backend/
├── 📂 api/                                # Aplicación principal Django
│   ├── 📂 management/
│   │   └── 📂 commands/
│   │       ├── simulate_collars.py        # Simulador V6 (Gravedad centroide)
│   │       ├── simulate_collars_v7.py     # Simulador V7 (Random walk)
│   │       ├── simulate_collars_v7_backup.py
│   │       └── simulate_collars_v8.py     # ⭐ Simulador V8 (Recomendado)
│   │
│   ├── models.py                          # Modelos: Animal, Telemetria, Alerta, etc.
│   ├── views.py                           # Endpoints de la API REST
│   ├── consumers.py                       # WebSocket handlers
│   ├── serializers.py                     # Serializadores DRF
│   ├── urls.py                            # URLs de la API
│   ├── routing.py                         # Rutas WebSocket
│   ├── admin.py                           # Panel de administración
│   └── ...
│
├── 📂 ganadoproject/                      # Configuración Django
│   ├── settings.py                        # Configuración principal
│   ├── urls.py                            # URLs principales
│   ├── asgi.py                            # Configuración ASGI
│   └── wsgi.py                            # Configuración WSGI
│
├── 📂 utils/                              # 🛠️ Scripts de utilidad
│   ├── diagnostico_sistema.py             # Diagnóstico completo del sistema
│   ├── test_envio_simple.py               # Prueba simple de WebSocket
│   ├── test_sistema_completo.py           # Suite de pruebas completa
│   ├── actualizar_telemetria.py           # Actualizar telemetría manual
│   ├── check_alertas.py                   # Verificar alertas
│   ├── check_animals.py                   # Verificar animales
│   ├── diagnostico_completo.py            # Diagnóstico detallado
│   ├── reset_animals.py                   # Resetear animales
│   └── verificar_coordenadas.py           # Verificar coordenadas
│
├── 📂 venv/                               # Entorno virtual Python (no en Git)
├── 📂 __pycache__/                        # Cache Python (no en Git)
│
├── manage.py                              # CLI de Django
├── populate_db.py                         # ⚡ Poblar base de datos inicial
├── simulator.py                           # Simulador simple (obsoleto, no usar)
├── db.sqlite3                             # Base de datos SQLite
├── requirements.txt                       # Dependencias Python
└── .gitignore
```

### 🔑 Scripts Importantes del Backend

| Archivo | Descripción | Comando |
|---------|-------------|---------|
| `manage.py` | CLI principal de Django | `python manage.py <comando>` |
| `populate_db.py` | Crear datos iniciales | `python populate_db.py` |
| `utils/diagnostico_sistema.py` | Ver estado del sistema | `python utils/diagnostico_sistema.py` |

---

## 🌐 Frontend (`frontend/`)

```
frontend/
├── 📂 public/                             # Archivos públicos
│   ├── index.html
│   └── ...
│
├── 📂 src/                                # Código fuente React
│   ├── 📂 components/                     # Componentes React
│   │   ├── 📂 map/                        # Componentes del mapa
│   │   ├── 📂 dashboard/                  # Dashboard y alertas
│   │   ├── 📂 admin/                      # Panel administrativo
│   │   └── ...
│   │
│   ├── 📂 context/                        # Context API
│   │   ├── AuthContext.js                 # Autenticación
│   │   └── ...
│   │
│   ├── 📂 services/                       # Servicios
│   │   ├── api.js                         # Cliente API REST
│   │   └── websocket.js                   # Cliente WebSocket
│   │
│   ├── App.js                             # Componente principal
│   ├── index.js                           # Punto de entrada
│   └── ...
│
├── 📂 node_modules/                       # Dependencias npm (no en Git)
├── 📂 build/                              # Build de producción (no en Git)
│
├── package.json                           # Configuración npm
├── package-lock.json                      # Lock de dependencias
└── .gitignore
```

---

## 📄 Documentación

| Archivo | Para Quién | Contenido |
|---------|-----------|-----------|
| **INICIO-RAPIDO.md** | 🚀 Nuevos usuarios | Cómo iniciar el sistema en 2 minutos |
| **README.md** | 📖 Todos | Visión general, características, instalación |
| **DOCUMENTACION-COMPLETA.md** | 👨‍💻 Desarrolladores | Arquitectura, API, modelos, detalles técnicos |
| **REPORTE-PRUEBA-SISTEMA-COMPLETO.md** | 🧪 QA/Testing | Resultados de pruebas del sistema |
| **RESUMEN-EJECUTIVO.md** | 👔 Gestión | Resumen ejecutivo del proyecto |

---

## 🛠️ Scripts de PowerShell

| Script | Función | Uso |
|--------|---------|-----|
| `start-backend.ps1` | Inicia el servidor Django | Terminal 1 |
| `start-frontend.ps1` | Inicia la app React | Terminal 2 |
| `start-simulator.ps1` | Inicia el simulador (v6/v7/v8) | Terminal 3 |
| `stop-all.ps1` | Detiene todos los servicios | Cualquier terminal |

---

## 🗑️ Archivos Eliminados (Obsoletos)

Durante la limpieza se eliminaron:

### Documentación Obsoleta
- ❌ `DIAGRAMA-FIX-ALERTAS.md`
- ❌ `FIX-ALERTAS-COOLDOWN.md`
- ❌ `FIX-DATOS-SIMULADOR-REFRESH.md`
- ❌ `FIX-SIMULADOR-CONGELAMIENTO.md`
- ❌ `GUIA-VERIFICACION-FIX.md`
- ❌ `INDICE-FIX-ALERTAS.md`
- ❌ `PRUEBAS-INICIO-SEPARADO.md`
- ❌ `REPORTE-PRUEBAS-START-ALL.md`
- ❌ `RESUMEN-FIX-ALERTAS.md`

### Scripts Obsoletos
- ❌ `test-fix-alertas.ps1`
- ❌ `test-start-all.ps1`
- ❌ `run-diagnostico.ps1`

### Scripts Movidos a `backend/utils/`
Todos los scripts de utilidad fueron reorganizados en `backend/utils/`

---

## 🎯 Archivos Clave por Tarea

### Para Iniciar el Sistema
1. `start-backend.ps1`
2. `start-frontend.ps1`
3. `start-simulator.ps1 v8`

### Para Poblar Datos Iniciales
1. `backend/populate_db.py`

### Para Diagnóstico
1. `backend/utils/diagnostico_sistema.py`

### Para Desarrollo

**Backend:**
- `backend/api/models.py` - Definir modelos
- `backend/api/views.py` - Crear endpoints
- `backend/api/consumers.py` - WebSocket handlers

**Frontend:**
- `frontend/src/components/` - Componentes React
- `frontend/src/services/api.js` - Llamadas API
- `frontend/src/services/websocket.js` - WebSocket

### Para Simulación
- `backend/api/management/commands/simulate_collars_v8.py` ⭐ **RECOMENDADO**
- `backend/api/management/commands/simulate_collars_v7.py`
- `backend/api/management/commands/simulate_collars.py` (v6)

---

## 📊 Resumen de Organización

### ✅ Acciones Realizadas

1. **Eliminados** 12 archivos de documentación obsoleta
2. **Eliminados** 3 scripts de PowerShell obsoletos
3. **Creada** carpeta `backend/utils/` para scripts de utilidad
4. **Movidos** 9 scripts de utilidad a `backend/utils/`
5. **Creado** `INICIO-RAPIDO.md` con guía clara de inicio
6. **Actualizado** `README.md` con información concisa
7. **Creado** este archivo de estructura

### 📦 Resultado

```
Antes: 26 archivos en raíz (desorganizado)
Ahora: 10 archivos en raíz (limpio y organizado)

- Documentación: 5 archivos relevantes
- Scripts: 4 archivos de inicio/stop
- Git: 1 archivo (.gitignore)
```

---

## 🚀 Próximos Pasos Recomendados

1. **Para nuevos usuarios:** Leer `INICIO-RAPIDO.md`
2. **Para desarrolladores:** Leer `DOCUMENTACION-COMPLETA.md`
3. **Para entender las pruebas:** Leer `REPORTE-PRUEBA-SISTEMA-COMPLETO.md`

---

**Última actualización:** Noviembre 2025  
**Organizado por:** Limpieza automática del proyecto
