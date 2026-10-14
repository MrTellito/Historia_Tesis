# Diccionario Metodológico de Variables del Modelo Predictivo SCOP

**Documento Técnico de Operacionalización de Variables**  
*Caso de Estudio:* Registro de Precios del Sistema de Control de Órdenes de Pedido (SCOP – Osinergmin, Perú)  
*Dataset Base:* Matriz Panel Longitudinal de 39,080,122 observaciones (2020–2026)  
*Formato:* Monocromático estándar para defensa de tesis y revisión académica.  

---

## 1. Definición Formal de la Variable Dependiente (Target)

| Propiedad | Especificación Técnica |
| :--- | :--- |
| **Nombre en Código** | `cambia` |
| **Símbolo Matemático** | $Y_{i,c,t} \in \{0, 1\}$ |
| **Definición Operacional** | Indicador binario que registra si el establecimiento $i$ modifica el precio del combustible $c$ en el surtidor en algún momento dentro de la ventana de 5 días calendario posteriores al día de predicción $t$. |
| **Formulación Matemática** | $$Y_{i,c,t} = \begin{cases} 1 & \text{si } \exists \, k \in [t+1, t+5] \text{ tal que } P_{i,c,k} \neq P_{i,c,t} \\ 0 & \text{en caso contrario} \end{cases}$$ |
| **Tipo de Variable** | Binaria dicotómica |
| **Tipo de Dato (`dtype`)** | `int8` |
| **Horizonte Temporal ($H$)** | **5 días calendario** (Semana laboral de supervisión). |
| **Justificación del Horizonte** | • **¿Por qué no 1 día?** La logística de despacho de órdenes de inspección y desplazamiento de cuadrillas inspectoras en territorio peruano requiere un margen operativo mínimo de preparación.<br>• **¿Por qué no 30 días?** Una ventana mensual generaría una tasa positiva excesivamente alta, perdiendo especificidad táctica para la programación semanal.<br>• **¿Por qué 5 días?** Coincide con la jornada de fiscalización de lunes a viernes y equilibra la tasa base de eventos. |
| **Tasa Base Observada** | • **Año 2025 (Validación Temporal 12 Bloques):** **13.12%** de casos positivos ($1$ de cada $8$ registros cambia de precio).<br>• **Año 2026 (Prueba Operativa Real 262 Días):** **32.61%** promedio anual (periodo de alta volatilidad macroeconómica). |
| **Regla de Continuidad** | **Arrastre (*Forward-Fill*) de 60 días:** Si un establecimiento no emite un nuevo reporte diario, se asume vigente su último precio oficial hasta un límite de 60 días sin actividad. |
| **Blindaje Metodológico** | **Purga Temporal de 6 días ($H+1$):** Separación obligatoria entre el fin de la ventana de entrenamiento y el inicio del bloque de evaluación para evitar filtración del futuro (*data leakage*). |

---

## 2. Estructura del Vector de Variables Independientes ($X \in \mathbb{R}^{29}$)

El vector predictivo está compuesto por **29 características estructuradas** agrupadas en **4 dimensiones analíticas**:

1. **Dimensión I: Inercia y Dinámica Temporal del Establecimiento (10 variables)**  
   Capturan la rigidez o frecuencia intrínseca de ajuste de precios de cada local, su velocidad de cambio reciente y su tendencia direccional (alzas vs. bajas).
2. **Dimensión II: Señales de Mercado y Tendencia Macroeconómica (8 variables)**  
   Miden el comportamiento global del mercado nacional, la desviación del precio respecto a la media de la industria y la volatilidad longitudinal.
3. **Dimensión III: Presión Competitiva Espacial y Geográfica (5 variables)**  
   Registran la presión ejercida por competidores cercanos dentro del mismo departamento y provincia, midiendo qué porcentaje de los vecinos ya ajustó su precio.
