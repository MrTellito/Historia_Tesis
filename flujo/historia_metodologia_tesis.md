# La Odisea del Dato: La Historia Completa de Nuestra Metodología de Priorización

> **Documento Maestro de Sustentación Metodológica**  
> *Autor:* Tesista / Equipo de Investigación  
> *Caso de Estudio:* Registro de Precios del SCOP (Osinergmin, Perú, 2020–2026)  
> *Propósito:* Explicación narrativa, profunda y rigurosa de cada decisión de ingeniería, modelado y validación: el porqué de lo que se hizo y el porqué inapelable de lo que se descartó.

---

## Prólogo: El Dilema en las Oficinas de Osinergmin (El Dolor del Negocio)

Imagina que eres el Director de Supervisión de Hidrocarburos en el organismo regulador del Perú (**Osinergmin**). 

Bajo tu jurisdicción operan más de **24,000 establecimientos** a nivel nacional: desde grandes estaciones de servicio en avenidas principales de Lima hasta pequeños grifos rurales en la selva y locales comunales de venta de balones de gas doméstico (GLP).

Por ley, en el Perú el mercado de combustibles es de libre competencia, pero con una exigencia estricta: **los precios que el grifo cobra en el surtidor deben coincidir exactamente con los precios que reporta a la plataforma oficial del Estado (el SCOP)**. Si un grifo cobra en la calle un sol más de lo que declaró ante el regulador, comete una infracción grave que perjudica directamente el bolsillo de los ciudadanos.

Aquí nace el gran dolor operativo:
1. **Recursos limitados:** Osinergmin cuenta con un número acotado de inspectores físicos y camionetas para fiscalizar todo el territorio peruano. Es físicamente imposible visitar 24,000 locales todos los días.
2. **El costo del azar:** En un día ordinario, solo entre el **10% y el 20%** de los establecimientos cambian de precio. Si mandas a tus inspectores al azar o por intuición, entre el **80% y 90% de las visitas serán totalmente estériles** (el inspector llega, constata que el precio no cambió y se va; tiempo y presupuesto público desperdiciados).
3. **La ventana de riesgo:** La discrepancia entre la calle y el sistema ocurre casi exclusivamente **en el momento exacto en que el precio cambia**. Es allí donde el operario del grifo puede subir el letrero físico y "olvidar" actualizar el sistema SCOP.

### La Pregunta Central de la Tesis
Ante este dilema, la investigación se propuso sustituir la intuición por analítica predictiva de frontera. Definimos una pregunta binaria nítida:
> *¿Este establecimiento, para este combustible específico, cambiará su precio en algún momento de los próximos 5 días?*

#### ¿Por qué 5 días y no 1 día o 30 días?
* **¿Por qué NO 1 día?** En la logística pública, programar una ruta de fiscalización, emitir las órdenes de inspección y desplazar cuadrillas toma tiempo operativo. Una ventana de 24 horas es demasiado estrecha para reaccionar.
* **¿Por qué NO 30 días?** Una ventana de un mes es tan amplia que casi cualquier grifo activo cambiará de precio; la predicción pierde especificidad operativa y no ayuda a priorizar a quién visitar *esta semana*.
* **¿Por qué SÍ 5 días?** Coincide con una **semana laboral completa de supervisión** (lunes a viernes). Permite emitir una lista de trabajo accionable y genera una proporción balanceada de casos en la naturaleza (alrededor del 13.1% de eventos positivos en 2025). Además, en la Sección 18.1 se evaluaron horizontes de **3 y 7 días**, comprobando que la superioridad del modelo se mantiene inalterada en todos los meses.

La meta final no es emitir un veredicto judicial, sino generar cada medianoche una **Lista de Prioridad Diaria (Top 100)**: los 100 locales con mayor probabilidad de cambio para concentrar allí los recursos de inspección del Estado.

---

## Capítulo 1: La Arqueología de 15 Millones de Datos y las Decisiones de Descarte

La investigación comenzó descargando la totalidad de reportes públicos almacenados en el portal del SCOP entre marzo de 2020 y septiembre de 2026, distribuidos en **21 libros masivos de Excel** correspondientes a dos familias regulatorias: combustibles líquidos y GLP.

El volumen inicial fue colosal: **15,163,031 transacciones brutas**. Pero la data del mundo real viene repleta de ruido. Aquí comenzó el proceso de selección y filtrado:

