# Justificación Metodológica: ¿Por Qué No Balanceamos la Data?

**Documento Técnico de Sustentación para el Asesor y Jurado de Tesis**  
*Caso de Estudio:* Registro de Precios del SCOP (Osinergmin, Perú)  
*Referencia Experimental:* Sección 11 del Cuaderno `tesis_priorizacion_scop_v6.ipynb` y archivos `salidas_v6/balanceo_lightgbm.csv` y `salidas_v6/balanceo_cuatro_modelos.csv`.

---

## 1. Contexto y Respuesta al Revisor

En este problema **no conviene aplicar SMOTE**. Sin embargo, la observación del asesor/revisor apuntaba a una exigencia metodológica válida: **había que probarlo experimentalmente**, y eso ya se hizo de forma exhaustiva.

La exigencia del revisor fue *"probar varios tipos de balanceo y quedarse con el mejor"*, directriz que el cuaderno de investigación cumple con rigor. Tras someter a prueba 8 métodos distintos en los 12 bloques mensuales de 2025 frente a los 4 algoritmos base, **el mejor método empírico fue no balancear (conservar la distribución natural)**.

---

## 2. Lo que Dicen los Datos Empíricos (Validación Temporal 2025, 12 Meses)

A lo largo de los 12 meses de evaluación fuera de muestra (*Walk-Forward*), los resultados promedio consolidados fueron:

| Método de Balanceo | Capacidad de Ordenar (AUC) | Aciertos en 100 Primeros ($p@100$) | Diagnóstico Empírico |
| :--- | :---: | :---: | :--- |
| **Ninguno (Distribución Real)** | **0.733** | **61.5 %** | **Referencia óptima y ganador consolidado.** |
| **Pesos, Tomek, Sobremuestreo, Submuestreo** | 0.732 – 0.733 | 60.0 – 61.5 % | Desempeño equivalente (diferencias de milésimas en AUC). |
| **SMOTENC (Sintéticos Mixtos)** | 0.698 | 49.4 % | **Deterioro severo:** caída de 3.5 puntos de AUC y 12.1% en $p@100$. |
| **ADASYN (Sintéticos Adaptativos)** | 0.691 | 42.8 % | **Colapso:** caída de 4.2 puntos de AUC y 18.7% en $p@100$. |

> **Resultado categórico:** SMOTENC perdió contra no balancear en **los 12 meses de 2025, sin excepción alguna**. Aplicar SMOTE en este proyecto equivaldría a elegir conscientemente un modelo con un 12 % menos de aciertos en la labor diaria de los inspectores en campo.

---

## 3. ¿Por Qué Falla SMOTE en Este Problema?

1. **Fabrica establecimientos que no existen en la realidad física:**  
   SMOTE crea casos positivos interpolando linealmente un punto medio entre dos establecimientos reales. Por ejemplo, al promediar un grifo rural con 3 cambios históricos y otro urbano con 40 cambios, crea un establecimiento ficticio con 21 cambios, con coordenadas intermedias y un precio artificial. El algoritmo consume capacidad de cómputo aprendiendo sobre combinaciones inexistentes en la geografía peruana, lo que degrada su precisión al enfrentarse a los grifos reales.
2. **El desbalance de clases no es severo:**  
   En los datos de 2025, la tasa base de cambio es de aproximadamente **13.1 %** (1 de cada 8 casos es positivo). En una ventana de entrenamiento estándar de 300,000 filas, el modelo cuenta con más de **40,000 ejemplos reales de cambio de precio**, saturación muestral plenamente suficiente para aprender los patrones de riesgo. Técnicas como SMOTE fueron concebidas para desbalances extremos (por ejemplo, detección de fraude o fallas industriales con ratios de 1 en 1,000 o 1 en 10,000), no para tasas del 13 %.
