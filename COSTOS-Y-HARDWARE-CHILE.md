# 💰 COSTOS Y HARDWARE PARA SISTEMA CAMPORT REAL - CHILE

**Documento:** Presupuesto y Especificaciones de Hardware  
**Moneda:** Pesos Chilenos (CLP)  
**Tipo de Cambio Referencial:** 1 USD = 950 CLP (Nov 2025)  
**Fecha:** Noviembre 2025

---

## 📋 RESUMEN EJECUTIVO DE COSTOS

### Inversión Inicial (50 animales)

| Categoría | Cantidad | Costo Unitario | Total CLP |
|-----------|----------|----------------|-----------|
| **Collares GPS** | 50 unidades | $80.000 | **$4.000.000** |
| **Gateways LoRa** | 3 unidades | $280.000 | **$840.000** |
| **Servidor Local** | 1 unidad | $1.200.000 | **$1.200.000** |
| **Infraestructura Red** | 1 set | $450.000 | **$450.000** |
| **Herramientas/Repuestos** | - | - | **$380.000** |
| **Instalación** | - | - | **$500.000** |
| | | **TOTAL INICIAL** | **$7.370.000** |

### Costos Operacionales Anuales

| Categoría | Mensual | Anual |
|-----------|---------|-------|
| **Internet/Conectividad** | $30.000 | $360.000 |
| **Electricidad** | $15.000 | $180.000 |
| **Mantenimiento** | $50.000 | $600.000 |
| **Reemplazo Baterías** | $40.000 | $480.000 |
| **Dominio + SSL** | $4.200 | $50.000 |
| **Respaldo Cloud (opcional)** | $25.000 | $300.000 |
| | **TOTAL MENSUAL** | **$164.200** |
| | **TOTAL ANUAL** | **$1.970.000** |

### **INVERSIÓN TOTAL PRIMER AÑO: $9.340.000 CLP**

### **COSTO POR ANIMAL/AÑO: $186.800 CLP**

---

## 🔧 ESPECIFICACIONES DE HARDWARE DETALLADAS

### 1. COLLAR GPS PARA GANADO

#### Opción A: Collar Económico (Recomendado para Piloto)

**Componentes:**

| Componente | Modelo/Especificación | Precio CLP | Proveedor Chile |
|------------|----------------------|------------|-----------------|
| **Microcontrolador** | ESP32-WROOM-32D | $7.500 | vistronica.com |
| **GPS Module** | NEO-6M con antena | $12.000 | diyelectric.cl |
| **Sensor Temperatura** | DHT22 / DS18B20 | $4.000 | electan.com |
| **Sensor FC** | MAX30102 (pulso/oximetría) | $8.500 | vistronica.com |
| **Módulo LoRa** | SX1278 Ra-02 433MHz | $10.500 | diyelectric.cl |
| **Batería** | Li-Ion 18650 3.7V 3000mAh | $6.000 | baterias.cl |
| **Panel Solar** | 5V 1W 110x60mm | $12.000 | solartec.cl |
| **Módulo Carga** | TP4056 con protección | $1.500 | electan.com |
| **Carcasa** | Impermeable IP67 100x68x50mm | $15.000 | carcasas.cl |
| **PCB Custom** | Fabricación local | $8.000 | pcblatam.com |
| **Conectores/Cables** | Diversos | $3.000 | vistronica.com |
| **Correas/Montaje** | Collar ajustable resistente | $7.000 | agricola-cl.com |
| | | **TOTAL** | **~$95.000** |

**Características:**
- Autonomía: 30-45 días con panel solar
- Rango LoRa: Hasta 5km en campo abierto
- Frecuencia GPS: Cada 60 segundos
- Peso: ~250 gramos
- Resistencia: IP67 (polvo y agua)

#### Opción B: Collar Profesional (Producción a Escala)