```
[ 15,163,031 Reportes Brutos del SCOP ]
   │
   ├── (-)   595,465 : Actividades ajenas a venta al público minorista
   ├── (-)     3,023 : GLP mayorista no destinado a consumidor final
   ├── (-) 2,438,109 : Productos fuera del alcance (GNV, gasolinas antiguas, etc.)
   ├── (-)        12 : GLP a granel en kg (no convertible sin densidad)
   └── (-)   392,149 : Marcas secundarias de GLP envasado (se conserva marca principal)
   │
   ▼
[ 11,734,273 Reportes Seleccionados de 24,771 Establecimientos Minoristas ]
   │
   ├── (-)     9,889 : Duplicados exactos eliminados
   ├── (-)        19 : Precios nulos o no positivos eliminados
   └── (-)     5,458 : Precios imposibles (fuera de [0.5, 2.0] x mediana mensual)
   │
   ▼
[ 11,718,907 Reportes Limpios Finales (99.87% retenido) ]
```

### 1. ¿Por qué se descartó la venta no minorista (-595,465 filas)?
* **Razón:** El SCOP registra a toda la cadena de hidrocarburos. Entre las filas aparecían barcazas de transporte fluvial, distribuidores mayoristas de asfalto, camiones de combustible industrial para minas y plantas de mezcla.
* **Sustentación:** Un camión cisterna en carretera no es un grifo con letrero al consumidor final; incluirlo habría distorsionado la dinámica de precios minoristas con transacciones de volumen mayorista B2B.

### 2. ¿Por qué solo 5 combustibles y se descartó el resto (-2.43M filas)?
* **Razón:** Se aislaron estrictamente los 5 productos masivos que rigen la economía del transporte y los hogares peruanos:
  1. **Diesel B5 S-50 UV**
  2. **Gasolina / Gasohol Regular**
  3. **Gasolina / Gasohol Premium**
  4. **GLP Automotriz a Granel (GLP-G)**
  5. **GLP Envasado en Cilindro de 10 kg (GLP-E)**
* **Sustentación:** Se descartaron productos como gasolinas antiguas en desuso, gas natural vehicular GNV (que opera con redes fijas de gasoducto y otra lógica de mercado) y petróleos industriales pesados. Los 5 seleccionados representan la interacción diaria del consumidor en estaciones de servicio y gasocentros.

### 3. ¿Por qué se convirtieron litros a galones en GLP a granel?
* **Razón:** Hasta el año 2022, el GLP automotriz en gasocentros se reportaba en **litros**. A partir de la estandarización regulatoria, pasó a reportarse en **galones**.
* **Sustentación:** Para no romper la serie histórica longitudinal, convertimos 306,931 registros multiplicando el precio en litros por el factor físico exacto:
  $$\text{Precio por Galón} = \text{Precio por Litro} \times 3.78541$$
  Los 12 registros aislados que venían erróneamente en kilogramos se descartaron, pues convertir peso a volumen sin conocer la gravedad API o densidad exacta del lote generaría errores inaceptables.

### 4. ¿Por qué nos quedamos con la "marca principal" en GLP envasado (-392,149 filas)?
* **El dilema:** Un pequeño local de barrio que vende balones de gas de 10 kg comercializa simultáneamente 4 o 5 marcas (Solgas, Lima Gas, Zeta Gas, marcas regionales). Cada marca tiene su propio precio y su propio prestigio.
* **El peligro:** Si el local reporta hoy Solgas a S/ 52 y mañana reporta Lima Gas a S/ 48, el algoritmo creería falsamente que *el precio bajó S/ 4*, cuando en realidad solo cambió de marca.
* **Sustentación:** Para cada establecimiento de GLP envasado, identificamos cuál es su **marca principal** (la que más reporta históricamente en los 11,239 locales de GLP-E) y descartamos las secundarias. Así, cada observación refleja la evolución genuina del precio del producto más representativo del local.

### 5. ¿Por qué seudonimización criptográfica SHA-256?
* **Exigencia legal:** En el Perú rige la **Ley 29733 de Protección de Datos Personales**. Muchos grifos rurales y locales de balones de gas están a nombre de personas naturales (RUC 10), donde el RUC, nombre y dirección constituyen datos personales.
* **Sustentación:** Al cargar los Excel originales, el identificador fue reemplazado de inmediato por un hash criptográfico `SHA-256` salado con una clave local secreta de 128 bits guardada en `datos/clave_seudonimo.txt`, truncado a 12 caracteres hexadecimales. Se eliminaron RUC, razón social, dirección y distrito. Ningún dato sensible llegó a los archivos Parquet ni a las salidas públicas.

---

## Capítulo 2: Reconstruyendo el Tiempo: Del Reporte al Panel Diario (39M Filas)

Tras la limpieza, nos topamos con la barrera estructural más desafiante de los datos administrativos: **el SCOP contiene reportes de eventos aislados, NO una serie temporal diaria**.

Si un grifo en Puno reportó su Diesel a S/ 17.20 el 1 de febrero y no volvió a reportar hasta el 28 de febrero, en la base de datos hay un **vacío absoluto de 27 días**. Los algoritmos de Machine Learning no pueden aprender sobre el tiempo si el tiempo tiene agujeros.