3. **Los algoritmos basados en árboles son inmunes al desbalance moderado:**  
   Algoritmos como `CatBoost`, `LightGBM`, `XGBoost` y `Random Forest` optimizan particiones recursivas locales basadas en impureza o gradientes. El desbalance solo desplaza el umbral global de probabilidad hacia valores menores, pero **no altera el orden relativo del ranking diario**, que es precisamente lo que se necesita para emitir la lista Top 100 de fiscalización.

---

## 4. Respaldo en la Literatura Científica Reciente

Esta evidencia empírica coincide plenamente con los consensos científicos más recientes en Machine Learning y predicción de riesgo:

1. **van den Goorbergh et al. (2022):**  
   *The harm of class imbalance corrections for risk prediction models.* Publicado en el *Journal of the American Medical Informatics Association* (JAMIA), Vol. 29, Issue 9.  
   **Conclusión:** Demuestran matemáticamente que las correcciones artificiales de desbalance distorsionan la calibración probabilística sin mejorar la capacidad discriminante (AUC) del modelo.
2. **Elor & Averbuch-Elor (2022):**  
   *To SMOTE, or not to SMOTE?* ArXiv preprint arXiv:2201.08528.  
   **Conclusión:** Con modelos modernos de alto rendimiento (particularmente *Gradient Boosted Decision Trees*), las técnicas de balanceo sintético como SMOTE no generan mejoras y suelen introducir sesgo y sobreajuste en los límites de decisión.

---

## 5. Argumentario Ejecutivo para la Sustentación ante el Asesor

Si el asesor consulta el motivo de mantener la distribución natural, la respuesta técnica recomendada es:

> *"Atendiendo la sugerencia metodológica, sometimos a prueba ocho estrategias de balanceo (incluyendo SMOTENC y ADASYN) a lo largo de los 12 bloques mensuales de validación temporal con los cuatro algoritmos base. Los métodos sintéticos deterioraron el desempeño en todos los meses sin excepción, reduciendo el AUC de 0.733 a 0.698 y la precisión en el Top 100 de 61.5% a 49.4%. Las demás técnicas (pesos, Tomek, submuestreo) empataron en milésimas con la distribución natural. Bajo el criterio metodológico predefinido de optimizar simultáneamente las cuatro métricas cardinales sin distorsionar la calibración (Brier Score), el método ganador seleccionado por el propio pipeline fue no balancear. Con una tasa base del 13% y modelos basados en árboles potenciados por gradiente, el desbalance no deteriora el ordenamiento del ranking, que es el objetivo operativo de la fiscalización."*

---

## 6. Trazabilidad en el Repositorio

La evidencia reproducible completa se encuentra registrada en los siguientes componentes:
* **Sección 11 del Cuaderno:** `prueba7.1/tesis_priorizacion_scop_v6.ipynb` (subsecciones 11.1 y 11.2).
* **Tablas de Salida Consolidadas:**
  - `prueba7.1/salidas_v6/balanceo_lightgbm.csv` (evaluación de los 8 métodos mes a mes en LightGBM).
  - `prueba7.1/salidas_v6/balanceo_cuatro_modelos.csv` (evaluación de los finalistas en CatBoost, LightGBM, XGBoost y Random Forest).
* **Capítulo 4 del Documento Maestro:** `flujo/historia_metodologia_tesis.docx` (párrafos dedicados al análisis comparativo y la corrección de priors de Dal Pozzolo).

---

## 7. Plan de Contingencia

Si a pesar de la evidencia matemática y empírica el asesor insistiera en forzar la aplicación de un método de balanceo en el documento final:
* **La opción técnica menos dañina:** Sería el **submuestreo moderado 1 a 3** (`submuestreo_1_3`), el cual retuvo un $p@100$ de **$61.51\%$** en LightGBM prácticamente idéntico a no balancear ($61.54\%$), evitando inventar datos sintéticos irreales.
* **Recomendación científica:** Registrarlo como un requerimiento normativo del revisor, haciendo constar en la discusión que la evidencia empírica directa de los 12 meses demuestra que no balancear maximiza la fidelidad probabilística con el menor costo computacional. En ningún caso se recomienda adoptar SMOTE.

