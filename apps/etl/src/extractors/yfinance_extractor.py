import yfinance as yf
import pandas as pd
import logging
import requests
import requests_cache

def fetch_data(ticker: str, period: str = "max") -> pd.DataFrame:
    """
    Obtiene datos históricos de un ticker usando yfinance, con reintentos y cache.

    Args:
        ticker (str): El símbolo del activo en Yahoo Finance (ej: "^TWII").
        period (str): El período a descargar.

    Returns:
        pd.DataFrame: Un DataFrame con los datos OHLCV, o un DataFrame vacío si hay un error.
    """
    try:
        # Configurar una sesión con cache y un User-Agent para parecer un navegador
        session = requests_cache.CachedSession('yfinance.cache')
        session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        
        logging.info("Iniciando descarga para el ticker: %s con período: %s", ticker, period)
        stock = yf.Ticker(ticker, session=session)
        
        # yfinance a veces falla al primer intento, un reintento simple puede funcionar.
        hist = stock.history(period=period)
        if hist.empty:
            logging.warning("Primer intento falló o no devolvió datos para %s. Reintentando...", ticker)
            hist = stock.history(period=period)

        if hist.empty:
            logging.warning("No se encontraron datos para el ticker: %s tras el reintento.", ticker)
            # Devolvemos un DF vacío, el orquestador lo marcará como error.
            return pd.DataFrame()

        # Reseteamos el índice para que 'Date' se convierta en una columna
        hist.reset_index(inplace=True)

        # Renombramos las columnas para nuestro formato estándar y las ponemos en minúsculas
        hist.rename(columns={
            "Date": "date",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume"
        }, inplace=True)
        
        # Seleccionamos solo las columnas que nos interesan
        required_columns = ["date", "open", "high", "low", "close", "volume"]
        hist = hist[required_columns]

        logging.info("Descarga completada para %s. Obtenidas %d filas.", ticker, len(hist))
        return hist

    except Exception as e:
        logging.error("Error al descargar datos para el ticker %s: %s", ticker, e, exc_info=True)
        return pd.DataFrame()

if __name__ == '__main__':
    # Ejemplo de uso para probar el extractor directamente
    logging.basicConfig(level=logging.INFO)
    taiex_ticker = "^TWII"
    data = fetch_data(taiex_ticker, period="5d")
    if not data.empty:
        print(f"Últimos 5 días de datos para {taiex_ticker}:")
        print(data.head())
        print("\nTipos de datos:")
        print(data.dtypes)
    else:
        print(f"No se pudieron obtener datos para {taiex_ticker}") 