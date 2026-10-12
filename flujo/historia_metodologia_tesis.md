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
* **¿Por qué SÍ 5 días?** Coincide con una **semana laboral completa de supervisión** (lunes a viernes). Permite emitir una lista de trabajo accionable y genera una proporción balanceada de casos en la naturaleza (alrededor del 13% de eventos positivos en 2025). Además, en la Sección 18.1 se evaluaron horizontes de **3 y 7 días**, comprobando que la superioridad del modelo se mantiene inalterada.

La meta final no es emitir un veredicto judicial, sino generar cada medianoche una **Lista de Prioridad Diaria (Top 100)**: los 100 locales con mayor probabilidad de cambio para concentrar allí los recursos del Estado.

---

## Capítulo 1: La Arqueología de 15 Millones de Datos y las Decisiones de Descarte

La investigación comenzó descargando la totalidad de reportes públicos almacenados en el portal del SCOP entre marzo de 2020 y septiembre de 2026, distribuidos en **21 libros masivos de Excel** correspondientes a dos familias regulatorias: combustibles líquidos y GLP.

El volumen inicial fue colosal: **15,163,031 transacciones brutas**. Pero la data del mundo real viene repleta de ruido. Aquí comenzó el primer gran filtro de decisiones:

```
[ 15,163,031 Reportes Brutos del SCOP ]
   │
   ├── (-) 595,465  : Actividades ajenas a venta al público minorista
   ├── (-)   3,023  : GLP mayorista no destinado a consumidor final
   ├── (-) 2,438,109: Productos fuera del alcance (GNV, gasolinas 84 oct, etc.)
   ├── (-)      12  : GLP a granel en kg (no convertible sin densidad)
   └── (-) 392,149  : Marcas secundarias de GLP envasado (se conserva serie modal)
   │
   ▼
[ 11,734,273 Reportes Limpios de 24,771 Establecimientos Minoristas ]
```

### 1. ¿Por qué se descartó la venta no minorista (-595,465 filas)?
* **Razón:** El SCOP registra a toda la cadena de hidrocarburos. Entre las filas aparecían barcazas de transporte fluvial, distribuidores mayoristas de asfalto, camiones de combustible industrial para minas y plantas de mezcla.
* **Sustentación:** Un camión cisterna en carretera no es un grifo con letrero al consumidor final; incluirlo habría distorsionado la dinámica de precios minoristas con transacciones de volumen B2B.

### 2. ¿Por qué solo 5 combustibles y se descartó el resto (-2.43M filas)?
* **Razón:** Se aislaron estrictamente los 5 productos masivos que rigen la economía del transporte y los hogares peruanos:
  1. **Diesel B5 S-50 UV**
  2. **Gasolina / Gasohol Regular**
  3. **Gasolina / Gasohol Premium**
  4. **GLP Automotriz a Granel (GLP-G)**
  5. **GLP Envasado en Cilindro de 10 kg (GLP-E)**
* **Sustentación:** Se descartaron productos como la Gasolina de 84 octanos (prohibida y retirada del mercado en la simplificación de combustibles del DS 014-2021-EM), el gas natural vehicular GNV (que opera con contratos y redes fijas de gasoducto con otra dinámica) y petróleos industriales pesados. Los 5 seleccionados representan más del 95% de la interacción diaria de los ciudadanos en los grifos.

### 3. ¿Por qué se convirtieron litros a galones en GLP a granel?
* **Razón:** Hasta el año 2022, el GLP automotriz en gasocentros se reportaba en **litros**. A partir de la estandarización regulatoria, pasó a reportarse en **galones**.
* **Sustentación:** Para no romper la serie histórica longitudinal, convertimos 306,931 registros multiplicando el precio en litros por el factor físico exacto:
  $$\text{Precio por Galón} = \text{Precio por Litro} \times 3.78541$$
  Los 12 registros aislados que venían erróneamente en kilogramos se descartaron, pues convertir peso a volumen sin conocer la gravedad API o densidad exacta del lote genera errores inaceptables.