```
Datos en Bruto (Eventos aislados):
Grifo A | 01-Feb | Diesel: S/ 17.20
Grifo A | 28-Feb | Diesel: S/ 17.50

Panel Diario Reconstruido (Arrastre de 60 días):
Grifo A | 01-Feb | S/ 17.20 (Reporte)
Grifo A | 02-Feb | S/ 17.20 (Arrastre vigente)
Grifo A | 03-Feb | S/ 17.20 (Arrastre vigente)
...
Grifo A | 28-Feb | S/ 17.50 (Cambio de precio -> Etiqueta = 1 en días previos)
```

### La Regla del Arrastre (*Carry-Forward*) de 60 Días
* **¿Cómo opera?** Asumimos que el último precio reportado por el establecimiento continúa vigente cada día siguiente hasta que ingrese un nuevo reporte que lo modifique.
* **¿Por qué 60 días y NO infinito?** Si un grifo cierra, quiebra o pierde su licencia, dejaría de reportar para siempre. Si arrastráramos el precio indefinidamente, el modelo creería que el grifo sigue operando con el mismo precio años después. Al cumplirse 60 días sin reporte, el establecimiento se considera inactivo y sale del panel.
* **¿Por qué NO 7 o 15 días?** Muchos grifos en zonas de baja competencia no cambian precios durante 3 o 4 semanas. Cortar el arrastre a los 15 días habría inventado falsas "bajas" de establecimientos que seguían operando activamente.
* **Calibración:** La cifra de 60 días se calibró en la Sección 4.1 reconstruyendo enero y febrero de 2026 con ventanas de 15 a 120 días y contrastando el número de establecimientos con precio activo frente al propio panel diario publicado por Osinergmin; 60 días resultó ser el valor más cercano en promedio sobre los 5 combustibles.

### El Resultado: 39,080,122 Filas Etiquetadas
Cruzando cada establecimiento por cada combustible por cada día del calendario (con fecha inicial marzo de 2020 y final septiembre de 2026), construimos una matriz panel de **39,080,122 observaciones con etiqueta válida**. 

Para cada fila, calculamos la variable objetivo binaria:
$$\text{cambia}_{i,c,t} = \begin{cases} 1 & \text{si el precio del combustible } c \text{ en el grifo } i \text{ cambia entre } t+1 \text{ y } t+5 \\ 0 & \text{en caso contrario} \end{cases}$$

En el año 2025, la tasa base empírica de cambio resultó ser del **$13.12\%$** (aproximadamente 1 de cada 8 observaciones registra un cambio de precio en los siguientes 5 días).

---

## Capítulo 3: La Mente del Algoritmo: 29 Variables y el "Despertador"

Para que los modelos aprendan a detectar cuándo un grifo está a punto de cambiar su precio, diseñamos **29 variables predictivas** distribuidas en 4 dimensiones estratégicas:

| Dimensión | Variables Clave | ¿Qué captura del mercado? |
| :--- | :--- | :--- |
| **Inercia del Establecimiento** | `dias_sin_cambio`, `n_cambios_7`, `n_cambios_14`, `n_cambios_28`, `n_cambios_90`, `reportes_sin_cambio_28`, `frac_subidas_28`, `magnitud_ultimo_cambio_pct` | La rigidez intrínseca del local: grifos hiperactivos vs. grifos pasivos, y su tendencia al alza o a la baja. |
| **Presión y Señal de Mercado** | `precio`, `mercado_delta_1_pct`, `mercado_pct_cambia`, `desv_mercado_pct`, `percentil_mercado`, `delta_1_pct`, `delta_3_pct`, `delta_7_pct`, `desv_media_movil_pct`, `volatilidad_7` | El pulso del entorno general: si el promedio del mercado se movió ayer y qué tan desalineado está el precio actual respecto al promedio nacional. |
| **Competencia Local** | `provincia_pct_cambia`, `desv_provincia_pct`, `depto_pct_cambia`, `desv_depto_pct`, `depto_code` | Presión del vecindario geográfico: si los grifos del mismo departamento o provincia ya se movieron, el local se ve forzado a reaccionar. |
| **Identidad y Calendario** | `combustible_code`, `actividad_code`, `n_productos`, `dia_semana`, `mes` | Heterogeneidad del producto, tamaño del establecimiento y ciclos logísticos semanales de abastecimiento. |