| Componente | Modelo/Especificación | Precio CLP | Proveedor |
|------------|----------------------|------------|-----------|
| **Microcontrolador** | Raspberry Pi Zero 2 W | $16.000 | raspberrypi.cl |
| **GPS Module** | u-blox NEO-M8N | $35.000 | ublox.com (importado) |
| **Sensor Temperatura** | MLX90614 infrarrojo | $22.000 | sparkfun.cl |
| **Sensor FC** | AD8232 ECG + electrodos | $18.000 | biomedica.cl |
| **Acelerómetro** | MPU6050 6DOF | $4.500 | electan.com |
| **Módulo 4G** | SIM7600SA-H LTE Cat4 | $38.000 | simcom.cl |
| **Batería** | LiPo 3.7V 6000mAh | $18.000 | baterias.cl |
| **Panel Solar** | 6V 2W 125x125mm | $22.000 | solartec.cl |
| **Regulador** | Buck-Boost ajustable | $5.500 | vistronica.com |
| **Carcasa** | Profesional IP68 + antena | $45.000 | pelican-chile.cl |
| **PCB Custom** | Fabricación profesional | $15.000 | pcblatam.com |
| **SIM Card** | Entel M2M IoT | $0 | entel.cl |
| **Correas/Montaje** | Profesional reforzado | $12.000 | agropecuaria.cl |
| | | **TOTAL** | **~$251.000** |

**Características:**
- Autonomía: 60-90 días con panel solar
- Conectividad: 4G LTE con fallback a LoRa
- Frecuencia GPS: Cada 30 segundos
- Sensores adicionales: Acelerómetro 3 ejes
- Peso: ~350 gramos
- Resistencia: IP68 (sumergible)
- OTA Updates: Actualización remota de firmware

---

### 2. GATEWAY / ANTENA RECEPTORA

#### Gateway LoRa (Recomendado)

| Componente | Modelo/Especificación | Precio CLP | Proveedor |
|------------|----------------------|------------|-----------|
| **Computadora** | Raspberry Pi 4 Model B 4GB | $65.000 | raspberrypi.cl |
| **Concentrador LoRa** | RAK2245 Pi HAT 915MHz | $120.000 | rakwireless.cl |
| **Antena LoRa** | Omnidireccional 8dBi 915MHz | $35.000 | antenas.cl |
| **GPS (opcional)** | Para sincronización tiempo | $12.000 | diyelectric.cl |
| **Carcasa Exterior** | IP65 para exterior | $45.000 | pelican-chile.cl |
| **PoE Injector** | Para alimentación remota | $18.000 | networking.cl |
| **Cable Red** | Cat6 exterior 50m | $25.000 | cables.cl |
| **SSD 128GB** | Almacenamiento local | $28.000 | spdigital.cl |
| **Fuente 12V** | Con respaldo batería | $22.000 | energía.cl |
| **Montaje/Poste** | Soporte y mástil | $15.000 | construccion.cl |
| | | **TOTAL** | **~$385.000** |

**Reducido a:** $280.000 (sin opcionales)

**Características:**
- Cobertura: 5-10km en terreno abierto
- Canales: 8 canales simultáneos
- Capacidad: Hasta 500 collares por gateway
- Conectividad: Ethernet + WiFi + 4G backup
- Alimentación: PoE o 12V DC
- Consumo: 10W promedio

---

### 3. SERVIDOR CENTRAL

#### Opción A: Servidor Local (On-Premise)

| Componente | Especificación | Precio CLP |
|------------|----------------|------------|
| **Servidor Dell/HP** | PowerEdge T340 o similar | $850.000 |
| • CPU | Intel Xeon E-2224 (4 core) | - |
| • RAM | 16GB DDR4 ECC | - |
| • Almacenamiento | 2x 2TB HDD RAID-1 | - |
| • Red | 2x 1Gbps Ethernet | - |
| **SSD Sistema** | 240GB SATA SSD | $45.000 |
| **UPS** | APC 1500VA con baterías | $280.000 |
| **Switch Red** | 8 puertos Gigabit PoE | $85.000 |
| **Rack 6U** | Gabinete con ventilación | $120.000 |
| | **TOTAL** | **$1.380.000** |

**Reducido a:** $1.200.000 (config básica)

#### Opción B: Servidor Cloud (AWS/Azure/Google Cloud)

**Estimación Mensual Chile (AWS sa-east-1 - São Paulo):**

| Servicio | Especificación | Precio Mensual CLP |
|----------|----------------|-------------------|
| **EC2 Instance** | t3.medium (2vCPU, 4GB RAM) | $45.000 |
| **RDS PostgreSQL** | db.t3.micro (1vCPU, 1GB) | $28.000 |
| **ElastiCache Redis** | cache.t3.micro | $22.000 |
| **S3 Storage** | 100GB + transferencia | $8.000 |
| **CloudWatch Logs** | Monitoreo básico | $5.000 |
| **Data Transfer** | 500GB/mes salida | $42.000 |
| | **TOTAL MENSUAL** | **~$150.000** |
| | **TOTAL ANUAL** | **$1.800.000** |

