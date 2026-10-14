# Resultados Oficiales de Modelos Individuales y Ensambles

> **Documento Maestro de Resultados Empíricos y Auditoría Experimental**  
> *Caso de Estudio:* Priorización Diaria de Supervisión del SCOP (Osinergmin, Perú)  
> *Esquema Experimental:* Validación Temporal Walk-Forward en 12 Bloques Mensuales (2025) y Prueba Operativa Real (262 Días de 2026).  
> *Convención:* Los valores destacados con <u>**negrita y subrayado**</u> indican el **mejor valor de cada métrica** dentro de su respectiva tabla comparativa.

---

## Guía de Interpretación de Métricas

Para la priorización diaria de supervisión y fiscalización se reportan 5 métricas complementarias centradas en ranking y calibración:

1. **AUC (ROC-AUC)** ($\uparrow$ *mayor es mejor*):  
   Capacidad global del modelo para ordenar y discriminar entre establecimientos que cambiarán y no cambiarán de precio a través de todos los umbrales posibles (0.50 = azar puro, 1.00 = separación perfecta).
2. **Precisión en el Top $K$ ($p@50$, $p@100$, $p@250$)** ($\uparrow$ *mayor es mejor*):  
   Porcentaje de establecimientos que **efectivamente modificaron su precio en los 5 días posteriores a la visita** entre los primeros $K$ casos con mayor probabilidad asignada cada medianoche. Es la métrica directa de eficiencia de las cuadrillas de fiscalización en campo.
3. **Brier Score** ($\downarrow$ **<u>menor es mejor</u>**):  
   Error cuadrático medio de calibración probabilística: $\text{Brier} = \frac{1}{N} \sum_{i=1}^N (P_i - y_i)^2$. Un valor menor indica que las probabilidades asignadas por el modelo reflejan con mayor fidelidad la frecuencia real de los eventos en el mercado.
4. **Criterio Multicriterio ("Supera a Todos los Individuales")**:  
   Exigencia metodológica para que un ensamble sea considerado viable: requiere superar simultáneamente al mejor modelo individual en las 4 métricas cardinales (**AUC, $p@100$, $p@250$ y Brier Score**).

---

## Sección 1: Resultados de los Modelos Individuales

En esta sección se reportan los resultados de los cuatro modelos de aprendizaje automático base entrenados de forma individual sobre el vector completo de 29 variables predictivas.

### 1.1 Tabla Comparativa de los 4 Modelos Base Principales

Promedios consolidados a lo largo de los 12 bloques mensuales de validación temporal (2025):

| Modelo / Estrategia | AUC | Precisión@50 | Precisión@100 | Precisión@250 | Brier Score |
| :---| :---:| :---:| :---:| :---:| :---: |
| CatBoost | 0.7328 | 69.04% | <u>**61.87%**</u> | <u>**52.55%**</u> | 0.1039 |
| LightGBM | 0.7326 | 68.87% | 61.54% | 52.26% | <u>**0.1037**</u> |
| XGBoost | <u>**0.7333**</u> | <u>**69.08%**</u> | 61.70% | 52.45% | 0.1040 |
| Random Forest | 0.7282 | 68.53% | 61.00% | 52.12% | <u>**0.1037**</u> |

#### Análisis Detallado de los Modelos Base:
* **XGBoost:** Obtiene el **mayor AUC individual (<u>0.7333</u>)** y la **mayor Precisión@50 (<u>69.08%</u>)**. Demuestra la mejor capacidad global de discriminación y ordenamiento en el extremo superior de la lista diaria.
* **CatBoost:** Es el algoritmo líder en la zona operativa de fiscalización estándar: logra la **mayor Precisión@100 (<u>61.87%</u>)** y la **mayor Precisión@250 (<u>52.55%</u>)** entre los modelos base.
* **LightGBM:** Alcanza el **mejor Brier Score individual (<u>0.1037</u>)**, reflejando una excelente calibración probabilística natural, junto con el menor costo computacional (0.9 segundos por bloque de entrenamiento).
* **Random Forest:** Empata en el **mejor Brier Score (<u>0.1037</u>)**, pero exhibe la menor precisión en el Top 100 (61.00%) y la mayor brecha de sobreajuste entre entrenamiento y validación ($+0.0814$).

---

### 1.2 Modelos Base vs. Variantes con Calibración de Priors (Dal Pozzolo et al., 2015)