### 4. ¿Por qué nos quedamos con la "marca principal" en GLP envasado (-392,149 filas)?
* **El dilema:** Un pequeño local de barrio que vende balones de gas de 10 kg comercializa simultáneamente 4 o 5 marcas (Solgas, Lima Gas, Zeta Gas, marcas regionales). Cada marca tiene su propio precio y su propio prestigio.
* **El peligro:** Si el local reporta hoy Solgas a S/ 52 y mañana reporta Lima Gas a S/ 48, el algoritmo creería falsamente que *el precio bajó S/ 4*, cuando en realidad solo cambió de marca.
* **Sustentación:** Para cada establecimiento de GLP envasado, identificamos cuál es su **marca principal** (la que más reporta históricamente) y descartamos las secundarias. Así, cada observación refleja la evolución genuina del precio del producto más representativo del local.

### 5. ¿Por qué seudonimización criptográfica SHA-256?
* **Exigencia legal:** En el Perú rige la **Ley 29733 de Protección de Datos Personales**. Muchos grifos rurales y locales de balones de gas están a nombre de personas naturales (RUC 10), donde el RUC, nombre y dirección constituyen datos personales.
* **Sustentación:** Al cargar los Excel originales, el Registro de Hidrocarburos fue reemplazado de inmediato por un hash criptográfico `SHA-256` salado con una clave secreta local de 128 bits guardada en `datos/clave_seudonimo.txt`. Se eliminaron RUC, razón social y dirección. Ningún dato sensible llegó a los archivos Parquet ni a las salidas. Esto permitió mantener la continuidad temporal del establecimiento sin vulnerar la privacidad.

---

## Capítulo 2: Reconstruyendo el Tiempo: Del Reporte al Panel Diario (39M Filas)

Tras la limpieza, nos topamos con la barrera estructural más desafiante de los datos administrativos: **el SCOP contiene reportes de eventos, NO una serie temporal diaria**.

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
* **¿Por qué 60 días y NO infinito?** Si un grifo cierra, quiebra o pierde su licencia, dejaría de reportar para siempre. Si arrastráramos el precio indefinidamente, el modelo creería que el grifo sigue operando con el mismo precio en 2026. Al cumplirse 60 días sin reporte, el establecimiento se considera inactivo y sale del panel.
* **¿Por qué NO 7 o 15 días?** Muchos grifos en zonas de baja competencia no cambian precios durante 3 o 4 semanas. Cortar el arrastre a los 15 días habría inventado falsas "bajas" de establecimientos que seguían operando activamente. La cifra de 60 días se calibró en la Sección 4.1 contrastando con la propia regla empírica del panel de Osinergmin.

### El Resultado: 39,080,122 Filas Etiquetadas
Cruzando cada establecimiento por cada combustible por cada día del calendario, construimos una matriz panel de **39,080,122 observaciones**. 

Para cada fila, calculamos la variable objetivo binaria:
$$\text{cambia}_{i,c,t} = \begin{cases} 1 & \text{si el precio del combustible } c \text{ en el grifo } i \text{ cambia entre } t+1 \text{ y } t+5 \\ 0 & \text{en caso contrario} \end{cases}$$

En el año 2025, la tasa base empírica de cambio resultó ser del **$13.1\%$** (aproximadamente 1 de cada 8 observaciones registra un cambio de precio en los siguientes 5 días).

---

## Capítulo 3: La Mente del Algoritmo: 29 Variables y el "Despertador"

Para que la Inteligencia Artificial aprenda a detectar cuándo un grifo está a punto de cambiar su precio, diseñamos **29 variables predictivas** distribuidas en 4 dimensiones estratégicas:

