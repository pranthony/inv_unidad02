# INTRODUCCIÓN

## 1.1 Descripción del problema de investigación

En el campo de las finanzas empíricas y la econometría aplicada, el estudio de los canales de transmisión de los choques macroeconómicos hacia el valor patrimonial de las instituciones financieras constituye un área de creciente relevancia. Las corporaciones financieras no operan de manera aislada del entorno macroeconómico; sus balances y, en consecuencia, su valoración de mercado son altamente sensibles tanto a las fluctuaciones del sector real como a los ciclos de liquidez internacional. El periodo comprendido entre 2020 y mediados de 2026 ha configurado un escenario de volatilidad sin precedentes para las economías emergentes, y particularmente para el Perú, marcado por la disrupción de las cadenas globales de suministro tras la pandemia, presiones inflacionarias generalizadas, un ciclo histórico de contracción monetaria liderado por la Reserva Federal (Fed) y el Banco Central de Reserva del Perú (BCRP), así como por episodios de incertidumbre política interna.

En este contexto, el sistema bancario actúa simultáneamente como receptor y como amplificador de los ciclos económicos. En el caso peruano, Credicorp Ltd. (NYSE: BAP) constituye un objeto de estudio idóneo, dado su carácter de holding financiero dominante, que articula entidades líderes en banca comercial (BCP), microfinanzas (Mibanco) y seguros (Pacífico). Su doble cotización en la Bolsa de Valores de Nueva York y la Bolsa de Valores de Lima determina que la dinámica de su rendimiento bursátil no responda únicamente a indicadores de eficiencia corporativa interna, sino que funcione también como un activo proxy del riesgo país y de la estabilidad macroeconómica peruana ante la percepción de los inversionistas internacionales.


## 1.2 Bases teóricas

El sustento conceptual de la valoración de activos financieros ha estado históricamente dominado por el Capital Asset Pricing Model (CAPM), desarrollado de forma independiente por Sharpe (1964) y Lintner (1965), el cual postula que el rendimiento esperado de un activo es una función lineal de su sensibilidad —medida a través del coeficiente Beta— respecto a un único portafolio de mercado agregado:

$$E(R_i) = R_f + \beta_i [E(R_m) - R_f]$$

Sin embargo, el supuesto de que un único índice de mercado captura la totalidad de las fuerzas sistémicas resulta insuficiente al analizar empresas financieras que operan en mercados emergentes. Las corporaciones bancarias presentan una estructura de balance particular, expuesta tanto al riesgo de descalce de tasas de interés como a la salud crediticia de los agentes económicos locales, la cual, en economías primario-exportadoras, depende en gran medida de factores exógenos como los precios internacionales de las materias primas.

Para superar esta limitación de especificación del CAPM, el presente estudio se fundamenta en la Teoría de Valoración por Arbitraje (Arbitrage Pricing Theory, APT) propuesta por Ross (1976). A diferencia del enfoque uniforme, la APT postula que el rendimiento de un activo resulta de su sensibilidad a múltiples factores de riesgo macroeconómicos, comunes e independientes entre sí:

$$R_{i,t} = E(R_{i}) + \beta_{i1}F_{1,t} + \beta_{i2}F_{2,t} + \dots + \beta_{in}F_{n,t} + \varepsilon_{i,t}$$

Sobre la base de este enfoque multifactorial, la presente investigación incorpora dos dimensiones adicionales de carácter sectorial y macroeconómico. Por un lado, se considera el factor sectorial transfronterizo planteado por Flannery y James (1984), quienes documentaron que las acciones de las instituciones financieras presentan una sensibilidad diferenciada ante las condiciones financieras globales y las tasas de interés internacionales, un efecto que los índices de mercado de carácter general, como el S&P 500, tienden a diluir. Por otro lado, se incorpora la teoría de los choques en los términos de intercambio formulada por Mendoza (1995), según la cual, en economías en desarrollo dependientes de la minería, las fluctuaciones de los precios internacionales de los commodities determinan de manera exógena los ciclos económicos internos, el comportamiento de la balanza comercial y los niveles de liquidez del sistema bancario nacional.

## 1.3 Antecedentes de la investigación

La evidencia empírica internacional respalda de manera consistente la naturaleza multifactorial del riesgo bancario. Beck, Demirgüç-Kunt y Levine (2015) examinaron el impacto de los choques de materias primas sobre los sistemas financieros de mercados emergentes y concluyeron que las caídas en los precios de exportación elevan de forma significativa los ratios de morosidad, contraen el margen neto de interés de los bancos y deterioran su valor de mercado de manera sistémica. En el plano de la integración financiera global, Borio y Zhu (2012), a través del denominado "canal de toma de riesgo", evidenciaron cómo las políticas restrictivas de la Reserva Federal y el estrés en los índices financieros de Wall Street se transmiten con rapidez hacia las corporaciones financieras latinoamericanas que emiten deuda o cotizan en mercados internacionales.

