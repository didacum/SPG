# Sistema de Predicción Geopolítica (SPG)



Un proyecto de *Data Science* para explorar la viabilidad de **anticipar conflictos geopolíticos** mediante el análisis combinado de mercados financieros, cadenas de suministro e inteligencia pública.

---

## 🌍 Visión del Proyecto

Los mercados financieros actúan como un gigantesco mecanismo de agregación de información y, por tanto, **pueden reflejar tensiones geopolíticas antes de que se materialicen**. El objetivo es combinar el "qué" y el "cuándo" de los datos cuantitativos con el "porqué" del análisis cualitativo para producir un *dashboard* de riesgo global y, en fases posteriores, un modelo predictivo.

Este repositorio documenta la evolución del proyecto: desde la prueba de concepto (PoC) hasta la futura versión beta que incluya un motor de predicción.

---

## 🏛️ Estructura del Repositorio

```text
/
├── apps/                      # Aplicaciones ejecutables
│   ├── dashboard/             # 📊 Taiwan Strait Risk Dashboard (Next.js + v0)
│   └── etl/                   # ⚙️  Scripts ETL & loaders (futuro)
├── PoC/                       # Notebooks de la Prueba de Concepto original
│   ├── data/
│   │   └── MOEX.csv
│   ├── PoC_Crimea_2014.ipynb
│   ├── PoC_Ucrania_2022.ipynb
│   ├── PoC_Irak_2003.ipynb
│   └── requirements.txt
├── .gitignore
├── LICENSE
└── README.md                  
```

> **Nota** — La carpeta `apps/etl` se añadirá en la siguiente iteración.

---

## 🚦 Estado del Roadmap

| Fase  | Descripción                                | Estado          |
| ----- | ------------------------------------------ | --------------- |
| **0** | Fundación y diseño                         | ✅ Completada    |
| **1** | Prueba de Concepto (PoC)                   | ✅ Completada    |
| **2** | Producto Mínimo Viable (MVP) – *Dashboard* | 🚧 **En curso** |
| **3** | Versión Alfa – Modelo Predictivo           | ⏳ Planificado   |
| **4** | Versión Beta – Aplicación completa         | ⏳ Planificado   |

Los resultados de la Fase 1 (caso de estudio Crimea 2014) se encuentran en `/PoC`.

---

## 🚀 Cómo empezar

### 1. Clonar el repositorio

```bash
git clone https://github.com/<tu-usuario>/SPG.git
cd SPG
```

### 2. Configurar entorno Python para la PoC

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
# .\venv\Scripts\activate  # Windows
pip install -r PoC/requirements.txt
```

### 3. Ejecutar los notebooks de la PoC

Abre `PoC/PoC_Crimea_2014.ipynb` (o cualquiera de los otros) en Jupyter / VS Code.

---

## 🖥️  Cómo lanzar el Dashboard (MVP)

El *dashboard* es una aplicación **Next.js 15** generada con **v0** y empaquetada en la carpeta `apps/dashboard`.

> Requiere Node ≥ 20 y **pnpm** (o npm/yarn).

```bash
# Instalación de dependencias
cd apps/dashboard
pnpm install          # o npm install / yarn

# Arrancar en modo desarrollo
pnpm dev              # abre http://localhost:3000
```

---

## 🤝 Contribuir

1. Haz *fork* y crea una rama: `git checkout -b feature/tu-mejora`
2. Sigue la guía de estilo (PEP‑8 para Python, ESLint/Prettier para JS).
3. Lanza `pnpm test` (o `pytest`) antes de abrir el *pull request*.

---

## 📜 Licencia

Este proyecto está bajo la licencia **Creative Commons Atribución‑NoComercial‑CompartirIgual 4.0 Internacional**.\
Consulta el texto completo en [LICENSE](LICENSE).