| Dimensión | Variables Clave | ¿Qué captura del mercado? |
| :--- | :--- | :--- |
| **Inercia del Establecimiento** | `dias_sin_cambio`, `n_cambios_7`, `n_cambios_14`, `n_cambios_28`, `n_cambios_90`, `reportes_sin_cambio_28` | La rigidez intrínseca del local: grifos hiperactivos vs. grifos pasivos. |
| **Presión Mayorista Nacional** | `mercado_delta_1_pct`, `mercado_pct_cambia`, `desv_mercado_pct`, `percentil_mercado` | El pulso del crudo: si la refinería (Petroperú/Repsol) subió precios ayer, el grifo se moverá pronto. |
| **Competencia Local Provincial** | `provincia_pct_cambia`, `desv_provincia_pct`, `depto_pct_cambia`, `desv_depto_pct` | Presión del entorno: si mis vecinos de la provincia ya cambiaron precio, estoy forzado a reaccionar. |
| **Temporales y Calendario** | `dia_semana`, `mes` | Los ciclos de logística de los camiones cisterna (jueves/viernes vs. fines de semana). |

### La Joya de la Corona: El "Despertador" de Precios (`anomalia_espera`)
* **Intuición matemática:** Cada grifo tiene un ritmo biológico propio. Algunos cambian de precio cada 4 días; otros, cada 25 días. Modelamos este comportamiento como un proceso de supervivencia o tasa de salida (*hazard rate*).
* **Definición:** Calculamos la mediana histórica de días de espera entre cambios para cada grifo ($M_i$). Luego medimos cuántos días lleva sin cambiar hoy ($D_{i,t}$).
  $$\text{anomalia\_espera}_{i,t} = \frac{D_{i,t}}{M_i + 1}$$
* **El hallazgo:** Si un grifo suele esperar 10 días, y hoy lleva 18 días sin cambiar ($\text{anomalia} = 1.8$), la probabilidad de cambio inminente se dispara. En la Sección 19 (Interpretabilidad por Permutación), `anomalia_espera` resultó ser la **quinta variable más importante de todo el modelo**, superando a variables tradicionales.

### La Incorporación de las 3 Nuevas Variables (Sección 10)
Atendiendo las observaciones del revisor, se evaluó si incorporar `anomalia_espera`, `provincia_pct_cambia` y `desv_provincia_pct` frente a las 26 variables originales:
* **El experimento:** Se corrieron los 12 bloques mensuales de 2025 con 26 variables vs. 29 variables.
* **El resultado:** La matriz de 29 variables superó a la de 26 en **los 12 de 12 meses evaluados**, con una ganancia promedio de $+0.00185$ en AUC ($p = 0.000488$ en la prueba de signos). Se ganaron su derecho matemático de entrar al modelo final.

### ¿Por qué toleramos colinealidad y VIF alto en algunas variables?
En la Sección 6.3 se auditó el Factor de Inflación de la Varianza (VIF). Variables como `desv_media_movil_pct` tuvieron un $\text{VIF} = 22.4$ y `delta_7_pct` tuvo $\text{VIF} = 10.1$.
* **¿Por qué NO las eliminamos?** En regresiones lineales econométricas ordinarias (MCO), un VIF alto infla los errores estándar de los coeficientes $\beta$. Sin embargo, nuestros modelos base son **árboles de decisión no lineales (XGBoost, LightGBM, CatBoost)**. Los árboles de decisión son inmunes al VIF: si dos variables están correlacionadas, el árbol simplemente divide por una de ellas sin distorsionar la predicción. Eliminar la media móvil habría destruido señal predictiva útil.

---

## Capítulo 4: El Gran Juicio del Balanceo de Clases: Por qué NO Balanceamos

Uno de los errores más comunes cometidos por estudiantes y profesionales al enfrentarse a un problema desbalanceado (13% de casos positivos vs. 87% de negativos) es asumir automáticamente: *"Tengo que aplicar SMOTE o submuestrear para que quede 50/50"*.

En la **Sección 11**, sometimos este dogma a juicio experimental riguroso.

