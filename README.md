## 📊 Modelo Econométrico — Tema 8
### *"Infraestructura vial y desarrollo económico local en las provincias de Huánuco"*

---

## 1. VARIABLE DEPENDIENTE (Y)

### 🎯 **Ingreso per cápita provincial** *(en soles constantes)*
Mide el nivel de bienestar económico de la población en cada provincia de Huánuco. Es el indicador más directo del desarrollo económico local y tiene disponibilidad anual por provincia en el INEI.

> **¿Por qué esta y no el PBI?** El PBI regional está disponible solo a nivel departamental, no provincial. El ingreso per cápita de la ENAHO sí se puede desagregar a nivel de provincias de Huánuco, lo que permite el panel de datos.


---

## 2. VARIABLES EXPLICATIVAS (X₁ ... X₅)

---

### 🛣️ X₁ — Kilómetros de red vial pavimentada per cápita
**Fuente:** MTC — Inventario Vial Georeferenciado
**Unidad:** km pavimentados / 1,000 habitantes por provincia
**Hipótesis:** A mayor red vial pavimentada, mayor acceso a mercados y mayor ingreso.
**Respaldo:** Investigaciones en la Macro Región Centro del Perú confirman que la inversión pública en infraestructura vial per cápita explica el aumento del PBI per cápita en un 73.2%; si la inversión vial aumenta 10%, el PBI sube aproximadamente 1.2%.

---

### 💰 X₂ — Inversión pública en transporte (gasto ejecutado, S/.)
**Fuente:** MEF — Consulta Amigable / SIAF, por provincia y año
**Unidad:** Soles ejecutados en función transporte por habitante
**Hipótesis:** Mayor gasto en infraestructura vial impulsa el desarrollo económico local.
**Respaldo:** Investigaciones peruanas con EViews han evaluado cómo el gasto público y privado en infraestructura vial explica el crecimiento económico regional, siendo esta una de las variables centrales del modelo.

---

### 🎓 X₃ — Tasa de asistencia escolar (capital humano)
**Fuente:** INEI — ENAHO / Censos de Población
**Unidad:** Porcentaje de población 6–17 años que asiste a la escuela
**Hipótesis:** El capital humano actúa como complemento de la infraestructura para elevar el ingreso.
**Respaldo:** Estudios peruanos con panel de datos para las 24 regiones confirman que la infraestructura resulta relevante para las diferencias en el producto regional cuando se combina con variables de capital humano, conforme a las teorías neoclásicas de crecimiento.

---

### ⚡ X₄ — Acceso a electricidad (% de hogares con luz)
**Fuente:** INEI — Censos Nacionales / ENAHO por provincia
**Unidad:** Porcentaje de hogares con acceso a red eléctrica pública
**Hipótesis:** La electricidad es infraestructura complementaria que potencia el efecto de las carreteras sobre el ingreso.
**Respaldo:** Estudios econométricos peruanos encontraron impactos significativos de la infraestructura de electricidad sobre la pobreza, siendo incluso más determinante que otras infraestructuras en zonas rurales andinas.

---

### 🌾 X₅ — Valor bruto de producción agrícola provincial
**Fuente:** MIDAGRI — Anuario Estadístico Agropecuario / DRASAM Huánuco
**Unidad:** Miles de soles corrientes de producción agropecuaria por provincia
**Hipótesis:** La infraestructura vial solo eleva el ingreso si hay producción que comercializar; esta variable captura ese efecto indirecto.
**Respaldo:** Investigaciones en zonas rurales peruanas confirman que la infraestructura vial es la base del desarrollo económico porque asegura el suministro de insumos agrícolas y facilita la entrega de productos a los mercados.

---

## 3. EL MODELO ECONOMÉTRICO

$$\ln(Y_{it}) = \beta_0 + \beta_1 \ln(VIAL_{it}) + \beta_2 \ln(GASTO_{it}) + \beta_3 EDUC_{it} + \beta_4 ELEC_{it} + \beta_5 \ln(AGRO_{it}) + \mu_i + \varepsilon_{it}$$

| Símbolo | Significado |
|---|---|
| $Y_{it}$ | Ingreso per cápita, provincia $i$, año $t$ |
| $VIAL_{it}$ | Km vial pavimentada per cápita |
| $GASTO_{it}$ | Inversión pública en transporte per cápita |
| $EDUC_{it}$ | Tasa de asistencia escolar (%) |
| $ELEC_{it}$ | % hogares con electricidad |
| $AGRO_{it}$ | Valor de producción agrícola |
| $\mu_i$ | Efectos fijos por provincia |
| $\varepsilon_{it}$ | Término de error |

> Las variables en **logaritmo** permiten interpretar los coeficientes directamente como **elasticidades** (variación % ante variación %).

---

## 4. ESTRUCTURA DEL PANEL

| Elemento | Detalle |
|---|---|
| **Unidades (i)** | 11 provincias de Huánuco |
| **Período (t)** | 2010–2022 (13 años) |
| **Observaciones totales** | ~143 obs. (panel balanceado) |
| **Estimador sugerido** | Efectos fijos (FE) o efectos aleatorios (RE) → confirmar con **Test de Hausman** en EViews |

---

## 5. PRUEBAS A REALIZAR EN EViews

1. **Test de Hausman** → ¿Efectos fijos o aleatorios?
2. **Test F de efectos fijos** → ¿Son significativos los efectos provincia?
3. **Test de heterocedasticidad** (White/Breusch-Pagan)
4. **Test de autocorrelación** (Wooldridge para panel)
5. **VIF** → Verificar multicolinealidad entre variables

---

¿Quieres que te ayude ahora a construir la base de datos con las fuentes exactas (links INEI, MEF, MTC, MIDAGRI) o que elaboremos el marco teórico y las hipótesis formales del modelo?