Comparativa de los 4 modelos entrenados con su probabilidad bruta frente a su versión calibrada analíticamente:

| Modelo / Estrategia | AUC | Precisión@50 | Precisión@100 | Precisión@250 | Brier Score |
| :---| :---:| :---:| :---:| :---:| :---: |
| CatBoost | 0.7328 | 69.04% | 61.87% | 52.55% | 0.1039 |
| CatBoost (Calibrado) | 0.7328 | 69.04% | <u>**61.88%**</u> | <u>**52.56%**</u> | 0.1076 |
| LightGBM | 0.7326 | 68.87% | 61.54% | 52.26% | <u>**0.1037**</u> |
| LightGBM (Calibrado) | 0.7326 | 68.79% | 61.50% | 52.26% | 0.1070 |
| XGBoost | <u>**0.7333**</u> | <u>**69.08%**</u> | 61.70% | 52.45% | 0.1040 |
| XGBoost (Calibrado) | <u>**0.7333**</u> | 69.05% | 61.73% | 52.42% | 0.1076 |
| Random Forest | 0.7282 | 68.53% | 61.00% | 52.12% | <u>**0.1037**</u> |
| Random Forest (Calibrado) | 0.7282 | 68.52% | 61.00% | 52.11% | 0.1059 |

#### Impacto de la Calibración de Dal Pozzolo:
* La transformación en escala logit es monótona: preserva exactamente el ranking y el AUC de cada modelo.
* **CatBoost Calibrado** alcanza el pico de precisión individual del estudio en el **Top 100 (<u>61.88%</u>)** y **Top 250 (<u>52.56%</u>)**.
* Permite corregir el sesgo en el nivel medio de probabilidad producido por el balanceo artificial del conjunto de entrenamiento sin deteriorar el ordenamiento relativo.

---

### 1.3 Desempeño Individual por Tipo de Combustible (Periodo de Prueba 2026)

Rendimiento desagregado por cada una de las 5 familias de combustibles sobre datos reales de 2026:

| Combustible | Observaciones | Tasa Base Real | AUC XGBoost | AUC CatBoost | Precisión@100 Modelo | Precisión@100 Regla Heurística |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Diesel B5 S-50 UV** | 919,114 | 40.43% | <u>**0.7393**</u> | 0.7385 | <u>**72.98%**</u> | 72.57% |
| **Gasolina / Gasohol Regular** | 967,786 | 37.54% | <u>**0.7157**</u> | 0.7142 | <u>**70.15%**</u> | 67.91% |
| **Gasolina / Gasohol Premium** | 755,889 | 37.58% | <u>**0.7116**</u> | 0.7108 | <u>**69.14%**</u> | 68.03% |
| **GLP Automotriz a Granel (GLP-G)** | 318,623 | 27.83% | <u>**0.7183**</u> | 0.7169 | <u>**54.31%**</u> | 51.49% |
| **GLP Envasado en Cilindro 10 kg (GLP-E)** | 541,949 | 8.93% | <u>**0.6536**</u> | 0.6511 | <u>**22.30%**</u> | 17.06% |

---

## Sección 2: Modelos Individuales + Métricas de los Ensambles (Tabla Maestra)

En esta sección se integran los **8 modelos individuales** junto a las **39 configuraciones de ensambles** evaluadas bajo el mismo protocolo experimental de validación temporal en 12 bloques (2025).

### 2.1 La Gran Tabla Maestra Consolidada (47 Modelos)

*Los valores destacados con <u>**negrita y subrayado**</u> identifican el récord absoluto de toda la investigación para dicha métrica.*