### El Experimento de los 8 Métodos
Evaluamos 8 estrategias de balanceo con LightGBM a lo largo de los 12 meses de 2025:
1. `ninguno`: Entrenar con la distribución real (13% positivos).
2. `pesos`: Ponderar la función de pérdida inversamente a la frecuencia de clase.
3. `submuestreo_1_1`: Tirar a la basura registros negativos hasta igualar 50/50.
4. `submuestreo_1_3`: Submuestrear hasta una relación 1 positivo por cada 3 negativos.
5. `sobremuestreo`: Duplicar registros positivos al azar.
6. `smotenc`: Generar datos sintéticos por interpolación con k-vecinos para datos mixtos.
7. `adasyn`: Generar sintéticos enfocados en las zonas de frontera más difíciles.
8. `tomek`: Eliminar pares de puntos limítrofes ambiguos.

```
Resultados de Balanceo en Validación 2025 (LightGBM):
Método            AUC       p@100     Brier     Tiempo/Bloque
ninguno         0.7326    0.6154    0.1037        0.9 s  <-- GANADOR
pesos           0.7327    0.6161    0.1037        0.9 s
submuestreo_1_1 0.7314    0.6095    0.1040        0.4 s
smotenc         0.7012    0.5342    0.1082       24.8 s  <-- COLAPSO
adasyn          0.6975    0.4678    0.1091        4.6 s  <-- COLAPSO
```

### ¿Por qué SMOTE y ADASYN fracasaron rotundamente?
1. **Creación de monstruos sintéticos:** SMOTE toma dos grifos que cambiaron de precio e inventa matemáticamente un "grifo promedio" intermedio en el espacio vectorial. Pero un grifo con latitud intermedia, número de cambios fraccionario y precio artificial **no existe en la geografía real del Perú**. Creó observaciones irreales que confundieron a los árboles de decisión.
2. **Costo computacional disparatado:** SMOTE-NC tardó **25 segundos por bloque** frente a **0.9 segundos** de no balancear, multiplicando por 27 veces el tiempo de cómputo para obtener un resultado $3.1$ puntos de AUC **peor**.

### El Secreto Matemático: La Corrección de Dal Pozzolo et al. (2015)
Cuando alteras la proporción de clases al entrenar (por ejemplo, submuestreando al 50/50), el modelo se vuelve paranoico: cree que la mitad del mundo cambia de precio. Como consecuencia, **infla artificialmente todas las probabilidades predichas**.

Para que la comparación fuera honesta en todas las métricas, implementamos en la Sección 9.1 la fórmula analítica de calibración de priors de Dal Pozzolo:
$$P_{\text{real}} = \frac{P_{\text{bal}} \cdot \frac{y_0}{y_1}}{(1 - P_{\text{bal}}) + P_{\text{bal}} \cdot \frac{y_0}{y_1}}$$
Donde $y_0$ es la tasa real del mercado (13.1%) y $y_1$ es la tasa inflada de entrenamiento. Esta corrección devolvió las probabilidades a su escala real sin mover el orden del ranking.

### El Veredicto Final
Tras calibrar y evaluar en las 4 métricas con los 4 modelos base (Sección 11.2):
* **`ninguno` (entrenar con los datos naturales)** obtuvo la **mejor posición media en las 4 métricas** (AUC, $p@100$, $p@250$ y Brier).
* Demostramos con datos duros que alterar artificialmente la realidad distorsiona la frontera bayesiana óptima cuando el algoritmo cuenta con millones de observaciones reales.

---

## Capítulo 5: El Laboratorio Antifuga y la Ventana de 6 Meses (Rolling vs. Expanding)

Para evaluar los modelos, descartamos de plano el clásico corte 70/30 al azar por las razones expuestas en el Prólogo. Adoptamos una arquitectura de **Validación Temporal Walk-Forward en 12 Bloques Mensuales durante todo el año 2025**.

```
Enero 2025   : [ Jul 2024 - Dic 2024 ] -> Purga 6d -> Evalúa Enero 2025
Febrero 2025 : [ Ago 2024 - Ene 2025 ] -> Purga 6d -> Evalúa Febrero 2025
Marzo 2025   : [ Sep 2024 - Feb 2025 ] -> Purga 6d -> Evalúa Marzo 2025
... (la ventana avanza un mes en cada ciclo hasta Diciembre 2025)
```

