# Historia_Tesis: Metodología y Modelo de Priorización SCOP

Repositorio de investigación y sustentación metodológica del modelo predictivo para la priorización diaria de fiscalización de precios de combustibles en el Perú (Osinergmin / SCOP).

---

## 📁 Estructura del Repositorio

- **`flujo/`**:
  - `historia_metodologia_tesis.md`: Documento maestro de sustentación metodológica y narrativa científica completa.
  - `resultados.md`: Compendio oficial de métricas comparativas (individuales y ensambles) con valores destacados.
  - `diccionario_de_variables.md`: Definición formal de la variable objetivo y especificación de las 29 variables predictivas.
  - `porque_no_balanceamos_la_data.md`: Sustentación metodológica y evidencia empírica de por qué no se aplica balanceo sintético (SMOTE).
  - `explicacion_purga_y_aprendizaje.md`: Explicación detallada de la purga temporal de 6 días y cómo aprenden los modelos y ensambles.
  - Diagramas metodológicos y esquemas visuales de arquitectura (`.drawio`).
- **`flujo_words/`**:
  - Versiones ejecutivas y cartas de gestión en formato Word (`.docx`): `historia_metodologia_tesis.docx`, `resultados.docx`, `diccionario_de_variables.docx`, `carta_solicitud_osinergmin.docx`, `guia_reunion_osinergmin.docx`.
- **`resultados.md`**: Acceso directo en raíz al compendio oficial de métricas de modelos individuales y ensambles.
- **`prueba7.1/`**:
  - `tesis_priorizacion_scop_v6.ipynb`: Cuaderno Jupyter con la implementación completa de la metodología (pipeline de datos, ingeniería de variables, modelos base, ensambles temporales y validación).
  - `muestras_evolucion_datos/`: Muestras ilustrativas de las 5 etapas de evolución de los datos.
  - `salidas_v6/`: Resultados empíricos, tablas maestras, ablación de STJC, diagnósticos de sobreajuste/VIF y visualizaciones:
    - `graficos/`: Curvas ROC, curvas de fiabilidad, precisión diaria y pesos de ensamble.
    - Archivos CSV y JSON con todas las métricas de validación y auditoría de 2025 y 2026.

---

> **Nota sobre datasets y modelos binarios:**  
> Los datos crudos de Osinergmin (~1.1 GB), caches de parquet (~1.4 GB) y pesos serializados de modelos (`.joblib` / `.parquet` >1.4 GB) han sido excluidos vía `.gitignore` para cumplir con las directrices de tamaño de GitHub.

