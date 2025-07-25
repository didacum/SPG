import yfinance as yf
import pandas as pd
import logging
import requests
import requests_cache
import time
from datetime import date, timedelta

def fetch_data(ticker: str, period: str = "max") -> pd.DataFrame:
    """
    Obtiene datos históricos de un ticker usando yfinance, con reintentos explícitos y cache.

    Args:
        ticker (str): El símbolo del activo en Yahoo Finance (ej: "^TWII").
        period (str): El período a descargar.

    Returns:
        pd.DataFrame: Un DataFrame con los datos OHLCV, o un DataFrame vacío si hay un error.
    """
    # Configurar una sesión con cache y un User-Agent para parecer un navegador
    session = requests_cache.CachedSession('yfinance.cache', expire_after=timedelta(hours=1))
    session.headers['User-Agent'] = 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'
    
    stock = yf.Ticker(ticker, session=session)
    
    hist = pd.DataFrame() # Inicializar hist como DataFrame vacío

    # Intentar la descarga hasta 3 veces con pausas
    for attempt in range(3):
        try:
            logging.info("Intento %d/%d: Iniciando descarga para ticker: %s", attempt + 1, 3, ticker)
            hist = stock.history(period=period, auto_adjust=True)
            
            if not hist.empty:
                logging.info("Descarga completada en el intento %d. Obtenidas %d filas.", attempt + 1, len(hist))
                break  # Salir del bucle si tenemos éxito
            
            logging.warning("Intento %d/%d: No se encontraron datos para %s.", attempt + 1, 3, ticker)
            if attempt < 2:
                logging.info("Esperando 5 segundos antes de reintentar...")
                time.sleep(5)

        except Exception as e:
            logging.error("Intento %d/%d: Excepción durante la descarga para %s: %s", attempt + 1, 3, ticker, e)
            if attempt < 2:
                logging.info("Esperando 5 segundos antes de reintentar...")
                time.sleep(5)

    if hist.empty:
        logging.error("No se pudieron obtener datos para el ticker %s tras 3 intentos.", ticker)
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
    
    # Seleccionamos solo las columnas que nos interesan (si existen)
    required_columns = ["date", "open", "high", "low", "close", "volume"]
    existing_columns = [col for col in required_columns if col in hist.columns]
    hist = hist[existing_columns]

    return hist

if __name__ == '__main__':
    # Ejemplo de uso para probar el extractor directamente
    logging.basicConfig(level=logging.INFO)
    taiex_ticker = "^TWII"
    data = fetch_data(taiex_ticker, period="1y") # Reducimos el período para la prueba
    if not data.empty:
        print(f"Últimos 5 días de datos para {taiex_ticker}:")
        print(data.head())
        print("\nTipos de datos:")
        print(data.dtypes)
    else:
        print(f"No se pudieron obtener datos para {taiex_ticker}") 