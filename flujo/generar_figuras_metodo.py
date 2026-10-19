# -*- coding: utf-8 -*-
"""Figuras CONCEPTUALES para la sección de Metodología (sin resultados numéricos del modelo).

    python generar_figuras_metodo.py

Escribe balanceo_metodo.drawio, ensambles_metodo.drawio y stjc_metodo.drawio. Las versiones con
resultados (balanceo_por_que_no_articulo, metodo_STJC_articulo) quedan para la sección de Resultados.
Los ejemplos numéricos son ilustrativos; las cifras de datos (13 %, 300 000 filas) describen el material.
"""
from figuras_base import Lienzo, X0, FULLW

# ======================================================================= BALANCEO (método)
L = Lienzo()
L.banda("1 · Del desbalance observado a una lista de prioridad")
L.fila([["Datos de entrenamiento", "300 000 filas por mes", "≈ 13 % cambian; ≈ 87 % no cambian",
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
               "los aciertos esperados son la suma de las probabilidades elegidas (ejemplo ilustrativo).") + 6
L.banda("3 · Qué hace cada técnica con las filas de entrenamiento")
L.fila([["Eliminar filas", "Submuestreo 1:1 y 1:3; Tomek Links", "Se conservan menos negativos."],
        ["Repetir filas", "Sobremuestreo aleatorio", "Se duplican positivos reales."],
        ["Generar filas", "SMOTENC y ADASYN", "Se interpolan las variables de dos positivos."],
        ["Cambiar pesos", "Pesos de clase", "Cada positivo pesa ≈ 6,7 veces más."]], gap=8, flechas=False)
L.y += 4
L.y += L.texto("Ninguna técnica cambia una respuesta real ni iguala las variables, y el mes evaluado conserva su proporción real. "
               "Si se remuestrea, las probabilidades vuelven a la proporción real con la Ec. 4.") + 6
L.banda("4 · Cómo se decide")
L.fila([["8 opciones", "Sin balanceo y 7 técnicas, todas con 300 000 filas"],
        ["12 meses de 2025", "Cada mes se evalúa con su proporción real, sin balancear"],
        ["Regla previa", "Mejor posición media en AUC, p@100, p@250 y Brier; las mejores se confirman con los 4 modelos"]],
       grosores=[1, 1, 2])
L.guardar("balanceo_metodo.drawio", "Balanceo (metodología)")

# ======================================================================= ENSAMBLES (método)
E = Lienzo()
E.banda("1 · Cuatro modelos base entrenados con la misma ventana")
E.fila([["CatBoost", "Boosting; árboles simétricos"], ["LightGBM", "Boosting; crece hoja por hoja"],
        ["XGBoost", "Boosting; crece nivel por nivel"], ["Random Forest", "Promedio de 300 árboles"]], gap=8, flechas=False)
E.y += 4
E.y += E.texto("Sus predicciones se parecen mucho, por lo que combinarlas solo ayuda si los pesos se estiman con cuidado.") + 6
E.banda("2 · Cada fila recibe cuatro probabilidades (ejemplo ilustrativo)")
ex, h = E.caja(["Establecimiento X · diésel · un día cualquiera",
                "CatBoost 0,40   ·   LightGBM 0,36   ·   XGBoost 0,44   ·   Random Forest 0,32"], X0, E.y, FULLW)
E.y += h + 10
E.banda("3 · Cómo fijan los pesos las cuatro estrategias de la Ec. 5")
E.fila([["Votación suave", "Cada modelo pesa 1/4. No aprende nada.", "Ej.: (0,40 + 0,36 + 0,44 + 0,32) / 4 = 0,380"],
        ["Votación ponderada", "Peso proporcional al AUC de cada modelo en el último mes de la ventana."]], gap=10, flechas=False)
E.y += 8
E.fila([["Selección de Caruana", "En 40 rondas agrega, con reemplazo, el modelo que más sube el AUC; el peso es la fracción "
         "de rondas en que se eligió.", "Ej.: 20, 14 y 6 rondas → pesos 0,50 · 0,35 · 0,15"],
        ["Caruana temporal", "Igual, pero aprende con el último mes de la ventana predicho por modelos entrenados antes de él."]],
       gap=10, flechas=False)
E.y += 10
E.banda("4 · Cómo se aprenden los pesos sin mirar el futuro")
E.fila([["Por establecimiento", "Cinco pliegues; un mismo establecimiento nunca queda en dos pliegues. Predice "
         "establecimientos no vistos, pero del mismo periodo."],
        ["Temporal", "Los modelos base, entrenados hasta el mes anterior, predicen el último mes de la ventana. Reproduce el "
         "uso real: predecir días que no se vieron."]], gap=10, flechas=False)
E.y += 6
r, h = E.caja(["Riesgo del stacking (Ec. 6)", "Un metamodelo libre puede asignar pesos negativos o extremos a modelos casi "
               "idénticos; el STJC (sección 3.5) restringe y contrae esos pesos."], X0, E.y, FULLW, grosor=1, relleno="#F2F2F2")
E.y += h + 10
E.banda("5 · Regla fijada antes de ver resultados (promedio de los 12 meses de 2025)")
E.fila([["39 estrategias", "10 familias, incluido el STJC, en sus versiones por establecimiento y temporal"],
        ["Regla de selección", "1) más métricas en que supera a todos los individuales; 2) mejor posición media; 3) mayor AUC"],
        ["Ensamble elegido", "Pasa a la prueba prospectiva de 2026"]], grosores=[1, 1, 2])
E.guardar("ensambles_metodo.drawio", "Ensambles (metodología)")

# ======================================================================= STJC (método)
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
        ["C. Pesos por combustible", "Pesos propios atraídos a los generales; solo si mejoran (≥ 2 000 filas y ambas clases)."]],
       gap=8, flechas=False)
S.y += 8
S.banda("3 · Bagging temporal, solo si mejora")
y0 = S.y
bw, g = 88, 6
vers = []
for k, t in enumerate(["Versión completa", "Ventana antigua", "Ventana intermedia", "Ventana reciente"]):
    i, _ = S.caja([t], X0 + k * (bw + g), y0, bw, 34, centrado=True, titulo=False)
    vers.append(i)
anchoV = 4 * bw + 3 * g
prom, _ = S.caja(["Promedio de probabilidades"], X0 + anchoV / 2 - 95, y0 + 56, 190, 26, centrado=True)
for k, i in enumerate(vers):
    cx = X0 + k * (bw + g) + bw / 2
    S.edge(i, prom, exit_=(0.5, 1), entry=(0.5, 0), pts=[(cx, y0 + 45), (X0 + anchoV / 2, y0 + 45)])
dx = X0 + anchoV + 22
dec, _ = S.caja(["¿Mejora el AUC interno?", "Sí: promedio temporal; no: versión completa.",
                 "Se decide antes del mes evaluado."], dx, y0, FULLW - (dx - X0), 82)
S.edge(prom, dec, exit_=(1, 0.5), entry=(0, 0.75))
S.y = y0 + 82 + 10
S.banda("4 · Ejemplo ilustrativo: de cuatro probabilidades a una prioridad")
y0 = S.y
ids = []
for k, t in enumerate(["CatBoost 0,80 · peso 0,40", "LightGBM 0,60 · peso 0,30", "XGBoost 0,40 · peso 0,20",
                       "Random Forest 0,20 · peso 0,10"]):
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
S.y += S.texto("Las probabilidades no se promedian directamente: se combinan en escala logit con los pesos aprendidos. "
               "El aporte de cada pieza se mide con una ablación (sección 3.5).")
S.guardar("stjc_metodo.drawio", "STJC (metodología)")