4. **Dimensión IV: Estructurales, Identidad de Producto y Calendario (6 variables)**  
   Codifican la heterogeneidad técnica del combustible (5 familias regulatorias), la escala del local (número de productos comercializados) y los ciclos de abastecimiento semanal y mensual.

---

## 3. Descripción Detallada por Dimensión Analítica

### 3.1 Dimensión I: Inercia y Dinámica Temporal del Establecimiento (10 Variables)

* **`dias_sin_cambio` (Conteo):** Días continuos transcurridos desde la última modificación efectiva del precio en dicho combustible.
* **`n_cambios_7`, `n_cambios_14`, `n_cambios_28`, `n_cambios_90` (Conteos):** Número de ajustes de precio ejecutados por el local en los últimos 7, 14, 28 y 90 días calendario.
* **`reportes_sin_cambio_28` (Conteo):** Frecuencia con la que el establecimiento envió reportes al SCOP ratificando su precio sin alterarlo durante las últimas 4 semanas.
* **`frac_subidas_28` (Proporción $[0, 1]$):** Proporción de cambios que representaron incrementos de precio respecto al total de movimientos en 28 días.
* **`magnitud_ultimo_cambio_pct` (Continua):** Magnitud porcentual del último ajuste registrado: $\frac{P_{\text{nuevo}} - P_{\text{anterior}}}{P_{\text{anterior}}} \times 100$.
* **`anomalia_espera` (Continua - Hazard Rate / "Despertador"):**  
  Mide cuántas veces su intervalo típico de espera lleva el establecimiento sin modificar su precio. Si un local cambia históricamente cada 15 días y acumula 30 días estático, su probabilidad de cambio inminente se incrementa:
  $$\text{anomalia\_espera}_{i,t} = \frac{\text{dias\_sin\_cambio}_{i,t} \cdot (n\text{\_cambios\_90}_{i,t} + 1)}{90}$$
  *Impacto empírico:* Resultó ser la **5.ª variable más importante** de todo el modelo final (caída de AUC por permutación de $+0.00478$).

### 3.2 Dimensión II: Señales de Mercado y Tendencia Macroeconómica (8 Variables)

* **`precio` (Continua):** Precio oficial vigente en soles (PEN) por galón (o cilindro de 10 kg en GLP-E).
* **`delta_1_pct`, `delta_3_pct`, `delta_7_pct` (Continuas):** Variación porcentual acumulada del precio del propio establecimiento en los últimos 1, 3 y 7 días.
* **`desv_media_movil_pct` (Continua):** Diferencia porcentual entre el precio actual y su media móvil de 28 días.
* **`volatilidad_7` (Continua):** Desviación estándar muestral del precio del local en la última semana.
* **`mercado_delta_1_pct` (Continua):** Tasa de variación del precio promedio nacional de dicho combustible en las últimas 24 horas.
* **`mercado_pct_cambia` (Proporción $[0, 1]$):** Porcentaje del total de establecimientos del país que cambiaron de precio en las últimas 24 horas.
* **`desv_mercado_pct` (Continua):** Brecha porcentual entre el precio del local y el promedio nacional vigente.
* **`percentil_mercado` (Proporción $[0, 1]$):** Posición relativa del precio del local en la distribución acumulada nacional (0.0 = más barato del país, 1.0 = más caro).

### 3.3 Dimensión III: Presión Competitiva Espacial y Geográfica (5 Variables)

* **`provincia_pct_cambia` (Proporción $[0, 1]$):** Porcentaje de establecimientos de la misma provincia que cambiaron de precio ayer.
* **`desv_provincia_pct` (Continua):** Brecha porcentual del precio respecto a la mediana provincial.
* **`depto_pct_cambia` (Proporción $[0, 1]$):** Porcentaje de establecimientos del mismo departamento que cambiaron de precio ayer.
* **`desv_depto_pct` (Continua):** Brecha porcentual del precio respecto a la mediana departamental.
* **`depto_code` (Categórica Nominal):** Código numérico del departamento geográfico (25 regiones del Perú).

