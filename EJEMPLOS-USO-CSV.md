# 📊 EJEMPLOS DE USO DEL CSV EXPORTADO

## Casos de Uso Prácticos

---

## 1. 📈 Análisis en Excel

### Abrir el archivo
1. Abrir Excel
2. Archivo → Abrir
3. Seleccionar el CSV descargado
4. Excel lo importa automáticamente

### Crear tabla dinámica
1. Seleccionar todos los datos
2. Insertar → Tabla dinámica
3. Arrastrar "Tipo Alerta" a Filas
4. Arrastrar "ID Reporte" a Valores (contar)
5. Ver distribución de alertas por tipo

### Gráfico de barras
1. Seleccionar columna "Tipo Alerta"
2. Insertar → Gráfico de barras
3. Visualizar qué tipo de alerta es más común

### Filtros
1. Seleccionar encabezados
2. Datos → Filtro
3. Filtrar por fecha, animal, tipo, etc.

---

## 2. 🐍 Análisis en Python (pandas)

### Cargar CSV
```python
import pandas as pd
import matplotlib.pyplot as plt

# Cargar datos
df = pd.read_csv('reportes_camport_20250119.csv')

# Ver primeras filas
print(df.head())
```

### Estadísticas básicas
```python
# Contar alertas por tipo
print(df['Tipo Alerta'].value_counts())

# Estadísticas de valores registrados
print(df['Valor Registrado'].describe())

# Alertas por animal
print(df.groupby('Collar ID').size())
```

### Análisis de temperatura
```python
# Filtrar solo alertas de temperatura
temp = df[df['Tipo Alerta'] == 'TEMPERATURA']

# Convertir valores a numérico
temp['Valor'] = pd.to_numeric(temp['Valor Registrado'], errors='coerce')

# Estadísticas
print(f"Temperatura promedio: {temp['Valor'].mean():.2f}°C")
print(f"Temperatura máxima: {temp['Valor'].max():.2f}°C")
print(f"Temperatura mínima: {temp['Valor'].min():.2f}°C")
```

### Gráficos
```python
# Gráfico de barras: alertas por tipo
df['Tipo Alerta'].value_counts().plot(kind='bar')
plt.title('Distribución de Alertas por Tipo')
plt.xlabel('Tipo de Alerta')
plt.ylabel('Cantidad')
plt.show()

# Gráfico de pastel: alertas por animal
df['Collar ID'].value_counts().plot(kind='pie', autopct='%1.1f%%')
plt.title('Alertas por Animal')
plt.show()
```

### Análisis temporal
```python
# Convertir fechas
df['Fecha Alerta'] = pd.to_datetime(df['Fecha Alerta'])

# Agrupar por día
por_dia = df.groupby(df['Fecha Alerta'].dt.date).size()
por_dia.plot(kind='line')
plt.title('Alertas por Día')
plt.xlabel('Fecha')
plt.ylabel('Cantidad de Alertas')
plt.xticks(rotation=45)
plt.show()
```

---

## 3. 📊 Análisis en R

```r
# Cargar datos
library(tidyverse)

df <- read_csv("reportes_camport_20250119.csv")

# Ver estructura
glimpse(df)

# Contar por tipo
df %>% 
  group_by(`Tipo Alerta`) %>% 
  summarise(n = n()) %>%
  arrange(desc(n))

# Gráfico
ggplot(df, aes(x = `Tipo Alerta`)) +
  geom_bar(fill = "steelblue") +
  labs(title = "Alertas por Tipo",
       x = "Tipo de Alerta",
       y = "Cantidad") +
  theme_minimal()
```

---

## 4. 📈 Power BI

### Importar datos
1. Abrir Power BI Desktop
2. Obtener datos → Texto/CSV
3. Seleccionar archivo CSV
4. Click en "Cargar"

### Crear visualizaciones
1. **Tarjeta**: Total de reportes
2. **Gráfico de barras**: Alertas por tipo
3. **Gráfico circular**: Distribución por animal
4. **Tabla**: Detalles de alertas
5. **Línea temporal**: Alertas por fecha

### Medidas DAX
```dax
Total Alertas = COUNT(Reportes[ID Reporte])

Temperatura Promedio = 
CALCULATE(
    AVERAGE(Reportes[Valor Registrado]),
    Reportes[Tipo Alerta] = "TEMPERATURA"
)

Alertas Críticas = 
CALCULATE(
    COUNT(Reportes[ID Reporte]),
    OR(
        Reportes[Tipo Alerta] = "PERIMETRO",
        AND(
            Reportes[Tipo Alerta] = "TEMPERATURA",
            Reportes[Valor Registrado] > 40
        )
    )
)
```

---

## 5. 🔍 Google Sheets

### Importar CSV
1. Abrir Google Sheets
2. Archivo → Importar
3. Subir → Seleccionar CSV
4. Click en "Importar datos"