**Alternativa Cloud Nacional (Genesys o ENTEL Cloud):**
- Más caro (~20-30% más)
- Pero datos en Chile (mejor latencia)
- Soporte en español

---

## 📡 CONECTIVIDAD Y SERVICIOS

### Conectividad de Datos

#### Para Collares con 4G/LTE

| Proveedor | Plan | Datos | Precio Mensual | Anual |
|-----------|------|-------|----------------|-------|
| **Entel M2M** | IoT 10MB | 10MB | $2.000 | $24.000 |
| **Movistar IoT** | Smart 20MB | 20MB | $2.500 | $30.000 |
| **Claro M2M** | Básico 15MB | 15MB | $2.200 | $26.400 |

**Para 50 collares 4G:** $2.000 x 50 = **$100.000/mes = $1.200.000/año**

#### Para Gateway

| Servicio | Proveedor | Precio Mensual |
|----------|-----------|----------------|
| **Internet Fibra** | Movistar/VTR/Mundo | $25.000 |
| **4G Backup** | Entel Datos 50GB | $15.000 |
| **IP Fija (opcional)** | Cualquier ISP | $8.000 |

**Total Gateway:** $40.000-48.000/mes

---

## 🛠️ COSTOS DE DESARROLLO Y SERVICIOS

### Software y Licencias

| Servicio | Tipo | Costo Anual CLP |
|----------|------|-----------------|
| **Dominio .cl** | camport.cl | $12.000 |
| **Certificado SSL** | Let's Encrypt | $0 (Gratis) |
| **MQTT Broker Cloud** | HiveMQ/CloudMQTT | $0-$95.000 |
| **Servicio Email** | SendGrid/Mailgun | $0-$45.000 |
| **Monitoreo** | UptimeRobot básico | $0 |
| **Backup Cloud** | Backblaze B2 100GB | $50.000 |
| | **TOTAL** | **$62.000-202.000** |

### Desarrollo (Si contratas)

| Ítem | Horas Estimadas | Tarifa/Hora | Total CLP |
|------|----------------|-------------|-----------|
| **Modificación Backend** | 80h | $25.000 | $2.000.000 |
| **Desarrollo App Móvil** | 120h | $28.000 | $3.360.000 |
| **Firmware Collar** | 100h | $30.000 | $3.000.000 |
| **Testing e Integración** | 60h | $22.000 | $1.320.000 |
| **Documentación** | 20h | $18.000 | $360.000 |
| | | **TOTAL** | **$10.040.000** |

**Nota:** Si lo desarrollas tú mismo, ahorras estos costos pero inviertes ~380 horas de trabajo.

---

## 🔋 MANTENIMIENTO Y OPERACIÓN

### Mantenimiento Preventivo

| Actividad | Frecuencia | Costo Unitario | Anual |
|-----------|------------|----------------|-------|
| **Revisión Collares** | Trimestral | $5.000/collar | $240.000 |
| **Cambio Baterías** | 2 años (25/año) | $18.000 | $450.000 |
| **Limpieza Sensores** | Semestral | $3.000/collar | $72.000 |
| **Actualización Firmware** | Anual | $2.000/collar | $24.000 |
| **Mantención Gateways** | Trimestral | $15.000 | $45.000 |
| **Revisión Servidor** | Trimestral | $35.000 | $105.000 |
| | | **TOTAL** | **$936.000** |

### Repuestos Estimados (Anual)

| Ítem | Cantidad | Precio | Total |
|------|----------|--------|-------|
| **Collares completos** | 3 | $95.000 | $285.000 |
| **Baterías 18650** | 30 | $6.000 | $180.000 |
| **Paneles solares** | 5 | $12.000 | $60.000 |
| **Módulos GPS** | 4 | $12.000 | $48.000 |
| **Módulos LoRa** | 3 | $10.500 | $31.500 |
| **Correas/montaje** | 10 | $7.000 | $70.000 |
| | | **TOTAL** | **$674.500** |

---

## 📊 COMPARATIVA DE OPCIONES

### Escenario 1: Básico LoRa (50 animales)

| Categoría | Costo |
|-----------|-------|
| **Collares Económicos** (50) | $4.750.000 |
| **Gateways LoRa** (3) | $840.000 |
| **Servidor Local** | $1.200.000 |
| **Infraestructura** | $450.000 |
| **Instalación** | $500.000 |
| **TOTAL INICIAL** | **$7.740.000** |
| **Operación Anual** | **$770.000** |
| | |
| **Total 3 años** | **$10.050.000** |
| **Costo/animal/año** | **$66.000** |