### La Joya de la Corona: El "Despertador" de Precios (`anomalia_espera`)
* **Intuición matemática:** Cada grifo tiene un ritmo propio. Si un grifo cambia en promedio cada 15 días y hoy lleva 30 días sin cambiar, su probabilidad de cambio inminente se dispara porque acumula un "retraso" anormal.
* **Formulación exacta en el código:** Si un establecimiento registró $n_{\text{cambios\_90}}$ cambios en los últimos 90 días, su intervalo medio de espera entre cambios es aproximadamente $\frac{90}{n_{\text{cambios\_90}} + 1}$ días. La variable mide cuántas veces su intervalo típico lleva el grifo esperando sin moverse:
  $$\text{anomalia\_espera}_{i,t} = \frac{\text{dias\_sin\_cambio}_{i,t} \cdot (n\text{\_cambios\_90}_{i,t} + 1)}{90}$$
* **El hallazgo empírico:** En la Sección 19 (Interpretabilidad por Permutación de Características), `anomalia_espera` resultó ser la **quinta variable más importante de todo el modelo** (caída de AUC de $0.00478$), superando ampliamente a variables financieras tradicionales.

### La Incorporación de las 3 Nuevas Variables (Sección 10)
Atendiendo las recomendaciones metodológicas del revisor, se evaluó incorporar formalmente `anomalia_espera`, `provincia_pct_cambia` y `desv_provincia_pct` frente al conjunto base de 26 variables:
* **El experimento:** Se corrieron los 12 bloques mensuales de 2025 comparando la matriz de 26 variables vs. 29 variables con los mismos datos y particiones.
* **El resultado:** La matriz de 29 variables superó a la de 26 en **11 de los 12 meses evaluados** (con empate o ligera variación solo en febrero de 2025: $-0.0010$). La ganancia promedio fue de **$+0.00185$ en AUC**, con un valor $p = 0.000488$ en la prueba de rangos con signo de Wilcoxon. Ganaron con holgura su derecho de permanencia en el modelo final.

### ¿Por qué toleramos colinealidad y VIF alto en algunas variables?
En la Sección 6.3 se auditó el Factor de Inflación de la Varianza (VIF). Variables como `desv_media_movil_pct` tuvieron un $\text{VIF} = 22.4$ y `delta_7_pct` tuvo $\text{VIF} = 10.1$.
* **¿Por qué NO las eliminamos?** En regresiones lineales econométricas ordinarias (MCO), un VIF alto infla los errores estándar de los estimadores. Sin embargo, nuestros algoritmos base son **árboles de decisión no lineales con ensambles (XGBoost, LightGBM, CatBoost, Random Forest)**. Los árboles de partición recursiva seleccionan divisiones locales independientes sin verse afectados por colinealidad distributiva global. Eliminar la media móvil habría mutilado información predictiva útil.

---

## Capítulo 4: El Gran Juicio del Balanceo de Clases: Por qué NO Balanceamos

Uno de los errores más comunes al enfrentarse a un problema desbalanceado (13.1% de casos positivos vs. 86.9% de negativos) es asumir por defecto: *"Tengo que aplicar SMOTE o submuestrear para dejarlo en 50/50"*.

En la **Sección 11**, sometimos este dilema a juicio experimental estricto.

### El Experimento de los 8 Métodos con LightGBM (Sección 11.1)
Evaluamos 8 estrategias de balanceo a lo largo de los 12 bloques mensuales de 2025:

| Método de Balanceo | AUC Promedio | Precisión@100 ($p@100$) | Precisión@250 ($p@250$) | Brier Score | Tiempo / Bloque |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **`ninguno` (Distribución real)** | **0.7326** | **61.54%** | **52.26%** | **0.1037** | **0.9 s** |
| `pesos` (Ponderación de pérdida) | 0.7327 | 61.45% | 51.90% | 0.1035 | 0.9 s |
| `submuestreo_1_1` (50 / 50) | 0.7318 | 60.28% | 51.63% | 0.1037 | 0.4 s |
| `submuestreo_1_3` (1 a 3) | 0.7323 | 61.51% | 52.23% | 0.1037 | 0.6 s |
| `sobremuestreo` (Duplicación aleatoria) | 0.7325 | 61.20% | 52.03% | 0.1035 | 1.6 s |
| `tomek` (Limpieza de fronteras) | 0.7327 | 61.33% | 52.25% | 0.1039 | 22.5 s |
| **`smotenc` (Datos sintéticos mixtos)** | **0.6983** | **49.41%** | **42.94%** | **0.1081** | **24.5 s** |
| **`adasyn` (Sintéticos adaptativos)** | **0.6911** | **42.75%** | **39.38%** | **0.1093** | **4.6 s** |