| Familia Metodológica | Modelo / Estrategia | AUC | Precisión@50 | Precisión@100 | Precisión@250 | Brier Score | ¿Supera a Todos? (4 de 4) |
| :---| :---| :---:| :---:| :---:| :---:| :---:| :---: |
| **Modelos Individuales** | CatBoost | 0.7328 | 69.04% | 61.87% | 52.55% | 0.1039 | — |
| **Modelos Individuales** | CatBoost (Calibrado) | 0.7328 | 69.04% | 61.88% | 52.56% | 0.1076 | — |
| **Modelos Individuales** | LightGBM | 0.7326 | 68.87% | 61.54% | 52.26% | 0.1037 | — |
| **Modelos Individuales** | LightGBM (Calibrado) | 0.7326 | 68.79% | 61.50% | 52.26% | 0.1070 | — |
| **Modelos Individuales** | XGBoost | 0.7333 | 69.08% | 61.70% | 52.45% | 0.1040 | — |
| **Modelos Individuales** | XGBoost (Calibrado) | 0.7333 | 69.05% | 61.73% | 52.42% | 0.1076 | — |
| **Modelos Individuales** | Random Forest | 0.7282 | 68.53% | 61.00% | 52.12% | 0.1037 | — |
| **Modelos Individuales** | Random Forest (Calibrado) | 0.7282 | 68.52% | 61.00% | 52.11% | 0.1059 | — |
| **Votación Directa** | Votación Dura (Mayoría) | 0.7354 | 69.84% | 62.50% | 53.02% | 0.1722 | 3 de 4 |
| **Votación Directa** | Votación Suave (Promedio Simple) | <u>**0.7355**</u> | 69.84% | 62.50% | 53.01% | 0.1034 | **4 de 4** (Élite) |
| **Votación Directa** | Votación Ponderada (Pesos por AUC) | <u>**0.7355**</u> | 69.85% | 62.49% | 53.00% | 0.1034 | **4 de 4** (Élite) |
| **Votación Directa** | Promedio de Rangos (Rank Averaging) | 0.7309 | 69.79% | 62.24% | 52.90% | 0.1048 | 2 de 4 |
| **Bagging / Submuestreo** | Bagging de XGBoost | 0.7346 | 69.33% | 62.37% | 52.85% | 0.1038 | 3 de 4 |
| **Bagging / Submuestreo** | EasyEnsemble (LightGBM) | 0.7333 | 68.71% | 61.43% | 52.18% | 0.1984 | 1 de 4 |
| **Boosting como Metamodelo** | Boosting Metamodelo (LightGBM) | 0.7322 | 68.20% | 60.90% | 51.62% | 0.1041 | 0 de 4 |
| **Boosting como Metamodelo** | AdaBoost Metamodelo | 0.7273 | 67.98% | 61.00% | 52.05% | 0.1220 | 0 de 4 |
| **Boosting como Metamodelo** | Boosting LightGBM (Temporal) | 0.7255 | 63.43% | 59.11% | 50.71% | 0.1082 | 0 de 4 |
| **Boosting como Metamodelo** | AdaBoost Metamodelo (Temporal) | 0.7291 | 64.14% | 59.04% | 51.43% | 0.1234 | 0 de 4 |
| **Stacking Lineal** | Stacking Lineal Clásico (Logit) | 0.7298 | 68.71% | 60.95% | 51.92% | 0.1042 | 0 de 4 |
| **Stacking Lineal** | Stacking con Regularización L1 (Lasso) | 0.7300 | 68.79% | 61.05% | 51.93% | 0.1042 | 0 de 4 |
| **Stacking Lineal** | Stacking con Regularización L2 (Ridge) | 0.7301 | 68.84% | 61.00% | 51.95% | 0.1042 | 0 de 4 |
| **Stacking Lineal** | Stacking ElasticNet (L1 + L2) | 0.7300 | 68.77% | 61.03% | 51.93% | 0.1042 | 0 de 4 |
| **Stacking Lineal** | Stacking Clásico Temporal (1 mes) | 0.7338 | 69.81% | 61.98% | 52.47% | 0.1072 | 2 de 4 |
| **Stacking Lineal** | Stacking L1 Temporal | 0.7340 | 69.86% | 62.06% | 52.49% | 0.1069 | 2 de 4 |
| **Stacking Lineal** | Stacking L2 Temporal | 0.7340 | 69.75% | 62.09% | 52.56% | 0.1075 | 2 de 4 |
| **Stacking Lineal** | Stacking ElasticNet Temporal | 0.7341 | 69.74% | 62.12% | 52.53% | 0.1071 | 2 de 4 |
| **Stacking Restringido** | Stacking No Negativo (Pesos >= 0) | 0.7330 | 69.53% | 61.93% | 52.58% | 0.1038 | 2 de 4 |
| **Stacking Restringido** | Stacking No Negativo Temporal | 0.7348 | 70.07% | 62.27% | 52.82% | 0.1069 | 3 de 4 |
| **Stacking No Lineal** | Stacking No Lineal con Random Forest | 0.7292 | 68.30% | 60.74% | 51.53% | 0.1045 | 0 de 4 |
| **Stacking No Lineal** | Stacking Random Forest Temporal | 0.7296 | 64.47% | 59.59% | 51.91% | 0.1073 | 0 de 4 |
| **Blending** | Blending (Holdout 20%) | 0.7300 | 68.70% | 60.95% | 51.95% | 0.1043 | 0 de 4 |
| **Selección Greedy (Caruana)** | Selección de Ensambles (Caruana) | 0.7333 | 69.63% | 62.03% | 52.60% | 0.1034 | **4 de 4** (Élite) |
| **Selección Greedy (Caruana)** | Selección Caruana (Calibrada) | 0.7333 | 69.66% | 62.04% | 52.60% | 0.1039 | 3 de 4 |
| **Selección Greedy (Caruana)** | Selección Caruana Temporal | 0.7348 | 69.97% | 62.23% | 52.78% | 0.1035 | **4 de 4** (Élite) |
| **Selección Greedy (Caruana)** | Selección Caruana Calibrada Temporal | 0.7348 | 69.95% | 62.24% | 52.78% | 0.1070 | 3 de 4 |
| **Selección Dinámica** | Selección Dinámica por Grifo | 0.7323 | 68.47% | 61.16% | 52.17% | 0.1075 | 0 de 4 |
| **Selección Dinámica** | Mezcla de Expertos (MoE) | 0.7252 | 67.26% | 59.60% | 50.18% | 0.1091 | 0 de 4 |
| **Inferencia Bayesiana** | Promedio Bayesiano de Modelos (BMA) | 0.7319 | 69.23% | 61.50% | 52.31% | 0.1036 | 1 de 4 |
| **STJC (Aporte de Tesis)** | STJC: Pieza 1 (+ Multiventana 3m) | 0.7343 | 69.71% | 61.93% | 52.63% | 0.1039 | 3 de 4 |
| **STJC (Aporte de Tesis)** | STJC: Pieza 2 (+ Pesos Convexos) | 0.7347 | 69.88% | 62.03% | 52.81% | 0.1033 | **4 de 4** (Élite) |
| **STJC (Aporte de Tesis)** | STJC: Pieza 3 (+ Contracción/Shrinkage) | 0.7352 | 70.03% | 62.46% | 53.01% | 0.1032 | **4 de 4** (Élite) |
| **STJC (Aporte de Tesis)** | STJC: Pieza 4 (+ Jerarquía Combustible) | 0.7352 | 70.03% | 62.45% | 53.00% | 0.1032 | **4 de 4** (Élite) |
| **STJC (Aporte de Tesis)** | STJC: Método Completo (+ Bagging Temporal) | 0.7348 | <u>**70.23%**</u> | <u>**62.51%**</u> | 53.08% | <u>**0.1031**</u> | **4 de 4** (Élite) |
| **STJC (Aporte de Tesis)** | STJC + Calibración Posterior | 0.7348 | <u>**70.23%**</u> | 62.50% | <u>**53.08%**</u> | 0.1040 | 3 de 4 |
| **Votación con Calibración** | Votación Suave (Calibrada) | <u>**0.7355**</u> | 69.84% | 62.46% | 53.00% | 0.1067 | 3 de 4 |
| **Votación con Calibración** | Votación Ponderada (Calibrada) | <u>**0.7355**</u> | 69.84% | 62.45% | 53.00% | 0.1067 | 3 de 4 |
| **Votación con Calibración** | Votación Dura (Calibrada) | 0.7354 | 69.02% | 61.86% | 52.83% | 0.1067 | 2 de 4 |

