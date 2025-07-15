# Sistema de Predicción Geopolítica (SPG)

![Licencia](https://img.shields.io/badge/license-CC%20BY--NC--SA%204.0-blue)

Un proyecto de Data Science para explorar la viabilidad de anticipar conflictos geopolíticos mediante el análisis combinado de datos de mercados financieros e inteligencia pública.

---

## Visión del Proyecto

Este proyecto nace de la hipótesis de que los mercados financieros, al ser un gigantesco mecanismo de agregación de información, pueden reflejar tensiones geopolíticas antes de que estas se materialicen en conflictos abiertos. El objetivo es combinar el "qué" y "cuándo" de los datos cuantitativos del mercado con el "porqué" del análisis cualitativo para obtener una visión más completa del riesgo global.

Este repositorio documentará el desarrollo del proyecto, desde la prueba de concepto inicial hasta la creación de un posible modelo predictivo.

---

## 🏛️ Estructura del Repositorio

El proyecto está organizado en fases, y cada fase o componente importante tendrá su propia carpeta en este repositorio.

```
/
├── PoC/
│   ├── data/
│   │   └── MOEX.csv                  # Datos históricos del índice MOEX.
│   ├── PoC_Crimea_2014.ipynb         # Notebook del primer caso de estudio.
│   ├── PoC_Ucrania_2022.ipynb        # Notebook del segundo caso de estudio.
│   ├── PoC_Irak_2003.ipynb           # Notebook del tercer caso de estudio.
│   └── requirements.txt              # Dependencias de Python para la PoC.
├── LICENSE                           # La licencia del proyecto.
└── README.md                         # Este documento.
```

---

## 🚀 Estado Actual del Proyecto

El proyecto sigue el roadmap definido en el documento de planificación inicial.

* ✅ **Fase 0: Fundación y Diseño** - *COMPLETADA*
* ✅ **Fase 1: Prueba de Concepto (PoC)** - *COMPLETADA*
* ⏳ **Fase 2: Producto Mínimo Viable (MVP)** - *Próxima fase*
* 🔲 **Fase 3: Versión Alfa (Modelo Predictivo)** - *Pendiente*
* 🔲 **Fase 4: Versión Beta (La Aplicación)** - *Pendiente*

El trabajo completado hasta ahora (Fase 1) ha validado la hipótesis fundamental para el caso de estudio de Crimea 2014. El informe completo se encuentra en la carpeta `/PoC`.

---

## 🛠️ Cómo Empezar

Para replicar el análisis de la Prueba de Concepto, sigue estos pasos:

1.  **Clona el repositorio:**
    ```bash
    git clone [https://github.com/](https://github.com/)/didacum/SPG.git
    cd SPG
    ```

2.  **Crea y activa un entorno virtual:**
    ```bash
    # Crear el entorno
    python -m venv venv

    # Activar en macOS/Linux
    source venv/bin/activate

    # Activar en Windows
    # venv\Scripts\activate
    ```

3.  **Instala las dependencias:**
    El archivo de requerimientos se encuentra dentro de la carpeta `/PoC`.
    ```bash
    pip install -r PoC/requirements.txt
    ```

4.  **Ejecuta el análisis:**
    Abre la carpeta `SPG` en VS Code y ejecuta cualquiera de los notebooks que se encuentran en la carpeta `/PoC`:
    * `PoC_Crimea_2014.ipynb`
    * `PoC_Ucrania_2022.ipynb`
    * `PoC_Irak_2003.ipynb`
---

## 📜 Licencia

Este proyecto está bajo la licencia **Creative Commons Atribución-NoComercial-CompartirIgual 4.0 Internacional**. Puedes leer el texto completo en el archivo [LICENSE](LICENSE.md) de este repositorio.