### ¿Por qué SMOTE y ADASYN fracasaron rotundamente?
1. **Creación de perfiles sintéticos irreales:** SMOTE toma dos establecimientos positivos e interpola un punto medio matemático. Pero un grifo con latitud intermedia, número fraccionario de reportes y precio artificial no existe en la geografía del Perú. Introdujo ruido en la frontera de decisión.
2. **Caída drástica de rendimiento y tiempo:** SMOTE-NC cayó **3.4 puntos porcentuales de AUC** y más de **12 puntos de precisión en el Top 100**, multiplicando por 27 veces el tiempo de cómputo por bloque (24.5 s frente a 0.9 s).

### La Corrección Analítica de Priors de Dal Pozzolo et al. (2015)
Cuando se altera la proporción de clases en el entrenamiento (por ejemplo, submuestreando al 50/50 o asignando pesos), el modelo aprende sobre una tasa artificial ($\pi_{\text{ent}}$) y sobreestima todas las probabilidades.

Para que la comparación entre métodos fuera científicamente justa en métricas de calibración (Brier Score), implementamos en la Sección 9.1 la corrección analítica de Dal Pozzolo en escala logit:
$$\text{logit}(P_{\text{real}}) = \text{logit}(P_{\text{bal}}) + \ln\left(\frac{\pi_{\text{real}}}{1 - \pi_{\text{real}}}\right) - \ln\left(\frac{\pi_{\text{ent}}}{1 - \pi_{\text{ent}}}\right)$$

O en su expresión algebraica directa equivalente:
$$P_{\text{real}} = \frac{P_{\text{bal}} \cdot \frac{\pi_{\text{real}}}{\pi_{\text{ent}}}}{P_{\text{bal}} \cdot \frac{\pi_{\text{real}}}{\pi_{\text{ent}}} + (1 - P_{\text{bal}}) \cdot \frac{1 - \pi_{\text{real}}}{1 - \pi_{\text{ent}}}}$$

Esta transformación es estrictamente monótona: devuelve las probabilidades a su escala natural sin alterar el ordenamiento del ranking (AUC, $p@100$ y $p@250$ se mantienen intactos).

### El Veredicto Final (Sección 11.2)
Al contrastar los 4 candidatos finalistas (`ninguno`, `pesos`, `pesos_catboost`, `tomek`) en los 4 modelos base, entrenar con la **distribución natural (`ninguno`)** obtuvo la mejor posición media consolidada en las 4 métricas, garantizando máxima fidelidad bayesiana con el menor costo de cómputo.

---

## Capítulo 5: El Laboratorio Antifuga y la Ventana de 6 Meses

Para evaluar los modelos, descartamos de plano la partición aleatoria clásica 70/30 (que filtra información del futuro hacia el pasado). Adoptamos una arquitectura de **Validación Temporal Walk-Forward en 12 Bloques Mensuales durante todo el año 2025**:

```
Enero 2025   : [ Jul 2024 - Dic 2024 ] -> Purga 6d -> Evalúa Enero 2025
Febrero 2025 : [ Ago 2024 - Ene 2025 ] -> Purga 6d -> Evalúa Febrero 2025
Marzo 2025   : [ Sep 2024 - Feb 2025 ] -> Purga 6d -> Evalúa Marzo 2025
... (la ventana avanza un mes en cada ciclo hasta Diciembre 2025)
```

### La Purga Temporal ($H+1 = 6$ días)
Como la etiqueta mira 5 días hacia adelante ($t+1$ a $t+5$), si el entrenamiento terminara el 31 de diciembre, la etiqueta del 28 de diciembre ya estaría leyendo si el grifo cambió el 2 de enero. Para blindar el modelo contra esta fuga invisible (*data leakage*), la función de entrenamiento detiene los datos **6 días antes** del inicio del mes evaluado. Cero contaminación.

### Justificación de la Ventana Rodante de 6 Meses (*Rolling Window*)
1. **Quiebres Estructurales (*Concept Drift*):** El mercado de hidrocarburos cambia drásticamente ante shocks internacionales (pandemia 2020, guerra en Ucrania 2022 con subsidios estatales de emergencia). Acumular años pasados envenena el modelo enseñándole relaciones precio-margen que ya no rigen.
2. **Volumen de datos garantizado:** Una ventana de 6 meses contiene en promedio **3,370,327 filas**. Hay saturación muestral suficiente sin necesidad de arrastrar historia obsoleta.
3. **Memoria de largo plazo integrada en las variables:** El modelo no "olvida" el pasado lejano del grifo porque variables como `n_cambios_90` y `anomalia_espera` ya codifican su inercia histórica dentro del vector de entrada ($X$), mientras que la ventana móvil mantiene la función predictiva calibrada al régimen macroeconómico presente.

---

## Capítulo 6: La Curva de Aprendizaje: Por qué 300,000 Filas y luego 1 Millón

Dentro de la ventana de 6 meses hay más de 3.3 millones de filas disponibles. ¿Con cuántas debemos entrenar en las fases experimentales?