En el ámbito nacional, las investigaciones del Banco Central de Reserva del Perú (BCRP) confirman la fuerte dependencia macro-financiera de la economía peruana respecto a sus términos de intercambio. La literatura local ha documentado que el precio del cobre opera como el principal canal de transmisión real hacia el sistema financiero: un incremento en su cotización genera un ingreso significativo de divisas, dinamiza la inversión privada y el empleo, y reduce el riesgo de incumplimiento de los deudores corporativos y de consumo de la banca minorista.

No obstante, la literatura empírica peruana presenta una brecha metodológica relevante. La mayoría de los estudios analiza los determinantes del desempeño bancario mediante indicadores contables tradicionales —como el ROE o el ROA— con datos trimestrales o anuales, dejando de lado el análisis en tiempo real basado en datos bursátiles de alta frecuencia. Asimismo, los escasos estudios centrados en el mercado de valores suelen limitarse al CAPM clásico, sin considerar que una corporación transnacional como Credicorp responde simultáneamente a determinantes sectoriales globales que exceden el riesgo puramente doméstico.

## 1.4 Problema, objetivos e hipótesis de investigación

A partir de las limitaciones identificadas en la literatura previa, el presente artículo aborda la necesidad de cuantificar de manera simultánea y diferenciada las fuerzas que explican el rendimiento bursátil de la banca líder peruana en un contexto de alta turbulencia (2020-2026). La omisión de factores sectoriales transfronterizos o de choques en los términos de intercambio expone a los modelos tradicionales a sesgos por variables omitidas, lo cual distorsiona las decisiones de cobertura y de asignación de capital. En este sentido, se plantea la siguiente pregunta de investigación:

¿En qué medida el rendimiento logarítmico de Credicorp Ltd. es explicado simultáneamente por el riesgo de mercado local, los choques en el precio internacional del cobre y las condiciones de rentabilidad del sector financiero bancario global durante el periodo 2020-2026?

El objetivo general de la investigación es estimar y validar econométricamente un modelo multifactorial del rendimiento bursátil de Credicorp Ltd. bajo el enfoque de la teoría APT, que permita aislar los efectos domésticos de los globales. Como objetivos específicos, el estudio busca:

1. Cuantificar el coeficiente de sensibilidad (Beta) sistemático local, utilizando el iShares MSCI Peru ETF (EPU) como proxy del mercado doméstico.
2. Evaluar el impacto de transmisión de las materias primas a través de los retornos logarítmicos de los futuros del cobre (HG=F).
3. Aislar el riesgo sectorial bancario internacional mediante los retornos del Financial Select Sector SPDR Fund (XLF).

De acuerdo con estos objetivos, se formulan las siguientes hipótesis de investigación:

H1: El rendimiento del mercado local ejerce un impacto positivo y estadísticamente significativo sobre el rendimiento de Credicorp Ltd., constituyéndose como el principal factor de co-movimiento.

H2: La variación del precio del cobre influye de manera positiva y estadísticamente significativa sobre el rendimiento de la acción, operando como proxy de la salud crediticia de la economía real peruana.

H3: El rendimiento del sector financiero global guarda una relación directa y significativa con la cotización de Credicorp Ltd., evidenciando los canales de integración financiera e interdependencia sectorial respecto a Wall Street.

# MATERIALES Y MÉTODOS

## 2.1 Tipo y diseño de investigación

La presente investigación se clasifica como un estudio de tipo aplicado, con enfoque cuantitativo y nivel explicativo. Su carácter aplicado responde al uso de teorías financieras preestablecidas —específicamente la Teoría de Valoración por Arbitraje (APT)— para abordar un problema empírico de valoración en el sector bancario. El enfoque cuantitativo se sustenta en que la recolección, el procesamiento y el contraste de las hipótesis se realizan mediante herramientas estadísticas y modelos econométricos basados en datos numéricos observados.

El diseño de investigación es no experimental, longitudinal y retrospectivo. Es no experimental porque no existe manipulación deliberada de las variables independientes: los fenómenos económicos ocurrieron en su entorno natural y son analizados ex post facto. Su carácter longitudinal y retrospectivo se deriva del análisis de una serie de tiempo continua, construida a partir de registros históricos mensuales correspondientes al periodo comprendido entre enero de 2020 y junio de 2026.

## 2.2 Población y muestra

La población está constituida por el universo de cotizaciones bursátiles históricas de Credicorp Ltd., los índices del sector bancario transfronterizo, el mercado de valores peruano y los precios de los contratos de futuros de metales industriales.

La muestra es de tipo no probabilístico, por conveniencia, y está conformada por las observaciones consolidadas en frecuencia mensual durante el periodo enero 2020 – junio 2026, lo que arroja un tamaño de muestra de N = 77 observaciones mensuales por variable. Este tamaño resulta adecuado para la estimación de modelos de regresión lineal múltiple bajo el supuesto asintótico de Mínimos Cuadrados Ordinarios (MCO).

Los datos corresponden a los precios de cierre ajustados, los cuales incorporan los efectos de los splits corporativos y el pago de dividendos, y fueron agregados a su valor mensual mediante el último precio de cierre disponible de cada mes. La extracción de la información se realizó de manera automatizada en el entorno de programación Python, utilizando la API financiera de código abierto yfinance, con el propósito de garantizar la replicabilidad del estudio.

