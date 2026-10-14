# La Purga de 6 Días y Cómo Aprende el Modelo

La purga es de 6 días. El modelo aprende con ejemplos del pasado en los que ya se sabe qué pasó después.

---

## Las fechas exactas del bloque de enero de 2025

```text
27 jun 2024 ─────── 6 meses para aprender ─────── 25 dic 2024 | 26–31 dic: purga | ENERO 2025: se evalúa
```

* **Aprende con:** del 27 de junio al 25 de diciembre de 2024 (182 días, unos 6 meses).
* **Purga:** del 26 al 31 de diciembre no se usa.
* **Evalúa con:** todos los días de enero de 2025.

Febrero sigue la misma regla, corrida un mes, y así hasta diciembre.

---

## ¿Por qué 6 días y no 5?

Cada fila responde “¿cambió el precio en los 5 días siguientes?”. Mira estos dos casos:

* **Fila del 30 de diciembre:** su respuesta depende de lo que pasó del 31 de diciembre al 4 de enero, que ya es el mes evaluado. Si se usara, el modelo estaría viendo enero mientras aprende. Por eso se descarta.
* **Fila del 25 de diciembre (la última que se usa):** su respuesta mira del 26 al 30 de diciembre. Queda antes de enero, así que es segura.

Esos 5 días que mira la respuesta, más 1 de margen, dan los 6 días de purga.

---

## Cómo aprende el modelo

### 1. Cada fila es un ejemplo con su respuesta conocida

Una fila es “un grifo, un combustible, un día”:

| Grifo | Combustible | Día | Cambios en 90 días | Días sin cambiar | % de su región que cambió hoy | … (29 datos) | ¿Cambió en los 5 días siguientes? |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| A | Diésel | 10 oct 2024 | 45 | 1 | 30 % | … | **Sí** |
| B | GLP | 10 oct 2024 | 0 | 200 | 2 % | … | **No** |

Como son fechas pasadas, la última columna ya se conoce: es lo que pasó de verdad.

### 2. El modelo busca preguntas que separen el “sí” del “no”

Cada algoritmo arma muchos árboles de preguntas, por ejemplo:

```text
¿Cambió su precio más de 10 veces en 90 días?
├─ Sí → ¿Su región está cambiando precios hoy?
│        ├─ Sí → 85 % de los casos así cambiaron
│        └─ No → 60 %
└─ No → ¿Lleva más de 100 días sin cambiar?
         ├─ Sí → 3 %
         └─ No → 20 %
```

Los porcentajes salen de contar, en los 6 meses de ejemplos, cuántos casos de cada grupo cambiaron.

### 3. Muchos árboles juntos

* **CatBoost, LightGBM y XGBoost (boosting)** arman unos 300 árboles uno tras otro: cada árbol nuevo se fija en los casos que los anteriores se equivocaron y los corrige un poco.
* **Random Forest** arma 300 árboles independientes, cada uno con una parte distinta de los datos, y promedia sus respuestas.

### 4. La votación suave junta a los 4

Cada modelo da su probabilidad y el ensamble las promedia. Por ejemplo, 84 %, 88 %, 86 % y 86 % dan un 86 %.

### 5. Se pone a prueba con enero

Para cada grifo y cada día de enero, el modelo da una probabilidad sin saber lo que pasó. Luego se compara con lo que realmente ocurrió y salen el AUC, los aciertos en los primeros puestos y el Brier.

---

## Para la defensa:

> “El modelo aprende de ejemplos pasados cuya respuesta ya se conoce: para cada grifo y día, si su precio cambió en los 5 días siguientes. Busca qué combinaciones de características (cuántas veces cambió antes, cuánto lleva sin cambiar, qué hace su región) separan a los que cambian de los que no. Para evaluarlo en un mes, solo aprende de los 6 meses anteriores y deja 6 días de separación, para que ninguna respuesta del entrenamiento dependa del mes evaluado.”