### Escenario 2: Profesional 4G (50 animales)

| Categoría | Costo |
|-----------|-------|
| **Collares Profesionales** (50) | $12.550.000 |
| **Gateways Hybrid** (2) | $560.000 |
| **Cloud Server** (anual) | $1.800.000 |
| **Conectividad 4G** (anual) | $1.200.000 |
| **Infraestructura** | $350.000 |
| **TOTAL INICIAL** | **$13.460.000** |
| **Operación Anual** | **$4.170.000** |
| | |
| **Total 3 años** | **$25.970.000** |
| **Costo/animal/año** | **$173.000** |

### Escenario 3: Híbrido (Recomendado)

| Categoría | Costo |
|-----------|-------|
| **Collares Mixtos** 30 básicos + 20 pro | $8.870.000 |
| **Gateways LoRa** (3) | $840.000 |
| **Servidor Local + Cloud Backup** | $1.500.000 |
| **Conectividad 4G** (20 collares) | $480.000 |
| **Infraestructura** | $400.000 |
| **TOTAL INICIAL** | **$12.090.000** |
| **Operación Anual** | **$2.150.000** |
| | |
| **Total 3 años** | **$18.540.000** |
| **Costo/animal/año** | **$123.600** |

---

## 🏪 PROVEEDORES RECOMENDADOS EN CHILE

### Electrónica y Componentes

| Proveedor | Categoría | Ubicación | Web |
|-----------|-----------|-----------|-----|
| **Vistronica** | Componentes generales | Santiago | vistronica.com |
| **DIY Electric** | IoT y módulos | Santiago | diyelectric.cl |
| **Electan** | Sensores y Arduino | Santiago | electan.com |
| **SpDigital** | Computación y storage | Santiago | spdigital.cl |
| **PC Factory** | Servidores y red | Nacional | pcfactory.cl |

### Servicios Cloud

| Proveedor | Tipo | Ubicación Datos |
|-----------|------|-----------------|
| **AWS** | Cloud global | São Paulo (BR) |
| **Google Cloud** | Cloud global | São Paulo (BR) |
| **Genesys** | Cloud nacional | Santiago |
| **ENTEL Cloud** | Cloud nacional | Santiago |

### Conectividad IoT

| Proveedor | Servicio | Cobertura |
|-----------|----------|-----------|
| **Entel** | M2M IoT 4G | Nacional |
| **Movistar** | IoT Connect | Nacional |
| **Claro** | M2M Empresas | Nacional |
| **WOM** | IoT (limitado) | Urbano |

### Fabricación PCB

| Proveedor | Servicio | Tiempo |
|-----------|----------|--------|
| **PCB Latam** | Fabricación local | 7-10 días |
| **JLCPCB** | Fabricación China | 15-20 días |
| **PCBWay** | Fabricación China | 12-18 días |

### Carcasas y Montaje

| Proveedor | Producto | Ubicación |
|-----------|----------|-----------|
| **Pelican Chile** | Carcasas profesionales | Santiago |
| **Sodimac** | Materiales construcción | Nacional |
| **Easy** | Herramientas y montaje | Nacional |

---

## 💡 ESTRATEGIAS DE AHORRO

### 1. Fabricación Propia de PCBs

**Ahorro:** $3.000-8.000 por collar

- Diseñar PCB custom que integre todos los componentes
- Mandar a fabricar en lote (mínimo 50 unidades)
- Costo PCB fabricado: $5.000-8.000 c/u en lote
- Ahorro vs comprar módulos separados: 30-40%

### 2. Compra en Volumen

**Ahorro:** 15-25% en componentes

| Componente | Precio Unit | Precio 50+ | Ahorro |
|------------|-------------|------------|--------|
| ESP32 | $7.500 | $5.500 | 27% |
| GPS NEO-6M | $12.000 | $8.500 | 29% |
| LoRa SX1278 | $10.500 | $7.800 | 26% |
| Baterías | $6.000 | $4.500 | 25% |

### 3. Energía Solar Optimizada

**Ahorro:** $280.000/año en reemplazo de baterías

- Dimensionar correctamente paneles solares
- Usar baterías de mayor calidad (menor degradación)
- Implementar modo sleep inteligente
- ROI en 18 meses

### 4. Servidor Local vs Cloud (3 años)