### La Purga Temporal ($H+1 = 6$ días)
Como la etiqueta mira 5 días hacia adelante ($t+1$ a $t+5$), si el entrenamiento terminara el 31 de diciembre, la etiqueta del 28 de diciembre ya estaría leyendo si el grifo cambió el 2 de enero. Para blindar el modelo contra esta fuga invisible, la función `entrenamiento()` detiene los datos **6 días antes** del inicio del mes evaluado. Cero contaminación.

### El Gran Debate: ¿Por qué Ventana Rodante de 6 Meses (*Rolling*) y NO Ventana Acumulativa (*Expanding*)?
Un revisor o jurado podría cuestionar: *"¿Por qué limitarse a 6 meses fijos en lugar de acumular toda la historia desde 2020 a medida que avanza el tiempo?"*.

La respuesta se sustenta en tres principios econométricos y empíricos:

#### 1. Quiebres Estructurales y *Concept Drift* (El mercado cambia)
Los precios de los combustibles en el Perú no son juguetes navideños con estacionalidad anual de 12 meses; responden a la paridad de importación del crudo internacional, el tipo de cambio y decretos supremos del Fondo de Estabilización de Precios (FEPC).
* Acumular datos de 2020 (pandemia, barril a 20 USD y demanda colapsada) o de 2022 (shock por la guerra de Ucrania con subsidios estatales de emergencia) **envenena el entrenamiento** enseñándole relaciones precio-margen que ya no existen en 2025.
* La literatura económica de frontera (**Pesaran & Timmermann, 2005; López de Prado, 2018**) demuestra formalmente que ante la presencia de quiebres estructurales continuos, una **ventana rodante (*Rolling Window*) supera a la ventana acumulativa (*Expanding Window*)** porque minimiza el sesgo por obsolescencia.

#### 2. Cero Desperdicio de Datos (3.37 Millones de Observaciones)
Una ventana de 6 meses contiene en promedio **3,370,327 filas**. No existe escasez muestral que justifique arrastrar años obsoletos.

#### 3. La Memoria Larga ya está en las Variables
El modelo no "olvida" el pasado lejano del grifo porque variables como `n_cambios_90` y `anomalia_espera` ya codifican la inercia histórica de largo plazo dentro del vector de características ($X$), mientras que la ventana móvil garantiza que la función predictiva ($f(X) \rightarrow y$) se mantenga calibrada al régimen macroeconómico actual.

---

## Capítulo 6: La Curva de Aprendizaje: Por qué 300,000 Filas y luego 1 Millón

Dentro de la ventana de 6 meses hay más de 3.3 millones de filas disponibles. ¿Con cuántas debemos entrenar?

En la **Sección 12**, trazamos la curva de aprendizaje empírica evaluando 4 tamaños de muestra en los 12 meses de 2025:

| Filas de Entrenamiento | AUC Promedio | Precisión@100 ($p@100$) | Tiempo por Bloque |
| :---: | :---: | :---: | :---: |
| **50,000** | 0.7263 | 59.68% | 2.2 s |
| **100,000** | 0.7292 | 61.25% | 3.3 s |
| **300,000** | **0.7317** | **61.56%** | **11.1 s** |
| **1,000,000** | **0.7325** | **61.83%** | **31.2 s** |

### La Ley de Rendimientos Decrecientes (*Diminishing Returns*)
* Al pasar de 50k a 300k filas, el modelo dio un salto cuantitativo fundamental ($+0.0054$ de AUC y casi $2$ puntos porcentuales de precisión).
* Al pasar de 300k a 1,000,000 de filas, **el AUC solo aumentó $+0.0008$** (menos de un $0.08\%$), pero el tiempo de entrenamiento se multiplicó por **$2.8 \times$** y la memoria RAM se triplicó.