## 2.3 Operacionalización de variables

A fin de evitar el problema de no estacionariedad —es decir, la presencia de tendencias estocásticas que invalidan los estadísticos t y F convencionales— y prevenir la estimación de una regresión espuria, los precios brutos de los activos fueron transformados en rendimientos logarítmicos continuos, de acuerdo con la siguiente expresión:

$$R_{i,t} = \ln\left(\frac{P_{i,t}}{P_{i,t-1}}\right) = \ln(P_{i,t}) - \ln(P_{i,t-1})$$

donde $P_{i,t}$ representa el precio de cierre ajustado del activo $i$ en el mes $t$, $P_{i,t-1}$ representa el precio de cierre ajustado del mismo activo en el mes inmediatamente anterior, y $\ln$ denota el logaritmo natural.

La operacionalización de las variables que componen el modelo es la siguiente:

La variable dependiente ($Y$) corresponde al rendimiento logarítmico mensual de Credicorp Ltd. ($R_{Credicorp}$), aproximado mediante la cotización de su ticker BAP en la Bolsa de Valores de Nueva York.

La variable independiente $X_1$ corresponde al rendimiento logarítmico mensual del mercado de valores peruano ($R_{Mercado\_Peru}$), aproximado mediante el instrumento iShares MSCI Peru ETF (ticker EPU).

La variable independiente $X_2$ corresponde a la variación logarítmica mensual del precio internacional del cobre ($R_{Cobre}$), instrumentada a través de los precios de los contratos de futuros de cobre (ticker HG=F) negociados en el New York Mercantile Exchange (NYMEX).

La variable independiente $X_3$ corresponde al rendimiento logarítmico mensual del sector financiero e instituciones bancarias internacionales ($R_{Financiero\_Global}$), aproximado mediante el Financial Select Sector SPDR Fund (ticker XLF).

## 2.4 Especificación del modelo econométrico

De acuerdo con los postulados multifactoriales de la Teoría APT (Ross, 1976), se formula un modelo de regresión lineal múltiple, estimado mediante el método de Mínimos Cuadrados Ordinarios (MCO), cuya ecuación estructural es la siguiente:

$$R_{Credicorp, t} = \beta_0 + \beta_1 R_{Mercado\_Peru, t} + \beta_2 R_{Cobre, t} + \beta_3 R_{Financiero\_Global, t} + \varepsilon_t$$

En esta ecuación, $\beta_0$ representa el intercepto del modelo, es decir, el rendimiento promedio esperado de Credicorp cuando las variables explicativas permanecen constantes; $\beta_1$ corresponde al coeficiente de sensibilidad (Beta local), que mide el impacto del mercado peruano sobre el rendimiento de la acción; $\beta_2$ mide la sensibilidad del rendimiento de Credicorp ante variaciones en los términos de intercambio de la economía peruana, aproximados por el precio del cobre; $\beta_3$ representa el parámetro de sensibilidad sectorial internacional, asociado a la transmisión del desempeño del sector financiero global hacia la cotización de Credicorp; y $\varepsilon_t$ es el término de error estocástico del modelo en el periodo $t$, que recoge las perturbaciones aleatorias no observables y el riesgo idiosincrático de la firma.

## 2.5 Pruebas de diagnóstico y robustez

Con el propósito de verificar que los estimadores $\beta$ obtenidos por MCO satisfacen las propiedades de Mejores Estimadores Lineales Insesgados (MELI), se aplicó un conjunto de pruebas de diagnóstico sobre los residuos del modelo ($\varepsilon_t$), empleando la librería econométrica statsmodels de Python.

En primer lugar, se realizó la prueba de normalidad de Jarque-Bera, que evalúa si los residuos siguen una distribución normal a partir de su asimetría y curtosis, bajo la hipótesis nula de que los errores se distribuyen normalmente, condición necesaria para la validez de los intervalos de confianza y de la inferencia individual sobre los coeficientes.

En segundo lugar, se evaluó la presencia de autocorrelación mediante el estadístico de Durbin-Watson, utilizado como indicador preliminar de correlación serial de primer orden, considerándose como valor de referencia un estadístico cercano a 2.0. De manera complementaria, se aplicó la prueba de Breusch-Godfrey (LM test), especificada con dos rezagos mensuales ($p = 2$), bajo la hipótesis nula de ausencia de autocorrelación serial de orden superior.

En tercer lugar, se evaluó el supuesto de homocedasticidad mediante la prueba de Breusch-Pagan, cuya hipótesis nula postula que la varianza de los errores es constante en el tiempo. En caso de rechazarse esta hipótesis ($p$-valor < 0.05), se procedió a reestimar el modelo utilizando errores estándar robustos a heterocedasticidad (HC3), de acuerdo con el enfoque de White.

Finalmente, se evaluó la presencia de multicolinealidad mediante el Factor de Inflación de la Varianza (VIF), considerando que valores de VIF superiores a 5 en alguna de las variables explicativas indicarían una correlación lineal excesiva entre regresores, lo cual incrementaría artificialmente los errores estándar y reduciría la significancia individual de los coeficientes del modelo.