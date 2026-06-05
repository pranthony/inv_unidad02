
## 🧮 Cálculo de Y — Ingreso per cápita real (S/ constantes 2007)

---

### 📌 FÓRMULA GENERAL

$$Y_{it} = \frac{\sum_{h} (ingreso\_neto_h \times factor\_expansion_h)}{Población_{it}} \times \frac{100}{IPC_t}$$

---

### PASO 1 — Descargar ENAHO desde INEI

🔗 **https://iinei.inei.gob.pe/microdatos/**

- Seleccionar: **Encuesta Nacional de Hogares (ENAHO)**
- Año: cada año de **2010 a 2022** (descargar uno por uno)
- Módulo a usar: **Módulo 500 — Empleo e Ingresos**
- Formato: **.SAV (SPSS)** o **.DTA (Stata)** — ambos abren en Excel con complementos, o puedes usar SPSS/Stata para exportar a Excel

---

### PASO 2 — Variables clave dentro del Módulo 500

| Variable ENAHO | Descripción |
|---|---|
| `UBIGEO` | Código de ubicación geográfica (filtrar por Huánuco = **"10XXXX"**) |
| `DOMINIO` | Dominio geográfico (para identificar área rural/urbana) |
| `i524a1` | **Ingreso neto mensual del trabajador** (en soles corrientes) |
| `FACTOR07` | **Factor de expansión** (peso estadístico de cada hogar) |
| `AÑO` | Año de la encuesta |

---

### PASO 3 — Filtrar por provincia de Huánuco

Los códigos UBIGEO para Huánuco son:

| Provincia | UBIGEO |
|---|---|
| Huánuco | 100101 – 100112 |
| Ambo | 100201 – 100208 |
| Dos de Mayo | 100301 – 100311 |
| Huacaybamba | 100401 – 100404 |
| Huamalíes | 100501 – 100512 |
| Lauricocha | 100601 – 100606 |
| Leoncio Prado | 100701 – 100707 |
| Marañón | 100801 – 100805 |
| Pachitea | 100901 – 100904 |
| Puerto Inca | 101001 – 101005 |
| Yarowilca | 101101 – 101107 |

> Filtrar las primeras **4 dígitos** del UBIGEO: provincia Huánuco = **1001**, Ambo = **1002**, etc.

---

### PASO 4 — Calcular el ingreso promedio ponderado (en soles corrientes)

En Excel, para **cada provincia** y **cada año**:

```
Ingreso_corriente_provincia =
   SUMAPRODUCTO(i524a1 × FACTOR07) / SUMA(FACTOR07)
```

> El factor de expansión es obligatorio porque la ENAHO es una muestra, no un censo. Sin él el promedio estaría sesgado.

---

### PASO 5 — Deflactar a soles constantes de 2007

Necesitas el **Índice de Precios al Consumidor (IPC)** base 2007 = 100.

🔗 Descargarlo del BCRP: **https://estadisticas.bcrp.gob.pe**
- Sección: Precios → IPC Lima Metropolitana → Serie mensual
- Calcular el **promedio anual** del IPC para cada año

| Año | IPC aprox. (base 2007=100) |
|---|---|
| 2010 | 109.2 |
| 2012 | 118.5 |
| 2014 | 128.3 |
| 2016 | 137.8 |
| 2018 | 146.2 |
| 2020 | 151.4 |
| 2022 | 172.6 |

Luego aplicar:

$$Y_{real} = \frac{Ingreso\_corriente}{IPC_t} \times 100$$

---

### PASO 6 — Dividir entre la población provincial

🔗 Población proyectada INEI: **https://www.inei.gob.pe → Estadísticas → Población**

$$Y_{pc} = \frac{Ingreso\_real\_total\_provincia}{Población\_provincial}$$

> Usar las **Estimaciones y Proyecciones de Población** por provincia, que el INEI publica en Excel anualmente.

---

### ✅ RESULTADO FINAL EN EXCEL

Tu columna Y quedará así para cada provincia-año:

```excel
=( SUMAPRODUCTO(i524a1 × FACTOR07) / SUMA(FACTOR07) / IPC_año * 100 )
```

En términos simples: **ingreso mensual promedio ponderado del hogar, en soles del año 2007, por habitante.**

---

### 💡 Consejo práctico

Si manejar el módulo ENAHO en SPSS/Stata es complicado, el INEI también publica tablas **ya procesadas** de ingreso promedio per cápita por departamento en sus **Informes Técnicos de Condiciones de Vida** — aunque a nivel provincial necesitarás sí o sí el microdato. ¿Quieres que te explique cómo hacer este proceso en SPSS o directamente en Excel?