### La Decisión Estratégica
* **Fase de Comparación de 39 Ensambles (Secciones 13 a 15):** Usamos **300,000 filas**. ¿Por qué? Porque teníamos que correr 39 variantes en 12 bloques (cientos de entrenamientos). Hacerlo con 1 millón habría demorado más de 20 horas sin alterar en lo absoluto el orden de quién era el mejor ensamble.
* **Fase de Prueba 2026 y Modelo Final (Secciones 18 y 20):** Como ya sabíamos cuál era el ensamble ganador, **activamos el tope de 1,000,000 de filas** (`filas_finales()`). Capturamos ese pequeño empujón final de precisión para el producto entregado a Osinergmin.

---

## Capítulo 7: La Batalla de los 39 Ensambles y el Nacimiento de STJC

En la Sección 13 entrenamos a nuestros 4 analistas base: **CatBoost, XGBoost, LightGBM y Random Forest**. 

Los 4 modelos demostraron ser muy competitivos (AUC entre $0.728$ y $0.733$), pero tenían una particularidad: sus predicciones tenían una **correlación de Spearman entre 0.912 y 0.978**. Estaban de acuerdo el 95% del tiempo.

En la Sección 14, nos propusimos combinarlos para superar al mejor de ellos. Pusimos a competir **39 configuraciones de ensambles** agrupadas en 11 familias metodológicas.

### El Fracaso de los Ensambles Hipercomplejos (13 ensambles sacaron 0 de 4)
* **Boosting como Metamodelo (AdaBoost, LightGBM meta):** Fracasó rotundamente. Un metamodelo de gradiente intentó encontrar relaciones no lineales ultra complejas entre las 4 probabilidades. Al estar tan correlacionadas, memorizó ruido y sobreajustó.
* **Stacking No Lineal con Random Forest:** Fracasó por la misma razón.
* **Stacking Lineal Clásico (sin regularización):** La regresión logística sin frenos asignó coeficientes absurdos (por ejemplo, $+1.8$ a XGBoost y $-0.9$ a CatBoost) debido a la multicolinealidad extrema de las 4 entradas. ¡Le restaba conocimiento a modelos excelentes!

### El Triunfo de la Parsimonia y la Creación de STJC
Solo **8 ensambles lograron la hazaña de superar a todos los modelos individuales en las 4 métricas al mismo tiempo (4 de 4)**. Entre ellos brillaron dos enfoques complementarios:

#### 1. Votación Suave (*Soft Voting* / Stacking Promedio)
* Asigna exactamente un $25\%$ de peso a cada modelo:
  $$P_{\text{final}} = \frac{P_{\text{Cat}} + P_{\text{Lgb}} + P_{\text{Xgb}} + P_{\text{RF}}}{4}$$
* **Resultado:** Logró el **mejor AUC global de toda la tesis ($0.7355$)**. Al promediar en partes iguales, los errores estocásticos de cada algoritmo se anulan mutuamente sin introducir sobreajuste alguno.

#### 2. STJC: Stacking Temporal Jerárquico con Contracción (Nuestra Propuesta Metodológica)
Diseñamos un método propio concebido para resolver las debilidades del stacking tradicional en series de tiempo:
1. **Multiventana Temporal:** Aprende los pesos evaluando cómo rindieron los modelos en las predicciones fuera de bolsa de los **3 meses previos** (no en filas estáticas).
2. **Pesos Convexos:** Restringe matemáticamente los coeficientes para que sean no negativos ($w_i \ge 0$) y sumen exactamente $100\%$ ($\sum w_i = 1$). Prohibido restar conocimiento.
3. **Contracción (*Shrinkage* hacia pesos iguales):** Si un modelo parece haber ganado por suerte en el último mes, el optimizador contrae los pesos hacia el reparto equitativo ($0.25$ cada uno).
4. **Jerarquía por Combustible:** Permite pesos ligeramente diferenciados por tipo de combustible (Diesel vs. GLP) únicamente si demuestran mejorar el AUC.