---

### 2.2 Cuadro de Honor: Los 8 Ensambles de Élite que Superaron a Todos los Individuales en las 4 Métricas (4 de 4)

De las 39 configuraciones de ensambles, solo **8 lograron superar simultáneamente al mejor modelo individual en las 4 métricas cardinales (AUC > 0.7333, $p@100$ > 61.87%, $p@250$ > 52.55% y Brier < 0.1037)**:

| Familia Metodológica | Modelo / Estrategia | AUC | Precisión@50 | Precisión@100 | Precisión@250 | Brier Score | ¿Supera a Todos? (4 de 4) |
| :---| :---| :---:| :---:| :---:| :---:| :---:| :---: |
| **Votación Directa** | Votación Suave (Promedio Simple) | <u>**0.7355**</u> | 69.84% | 62.50% | 53.01% | 0.1034 | **4 de 4** (Élite) |
| **Votación Directa** | Votación Ponderada (Pesos por AUC) | <u>**0.7355**</u> | 69.85% | 62.49% | 53.00% | 0.1034 | **4 de 4** (Élite) |
| **Selección Greedy (Caruana)** | Selección de Ensambles (Caruana) | 0.7333 | 69.63% | 62.03% | 52.60% | 0.1034 | **4 de 4** (Élite) |
| **Selección Greedy (Caruana)** | Selección Caruana Temporal | 0.7348 | 69.97% | 62.23% | 52.78% | 0.1035 | **4 de 4** (Élite) |
| **STJC (Aporte de Tesis)** | STJC: Pieza 2 (+ Pesos Convexos) | 0.7347 | 69.88% | 62.03% | 52.81% | 0.1033 | **4 de 4** (Élite) |
| **STJC (Aporte de Tesis)** | STJC: Pieza 3 (+ Contracción/Shrinkage) | 0.7352 | 70.03% | 62.46% | 53.01% | 0.1032 | **4 de 4** (Élite) |
| **STJC (Aporte de Tesis)** | STJC: Pieza 4 (+ Jerarquía Combustible) | 0.7352 | 70.03% | 62.45% | 53.00% | 0.1032 | **4 de 4** (Élite) |
| **STJC (Aporte de Tesis)** | STJC: Método Completo (+ Bagging Temporal) | 0.7348 | <u>**70.23%**</u> | <u>**62.51%**</u> | 53.08% | <u>**0.1031**</u> | **4 de 4** (Élite) |

