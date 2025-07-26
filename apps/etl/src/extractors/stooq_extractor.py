import pandas as pd
import logging
from datetime import date, timedelta
from urllib.error import HTTPError

def fetch_data(ticker: str, start_date_str: str = None) -> pd.DataFrame:
    """
    Descarga datos históricos de Stooq para un ticker específico usando la URL de descarga de CSV directa.
    Este método es más robusto que usar pandas-datareader.
    Si no se especifica start_date_str, se utiliza la fecha de hace 365 días.
    """
    end_date = date.today()
    if start_date_str:
        start_date = date.fromisoformat(start_date_str)
    else:
        # Por defecto, obtenemos el último año de datos.
        start_date = end_date - timedelta(days=365)
    
    start_d_str = start_date.strftime('%Y%m%d')
    end_d_str = end_date.strftime('%Y%m%d')
    
    # El ticker para la URL de Stooq no debe llevar el prefijo '^'
    ticker_for_url = ticker.replace('^', '')
    
    url = f"https://stooq.com/q/d/l/?s={ticker_for_url}&d1={start_d_str}&d2={end_d_str}&i=d"
    
    logging.info("Iniciando descarga directa desde Stooq para: %s (URL: %s)", ticker, url)

    try:
        hist = pd.read_csv(url)

        # Si el CSV viene vacío o con el mensaje 'No data', las columnas no existirán
        if hist.empty or 'Close' not in hist.columns:
            logging.warning("No se encontraron datos o el CSV está vacío para el ticker: %s en Stooq", ticker)
            return pd.DataFrame()

        logging.info("Descarga directa de Stooq completada para %s. Obtenidas %d filas.", ticker, len(hist))
        
        hist.rename(columns={
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
            'Volume': 'volume'
        }, inplace=True)

        hist['date'] = pd.to_datetime(hist['Date'])
        
        # Los datos de Stooq suelen venir en orden descendente, los ordenamos correctamente.
        hist.sort_values(by='date', ascending=True, inplace=True)
        
        # Seleccionar y devolver solo las columnas que nos interesan
        return hist[['date', 'open', 'high', 'low', 'close', 'volume']]

    except HTTPError as e:
        # Esto ocurre si el ticker es realmente inválido y la URL devuelve un 404
        logging.error("Error HTTP %s al descargar datos para el ticker %s desde Stooq (URL: %s)", e.code, ticker, url)
        return pd.DataFrame()
    except Exception as e:
        logging.error("Error inesperado al procesar datos para el ticker %s desde Stooq: %s", ticker, e)
        return pd.DataFrame()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    taiex_ticker = "^TWII"  # El ticker del TAIEX es el mismo en Stooq
    data = fetch_data(taiex_ticker)
    if not data.empty:
        print(f"Datos más recientes para {taiex_ticker} desde Stooq:")
        print(data.tail())
    else:
        print(f"No se pudieron obtener datos para {taiex_ticker} desde Stooq.") 