```
Ablación Pieza por Pieza de STJC (Sección 14.11):
Estrategia                     AUC     p@100     Brier     ¿Qué aportó la pieza?
Stacking clásico temporal    0.7338   0.6198    0.1072    Punto de partida
+ Multiventana (3 meses)     0.7343   0.6193    0.1039    Baja drásticamente el Brier (-0.0033)
+ Pesos convexos (w >= 0)    0.7347   0.6203    0.1033    Mejora AUC (+0.0004) y p@100
+ Contracción (Shrinkage)    0.7352   0.6246    0.1032    Dispara p@100 (+0.43%)
STJC Método Completo         0.7348   0.6251    0.1031    RÉCORD EN p@100 Y BRIER
```

* **Resultado de STJC:** Rompió el **récord absoluto de precisión en los 100 primeros inspeccionados ($p@100 = 62.51\%$)** y logró la **mejor calibración probabilística de toda la tesis (Brier $= 0.1031$)**.

---

## Capítulo 8: Pruebas de Estrés y Auditoría Científica

Antes de proclamar victoria, sometimos a los modelos ganadores a tres pruebas de estrés destructivas:

### 1. ¿Fue suerte o casualidad? (365 Pruebas Diarias de Wilcoxon + Holm)
En la Sección 15.1, evaluamos el desempeño día por día durante los **365 días del año 2025**.
* Comparamos cada ensamble contra cada uno de los 4 modelos individuales en las 4 métricas ($4 \times 4 = 16$ comparaciones pareadas).
* Aplicamos la prueba de rangos con signo de Wilcoxon con la corrección más estricta de la literatura: **Holm-Bonferroni**.
* **Resultado:** Tanto Votación Suave como STJC ganaron **16 de 16 comparaciones con $p_{\text{holm}} < 0.001$**. Quedó certificado: la ventaja del ensamble es estadísticamente indiscutible a lo largo de todo el año.

### 2. ¿Hubo trampa o fuga oculta? (Prueba Negativa de Etiquetas Permutadas)
En la Sección 17, tomamos la columna `cambia` y la **desordenamos completamente al azar** como barajando cartas. Si existiera alguna fuga de datos invisible en las 29 variables, el modelo haría trampa y obtendría un AUC alto.
* **Resultado:** El AUC promedio cayó a **`0.4886`** (con intentos entre $0.466$ y $0.518$, centrado exactamente en el $0.50$ de una moneda al aire).
* **Conclusión:** Queda demostrado que no existe fuga de información (*zero data leakage*).

### 3. ¿El ensamble sobreajusta o "alucina"?
Comparamos el AUC en el conjunto de entrenamiento contra el conjunto de validación:
* *Random Forest individual:* Mostró sobreajuste evidente (Entrenamiento: $0.8096$ vs. Validación: $0.7282$, brecha de $+0.0814$).
* *STJC y Votación Suave:* La brecha fue de **`+0.0001`** (prácticamente cero).
* **Conclusión:** El ensamble actúa como un escudo regularizador perfecto que cancela los vicios de memorización de los árboles individuales.

---

## Capítulo 9: El Examen de la Vida Real (2026) y el Despliegue Operativo

Todo lo anterior se ejecutó sobre datos hasta 2025. El año **2026 estuvo completamente sellado bajo llave**.

En la Sección 18, abrimos la bóveda de 2026 y ejecutamos la simulación operativa real sobre **262 días continuos (enero a septiembre de 2026)** con el modelo final entrenado con 1 millón de filas y reentrenamiento trimestral:

### 1. Precisión en la Calle: El Top 100 Diario ($p@100$)
* Cada día se ordenaron los más de 20,000 establecimientos activos y se tomaron los 100 primeros.
* **El resultado:** El modelo logró un promedio de **$78.4\%$ de aciertos reales** (en julio de 2026 alcanzó un impresionante **$93.8\%$**).
* De las 26,200 visitas simuladas en el año (100 por día $\times$ 262 días), **20,539 grifos efectivamente cambiaron de precio** en los 5 días posteriores a la visita.

