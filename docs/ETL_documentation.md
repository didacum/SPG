# ETL – Sistema de Ingesta y Normalización de Datos

*Proyecto SPG – MVP Estrecho de Taiwán*

---

## 1 · Propósito del ETL

Este pipeline automatiza la **extracción**, **transformación** y **carga** de indicadores financieros, métricas de cadena de suministro y señales de sentimiento hacia **Supabase Postgres**.\
Su objetivo es alimentar el *dashboard* con datos frescos cada madrugada (05:00 CET) y construir una base histórica homogénea que sirva al futuro modelo predictivo.

---

## 2 · Diagrama de alto nivel

```mermaid
graph TD
  A[GitHub Actions <br> cron 03:00 UTC] --> B[Contenedor<br>apps/etl]
  B -->|extract| C[APIs externas]
  B -->|load| D[(Supabase)]
  D --> E[Dashboard<br>(Next.js)]
  B --> F[Logs & métricas<br>→ Artifacts · Slack]
```

---

## 3 · Indicadores capturados

| Bloque dashboard | Símbolo `assets.symbol` | Descripción                            | Fuente                | Frecuencia | Justificación                   |
| ---------------- | ----------------------- | -------------------------------------- | --------------------- | ---------- | ------------------------------- |
| Mercado TW       | `TAIEX`                 | Taiwan Stock Index OHLC                | yfinance              | Diario     | Termómetro bursátil local       |
| Mercado TW       | `USD/TWD`               | Spot NT\$ por USD                      | TwelveData            | Diario     | Salidas/entradas de capital     |
| Mercado TW       | `VIXTWN`                | Índice de volatilidad opciones TAIEX   | TAIFEX CSV            | Diario     | Mide prime de riesgo implícita  |
| Riesgo fin.      | `CDS_TW_5Y`             | Credit‑Default Swap 5‑y soberano       | S&P Global API        | Diario     | Seguro de impago país           |
| Riesgo fin.      | `TW5Y_SPREAD`           | Yield 5‑y TW – UST                     | FRED                  | Diario     | Alternativa gratuita al CDS     |
| Shipping         | `AIS_CROSS`             | Nº buques >20 m que cruzan el estrecho | Spire AIS             | 6 h        | Bloqueo marítimo potencial      |
| Shipping         | `WCI`                   | World Container Index                  | Drewry                | Semanal    | Coste flete global / desvíos    |
| Shipping         | `BRENT`                 | Brent crude front‑m                    | yfinance              | Diario     | Proxy coste transporte, energía |
| Tech             | `SOX`                   | PHLX Semiconductor Index               | Stooq                 | Diario     | Salud sector chips mundial      |
| Tech             | `TSMC_REV_YOY`          | Ingresos YoY TSMC                      | MacroMicro            | Mensual    | Pulso gigante local             |
| Tech             | `TW_SEMI_EXP`           | Exportaciones chips TW YoY             | Customs API           | Mensual    | Cadena suministro física        |
| Sentimiento      | `SENT_SCORE`            | Sentiment 0‑100 titulares EN/ZH        | News API + DistilBERT | 4 h        | Narrativa mediática             |
| Sentimiento      | `ART_COUNT`             | Nº artículos                           | Idem                  | 4 h        | Volumen cobertura               |
| Termómetro       | `RISK_SCORE`            | Agregado 0‑100 ponderado               | Calculado ETL         | Diario     | KPI final del dashboard         |
| Actor China      | `CSI300`                | Índice China A‑shares                  | yfinance              | Diario     | Contagio regional               |
| Actor China      | `CNHUSD`                | Offshore Yuan                          | yfinance              | Diario     | Fuga capital china              |
| Actor USA        | `SP500`                 | S&P 500                                | yfinance              | Diario     | Risk‑off global                 |
| Actor USA        | `VIX`                   | Volatilidad S&P                        | yfinance              | Diario     | Stress global                   |

*(añadir más series = insertar nueva fila en **`assets`** y bloque en **`config.yaml`**)*

---

## 4 · Arquitectura del código ETL

```
apps/etl/
├── src/
│   ├── __main__.py          # orquestador CLI
│   ├── config.yaml          # mapping activos → extractores
│   ├── extractors/          # capa E
│   ├── transforms/          # capa T
│   ├── loaders/             # capa L
│   └── utils/               # logger, supabase_client, dates
├── Dockerfile               # imagen reproducible
└── tests/                   # pytest ≥85 % cobertura
```

### 4.1 Extractors

*Cada módulo **`extractors/*.py`** devuelve un **`pandas.DataFrame`** con columnas standard:*

```
[symbol, date, open, high, low, close, volume, value]
```

- **yfinance** genérico reutilizable.
- APIs con autenticación (Spire AIS, News API) leen la clave desde `os.environ`.

### 4.2 Transforms

- `clean_prices()` – ajusta duplicados, convierte zona horaria.
- `to_base100(df, base_date)` – calcula `base100` para comparabilidad.
- `compute_risk_index()` – fusiona z‑scores y guarda en tabla `risk_index`.

### 4.3 Loaders

Utilizan `supabase-py`:

```python
supabase.table("market_data").upsert(rows, on_conflict="asset_id,date")
```

Batch ≤ 500 filas → respeta rate‑limit Supabase.

---

## 5 · Configuración YAML de pipelines (ejemplo)

```yaml
pipelines:
  - id: taiex
    extractor: yfinance
    params: {ticker: "^TWII"}
    transform: prices
    asset_symbol: TAIEX

  - id: ais
    extractor: ais
    transform: shipping
    target_table: shipping_metrics
```

El orquestador recorre `pipelines` y ejecuta dinámicamente `extractor → transform → loader`.

---

## 6 · Programación en GitHub Actions

```yaml
on:
  schedule:
    - cron: "0 3 * * *"   # 05:00 CET
jobs:
  etl:
    steps:
      - checkout
      - docker build ./apps/etl
      - docker run -e SUPABASE_URL -e SUPABASE_SERVICE_ROLE_KEY spg-etl
```

Variables secretas: `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, `NEWSAPI_KEY`, `AIS_KEY`.

---

## 7 · Seguridad y observabilidad

- **RLS** en Supabase: sólo `service_role` inserta/actualiza.
- **Logs JSON** a stdout → capturados por GitHub Actions; si `exit != 0`, paso final envía webhook Slack.
- **Tests**: mock API responses; CI bloquea merge sin ≥85 % coverage.

---

## 8 · Extender el pipeline

1. Añadir símbolo en `assets`.
2. Crear extractor o reutilizar uno existente.
3. Escribir bloque YAML.
4. Merge → workflow cron ejecuta sin más cambios.

---

## 9 · Requisitos mínimos

| Software | Versión                    |
| -------- | -------------------------- |
| Python   | ≥ 3.12                     |
| Docker   | ≥ 24.0                     |
| Node     | ≥ 20 (sólo para dashboard) |

Claves API necesarias: **Supabase**, *News API*, *Spire AIS* (opcional), *TwelveData* (FX).

---

> **Estado** — Esqueleto desplegado el *23‑Jul‑2025*. Primeros indicadores en producción: **TAIEX, USD/TWD, VIXTWN**. Próximos pasos: añadir CSI 300 y Sentiment.