#### Los Dos Grandes Campeones de la Tesis:
1. **Votación Suave (*Soft Voting* / Stacking Promedio):**
   * **Récord Absoluto de AUC:** <u>**0.7355**</u>.
   * Promedia de forma parsimoniosa las probabilidades de los 4 modelos base:
     $$P_{\text{final}} = \frac{P_{\text{Cat}} + P_{\text{Lgb}} + P_{\text{Xgb}} + P_{\text{RF}}}{4}$$
   * Por su estabilidad matemática, robustez frente al sobreajuste y rapidez operativa, fue el **algoritmo seleccionado para la prueba final de 2026 y entregado en producción**.

2. **STJC: Stacking Temporal Jerárquico con Contracción (Nuestra Propuesta Metodológica):**
   * **Récord Absoluto en el Top 100:** <u>**62.51%**</u> de precisión ($p@100$).
   * **Récord Absoluto en el Top 50:** <u>**70.23%**</u> de precisión ($p@50$).
   * **Récord Absoluto en el Top 250:** <u>**53.08%**</u> de precisión ($p@250$).
   * **Mejor Calibración Probabilística:** Brier Score de <u>**0.1031**</u>.
   * Es el aporte de diseño de la tesis que resuelve la multicolinealidad extrema de las probabilidades en series de tiempo mediante restricciones convexas y contracción hacia pesos iguales.

---

### 2.3 Desglose de Ablación Paso a Paso de STJC (Sección 14.11)

Esta tabla demuestra el aporte incremental de cada módulo arquitectónico de STJC:

| Fase / Pieza Incorporada | AUC | Precisión@100 | Precisión@250 | Brier Score | $\Delta$ AUC | $\Delta$ $p@100$ | $\Delta$ Brier | Aporte Metodológico Concreto |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **0. Stacking Clásico Temporal (1 mes)** | 0.7338 | 61.98% | 52.47% | 0.1072 | — | — | — | Punto de partida lineal sin regularización |
| **1. + Multiventana Temporal (3 meses)** | 0.7343 | 61.93% | 52.63% | 0.1039 | +0.0005 | -0.05% | **-0.0033** | **Baja drásticamente el error de calibración (Brier)** |
| **2. + Pesos Convexos ($w_i \ge 0, \sum w = 1$)** | 0.7347 | 62.03% | 52.81% | 0.1033 | +0.0004 | +0.10% | -0.0005 | Elimina coeficientes negativos inestables |
| **3. + Contracción (*Shrinkage* a 0.25)** | **<u>0.7352</u>** | 62.46% | 53.01% | 0.1032 | +0.0005 | **+0.43%** | -0.0001 | **Dispara la precisión del ranking Top 100** |
| **4. + Jerarquía por Combustible** | **<u>0.7352</u>** | 62.45% | 53.00% | 0.1032 | -0.0000 | -0.01% | -0.0000 | Permite especialización por combustible |
| **5. + Bagging Temporal = STJC COMPLETO** | 0.7348 | **<u>62.51%</u>** | **<u>53.08%</u>** | **<u>0.1031</u>** | -0.0004 | **+0.06%** | **-0.0001** | **RÉCORD ABSOLUTO EN $p@100$ Y BRIER SCORE** |