En la **Sección 12**, trazamos la curva de aprendizaje empírica evaluando 4 tamaños de muestra a través de los 12 meses de 2025:

| Filas de Entrenamiento | AUC Promedio | Precisión@100 ($p@100$) | Tiempo Medio por Bloque |
| :---: | :---: | :---: | :---: |
| **50,000** | 0.7263 | 59.68% | 2.2 s |
| **100,000** | 0.7292 | 61.25% | 3.3 s |
| **300,000** | **0.7317** | **61.56%** | **11.1 s** |
| **1,000,000** | **0.7325** | **61.83%** | **31.2 s** |

### La Ley de Rendimientos Decrecientes (*Diminishing Returns*)
* Al pasar de 50k a 300k filas, el modelo dio un salto cuantitativo fundamental ($+0.0054$ de AUC y casi $2$ puntos porcentuales de precisión).
* Al pasar de 300k a 1,000,000 de filas, **el AUC solo aumentó $+0.0008$** (0.08 puntos de AUC), pero el tiempo de entrenamiento se multiplicó por **$2.8 \times$** (alcanzando más de 112 segundos por bloque en modelos como Random Forest).

### La Decisión Estratégica
* **Fase de Comparación de 39 Ensambles (Secciones 13 a 15):** Usamos **300,000 filas**. Al tener que entrenar 39 variantes a lo largo de 12 bloques (cientos de iteraciones), 300k ofreció el balance ideal de estabilidad estadística y agilidad experimental sin alterar el orden relativo de los ensambles.
* **Fase de Prueba 2026 y Modelo Final en Producción (Secciones 18 y 20):** Con el algoritmo campeón ya seleccionado, activamos el tope de **1,000,000 de filas** para capturar esa ganancia marginal en el modelo operativo entregado.

---

## Capítulo 7: La Batalla de los 39 Ensambles y el Nacimiento de STJC

En la Sección 13 entrenamos a nuestros 4 modelos base individuales: **CatBoost, XGBoost, LightGBM y Random Forest**. 

Los 4 modelos demostraron ser altamente competitivos (AUC entre $0.7282$ y $0.7333$), pero exhibieron una correlación de predicciones muy estrecha (**correlación de Spearman entre 0.912 y 0.978**).

En la Sección 14, nos propusimos combinarlos evaluando **39 configuraciones de ensambles** agrupadas en 12 familias metodológicas.

### El Fracaso de los Ensambles Complejos (13 ensambles sacaron 0 de 4)
* **Metamodelos no lineales y boosting meta (AdaBoost, LightGBM meta):** Fracasaron rotundamente (0 de 4 métricas superadas). Al estar las 4 entradas tan correlacionadas, un metamodelo no lineal sobreajustó el ruido.
* **Stacking Lineal Clásico sin regularización:** Asignó ponderaciones fuertemente inestables (por ejemplo, coeficientes de $+0.86$ a $+1.15$ para XGBoost y castigos negativos de hasta $-0.76$ para LightGBM) debido a la multicolinealidad de las probabilidades base.

### Los Dos Grandes Triunfadores

Solo **8 de los 39 ensambles lograron la hazaña de superar a todos los modelos individuales en las 4 métricas al mismo tiempo (4 de 4)**. Entre ellos brillaron dos soluciones con propósitos complementarios:

#### 1. Votación Suave (*Soft Voting* / Stacking Promedio)
* Asigna exactamente un $25\%$ de peso a cada modelo:
  $$P_{\text{final}} = \frac{P_{\text{Cat}} + P_{\text{Lgb}} + P_{\text{Xgb}} + P_{\text{RF}}}{4}$$
* **Resultado:** Logró el **mejor AUC global de toda la tesis ($0.7355$)**. Al promediar en partes iguales, cancela el error estocástico individual sin generar sobreajuste alguno. Por su simplicidad y robustez, fue el ensamble seleccionado para la prueba final de 2026 y el despliegue operativo.

#### 2. STJC: Stacking Temporal Jerárquico con Contracción (Nuestra Propuesta Metodológica)
Diseñamos un método propio concebido para resolver las debilidades del stacking tradicional en series de tiempo mediante 5 piezas arquitectónicas:

```
Ablación Pieza por Pieza de STJC (Sección 14.11):
Estrategia                     AUC     p@100     p@250     Brier     ¿Qué aportó la pieza?
Stacking clásico temporal    0.7338   0.6198    0.5247    0.1072    Punto de partida (1 mes)
+ Multiventana (3 meses)     0.7343   0.6193    0.5263    0.1039    Baja drásticamente el Brier (-0.0033)
+ Pesos convexos (w >= 0)    0.7347   0.6203    0.5281    0.1033    Mejora AUC (+0.0004) y p@100
+ Contracción (Shrinkage)    0.7352   0.6246    0.5301    0.1032    Dispara p@100 (+0.43%)
+ Jerarquía combustible      0.7352   0.6245    0.5300    0.1032    Flexibilidad diferenciada
STJC Método Completo         0.7348   0.6251    0.5308    0.1031    RÉCORD EN p@100 Y BRIER
```