| Opción | Costo 3 años |
|--------|--------------|
| Cloud AWS | $5.400.000 |
| Servidor Local | $1.200.000 + $450.000 (electricidad) = $1.650.000 |
| **Ahorro** | **$3.750.000** |

### 5. LoRa vs 4G para Comunicación

| Opción | Costo 50 collares/año |
|--------|----------------------|
| 4G ($2.000/mes x 50) | $1.200.000 |
| LoRa (infraestructura amortizada) | $0 |
| **Ahorro** | **$1.200.000/año** |

---

## 📈 RETORNO DE INVERSIÓN

### Beneficios Cuantificables

| Beneficio | Ahorro Anual Estimado | Fuente |
|-----------|----------------------|--------|
| **Reducción pérdida de ganado** | $2.500.000 | Detección temprana fugas |
| **Optimización alimentación** | $800.000 | Monitoreo de movimiento/rumia |
| **Reducción costos veterinarios** | $600.000 | Detección temprana enfermedades |
| **Mejora reproducción** | $450.000 | Monitoreo de celo |
| **Reducción mano de obra** | $1.200.000 | Menos tiempo en vigilancia |
| | **TOTAL** | **$5.550.000/año** |

### Análisis ROI (Escenario Híbrido)

| Año | Inversión | Operación | Ahorro | Balance |
|-----|-----------|-----------|--------|---------|
| **Año 0** | -$12.090.000 | $0 | $0 | -$12.090.000 |
| **Año 1** | $0 | -$2.150.000 | +$5.550.000 | -$8.690.000 |
| **Año 2** | $0 | -$2.150.000 | +$5.550.000 | -$5.290.000 |
| **Año 3** | $0 | -$2.150.000 | +$5.550.000 | -$1.890.000 |
| **Año 4** | $0 | -$2.150.000 | +$5.550.000 | +$1.510.000 ✅ |

**ROI Break-even:** 3.5 años  
**ROI a 5 años:** +$5.110.000 CLP

---

## 🎯 RECOMENDACIÓN FINAL

### Para Proyecto de Título/Piloto (10-20 animales)

**Presupuesto:** $2.500.000 - $3.500.000

- 15 collares económicos LoRa
- 1 gateway LoRa
- Servidor en Raspberry Pi 4
- Desarrollo propio del software (ya tienes 80%)

### Para Producción Real (50-100 animales)

**Presupuesto Inicial:** $12.000.000 - $18.000.000

- Collares híbridos (mezcla económicos + profesionales)
- 3-4 gateways LoRa con backup 4G
- Servidor local con backup cloud
- App móvil desarrollo externo

### Para Escala Comercial (500+ animales)

**Presupuesto:** $80.000.000+

- Collares profesionales fabricación custom
- Infraestructura distribuida multi-granja
- Cloud enterprise con SLA
- Equipo de soporte dedicado

---

## 📞 CONTACTO PROVEEDORES PRINCIPALES

### Electrónica

**Vistronica**
- 📍 Av. Libertador Bernardo O'Higgins 2842, Santiago
- 📞 +56 2 2698 6800
- 🌐 www.vistronica.com

**DIY Electric**
- 📍 Providencia, Santiago
- 📧 ventas@diyelectric.cl
- 🌐 www.diyelectric.cl

### Servicios Cloud

**AWS Chile**
- 📧 aws-chile@amazon.com
- 🌐 aws.amazon.com/es/contact-us

**Genesys Cloud Chile**
- 📞 600 400 7000
- 🌐 www.genesys.com/es-cl

### Conectividad IoT

**Entel Empresas IoT**
- 📞 600 360 0123
- 📧 empresas@entel.cl
- 🌐 www.entel.cl/empresas/iot

---

**Documento creado para:** Proyecto CAMPORT  
**Última actualización:** Noviembre 2025  
**Validez precios:** 3-6 meses (sujeto a variación)

---

## 📝 NOTAS IMPORTANTES

1. **Precios son referenciales** y pueden variar según:
   - Tipo de cambio USD/CLP
   - Disponibilidad de stock
   - Volumen de compra
   - Temporada del año

2. **IVA no incluido** en la mayoría de los precios mostrados (agregar 19%)

3. **Aranceles de importación** no incluidos para componentes importados (puede agregar 6-15%)

4. **Garantías** varían según proveedor (verificar antes de comprar)

5. **Contactar proveedores** directamente para cotización actualizada y formal

---

**FIN DEL DOCUMENTO DE COSTOS**
