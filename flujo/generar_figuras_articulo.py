# -*- coding: utf-8 -*-
"""Versiones para el ARTÍCULO de los diagramas de balanceo y del STJC.

    python generar_figuras_articulo.py

Escribe balanceo_por_que_no_articulo.drawio y metodo_STJC_articulo.drawio. No modifica los .drawio
originales (balanceo_por_que_no.drawio, metodo_STJC_explicacion.drawio).
Lienzo de 605 px = 16 cm y letra de 11 px (≈ 8 pt), en blanco y negro como los originales.
Cifras: salidas_v6/balanceo_lightgbm.csv, balanceo_cuatro_modelos.csv, ablacion_stjc.csv y salidas del
cuaderno v6 (sección 14.11: pesos por combustible en 8 de 12 meses, bagging temporal en 5 de 12).
"""
from figuras_base import Lienzo, X0, FULLW


# ======================================================================= BALANCEO
L = Lienzo()
L.banda("1 · Del desbalance observado a una lista de prioridad")
L.fila([["Datos de entrenamiento", "300 000 filas por mes", "13 % cambian (≈ 39 000)", "87 % no cambian (≈ 261 000)",
         "Cada fila: 29 variables (X) y la respuesta (y)"],
        ["El modelo aprende", "Relaciona X con y y estima p, la probabilidad de que el precio cambie en los próximos 5 días."],
        ["Se eligen los K primeros", "Ejemplo: 6 casos y 3 cupos", "A 0,80 · B 0,60 · C 0,40", "D 0,25 · E 0,10 · F 0,05",
         "Se eligen A, B y C (en el estudio, K = 100)"]])
L.y += 8
L.banda("2 · Con cupos fijos importa el orden, no superar un umbral de 50 %")
L.fila([["A + B + C: los 3 primeros", "0,80 + 0,60 + 0,40 = 1,80 aciertos esperados"],
        ["A + B + F: se omite el tercero", "0,80 + 0,60 + 0,05 = 1,45 aciertos esperados"]],
       gap=14, flechas=False, grosores=[2, 1])
L.y += 4
L.y += L.texto("C entra con 40 %: cuenta su puesto. Aprender ese orden no exige entrenar con 50 % de cada clase; "
               "los aciertos esperados son la suma de las probabilidades elegidas.") + 6
L.banda("3 · Qué hace cada técnica con las filas de entrenamiento")
L.fila([["Eliminar filas", "Submuestreo 1:1 y 1:3; Tomek Links", "Se conservan menos negativos."],
        ["Repetir filas", "Sobremuestreo aleatorio", "Se duplican positivos reales."],
        ["Generar filas", "SMOTENC y ADASYN", "Se interpolan las variables de dos positivos."],
        ["Cambiar pesos", "Pesos de clase", "Cada positivo pesa ≈ 6,7 veces más."]], gap=8, flechas=False)
L.y += 4
L.y += L.texto("Ninguna técnica cambia una respuesta real ni iguala las variables, y el mes evaluado conserva su proporción real.") + 6
L.banda("4 · Resultado en los 12 meses de 2025 (LightGBM; misma regla para todas)")
L.tabla([["Técnica", "AUC", "p@100", "Meses que supera a «sin balanceo» (AUC)", "Lectura"],
         ["Sin balanceo", "0,7326", "61,5 %", "—", "Referencia"],
         ["Pesos de clase", "0,7327", "61,5 %", "6 de 12", "Empate"],
         ["Tomek Links", "0,7327", "61,3 %", "7 de 12", "Empate"],
         ["Sobremuestreo", "0,7325", "61,2 %", "5 de 12", "Empate"],
         ["Submuestreo 1:3", "0,7323", "61,5 %", "4 de 12", "Empate"],
         ["Submuestreo 1:1", "0,7318", "60,3 %", "4 de 12", "Peor"],
         ["SMOTENC", "0,6983", "49,4 %", "0 de 12", "Mucho peor"],
         ["ADASYN", "0,6911", "42,8 %", "0 de 12", "Mucho peor"]],
        [150, 70, 70, 196, 95], resaltar=(1,))
L.y += 4
L.y += L.texto("p@100: aciertos entre los 100 primeros de cada día. «Empate»: diferencias en el cuarto decimal y ventaja en "
               "alrededor de la mitad de los meses.") + 6
L.banda("5 · Decisión")
L.fila([["La teoría permite", "Ordenar sin exigir clases 50/50."],
        ["La validación respalda", "«Sin balanceo»: 1.º de 8 (posición media 2,50); con los 4 modelos, 1.º de 4 (1,75)."],
        ["Decisión del estudio", "Entrenar con la distribución original, sin corrección de la Ec. 4."]],
       grosores=[1, 1, 2])
L.guardar("balanceo_por_que_no_articulo.drawio", "Balanceo (artículo)")

# ======================================================================= STJC
S = Lienzo()
S.banda("1 · Aprender del pasado como si cada mes fuera nuevo")
S.fila([["Ventana antigua", "Predicciones de los 4 modelos y lo que ocurrió"],
        ["Ventana intermedia", "Predicciones de los 4 modelos y lo que ocurrió"],
        ["Ventana reciente", "Elige los controles por AUC"],
        ["Mes evaluado", "Se aplica la receta; sus respuestas no se usan para ajustarla"]], gap=18)