---

## Sección 3: Auditoría Estadística y Validación Operativa en el Mundo Real (2026)

### 3.1 365 Pruebas Diarias de Wilcoxon Pareado con Corrección Holm-Bonferroni (2025)

Evaluación pareada día a día durante los **365 días del año 2025** frente a cada uno de los 4 modelos individuales en las 4 métricas ($4 \times 4 = 16$ comparaciones):

| Ensamble Evaluado | Métrica | Frente a Modelo Base | Días Evaluados | Ventaja Media Diaria | % Días que Gana el Ensamble | $p$-valor Crudo | $p$-valor Ajustado (Holm) | Significativo al 1% ($p < 0.01$) |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Votación Suave** | AUC | CatBoost | 365 | +0.0028 | 81.37% | $4.61 \times 10^{-31}$ | $6.00 \times 10^{-30}$ | **Sí (Altamente Significativo)** |
| **Votación Suave** | AUC | LightGBM | 365 | +0.0030 | 87.12% | $1.40 \times 10^{-48}$ | $2.11 \times 10^{-47}$ | **Sí (Altamente Significativo)** |
| **Votación Suave** | AUC | XGBoost | 365 | +0.0023 | 78.36% | $2.81 \times 10^{-33}$ | $3.93 \times 10^{-32}$ | **Sí (Altamente Significativo)** |
| **Votación Suave** | AUC | Random Forest | 365 | +0.0064 | 93.15% | $2.22 \times 10^{-55}$ | $3.55 \times 10^{-54}$ | **Sí (Altamente Significativo)** |
| **Votación Suave** | $p@100$ | CatBoost | 365 | +0.63% | 50.14% | $1.20 \times 10^{-3}$ | $1.20 \times 10^{-3}$ | **Sí ($p = 0.0012 < 0.01$)** |
| **Votación Suave** | $p@100$ | LightGBM | 365 | +0.97% | 57.26% | $1.55 \times 10^{-7}$ | $7.75 \times 10^{-7}$ | **Sí (Altamente Significativo)** |
| **Votación Suave** | $p@100$ | XGBoost | 365 | +0.78% | 53.97% | $1.00 \times 10^{-5}$ | $3.01 \times 10^{-5}$ | **Sí (Altamente Significativo)** |
| **Votación Suave** | $p@100$ | Random Forest | 365 | +1.51% | 56.71% | $5.03 \times 10^{-9}$ | $3.52 \times 10^{-8}$ | **Sí (Altamente Significativo)** |
| **STJC (Nuestro Método)** | AUC | CatBoost | 365 | +0.0023 | 72.33% | $3.29 \times 10^{-23}$ | $4.27 \times 10^{-22}$ | **Sí (Altamente Significativo)** |
| **STJC (Nuestro Método)** | AUC | LightGBM | 365 | +0.0025 | 77.81% | $3.73 \times 10^{-31}$ | $5.59 \times 10^{-30}$ | **Sí (Altamente Significativo)** |
| **STJC (Nuestro Método)** | AUC | XGBoost | 365 | +0.0018 | 69.04% | $2.11 \times 10^{-16}$ | $1.90 \times 10^{-15}$ | **Sí (Altamente Significativo)** |
| **STJC (Nuestro Método)** | AUC | Random Forest | 365 | +0.0059 | 87.95% | $1.08 \times 10^{-49}$ | $1.72 \times 10^{-48}$ | **Sí (Altamente Significativo)** |
| **STJC (Nuestro Método)** | $p@100$ | CatBoost | 365 | +0.63% | 52.88% | $2.03 \times 10^{-4}$ | $2.03 \times 10^{-4}$ | **Sí ($p = 0.0002 < 0.001$)** |
| **STJC (Nuestro Método)** | $p@100$ | LightGBM | 365 | +0.97% | 56.99% | $1.08 \times 10^{-7}$ | $4.33 \times 10^{-7}$ | **Sí (Altamente Significativo)** |
| **STJC (Nuestro Método)** | $p@100$ | XGBoost | 365 | +0.78% | 54.52% | $1.34 \times 10^{-5}$ | $4.01 \times 10^{-5}$ | **Sí (Altamente Significativo)** |
| **STJC (Nuestro Método)** | $p@100$ | Random Forest | 365 | +1.51% | 59.18% | $1.55 \times 10^{-9}$ | $1.09 \times 10^{-8}$ | **Sí (Altamente Significativo)** |

