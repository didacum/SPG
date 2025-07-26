# ETL – Sistema de Ingesta y Normalización de Datos

*Proyecto SPG – MVP Estrecho de Taiwán*

---

## 1 · Propósito del ETL

Este pipeline automatiza la **extracción**, **transformación** y **carga** de indicadores financieros y otras métricas hacia **Supabase Postgres**.\
Su objetivo es alimentar el *dashboard* con datos frescos cada madrugada (05:00 CET) y construir una base histórica homogénea que sirva al futuro modelo predictivo.

## 2 · Indicadores Implementados

Actualmente, el ETL extrae y procesa de forma estable los siguientes 5 indicadores financieros clave, utilizando **Stooq** como única fuente de datos.

| Símbolo (`assets.symbol`) | Descripción          | Ticker Stooq | Frecuencia |
| ------------------------- | -------------------- | :----------: | ---------- |
| `TAIEX`                   | Taiwan Stock Index   |    `^TWSE`   | Diario     |
| `SPX`                     | S&P 500              |    `^SPX`    | Diario     |
| `NKX`                     | Nikkei 225           |    `^NKX`    | Diario     |
| `KOSPI`                   | KOSPI Composite      |   `^KOSPI`   | Diario     |
| `SHC`                     | Shanghai Composite   |    `^SHC`    | Diario     |

*(La arquitectura está diseñada para añadir fácilmente nuevas fuentes e indicadores en el futuro a medida que se validen sus fuentes de datos).*

---

## 3 · Arquitectura del código ETL

```
apps/etl/
├── src/
│   ├── __main__.py          # orquestador CLI
│   ├── config.yaml          # mapping activos → extractores
│   ├── extractors/          # capa E
│   ├── transforms/          # capa T
│   ├── loaders/             # capa L
│   └── utils/               # logger, supabase_client
├── Dockerfile               # imagen reproducible
└── tests/                   # pytest ≥85 % cobertura
```

### 3.1 Extractores

Cada módulo en `extractors/*.py` devuelve un `pandas.DataFrame` con una estructura estándar.

El extractor principal, `extractors/stooq_extractor.py`, descarga los datos directamente desde la URL de descarga de CSV de Stooq, usando una cabecera `User-Agent` para asegurar la compatibilidad con todos los tickers. Este método ha demostrado ser más robusto que el uso de librerías intermediarias.

### 3.2 Transforms

- `clean_data()` – ajusta duplicados y convierte la zona horaria a UTC.
- `forward_fill_missing_dates()` – rellena días no bursátiles (festivos, fines de semana) con el último valor conocido.
- `calculate_base100(df, base_date)` – calcula la columna `value` normalizada a base 100 para permitir la comparabilidad entre series.

### 3.3 Loaders

Utilizan `supabase-py` para realizar una operación de `upsert` que inserta o actualiza registros basándose en la clave única (`asset_id`, `date`), garantizando la idempotencia del proceso.

```python
supabase.table("market_data").upsert(records, on_conflict="asset_id,date").execute()
```

---

## 4 · Configuración YAML de pipelines (ejemplo)

```yaml
pipelines:
  - id: "TAIEX_daily"
    asset_symbol: "TAIEX"
    enabled: true
    extractor:
      module: "extractors.stooq_extractor"
      function: "fetch_data"
      params:
        ticker: "^TWSE" # Símbolo para TAIEX en Stooq
    transform:
      module: "transforms.prices"
      functions:
        - name: "clean_data"
          params: {}
        - name: "forward_fill_missing_dates"
          params: {}
        - name: "calculate_base100"
          params:
            base_date_str: "2024-01-01"
    loader:
      module: "loaders.supabase_loader"
      function: "load_data"
```

El orquestador recorre `pipelines` y ejecuta dinámicamente `extractor → transform → loader`.

---

## 5 · Programación en GitHub Actions

```yaml
on:
  schedule:
    - cron: "0 3 * * *"   # 05:00 CET
jobs:
  etl:
    steps:
      - uses: actions/checkout@v4
      - name: Build and run ETL container
        run: |
          docker build -t spg-etl ./apps/etl
          docker run --rm -e SUPABASE_URL -e SUPABASE_SERVICE_ROLE_KEY spg-etl
```

Las variables `SUPABASE_URL` y `SUPABASE_SERVICE_ROLE_KEY` se configuran como *Secrets* en el repositorio de GitHub.

---

## 6 · Seguridad y observabilidad

- **RLS** en Supabase: Las políticas de seguridad a nivel de fila están activadas. Solo el rol de servicio (`service_role`) puede escribir en las tablas de datos.
- **Logs JSON** a `stdout` → capturados por GitHub Actions. Si el proceso termina con un código de error (`exit != 0`), la acción falla y notifica.
- **Tests**: Pruebas unitarias con `pytest` para validar la lógica de transformaciones y la correcta construcción de los módulos.

---

## 7 · Extender el pipeline

1.  Añadir el nuevo activo a la tabla `assets` de Supabase (se puede hacer con un script o manualmente).
2.  Crear un nuevo extractor en la carpeta `extractors/` si la fuente de datos es nueva.
3.  Añadir un nuevo bloque de pipeline al fichero `config.yaml`.
4.  Hacer `commit` y `push`. El workflow de GitHub Actions lo ejecutará en el siguiente ciclo programado sin necesidad de más cambios.

---

## 8 · Requisitos mínimos

| Software | Versión      |
| -------- | ------------ |
| Python   | ≥ 3.12       |
| Docker   | ≥ 24.0       |
| Node.js  | ≥ 20         |

---

> **Estado** — Pipeline ETL estable y en producción desde el **26-Jul-2025**. **Cinco indicadores clave** (`TAIEX`, `SPX`, `NKX`, `KOSPI`, `SHC`) se cargan diariamente desde Stooq. El sistema está listo para la integración de nuevas fuentes de datos.