### Fórmulas útiles
```
// Contar alertas de temperatura
=COUNTIF(E:E, "TEMPERATURA")

// Temperatura promedio
=AVERAGEIF(E:E, "TEMPERATURA", G:G)

// Alertas por animal
=UNIQUE(B:B)
=COUNTIF(B:B, "EQUINO-001")

// Filtrar por fecha
=FILTER(A:M, H:H >= DATE(2025,1,1))
```

### Tabla dinámica
1. Datos → Tabla dinámica
2. Filas: Tipo Alerta
3. Valores: CUENTA de ID Reporte
4. Columnas: Collar ID

---

## 6. 📧 Envío por Email Automatizado

### Python
```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def enviar_reporte(csv_path, destinatario):
    msg = MIMEMultipart()
    msg['Subject'] = 'Reporte de Alertas - CAMPORT'
    msg['From'] = 'sistema@camport.com'
    msg['To'] = destinatario
    
    # Adjuntar CSV
    with open(csv_path, 'rb') as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 
                       f'attachment; filename={os.path.basename(csv_path)}')
        msg.attach(part)
    
    # Enviar
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login('usuario@gmail.com', 'password')
    smtp.send_message(msg)
    smtp.quit()
```

---

## 7. 🗄️ Importar a Base de Datos

### MySQL
```sql
LOAD DATA LOCAL INFILE 'reportes_camport_20250119.csv'
INTO TABLE reportes
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(id_reporte, collar_id, display_id, tipo_animal, tipo_alerta, 
 mensaje, valor_registrado, @fecha_alerta, @fecha_resolucion, 
 @fecha_generacion, generado_por, observaciones, exportado)
SET fecha_alerta = STR_TO_DATE(@fecha_alerta, '%Y-%m-%d %H:%i:%s'),
    fecha_resolucion = STR_TO_DATE(@fecha_resolucion, '%Y-%m-%d %H:%i:%s'),
    fecha_generacion = STR_TO_DATE(@fecha_generacion, '%Y-%m-%d %H:%i:%s');
```

### PostgreSQL
```sql
COPY reportes (
    id_reporte, collar_id, display_id, tipo_animal, tipo_alerta,
    mensaje, valor_registrado, fecha_alerta, fecha_resolucion,
    fecha_generacion, generado_por, observaciones, exportado
)
FROM '/path/to/reportes_camport_20250119.csv'
DELIMITER ','
CSV HEADER;
```

---

## 8. 🔄 Integración con Sistemas Externos

### API REST
```python
import requests
import csv

# Leer CSV
with open('reportes_camport_20250119.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Enviar cada reporte a API externa
        response = requests.post('https://api.externa.com/alertas', json={
            'animal_id': row['Collar ID'],
            'tipo': row['Tipo Alerta'],
            'valor': row['Valor Registrado'],
            'fecha': row['Fecha Alerta']
        })
        print(f"Enviado: {row['ID Reporte']} - Status: {response.status_code}")
```

---

## 9. 📱 Dashboard en Tiempo Real

### Streamlit (Python)
```python
import streamlit as st
import pandas as pd
import plotly.express as px

st.title('📊 Dashboard de Alertas CAMPORT')

# Cargar datos
df = pd.read_csv('reportes_camport_20250119.csv')

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total Alertas", len(df))
col2.metric("Animales Afectados", df['Collar ID'].nunique())
col3.metric("Promedio Temp", f"{df[df['Tipo Alerta']=='TEMPERATURA']['Valor Registrado'].mean():.1f}°C")

# Gráficos
st.plotly_chart(
    px.bar(df['Tipo Alerta'].value_counts().reset_index(), 
           x='index', y='Tipo Alerta', 
           title='Distribución de Alertas')
)

# Tabla
st.dataframe(df)
```

---

## 10. 🤖 Machine Learning

### Predicción de alertas
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Preparar datos
df['Fecha'] = pd.to_datetime(df['Fecha Alerta'])
df['hora'] = df['Fecha'].dt.hour
df['dia_semana'] = df['Fecha'].dt.dayofweek

# Features
X = df[['hora', 'dia_semana']]
y = df['Tipo Alerta']

# Entrenar
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Predecir
accuracy = model.score(X_test, y_test)
print(f"Precisión: {accuracy:.2%}")
```

---

## 💡 TIPS ADICIONALES

### Automatización
- Crear script para descargar CSV automáticamente cada día
- Usar cron (Linux) o Task Scheduler (Windows)
- Enviar reporte por email automáticamente

### Visualización
- Crear dashboard en Tableau
- Usar Google Data Studio
- Implementar Grafana

### Análisis Avanzado
- Detección de anomalías
- Clustering de animales por comportamiento
- Predicción de fugas

---

**Fecha**: 2025-01-19
**Versión**: 1.0.0
**Autor**: GitHub Copilot