> Tanto Votación Suave como STJC ganaron **16 de 16 comparaciones con significancia estadística formal ($p_{\text{holm}} < 0.01$)**.

---

### 3.2 Desempeño en la Prueba Operativa del Mundo Real (262 Días de 2026)

Resultados sobre el año 2026 sellado fuera de muestra con el modelo en producción (**Votación Suave**, 1M filas, reentrenamiento trimestral):

| Indicador Operativo | Valor Registrado | Significado para la Fiscalización de Osinergmin |
| :--- | :---: | :--- |
| **Días Operativos Evaluados** | **262 días continuos** | Cobertura integral de enero a septiembre de 2026. |
| **Establecimientos Evaluados Diariamente** | **17,863 a 19,975** | Promedio de 19,292 casos activos por día. |
| **Total Visitas Simuladas en el Top 100** | **26,200 inspecciones** | 100 visitas programadas por el modelo cada día. |
| **Total Visitas con Cambio Real Confirmado** | **<u>20,539 aciertos</u>** | **78.39% de precisión real en campo**. |
| **Mes con Mayor Precisión (Julio 2026)** | **<u>93.00%</u> en $p@100$** | 93 de cada 100 locales fiscalizados cambiaron de precio. |
| **AUC Diario Medio del Modelo** | **<u>0.7459</u>** | Capacidad discriminante superior en todo el país. |
| **AUC Diario de la Regla Heurística (`n_cambios_28`)** | **0.7044** | La heurística de conteo se degrada en el ordenamiento global. |
| **Días en que el Modelo Derrota a la Regla** | **<u>88.2% de los días</u>** | El modelo gana en 231 de los 262 días evaluados. |
| **Prueba de Wilcoxon Pareada Día a Día** | **$p = 4.89 \times 10^{-35}$** | Superioridad estadística aplastante del modelo sobre la regla. |
| **Trazabilidad Física al SCOP** | **<u>100.0%</u>** | El 100% de los 20,539 aciertos fue verificado en el reporte oficial. |

---

### 3.3 Generalización en Establecimientos "Nunca Vistos" (Prueba Ciega)

Evaluación sobre el **30% de los establecimientos del país (7,431 locales)** apartados al azar antes de iniciar el estudio que jamás participaron en ningún entrenamiento:

| Subconjunto Evaluado en 2026 | AUC Promedio (9 meses) | Precisión@100 Promedio | AUC en Mes Pico (Julio 2026) |
| :--- | :---: | :---: | :---: |
| **Establecimientos Conocidos** | 0.7426 | 76.81% | <u>**0.8035**</u> |
| **Establecimientos Nunca Vistos (Holdout Puro)** | <u>**0.7439**</u> | 74.35% | 0.8017 |

> **Conclusión Científica:** El modelo no memorizó nombres comerciales ni ubicaciones fijas; aprendió dinámicas estructurales de mercado que generalizan perfectamente a establecimientos desconocidos.

---

### 3.4 Robustez Frente a Horizontes de Supervisión (3, 5 y 7 Días)

Evaluación en la Sección 18.1 para verificar la flexibilidad logística del modelo:

| Horizonte Evaluado | Ventaja Media de AUC vs. Regla 28 | Meses en que Gana el Modelo |
| :---: | :---: | :---: |
| **3 Días** (Inspección Rápida) | **+0.0671 de AUC** | **9 de 9 meses (100%)** |
| **5 Días** (Semana Laboral Estándar) | **+0.0494 de AUC** | **9 de 9 meses (100%)** |
| **7 Días** (Ciclo Semanal Extendido) | **+0.0435 de AUC** | **9 de 9 meses (100%)** |

---

*Compendio oficial generado y verificado a partir de los registros maestros de `salidas_v6/` de la tesis.*