### 3.4 Dimensión IV: Estructurales, Identidad de Producto y Calendario (6 Variables)

* **`combustible_code` (Categórica Nominal):** Identificador del producto:
  - `0`: Diesel B5 S-50 UV
  - `1`: Gasolina / Gasohol Premium
  - `2`: Gasolina / Gasohol Regular
  - `3`: GLP Envasado en Cilindro de 10 kg (GLP-E)
  - `4`: GLP Automotriz a Granel (GLP-G)
* **`actividad_code` (Categórica Nominal):** Modalidad operativa del local (Estación de servicio, Grifo rural, Gasocentro GLP, Local comunal GLP-E).
* **`n_productos` (Conteo):** Número de combustibles distintos comercializados por el mismo establecimiento (1 a 5).
* **`dia_semana` (Calendario Ordenado):** Día de la semana (0 = Lunes, ..., 6 = Domingo). Captura ciclos semanales de abastecimiento mayorista de Petroperú y refinerías.
* **`mes` (Calendario Ordenado):** Mes del año (1 a 12). Modela estacionalidad de transporte y cosechas.

---

## 4. Tabla Maestra de Especificación Técnica de las 29 Variables

| # | Variable | Dimensión Analítica | Tipo | `dtype` | Faltantes | Rango / Valores | Tratamiento Algorítmico | Caída AUC (Ranking) |
|---|:---|:---|:---|:---:|:---:|:---:|:---|:---:|
| 1 | `dia_semana` | Estructural / Cal. | calendario ordenado | `int8` | 0.0% | [0, 6] (7 cat) | numerica, sin escalar | +0.02447 |
| 2 | `mercado_delta_1_pct` | Mercado / Macro | continua | `float32` | 0.0% | [-2.46, 13.09] | numerica, sin escalar | +0.01359 |
| 3 | `n_cambios_90` | Inercia Temporal | conteo | `float32` | 0.0% | [0, 60] | numerica, sin escalar | +0.01195 |
| 4 | `precio` | Mercado / Macro | continua | `float32` | 0.0% | [4.09, 95.00] | numerica, sin escalar | +0.00864 |
| 5 | `anomalia_espera` | Inercia Temporal | continua | `float32` | 0.0% | [0.00, 16.20] | numerica, sin escalar | +0.00478 |
| 6 | `reportes_sin_cambio_28` | Inercia Temporal | conteo | `float32` | 0.0% | [0, 169] | numerica, sin escalar | +0.00444 |
| 7 | `provincia_pct_cambia` | Presión Espacial | proporcion (0 a 1) | `float32` | 0.0% | [0.00, 1.00] | numerica, sin escalar | +0.00434 |
| 8 | `n_cambios_28` | Inercia Temporal | conteo | `float32` | 0.0% | [0, 23] | numerica, sin escalar | +0.00379 |
| 9 | `mercado_pct_cambia` | Mercado / Macro | proporcion (0 a 1) | `float32` | 0.0% | [0.00, 0.61] | numerica, sin escalar | +0.00353 |
| 10 | `combustible_code` | Estructural / Cal. | categorica nominal | `int8` | 0.0% | [0, 4] (5 cat) | categoria nativa / one-hot en RF | +0.00325 |
| 11 | `dias_sin_cambio` | Inercia Temporal | conteo | `float32` | 0.0% | [0, 1458] | numerica, sin escalar | +0.00300 |
| 12 | `magnitud_ultimo_cambio_pct` | Inercia Temporal | continua | `float32` | 0.0% | [-45.60, 127.27] | numerica, sin escalar | +0.00239 |
| 13 | `desv_depto_pct` | Presión Espacial | continua | `float32` | 0.0% | [-51.63, 100.29] | numerica, sin escalar | +0.00220 |
| 14 | `depto_pct_cambia` | Presión Espacial | proporcion (0 a 1) | `float32` | 0.0% | [0.00, 1.00] | numerica, sin escalar | +0.00159 |
| 15 | `desv_provincia_pct` | Presión Espacial | continua | `float32` | 0.0% | [-50.52, 86.92] | numerica, sin escalar | +0.00117 |
| 16 | `delta_3_pct` | Mercado / Macro | continua | `float32` | 0.7% | [-38.04, 134.04] | numerica, sin escalar | +0.00105 |
| 17 | `volatilidad_7` | Mercado / Macro | continua | `float32` | 0.7% | [0.00, 39.73] | numerica, sin escalar | +0.00092 |
| 18 | `percentil_mercado` | Mercado / Macro | proporcion (0 a 1) | `float32` | 0.0% | [0.00, 1.00] | numerica, sin escalar | +0.00070 |
| 19 | `desv_media_movil_pct` | Mercado / Macro | continua | `float32` | 0.2% | [-31.37, 117.31] | numerica, sin escalar | +0.00057 |
| 20 | `desv_mercado_pct` | Mercado / Macro | continua | `float32` | 0.0% | [-49.57, 124.46] | numerica, sin escalar | +0.00051 |
| 21 | `depto_code` | Presión Espacial | categorica nominal | `int16` | 0.0% | [0, 24] (25 cat) | categoria nativa / one-hot en RF | +0.00048 |
| 22 | `frac_subidas_28` | Inercia Temporal | proporcion (0 a 1) | `float32` | 40.3% | [0.00, 1.00] | numerica, sin escalar | +0.00038 |
| 23 | `delta_7_pct` | Mercado / Macro | continua | `float32` | 1.7% | [-40.00, 184.97] | numerica, sin escalar | +0.00027 |
| 24 | `actividad_code` | Estructural / Cal. | categorica nominal | `int16` | 0.0% | [0, 10] (11 cat) | categoria nativa / one-hot en RF | +0.00016 |
| 25 | `n_productos` | Estructural / Cal. | conteo | `float32` | 0.0% | [1, 5] | numerica, sin escalar | +0.00013 |
| 26 | `delta_1_pct` | Mercado / Macro | continua | `float32` | 0.3% | [-45.60, 71.09] | numerica, sin escalar | +0.00009 |
| 27 | `mes` | Estructural / Cal. | calendario ordenado | `int8` | 0.0% | [1, 12] (12 cat) | numerica, sin escalar | +0.00000 |
| 28 | `n_cambios_7` | Inercia Temporal | conteo | `float32` | 0.0% | [0, 7] | numerica, sin escalar | -0.00010 |
| 29 | `n_cambios_14` | Inercia Temporal | conteo | `float32` | 0.0% | [0, 12] | numerica, sin escalar | -0.00082 |

