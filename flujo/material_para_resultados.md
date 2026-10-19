# Material para la sección de Resultados

Cifras y figuras que **salieron de la metodología** (versión v3, 19 oct 2026) para que la metodología describa
el procedimiento y Resultados muestre lo que salió. Nada se perdió: todo está aquí con su fuente.

> Pendiente: las cifras de **significancia** se reemplazan con las del cuaderno
> `prueba7.1/verificaciones_revisor_v6.ipynb` (Wilcoxon mensual y bootstrap por bloques), no con el Wilcoxon diario.

## 4.x Selección del tratamiento del desbalance

**Figura de resultados:** `flujo/balanceo_por_que_no_articulo.png` (incluye la tabla de los 8 tratamientos).
Fuente: `salidas_v6/balanceo_lightgbm.csv` y `balanceo_cuatro_modelos.csv`.

| Tratamiento | AUC | p@100 | Meses que supera a «sin balanceo» (AUC) |
|---|---|---|---|
| Sin balanceo | 0,7326 | 61,5 % | — |
| Pesos de clase | 0,7327 | 61,5 % | 6 de 12 |
| Tomek Links | 0,7327 | 61,3 % | 7 de 12 |
| Sobremuestreo | 0,7325 | 61,2 % | 5 de 12 |
| Submuestreo 1:3 | 0,7323 | 61,5 % | 4 de 12 |
| Submuestreo 1:1 | 0,7318 | 60,3 % | 4 de 12 |
| SMOTENC | 0,6983 | 49,4 % | 0 de 12 |
| ADASYN | 0,6911 | 42,8 % | 0 de 12 |

- Posición media: sin balanceo 2,50 (1.º de 8). Segunda ronda con los 4 modelos: sin balanceo 1,75; pesos solo en
  CatBoost 2,25; Tomek 2,75; pesos 3,25.
- Lectura: los cuatro primeros tratamientos empatan (cuarto decimal; ganan en la mitad de los meses); el submuestreo 1:1
  empeora; los sintéticos pierden los 12 meses. El modelo final no balancea ni aplica la Ec. 4.

## 4.x Tamaño de entrenamiento y controles

- Curva de aprendizaje: con 300 000 filas, pasar a 1 000 000 solo añadía 0,0005 de AUC.
- Prueba negativa: AUC medio 0,489 (rango 0,466–0,518).
- Bloques reutilizados: el AUC de los bloques recuperados coincide con la ejecución nueva (diferencia máxima 0,0003).
- Preparación sin información futura (marca principal, mediana del mes anterior, atributos fijos): **pendiente** del
  cuaderno de verificaciones.

## 4.x Variables nuevas

- Las 3 nuevas entraron: +0,0018 de AUC en 2025, Wilcoxon p = 0,0005 (12 meses).

## 4.x Comparación de ensambles (validación 2025)

- Correlación de Spearman entre modelos base: 0,91 a 0,98.
- Cuatro estrategias superan a todos los individuales en las 4 métricas, además de las versiones del STJC.
- Posición media entre los 39: votación suave 3,75 (1.º); STJC 4,25 (2.º); votación ponderada 5,25; Caruana temporal
  12,25; Caruana por establecimiento 16,25.
- Pesos medios aprendidos (CatBoost · LightGBM · XGBoost · Random Forest):
  - votación ponderada: entre 0,22 y 0,27 (casi iguales);
  - Caruana temporal: 0,25 · 0,20 · 0,35 · 0,20;
  - Caruana por establecimiento: 0 · 0 · 0,36 · 0,64;
  - stacking clásico por establecimiento: −0,07 · −0,60 · 0,96 · 0,89 (castiga a LightGBM; no supera a los
    individuales en ninguna métrica);
  - STJC: 0,20 · 0,25 · 0,24 · 0,31.
- Tabla de la validación 2025 (contexto maestro, sección 3) y Fig. con resultados: `flujo/ensambles_como_combinan.png`
  (versión anterior, con pesos y posiciones).

## 4.x Ablación del STJC

**Figura de resultados:** `flujo/metodo_STJC_articulo.png` (incluye la tabla de ablación). Fuente: `salidas_v6/ablacion_stjc.csv`.

| Pieza añadida | AUC | p@100 | Brier |
|---|---|---|---|
| Stacking temporal (1 ventana) | 0,7338 | 61,98 % | 0,1072 |
| + Tres ventanas | 0,7343 | 61,93 % | 0,1039 |
| + Pesos convexos | 0,7347 | 62,03 % | 0,1033 |
| + Contracción | 0,7352 | 62,46 % | 0,1032 |
| + Pesos por combustible | 0,7352 | 62,45 % | 0,1032 |
| + Bagging temporal = STJC | 0,7348 | 62,51 % | 0,1031 |
| + Calibración final (no entra) | 0,7348 | 62,50 % | 0,1040 |

- Activación en 2025: pesos por combustible 8 de 12 meses; bagging temporal 5 de 12; calibración 0 de 12.
- STJC: mejor en p@100, p@250 y Brier; 2.º por posición media; cara a cara empata con la votación suave (confirmar con
  el bootstrap por bloques del cuaderno de verificaciones).

## 4.x Prueba prospectiva 2026

- Del contexto maestro (sección 3) y del cuaderno de verificaciones (AUC frente a reglas con intervalos por bloques;
  100 establecimientos únicos).
