# 🧪 GUÍA DE VERIFICACIÓN - EXPORTACIÓN CSV

## Verificar que todo funciona correctamente

Sigue estos pasos para confirmar que el cambio de XML a CSV funciona:

---

## ✅ PASO 1: Verificar Backend

### Opción A: Con el servidor corriendo

1. **Iniciar el backend**:
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python manage.py runserver
```

2. **En otra terminal, ejecutar pruebas**:
```powershell
.\backend\venv\Scripts\Activate.ps1
python test_csv_directo.py
```

**Resultado esperado**:
```
✅ PRUEBA COMPLETADA EXITOSAMENTE
✓ Status Code: 200
✓ Content-Type: text/csv
```

### Opción B: Sin servidor (prueba directa)

```powershell
.\backend\venv\Scripts\Activate.ps1
python test_sistema_completo.py
```

**Resultado esperado**:
```
✅ PRUEBAS COMPLETADAS EXITOSAMENTE
✓ Sistema funcionando correctamente ✅
```

---

## ✅ PASO 2: Verificar Frontend

1. **Iniciar frontend y backend**:
```powershell
# Terminal 1 - Backend
cd backend
.\venv\Scripts\Activate.ps1
python manage.py runserver

# Terminal 2 - Frontend
cd frontend
npm start
```

2. **Abrir navegador**: http://localhost:3000

3. **Login con credenciales**:
   - Usuario: `admin`
   - Contraseña: (la que hayas configurado)

4. **Ir a Dashboard → Alertas**

5. **Click en tab "Historial de Reportes"**

6. **Verificar botones**:
   - ✅ Debe decir "📥 Exportar Todos (CSV)"
   - ✅ Debe decir "📥 Exportar Filtrado (CSV)"
   - ✅ NO debe decir "XML"

7. **Click en "Exportar Todos (CSV)"**

8. **Verificar descarga**:
   - ✅ Se descarga un archivo `.csv`
   - ✅ El nombre es `reportes_camport_YYYYMMDD_HHMMSS.csv`
   - ✅ Se puede abrir en Excel/Google Sheets
   - ✅ Contiene 13 columnas
   - ✅ Los datos están correctos

---

## ✅ PASO 3: Verificar Archivo CSV

### Abrir el archivo descargado

**En Excel/LibreOffice/Google Sheets**:
1. Abrir el archivo CSV
2. Verificar columnas:
   - ID Reporte
   - Collar ID
   - Display ID
   - Tipo Animal
   - Tipo Alerta
   - Mensaje
   - Valor Registrado
   - Fecha Alerta
   - Fecha Resolución
   - Fecha Generación
   - Generado Por
   - Observaciones
   - Exportado

3. Verificar datos:
   - ✅ Las fechas tienen formato `YYYY-MM-DD HH:MM:SS`
   - ✅ Los acentos se ven correctamente (ñ, á, é, etc.)
   - ✅ Los tipos de alerta son TEMPERATURA, FRECUENCIA o PERIMETRO
   - ✅ Los valores están completos

**En un editor de texto**:
```powershell
notepad reportes_camport_*.csv
```

Debe verse algo así:
```
ID Reporte,Collar ID,Display ID,Tipo Animal,Tipo Alerta,Mensaje,...
1,EQUINO-001,EQUINO-001,EQUINO,TEMPERATURA,Fiebre detectada: 40.5°C,...
```

---

## ✅ PASO 4: Verificar Filtros

1. En el frontend, configurar filtros:
   - **Desde**: (fecha de inicio)
   - **Hasta**: (fecha de fin)
   - **Tipo**: TEMPERATURA

2. Click en "📥 Exportar Filtrado (CSV)"

3. Verificar que el archivo descargado:
   - ✅ Se llama `reportes_camport_filtrado_*.csv`
   - ✅ Solo contiene alertas de TEMPERATURA
   - ✅ Solo contiene alertas en el rango de fechas

---

## ✅ PASO 5: Verificar Consola del Navegador

1. Abrir DevTools (F12)
2. Ir a tab "Console"
3. Exportar CSV
4. Verificar que NO haya errores en rojo
5. Debe mostrar algo como:
   ```
   ✓ Archivo CSV descargado correctamente
   ```

---

## ✅ PASO 6: Verificar Base de Datos

```powershell
.\backend\venv\Scripts\Activate.ps1
python test_sistema_completo.py
```

**Verificar**:
```
✓ Reportes generados: X
✓ Reportes exportados: X
```

El número de reportes exportados debe incrementar después de exportar.

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### Problema: "No se descarga el archivo"

**Solución**:
1. Verificar que el backend está corriendo
2. Abrir DevTools → Network
3. Buscar la petición a `/reportes/exportar_csv/`
4. Ver si hay errores (401, 403, 500)
5. Verificar token de autenticación

### Problema: "El CSV no se abre en Excel"

**Solución**:
1. Verificar que el archivo tiene extensión `.csv`
2. Click derecho → Abrir con → Excel
3. Seleccionar "Delimitado por comas"
4. Encoding: UTF-8

### Problema: "Los acentos se ven mal"

**Solución**:
1. Abrir Excel
2. Ir a Datos → Obtener datos externos → Desde texto
3. Seleccionar el CSV
4. Encoding: **UTF-8** (importante)
5. Delimitador: Coma

### Problema: "Dice que no hay reportes"

**Solución**:
1. Primero resolver algunas alertas
2. Dashboard → Alertas → Alertas Activas
3. Click en "Resolver" en una alerta
4. Agregar observaciones
5. Click en "Resolver y Reportar"
6. Ahora debería haber reportes

---

## 📊 CHECKLIST FINAL

Marca cada item cuando lo verifiques:

- [ ] ✅ Backend inicia sin errores
- [ ] ✅ Frontend inicia sin errores
- [ ] ✅ Puedo hacer login
- [ ] ✅ Veo el tab "Historial de Reportes"
- [ ] ✅ El botón dice "CSV" (no XML)
- [ ] ✅ Al hacer click se descarga un archivo
- [ ] ✅ El archivo tiene extensión `.csv`
- [ ] ✅ El archivo se abre en Excel
- [ ] ✅ El CSV tiene 13 columnas
- [ ] ✅ Los datos se ven correctos
- [ ] ✅ Los acentos se ven bien
- [ ] ✅ Las fechas tienen formato correcto
- [ ] ✅ Los filtros funcionan
- [ ] ✅ No hay errores en la consola
- [ ] ✅ Los reportes se marcan como exportados

---

## 🎯 SI TODO FUNCIONA

Si todos los checkboxes están marcados:

**🎉 ¡FELICITACIONES! 🎉**

El cambio de XML a CSV está **100% completo y funcional**.

---

## 📞 SOPORTE

Si algo no funciona:

1. Revisar los logs del backend:
   - Terminal donde corre `python manage.py runserver`
   - Buscar errores en rojo

2. Revisar la consola del navegador:
   - DevTools (F12) → Console
   - Buscar errores en rojo

3. Ejecutar pruebas:
   ```powershell
   python test_sistema_completo.py
   ```

4. Verificar archivos modificados:
   - `backend/api/views.py`
   - `frontend/src/services/api.js`
   - `frontend/src/components/dashboard/AlertasManager.js`

---

**Fecha**: 2025-01-19
**Versión**: 1.0.0
**Estado**: ✅ LISTO PARA VERIFICAR