S.y += 4
S.y += S.texto("Tres ventanas de 30 días dentro de la historia de entrenamiento, cada una predicha solo con datos anteriores "
               "y separada por una purga de 6 días. Las dos antiguas ajustan candidatos, la reciente elige y, al final, los "
               "pesos se reajustan con las tres.") + 6
S.banda("2 · Tres controles sobre los pesos")
S.fila([["A. Pesos convexos", "Pesos ≥ 0 que suman 100 %: ningún modelo resta la opinión de otro.", "Ejemplo: 40 / 30 / 20 / 10 %."],
        ["B. Contracción (Ec. 7)", "Penaliza alejarse de 25 / 25 / 25 / 25 %. La fuerza λ se elige por AUC en la ventana reciente."],
        ["C. Pesos por combustible", "Pesos propios atraídos a los generales; solo si mejoran (≥ 2 000 filas y ambas clases). "
         "Se usaron en 8 de 12 meses."]], gap=8, flechas=False)
S.y += 8
S.banda("3 · Bagging temporal, solo si mejora")
y0 = S.y
bw, g = 88, 6
vers = []
for k, t in enumerate(["Versión completa", "Ventana antigua", "Ventana intermedia", "Ventana reciente"]):
    i, h = S.caja([t], X0 + k * (bw + g), y0, bw, 34, centrado=True, titulo=False)
    vers.append(i)
anchoV = 4 * bw + 3 * g
prom, hp = S.caja(["Promedio de probabilidades"], X0 + anchoV / 2 - 95, y0 + 34 + 22, 190, 26, centrado=True)
for k, i in enumerate(vers):
    cx = X0 + k * (bw + g) + bw / 2
    S.edge(i, prom, exit_=(0.5, 1), entry=(0.5, 0), pts=[(cx, y0 + 34 + 11), (X0 + anchoV / 2, y0 + 34 + 11)])
dx = X0 + anchoV + 22
dec, hd = S.caja(["¿Mejora el AUC interno?", "Sí: promedio temporal; no: versión completa.",
                  "Se decide antes del mes evaluado; se usó en 5 de 12 meses."], dx, y0, FULLW - (dx - X0), 34 + 22 + 26)
S.edge(prom, dec, exit_=(1, 0.5), entry=(0, 0.75))
S.y = y0 + 34 + 22 + 26
S.y += 10
S.banda("4 · Ejemplo ilustrativo: de cuatro probabilidades a una prioridad")
y0 = S.y
mods = ["CatBoost 0,80 · peso 0,40", "LightGBM 0,60 · peso 0,30", "XGBoost 0,40 · peso 0,20", "Random Forest 0,20 · peso 0,10"]
ids = []
for k, t in enumerate(mods):
    i, _ = S.caja([t], X0, y0 + k * 30, 182, 24, titulo=False)
    ids.append(i)
alto4 = 3 * 30 + 24
cx = X0 + 182 + 16
comb, _ = S.caja(["Combinación en escala logit", "1. L = ln[p / (1 − p)] en cada modelo",
                  "2. z = 0,4 L(CB) + 0,3 L(LGB) + 0,2 L(XGB) + 0,1 L(RF) = 0,456", "3. p = 1 / (1 + e^(−z)) = 0,612",
                  "(sin escala ni intercepto, para simplificar)"], cx, y0, 232, alto4)
for i in ids:
    S.edge(i, comb, exit_=(1, 0.5), entry=(0, 0.5))
rx = cx + 232 + 16
ordn, _ = S.caja(["Ordenar todos los casos", "1. B 0,72", "2. A 0,61", "3. C 0,43", "4. D 0,21", "Con 2 cupos: B y A"],
                 rx, y0, FULLW - (rx - X0), alto4)
S.edge(comb, ordn)
S.y = y0 + alto4 + 4
S.y += S.texto("Las probabilidades no se promedian directamente: se combinan en escala logit con los pesos aprendidos.") + 6
S.banda("5 · Aporte de cada pieza (ablación, promedio de los 12 meses de 2025)")
S.tabla([["Pieza añadida", "AUC", "p@100", "Brier"],
         ["Stacking temporal (1 ventana)", "0,7338", "61,98 %", "0,1072"],
         ["+ Tres ventanas", "0,7343", "61,93 %", "0,1039"],
         ["+ Pesos convexos", "0,7347", "62,03 %", "0,1033"],
         ["+ Contracción", "0,7352", "62,46 %", "0,1032"],
         ["+ Pesos por combustible", "0,7352", "62,45 %", "0,1032"],
         ["+ Bagging temporal = STJC", "0,7348", "62,51 %", "0,1031"],
         ["+ Calibración final (no entra)", "0,7348", "62,50 %", "0,1040"]],
        [281, 100, 100, 100], resaltar=(6,), tenue=(7,))
S.y += 4
S.y += S.texto("Mayor AUC y p@100 es mejor; menor Brier es mejor. Ninguna pieza mejora todas las métricas: se evalúa el conjunto.")
S.guardar("metodo_STJC_articulo.drawio", "STJC (artículo)")