---

## 5. Tratamiento de Datos, Imputación y Diagnóstico de Colinealidad

1. **Valores Faltantes (`NaN`):**
   - En variables de variación corta (`delta_1_pct`, `volatilidad_7`), los faltantes ocurren únicamente en los primeros días de operación de un grifo nuevo antes de acumular historial. Se imputaron con $0.0$ (ausencia de variación).
   - En `frac_subidas_28`, los casos donde no hubo ningún cambio en 28 días se imputaron con el valor neutro $0.50$ (probabilidad a priori no informativa).
2. **Diagnóstico VIF (Factor de Inflación de la Varianza):**
   - Se toleraron valores de VIF elevados en variables como `desv_media_movil_pct` (VIF = 22.4) y `delta_7_pct` (VIF = 10.1) debido a que los estimadores base son **árboles de decisión no lineales particionados recursivamente** (`CatBoost`, `LightGBM`, `XGBoost`, `Random Forest`), los cuales seleccionan puntos de corte locales de manera invariante frente a colinealidad distributiva global.
3. **Escalamiento:**
   - No se aplicó normalización ni estandarización (*Z-score* / *MinMax*) debido a que los algoritmos basados en árboles son invariantes ante transformaciones monótonas de las variables numéricas, preservando la interpretabilidad directa de las escalas físicas originales (soles, galones, días y porcentajes).