* **Resultado de STJC:** Rompió el **récord absoluto de precisión en los 100 primeros inspeccionados ($p@100 = 62.51\%$)** y logró la **mejor calibración probabilística de toda la tesis (Brier $= 0.1031$)**.

---

## Capítulo 8: Pruebas de Estrés y Auditoría Científica

Antes de dar por válidos los resultados, sometimos a los modelos ganadores a tres pruebas de estrés destructivas:

### 1. ¿Fue suerte o casualidad? (365 Pruebas Diarias de Wilcoxon + Holm)
En la Sección 15.1, evaluamos el desempeño día por día durante los **365 días del año 2025**:
* Comparamos cada ensamble contra cada uno de los 4 modelos individuales en las 4 métricas ($4 \times 4 = 16$ comparaciones pareadas).
* Aplicamos la prueba de rangos con signo de Wilcoxon con la corrección más estricta de la literatura: **Holm-Bonferroni**.
* **Resultado:** Tanto Votación Suave como STJC ganaron **16 de 16 comparaciones con significancia estadística ($p_{\text{holm}} < 0.01$)**; en el caso de STJC, todas las comparaciones alcanzaron $p_{\text{holm}} < 0.001$. Quedó certificado que la superioridad del ensamble no fue fruto del azar.

### 2. ¿Hubo trampa o fuga oculta? (Prueba Negativa de Etiquetas Permutadas)
En la Sección 17, desordenamos completamente al azar la columna objetivo `cambia`. Si existiera alguna fuga de datos invisible en las 29 variables, el modelo obtendría un AUC artificialmente alto:
* **Resultado:** El AUC promedio cayó a **`0.4886`** (con intentos entre $0.466$ y $0.518$, centrado exactamente en el $0.50$ de una moneda al aire).
* **Conclusión:** Queda formalmente demostrado que no existe fuga de información (*zero data leakage*).

### 3. Diagnóstico de Sobreajuste (Brecha Entrenamiento vs. Validación)
Comparamos el AUC en el conjunto de entrenamiento frente al de validación:
* *Random Forest individual:* Mostró sobreajuste evidente (Entrenamiento: $0.8096$ vs. Validación: $0.7282$, brecha de $+0.0814$).
* *STJC y Votación Suave:* La brecha fue prácticamente nula ($+0.0001$ en STJC y $-0.0038$ en Votación Suave). El ensamble actúa como un escudo regularizador perfecto.

---

## Capítulo 9: El Examen de la Vida Real (2026) y el Despliegue Operativo

Todo lo anterior se desarrolló y calibró con datos hasta 2025. El año **2026 estuvo completamente sellado bajo llave**.

En la Sección 18, abrimos la bóveda de 2026 y ejecutamos la simulación operativa real a lo largo de **262 días continuos (enero a septiembre de 2026)** con el modelo final (**Votación Suave**, 1 millón de filas y reentrenamiento trimestral):

### Contexto del Mercado en 2026: El Choque de Precios
En 2026 el mercado experimentó una volatilidad inusual: la tasa base de cambio promedio subió al **$32.6\%$** (alcanzando un pico de **$56.9\%$ en marzo**). Esto puso a prueba la capacidad adaptativa del modelo frente a un entorno macroeconómico turbulento.

### 1. Precisión en la Calle: El Top 100 Diario ($p@100$)
* Cada día se ordenaron los casos activos (entre 17,863 y 19,975 casos diarios, promedio de 19,292) y se fiscalizaron los 100 primeros.
* **El resultado:** El modelo logró un promedio de **$78.4\%$ de aciertos reales** a lo largo de los 262 días (en julio de 2026 alcanzó un notable **$93.0\%$** en $p@100$ y **$93.8\%$** en $p@50$).
* De las 26,200 visitas simuladas en el año (100 diarias $\times$ 262 días), **20,539 establecimientos efectivamente cambiaron de precio** en los 5 días posteriores a la visita.