### 2. Derrota Contundente de las Reglas Tradicionales de Osinergmin
Comparamos el modelo contra la regla empírica histórica de Osinergmin (`n_cambios_28`, supervisar a los que más cambiaron el mes pasado):
* Regla histórica: AUC diario = $0.7044$.
* Modelo predictivo: AUC diario = **$0.7459$**.
* Prueba de Wilcoxon pareada día a día: **$p = 4.88 \times 10^{-35}$**. La superioridad del modelo sobre la heurística manual del Estado es abrumadora.

### 3. La Prueba de Establecimientos "Nunca Vistos"
Antes de empezar el estudio, apartamos al azar el **$30\%$ de los grifos del país** y prohibimos que entraran en ningún entrenamiento. En 2026 evaluamos cómo se comportaba el modelo en esos locales desconocidos:
* AUC en grifos conocidos: **$0.804$** (en julio 2026).
* AUC en grifos nunca vistos: **$0.802$** (en julio 2026).
* El modelo no memoriza nombres comerciales; aprendió dinámicas macro y microeconómicas transferibles a cualquier punto del mapa.

### 4. Trazabilidad del 100% al Comprobante Físico del SCOP (Sección 20.2)
Para responder a la pregunta de cualquier jurado: *"¿Cómo sé que el precio realmente cambió?"*:
* Para el **100.0% de los 20,539 aciertos** en el Top 100 de 2026, el código rastreó y encontró el reporte original en el sistema SCOP con su fecha, hora y precio exacto.

---

## Epílogo: Ficha Maestra de Preguntas Incómodas para la Defensa de Tesis

| Pregunta Incómoda del Jurado | Respuesta Técnica y Contundente |
| :--- | :--- |
| *1. ¿Por qué tu AUC es 0.74 y no 0.95?* | En economía y microdatos con decisiones humanas privadas, un AUC de 0.74 es **sólido según Hosmer & Lemeshow (2000)**. No tenemos sensores en los tanques de gasolina ni escuchamos las llamadas entre mayoristas y dueños. Un AUC de 0.95 en este problema sería síntoma inequívoco de trampa o fuga de datos (*data leakage*). Además, en el segmento operativo relevante (Top 100), el modelo acierta el **78.4% de las veces**. |
| *2. ¿Por qué no aplicaste SMOTE o balanceo de clases si tenías solo 13% de positivos?* | Probamos 8 métodos de balanceo en los 12 bloques de 2025. SMOTE y ADASYN colapsaron el AUC a 0.70 al generar datos sintéticos irreales en coordenadas geográficas inexistentes. Al aplicar la corrección analítica de Dal Pozzolo (2015), **entrenar con los datos naturales (`ninguno`) superó a todos los métodos en las 4 métricas**. |
| *3. ¿Por qué una ventana rodante de 6 meses y no acumular toda la historia desde 2020?* | El mercado de hidrocarburos sufre **quiebres estructurales (*Concept Drift*)**. Acumular 2020 (pandemia) o 2022 (shock de Ucrania y subsidios extintos) envenena el modelo con regímenes regulatorios muertos. Como demuestran Pesaran & Timmermann (2005) y López de Prado (2018), ante quiebres de régimen la ventana rodante es superior. Además, 6 meses contienen 3.37 millones de filas, garantizando saturación muestral. |
| *4. ¿Por qué entrenar con 300k filas y no con 1 millón en las comparaciones?* | Nuestra curva de aprendizaje (Sección 12) demostró que pasar de 300k a 1M de filas solo aportaba $+0.0008$ de AUC (menos de 0.08%), triplicando el tiempo de cómputo. Aplicamos la regla de parsimonia: 300k para comparar limpiamente 39 ensambles en 12 meses, y **1 millón de filas para el modelo final entregado en producción**. |
| *5. ¿Por qué ganaron ensambles simples como Votación Suave y STJC frente a redes o boosting como metamodelo?* | Porque nuestros 4 modelos base ya eran altamente competentes y estaban correlacionados al 95%. Cuando los expertos ya coinciden en un 95%, un metamodelo no lineal complejo solo sobreajusta e inventa ruido. Lo que el mercado requería era **parsimonia y regularización convexa** (como la contracción hacia pesos iguales de STJC). |
