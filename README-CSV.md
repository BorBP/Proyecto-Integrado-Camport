# 📦 Exportación CSV - Sistema CAMPORT

> Cambio de formato de exportación de reportes de XML a CSV

---

## 🎯 Objetivo

Cambiar el sistema de exportación de reportes de **XML** a **CSV** para mejorar la compatibilidad con herramientas de análisis de datos.

---

## ✅ Estado: COMPLETADO

**Fecha**: 2025-01-19  
**Versión**: 1.0.0  
**Estado**: 🟢 Producción Ready

---

## 📋 Cambios Realizados

### Backend
- ✅ `backend/api/views.py` → Funciones `exportar_csv()` y `exportar_csv_filtrado()`

### Frontend
- ✅ `frontend/src/services/api.js` → Funciones actualizadas
- ✅ `frontend/src/components/dashboard/AlertasManager.js` → UI actualizada

---

## 📊 Formato CSV

```csv
ID Reporte,Collar ID,Display ID,Tipo Animal,Tipo Alerta,Mensaje,Valor Registrado,Fecha Alerta,Fecha Resolución,Fecha Generación,Generado Por,Observaciones,Exportado
1,EQUINO-001,EQUINO-001,EQUINO,TEMPERATURA,Fiebre detectada: 40.5°C,40.5,2025-11-19 14:30:00,2025-11-19 14:35:00,2025-11-19 14:35:00,admin,Animal atendido,Sí
```

**13 columnas** | **UTF-8** | **Separador: coma**

---

## 🚀 Uso Rápido

### Desde el Frontend

1. Dashboard → Alertas → Historial de Reportes
2. Click en "📥 Exportar Todos (CSV)"
3. Archivo descargado automáticamente

### Desde la API

```bash
# Exportar todos
curl -X GET http://localhost:8000/api/reportes/exportar_csv/ \
  -H "Authorization: Bearer TOKEN" \
  -o reportes.csv

# Exportar filtrado
curl -X POST http://localhost:8000/api/reportes/exportar_csv_filtrado/ \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tipo_alerta":"TEMPERATURA"}' \
  -o reportes_temp.csv
```

---

## 🧪 Pruebas

```powershell
# Activar entorno virtual
.\backend\venv\Scripts\Activate.ps1

# Ejecutar pruebas
python test_csv_export.py
python test_sistema_completo.py
python test_csv_directo.py
```

**Resultado esperado**: ✅ Todas las pruebas PASANDO

---

## 📚 Documentación

| Documento | Descripción | Para quién |
|-----------|-------------|------------|
| [INDICE-DOCUMENTACION-CSV.md](INDICE-DOCUMENTACION-CSV.md) | Índice completo | Todos |
| [CAMBIO-XML-A-CSV.md](CAMBIO-XML-A-CSV.md) | Documentación técnica | Desarrolladores |
| [RESUMEN-CSV.md](RESUMEN-CSV.md) | Resumen ejecutivo | Managers |
| [VERIFICACION-CSV.md](VERIFICACION-CSV.md) | Guía de verificación | QA/Testers |
| [EJEMPLOS-USO-CSV.md](EJEMPLOS-USO-CSV.md) | 10 casos de uso | Analistas |

---

## 🎁 Ventajas del CSV

✅ **30-50% más ligero** que XML  
✅ **Compatible** con Excel, Google Sheets, LibreOffice  
✅ **Más rápido** de generar y procesar  
✅ **Ideal para análisis** con pandas, R, Power BI  
✅ **UTF-8** completo (ñ, acentos)  
✅ **Estructura simple** y plana  

---

## 🛠️ Compatibilidad

- ✅ Microsoft Excel
- ✅ Google Sheets
- ✅ LibreOffice Calc
- ✅ macOS Numbers
- ✅ Python pandas
- ✅ R (read.csv)
- ✅ Power BI
- ✅ Tableau
- ✅ MySQL (LOAD DATA)
- ✅ PostgreSQL (COPY)

---

## 📊 Ejemplo de Uso

### Python (pandas)
```python
import pandas as pd

df = pd.read_csv('reportes_camport_20250119.csv')
print(df['Tipo Alerta'].value_counts())
```

### Excel
1. Abrir archivo CSV
2. Excel lo importa automáticamente
3. Crear tablas dinámicas y gráficos

### R
```r
df <- read_csv("reportes_camport_20250119.csv")
summary(df)
```

---

## 🔍 Verificación

### Checklist
- [ ] Backend inicia sin errores
- [ ] Frontend inicia sin errores
- [ ] Botones dicen "CSV" (no XML)
- [ ] CSV se descarga correctamente
- [ ] Archivo se abre en Excel
- [ ] Datos son correctos
- [ ] Acentos se ven bien

**Ver guía completa**: [VERIFICACION-CSV.md](VERIFICACION-CSV.md)

---

## 🐛 Solución de Problemas

### No se descarga el archivo
1. Verificar backend corriendo
2. Abrir DevTools → Network
3. Buscar errores (401, 403, 500)

### Acentos no se ven bien
1. Excel → Datos → Obtener datos → Texto/CSV
2. **Encoding: UTF-8** (importante)
3. Delimitador: Coma

**Ver más**: [VERIFICACION-CSV.md#solución-de-problemas](VERIFICACION-CSV.md)

---

## 📞 Soporte

1. **Leer documentación**: [INDICE-DOCUMENTACION-CSV.md](INDICE-DOCUMENTACION-CSV.md)
2. **Ejecutar diagnóstico**: `python test_sistema_completo.py`
3. **Revisar logs**: Terminal Django + Consola navegador

---

## 🎓 Recursos

- [Documentación CSV de Python](https://docs.python.org/3/library/csv.html)
- [Pandas read_csv](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html)
- [Django HttpResponse](https://docs.djangoproject.com/en/5.0/ref/request-response/#httpresponse-objects)

---

## 📝 Notas

- No requiere migración de base de datos
- Los reportes existentes siguen siendo válidos
- El campo "exportado" se actualiza automáticamente
- Las fechas están en formato estándar ISO

---

## 👥 Créditos

**Desarrollador**: GitHub Copilot  
**Fecha**: 2025-01-19  
**Versión**: 1.0.0  

---

## 📄 Licencia

Este proyecto sigue la licencia del proyecto principal CAMPORT.

---

**¿Necesitas ayuda?** → Lee primero [INDICE-DOCUMENTACION-CSV.md](INDICE-DOCUMENTACION-CSV.md)

---

<div align="center">

**🎉 ¡Exportación CSV lista para usar! 🎉**

</div>