### 2. Contraste frente a las Reglas Heurísticas de Conteo
Comparamos el modelo contra la heurística del estudio piloto (`n_cambios_28`, supervisar a los que más cambiaron el último mes) y contra la regla histórica amplia (`n_cambios_90`):
* En el Top 100, la regla de 28 días obtuvo 20,595 aciertos ($78.6\%$). ¿Por qué? Porque en un año con alta tasa base general, una regla que repite siempre a los mismos locales hiperactivos logra un acierto local alto.
* **La superioridad global del modelo:** La regla heurística colapsa en la visión integral del mercado: su AUC diario fue de apenas $0.7044$. El modelo predictivo alcanzó un AUC diario de **$0.7459$**, superando a la regla en el **88.2% de los días evaluados** con una significancia estadística abrumadora en la prueba pareada de Wilcoxon ($p = 4.89 \times 10^{-35}$). Frente a `n_cambios_90` (AUC 0.7251), el modelo ganó en el **80.2% de los días** ($p = 1.55 \times 10^{-24}$).

### 3. La Prueba de Establecimientos "Nunca Vistos"
Antes de empezar el estudio (Sección 8), apartamos al azar el **$30\%$ de los establecimientos del país (7,431 locales)** y prohibimos que entraran en ningún entrenamiento. En 2026 evaluamos el comportamiento en esos locales desconocidos:
* **AUC promedio de todo 2026:**
  - Establecimientos conocidos: **$0.7426$**
  - Establecimientos nunca vistos: **$0.7439$**
* En julio de 2026, el modelo alcanzó un AUC de **0.804** en conocidos y **0.802** en nunca vistos. El modelo no memorizó nombres comerciales; aprendió dinámicas estructurales de mercado transferibles a cualquier punto del mapa.

### 4. Trazabilidad del 100% al Comprobante Físico del SCOP (Sección 20.2)
Para responder a la pregunta de cualquier jurado: *"¿Cómo sé que el precio realmente cambió?"*:
* Para el **100.0% de los 20,539 aciertos** en el Top 100 de 2026, el código rastreó y encontró el reporte original en el sistema SCOP con su fecha, hora y precio exacto.

### 5. Robustez en Múltiples Horizontes (Sección 18.1)
Al variar el horizonte de predicción a 3 y 7 días, el modelo superó a las reglas de conteo en **los 9 de los 9 meses evaluados de 2026**, confirmando que su superioridad es estructural y no depende de la ventana de 5 días.

---

## Epílogo: Ficha Maestra de Preguntas Incómodas para la Defensa de Tesis

| Pregunta Incómoda del Jurado | Respuesta Técnica y Contundente |
| :--- | :--- |
| *1. ¿Por qué tu AUC es ~0.74 y no 0.95?* | En economía y microdatos basados en decisiones humanas privadas, un AUC de 0.74 es **sólido y discriminante (Hosmer & Lemeshow, 2000)**. No tenemos sensores en los tanques de gasolina ni intervenimos las llamadas entre mayoristas y dueños. Un AUC de 0.95 en este problema sería síntoma inequívoco de fuga de datos (*data leakage*). Además, en el segmento operativo relevante (Top 100), el modelo acierta el **78.4% de las veces**. |
| *2. ¿Por qué no aplicaste SMOTE o balanceo de clases si tenías solo 13% de positivos?* | Probamos 8 métodos de balanceo en los 12 bloques de 2025. SMOTE y ADASYN colapsaron el AUC a 0.69 al crear datos sintéticos irreales en coordenadas geográficas inexistentes, multiplicando el cómputo por 27 veces. Con millones de observaciones reales y la corrección de priors de Dal Pozzolo (2015), **entrenar con la distribución natural (`ninguno`) logró la mejor posición media en las 4 métricas**. |
| *3. ¿Por qué una ventana rodante de 6 meses y no acumular toda la historia desde 2020?* | El mercado de hidrocarburos sufre **quiebres estructurales (*Concept Drift*)**. Acumular 2020 (pandemia) o 2022 (shock de Ucrania y subsidios extintos) envenena el modelo con regímenes regulatorios muertos. La ventana rodante de 6 meses contiene en promedio 3.37 millones de observaciones (saturación muestral plena) y se adapta dinámicamente al entorno macroeconómico vigente. |
| *4. ¿Por qué entrenar con 300k filas y no con 1 millón en las comparaciones?* | Nuestra curva de aprendizaje (Sección 12) demostró que pasar de 300k a 1M de filas solo aportaba $+0.0008$ de AUC (0.08 puntos), multiplicando por $2.8 \times$ el tiempo de cómputo. Aplicamos la regla de parsimonia: 300k para comparar limpiamente 39 ensambles en 12 meses, y **1 millón de filas para el modelo final entregado en producción**. |
| *5. ¿Por qué ganaron ensambles parsimoniosos como Votación Suave y STJC frente a metamodelos complejos de boosting?* | Porque nuestros 4 modelos base ya eran altamente competentes y sus predicciones presentaban una correlación de Spearman de hasta 0.978. Cuando los estimadores base coinciden fuertemente, un metamodelo no lineal complejo solo memoriza ruido y sobreajusta. La regularización convexa y la parsimonia equilibrada evitaron ese sobreajuste. |
