import pandas as pd
import pandas_datareader.data as web
import logging
from datetime import date, timedelta

def fetch_data(ticker: str, start_date_str: str = None) -> pd.DataFrame:
    """
    Obtiene datos históricos de un ticker desde Stooq.

    Args:
        ticker (str): El símbolo del activo en Stooq (ej: "^TWII").
        start_date_str (str): Fecha de inicio en formato "YYYY-MM-DD". 
                              Si es None, se usa hace un año desde hoy.

    Returns:
        pd.DataFrame: Un DataFrame con los datos OHLCV.
    """
    try:
        if start_date_str:
            start_date = pd.to_datetime(start_date_str)
        else:
            start_date = date.today() - timedelta(days=365)
        
        end_date = date.today()

        logging.info("Iniciando descarga desde Stooq para: %s (desde %s hasta %s)", ticker, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
        
        # Stooq devuelve los datos en orden descendente, así que los invertimos
        hist = web.DataReader(ticker, 'stooq', start=start_date, end=end_date).sort_index()

        if hist.empty:
            logging.warning("No se encontraron datos para el ticker: %s en Stooq", ticker)
            return pd.DataFrame()

        hist.reset_index(inplace=True)
        hist.rename(columns={
            "Date": "date",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume"
        }, inplace=True)
        
        required_columns = ["date", "open", "high", "low", "close", "volume"]
        hist = hist[required_columns]

        logging.info("Descarga de Stooq completada para %s. Obtenidas %d filas.", ticker, len(hist))
        return hist

    except Exception as e:
        logging.error("Error al descargar datos para el ticker %s desde Stooq: %s", ticker, e, exc_info=True)
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