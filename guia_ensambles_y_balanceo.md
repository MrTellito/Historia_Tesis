# Guía Sencilla y Resumida: Métodos de Balanceo y Ensambles del Estudio SCOP

Este documento resume en lenguaje claro, directo y sin tecnicismos innecesarios **todas las técnicas de balanceo de clases** (Sección 11) y **todas las familias de ensambles** (Secciones 13, 14 y 15) implementadas y evaluadas en el notebook [`tesis_priorizacion_scop_v6.ipynb`](file:///c:/Users/User/Desktop/tesis%20prueba/tesis_corrida_final_todosesambles/prueba7.1/tesis_priorizacion_scop_v6.ipynb).

---

## Parte 1. ¿En qué consisten los Tipos de Balanceo probados? (Sección 11)

### El problema de fondo
En los datos del SCOP (validación 2025), solo alrededor del **13.1 %** de los registros cambian de precio en los siguientes 5 días (aproximadamente **1 de cada 8** casos es positivo `cambia = 1`, y 7 de cada 8 son negativos `cambia = 0`).  
Si no tenemos cuidado, un algoritmo puede volverse "flojo" y enfocarse demasiado en la mayoría que no cambia de precio.

> **Regla de oro aplicada en el notebook:** El balanceo se aplica **únicamente a los datos de entrenamiento**. El mes de prueba/validación jamás se toca para que evalúe la realidad tal cual ocurre en el mercado.

### Los 8 métodos probados (más 1 variante híbrida)

| # | Nombre en código | ¿En qué consiste dicho de forma sencilla? | ¿Cómo le fue en tu experimento? |
|---|---|---|---|
| **1** | **`ninguno`** *(Sin balanceo)* | **Dejar los datos tal cual.** El modelo aprende con la proporción real del mercado (~13 % cambios vs. ~87 % sin cambio). | **Ganador global (1.° puesto en promedio de los 4 modelos).** Como los árboles modernos ya separan bien el riesgo, mantener la realidad intacta dio la mejor precisión en el Top 100 (`p@100 = 0.6151`) y Top 250 (`p@250 = 0.5234`). |
| **2** | **`pesos`** *(Pesos de clase inversos)* | **No se borra ni se inventa ninguna fila, pero cada error en un cambio de precio "duele" más.** Se le da más peso matemático a los casos positivos para que pesen 50 % / 50 % en total durante el aprendizaje. | Mejoró ligeramente el orden global (`AUC = 0.7321`), pero bajó un poco el acierto en los primeros 100 grifos del día (`p@100`). |
| **3** | **`pesos_catboost`** *(Híbrido en Sección 11.2)* | **Aplicar pesos solo a CatBoost y dejar los otros 3 modelos sin balanceo.** | Quedó en **2.° lugar global**, muy cerca de no balancear (`AUC = 0.7318`, `Brier = 0.1038`). |
| **4** | **`submuestreo_1_1`** *(Submuestreo agresivo)* | **Recortar la clase mayoritaria a la par.** Se conservan todos los casos que sí cambiaron de precio y se eligen al azar exactamente la misma cantidad de casos que no cambiaron (proporción **1 a 1**). | Descarta demasiada información útil de establecimientos estables, bajando el `p@100` a `0.6028` en LightGBM. |
| **5** | **`submuestreo_1_3`** *(Submuestreo moderado)* | **Recortar la clase mayoritaria con suavidad.** Por cada caso positivo que cambió de precio, se guardan al azar **3 casos negativos** (proporción **1 a 3**). | Mucho mejor que el 1:1 porque pierde menos contexto de mercado (`p@100 = 0.6151` en LightGBM), quedando casi igual que no balancear. |
| **6** | **`sobremuestreo`** *(Sobremuestreo aleatorio)* | **Fotocopiar a la minoría.** Se duplican al azar filas reales de grifos que sí cambiaron de precio hasta igualar la cantidad de los que no cambiaron (1 a 1). | No aporta información nueva (solo repite filas que el árbol ya vio), logrando `AUC = 0.7325` pero menor precisión en la lista diaria. |
| **7** | **`smotenc`** *(Casos sintéticos con categorías)* | **Inventar "grifos clonados" intermedios.** Toma un caso real que cambió de precio, busca sus 5 vecinos más parecidos **dentro del mismo tipo de combustible** (nunca mezcla Diésel con GLP) y crea un caso artificial promediando sus números y votando sus categorías. | **Cayó fuerte (`AUC = 0.6983`, `p@100 = 0.4941`).** En series de precios, promediar dos grifos distintos rompe la lógica real de los saltos discretos de precio. |
| **8** | **`adasyn`** *(Casos sintéticos adaptativos)* | **Inventar más clones donde el modelo más se confunde.** Igual que SMOTENC (por combustible), pero fabrica más casos sintéticos alrededor de los grifos positivos "difíciles" (los que están rodeados de grifos que no cambiaron). | **El peor resultado (`AUC = 0.6911`, `p@100 = 0.4275`).** Al fabricar casos artificiales justo en la frontera de ruido, confunde al modelo en los primeros puestos de la lista. |
| **9** | **`tomek`** *(Limpieza con Tomek Links)* | **Limpiar la frontera borrosa.** Busca parejas de casos muy parecidos donde uno cambió de precio y el otro no ("vecinos pegados de distinta clase") y elimina el caso negativo para despejar el camino. | Fue el mejor entre las técnicas que tocan filas (`AUC = 0.7327` en LightGBM), pasando a la final de 4 modelos y quedando en **3.° lugar global**. |

### El toque maestro de tu notebook: Corrección de Probabilidades de Dal Pozzolo (Sección 9.1)
Cuando entrenas un modelo con datos balanceados (por ejemplo, 50 % positivos y 50 % negativos), el modelo sale creyendo que la mitad de los grifos del Perú cambian de precio todos los días, y devuelve probabilidades infladas (ej. 0.60 cuando el riesgo real es 0.15), arruinando el **Brier Score**.
- **¿Qué hace tu código?** Aplica la fórmula analítica de *Dal Pozzolo et al. (2015)* que **recalcula la probabilidad de vuelta a la proporción real de entrenamiento (~13 %)** usando la diferencia de *log-odds* (logits).
- **Ventaja clave:** No altera ni un milímetro el orden de la lista diaria (el `AUC`, `p@100` y `p@250` quedan idénticos), pero hace que las probabilidades sean **100 % honestas y comparables**.

---

## Parte 2. Los 4 Modelos Base y cómo aprenden los Ensambles (Sección 13)

Antes de armar los ensambles, el notebook entrena **4 algoritmos de árboles con filosofías distintas** (los "4 expertos"):
1. **CatBoost:** Árboles **simétricos** (*oblivious trees*, usan la misma pregunta en todo un nivel de profundidad). Muy resistente al sobreajuste.
2. **LightGBM:** Árboles que crecen **por hoja** (*leaf-wise*, abren la rama que más reduce el error). El más veloz y fino detectando patrones locales.
3. **XGBoost:** Árboles que crecen **por nivel** (*depth-wise*) con fuerte penalización matemática ($L_1$/$L_2$). El mejor individual en `AUC` (`0.7333`).
4. **Random Forest:** **Bosque paralelo** de 300 árboles independientes (cada uno ve una muestra aleatoria de datos y variables) cuyas respuestas se promedian.

> Además, en la Sección 13 se evalúa cada uno en su versión **`_calibrado`** (pasando sus predicciones por una Regresión Isotónica aprendida en el último mes para ajustar sus probabilidades).

### Las 2 formas en que aprende un Metamodelo ("Juez Jefe") en la Sección 14
Cuando un ensamble necesita aprender "cuánto caso hacerle a cada uno de los 4 modelos", el notebook prueba dos modos:
- **Modo Por Grifo (sin sufijo):** Divide los 6 meses de entrenamiento en 5 grupos de establecimientos (`GroupKFold`). Los modelos predicen los grifos que no vieron y el metamodelo aprende ahí. *(Problema descubierto en tu tesis: dentro de los mismos 6 meses, premia al modelo que memoriza mejor el pasado, no necesariamente al que predice mejor el mes siguiente).*
- **Modo Temporal (sufijo `_temporal`):** Entrena los 4 modelos con los primeros 5 meses y predice el **último mes** (con purga de 5 días). El metamodelo aprende en ese último mes. *(Ventaja: imita exactamente la vida real de predecir el mes futuro).*

---

## Parte 3. ¿En qué consiste cada Ensamble realizado? (Sección 14)

En total, tu notebook evalúa **39 variantes de ensambles** agrupadas en **12 familias**. Aquí tienes qué hace cada una explicado de forma sencilla:

### 14.1 Familia 1: Votación (4 variantes — sin metamodelo complejo)
Combinan las opiniones de los 4 modelos con reglas directas:
1. **`votacion_dura` (Votación por mayoría):** Cada uno de los 4 modelos marca con "Sí" al porcentaje más alto de su lista (ej. top 13 %). El puntaje final es cuántos modelos votaron "Sí" (0, 1, 2, 3 o 4 votos de 4).
2. **`votacion_suave` (Promedio simple):** Suma las 4 probabilidades y las divide entre 4 (cada modelo pesa 25 %). **Fue el #1 en `AUC` (`0.7355`) y superó a todos los individuales en las 4 métricas.**
3. **`votacion_ponderada` (Promedio por mérito reciente):** Promedia las 4 probabilidades, pero dándole un poquito más de peso al modelo que tuvo mejor `AUC` en el último mes. Superó a todos los individuales en **4 de 4 métricas**.
4. **`promedio_de_rangos` (Promedio de puestos del ranking):** En vez de promediar probabilidades, mira en qué puesto del ranking diario quedó cada grifo según cada modelo (ej. puesto 10°, 15°, 8°, 20°), promedia esos puestos y los convierte a probabilidad con regresión isotónica.

---

### 14.2 Familia 2: Bagging (2 variantes — múltiples copias con muestras distintas)
1. **`bagging_xgboost` (Bagging del mejor individual):** Entrena **5 copias de XGBoost** con distintas semillas y muestras aleatorias con reemplazo (*bootstrap*), y promedia las 5 respuestas para reducir la varianza. Superó a los individuales en **3 de 4 métricas**.
2. **`easy_ensemble_lightgbm` (EasyEnsemble):** Entrena **5 modelos LightGBM**, donde cada uno recibe todos los casos positivos y un grupo distinto de casos negativos (1 a 1), y promedia los 5.

---

### 14.3 Familia 3: Boosting como Metamodelo (4 variantes — un árbol que combina a los 4)
En lugar de sumar las 4 predicciones con una fórmula recta, pone a otro algoritmo de *boosting* como "juez" para buscar combinaciones no lineales entre las 4 probabilidades:
1. **`boosting_lightgbm`** y **`boosting_lightgbm_temporal`:** Un LightGBM pequeño (pocas hojas: `num_leaves=7`) recibe las 4 predicciones + el tipo de combustible y decide la probabilidad final.
2. **`boosting_adaboost`** y **`boosting_adaboost_temporal`:** Un clasificador **AdaBoost** (100 árboles pequeños secuenciales) combina las 4 predicciones.
- *Resultado:* Ninguno superó a los individuales (0 de 4). Al ser un juez complejo sobre 4 modelos que ya se parecen mucho, termina sobreajustando.

---

### 14.4 Familia 4: Stacking Lineal (8 variantes — Regresión Logística sobre logits)
Convierte las probabilidades de los 4 modelos a escala *logit* ($\ln(\frac{p}{1-p})$) y entrena una **Regresión Logística** para encontrar los mejores pesos de cada modelo:
1. **`stacking_clasico`** y **`stacking_clasico_temporal`:** Regresión logística estándar sin freno (sin penalización).
2. **`stacking_l1`** y **`stacking_l1_temporal` (Lasso):** Penaliza con norma $L_1$, capaz de poner en **cero exacto** a los modelos redundantes.
3. **`stacking_l2`** y **`stacking_l2_temporal` (Ridge):** Penaliza con norma $L_2$, repartiendo los pesos suavemente sin dejar que uno solo se dispare.
4. **`stacking_elasticnet`** y **`stacking_elasticnet_temporal` (Red Elástica):** Mezcla 50 % Lasso ($L_1$) + 50 % Ridge ($L_2$).
- *Lección clave del notebook:* Las 4 versiones "por grifo" obtuvieron **0 de 4**, mientras que las 4 versiones **`_temporal`** subieron a **2 de 4** (superando a todos en `AUC` y `p@100`). Sin embargo, como la regresión logística libre permite **pesos negativos** (restar la opinión de un modelo cuando los 4 están muy correlacionados), seguía siendo inestable.

---

### 14.5 Familia 5: Stacking No Negativo (2 variantes — Breiman, 1996)
1. **`stacking_no_negativo`** y **`stacking_no_negativo_temporal`:** Es una regresión logística en escala logit pero con una regla estricta: **ningún modelo puede tener peso negativo ($\ge 0$)**; todos suman o valen cero, nunca restan.
- *Resultado:* La versión **`stacking_no_negativo_temporal`** dio un salto inmediato y superó a todos los individuales en **3 de 4 métricas** (`AUC = 0.7348`, `p@100 = 0.6227`, `p@250 = 0.5282`).

---

### 14.6 Familia 6: Stacking No Lineal (2 variantes — Random Forest como juez)
1. **`stacking_random_forest`** y **`stacking_random_forest_temporal`:** Usa un **Random Forest** (200 árboles con hojas grandes de mínimo 200 casos) como metamodelo para combinar las 4 predicciones.
- *Resultado:* Al igual que el boosting como metamodelo, dividir en ramas las probabilidades de 4 modelos muy correlacionados mete ruido (0 de 4 métricas).

---

### 14.7 Familia 7: Blending (1 variante — reserva rápida de un grupo)
1. **`blending`:** En vez de hacer validación cruzada de 5 pliegues completos, toma únicamente **1 quinto (20 %) de los establecimientos** como grupo apartado y entrena ahí una regresión logística sobre las predicciones de los 4 modelos. Es más rápido, pero aprovecha menos datos.

---

### 14.8 Familia 8: Selección de Ensambles de Caruana (4 variantes — el método de AutoGluon)
1. **`seleccion_caruana`** y **`seleccion_caruana_temporal`** (más sus 2 versiones **`_calibrada`**):  
   Empieza con una bolsa vacía y hace **40 rondas**. En cada ronda prueba meter a uno de los 4 modelos a la bolsa (pudiendo repetirlos) y elige al que más haga subir el `AUC` del promedio. Al final, el peso de cada modelo es cuántas veces fue elegido de las 40 (por ejemplo, si eligió 15 veces a CatBoost, 10 a LightGBM, 10 a XGBoost y 5 a RF, sus pesos son `15/40, 10/40, 10/40, 5/40`).
- *Resultado:* Excelente desempeño; tanto `seleccion_caruana` como `seleccion_caruana_temporal` superaron a todos los individuales en las **4 de 4 métricas**.

---

### 14.9 Familia 9: Selección Dinámica y Mezcla de Expertos (2 variantes — especialistas por nicho)
En vez de usar la misma receta para todo el Perú, buscan especializarse según el tipo de grifo o producto:
1. **`seleccion_dinamica`:** Divide el mercado en segmentos (**Combustible × Tipo de establecimiento**). Mira cuál de los 4 modelos fue el campeón el último mes en cada segmento y le delega el 100 % de la predicción de ese nicho.
2. **`mezcla_de_expertos` (Mixture of Experts):** Entrena un **stacking independiente para cada uno de los 5 combustibles** (uno exclusivo para GLP, otro para Diésel, otro para Gasohol Regular, etc.).
- *Resultado:* Al partir los datos en pedazos más pequeños sin regularización hacia el promedio general, los pesos por nicho se vuelven ruidosos (0 de 4 métricas). Esto inspiró la pieza jerárquica con contracción de tu método propio (STJC).

---

### 14.10 Familia 10: Promedio Bayesiano de Modelos — BMA (1 variante)
1. **`promedio_bayesiano`:** Calcula qué tan bien acertó cada modelo las probabilidades del último mes usando la **verosimilitud matemática** (*log-likelihood*, Hoeting et al., 1999). Como hay miles de filas, la fórmula exponencial le da casi el 100 % del peso a un solo modelo y apaga a los demás.

---

### 14.11 Familia 11: Tu Método Propuesto — STJC (*Stacking Temporal Jerárquico con Contracción*, 6 variantes)
Diseñado específicamente en tu tesis para resolver todos los defectos que sufren los stackings clásicos en paneles diarios de mercado. Se construye sumando **5 piezas clave** (más 1 prueba extra de calibración) en un estudio de ablación paso a paso:

| Variante en la tabla | Pieza que agrega | Explicación sencilla de qué hace y por qué funciona | ¿Cuántas métricas supera a TODOS los individuales? |
|---|---|---|---|
| **`nuestro_1_multiventana`** | **1. Múltiples ventanas temporales** | En vez de aprender de un solo mes pasado, el metamodelo aprende de los **3 últimos meses**, donde cada mes fue predicho limpiamente por modelos entrenados solo con su propio pasado (más datos recientes sin trampa temporal). | **3 de 4** |
| **`nuestro_2_pesos_convexos`** | **2. Pesos convexos ($\ge 0$, suman 1)** | Obliga a que los pesos de los 4 modelos en escala logit sean **positivos y sumen 100 %** (como en el *Super Learner*). Prohibido que un modelo reste a otro. | **4 de 4** |
| **`nuestro_3_contraccion`** | **3. Contracción hacia pesos iguales** | Agrega un "imán" ($\lambda$) que jala los pesos hacia el empate perfecto (`25 %, 25 %, 25 %, 25 %`). Si un modelo tuvo suerte un mes, el imán evita darle todo el peso. La fuerza del imán se calibra sola probando cómo ordena el mes más reciente. | **4 de 4** *(sube `p@100` a `0.6246`)* |
| **`nuestro_4_jerarquia`** | **4. Jerarquía por combustible (con freno)** | Permite que cada combustible (GLP, Diésel, Gasoholes) tenga sus propios pesos, pero **atraídos hacia los pesos generales**. Si en el último mes de validación interna diferenciar por combustible no ayuda, **se apaga solo**. | **4 de 4** |
| **`STJC_nuestro_metodo`** *(MÉTODO COMPLETO)* | **5. Bagging temporal adaptativo** | Cada uno de los 4 modelos base promedia su versión entrenada con los 6 meses y sus 3 versiones de las sub-ventanas temporales (suaviza el ruido). Solo se activa en los meses donde demuestra ordenar mejor el mes más reciente. | **4 de 4 (Ganador #1 de la Tabla Maestra: mejor `p@100 = 0.6251` y mejor `Brier = 0.1031`)** |
| **`nuestro_6_mas_calibracion`** | *(Prueba extra: + Calibración isotónica)* | Prueba agregar una regresión isotónica al final. Como desde la v6 cada modelo base ya trae sus probabilidades corregidas por Dal Pozzolo, esta pieza extra no hace falta (aunque logra el mejor `p@250 = 0.5308`). | **3 de 4** |

---

### 14.12 Familia 12: Calibración Final de los Mejores Ensambles (3 variantes)
1. **`votacion_suave_calibrado`**, **`votacion_ponderada_calibrado`** y **`votacion_dura_calibrado`:**  
   Toma a los 3 ensambles con mayor `AUC` de toda la corrida y pasa sus predicciones por una **Regresión Isotónica** final para comprobar si mejora su Brier Score.
- *Resultado:* Como los modelos base ya estaban bien calibrados con la corrección analítica de Dal Pozzolo, recalibrar encima con un solo mes empeoró ligeramente el Brier (bajaron de 4/4 a 3/4).

---

## Parte 4. Resumen Ejecutivo para tu Defensa / Artículo (Sección 15)

Si un jurado te pregunta ***"¿Qué concluiste después de probar 8 balanceos y 39 ensambles?"***, las 3 ideas clave son:

1. **Sobre el Balanceo:** No hace falta alterar ni inventar filas (`ninguno` ganó en el promedio de los 4 modelos). Inventar datos artificiales con `SMOTENC` o `ADASYN` en paneles diarios de precios **destruye la precisión en los primeros puestos de la lista** porque promedia precios de grifos distintos. Y si se usa algún balanceo, es obligatorio aplicar la **corrección analítica de Dal Pozzolo (2015)** para no deformar las probabilidades.
2. **Sobre el Stacking tradicional vs. Temporal:** En paneles de tiempo, armar un stacking separando solo establecimientos ("por grifo") fracasa (**0 de 4 métricas**) porque premia al modelo que memoriza esa ventana histórica. En cambio, entrenar el metamodelo sobre ventanas futuras (**modo `_temporal`**) más **pesos no negativos y contracción** resuelve el problema por completo.
3. **Los Ganadores Absolutos:** Tanto tu método diseñado **`STJC_nuestro_metodo`** (1.° puesto en la Tabla Maestra, mejor `precision@100 = 0.6251` y mejor `Brier = 0.1031`) como la **`votacion_suave`** (2.° puesto en la Tabla Maestra, mejor `AUC = 0.7355`) superaron a **todos los modelos individuales y sus versiones calibradas en las 4 métricas a la vez (4 de 4)** y de manera estadísticamente significativa en los 365 días del año (prueba de Wilcoxon + Holm, 16 de 16 comparaciones ganadas).

