import pandas as pd
import logging, sys
from pathlib import Path

# Añadimos el path de 'src' para poder importar 'utils'
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils.supabase_client import get_supabase

def load_data(df: pd.DataFrame, asset_symbol: str):
    """
    Carga un DataFrame transformado en la tabla 'market_data' de Supabase.

    Args:
        df (pd.DataFrame): DataFrame con datos limpios y transformados.
        asset_symbol (str): Símbolo del activo (ej: "TAIEX") para buscar su ID.
    
    Returns:
        bool: True si la carga fue exitosa, False en caso contrario.
    """
    if df.empty:
        logging.warning("El DataFrame está vacío. No hay datos que cargar para %s.", asset_symbol)
        return True

    try:
        supabase = get_supabase()
        
        # 1. Obtener el ID del activo desde la tabla 'assets'
        logging.info("Buscando el ID para el símbolo: %s", asset_symbol)
        asset_response = supabase.table("assets").select("id").eq("symbol", asset_symbol).single().execute()
        
        if not asset_response.data:
            logging.error("No se encontró el activo con el símbolo '%s' en la tabla 'assets'.", asset_symbol)
            return False
        
        asset_id = asset_response.data['id']
        logging.info("ID de activo para '%s' es: %d", asset_symbol, asset_id)

        # 2. Preparar los datos para la carga
        df_to_load = df.copy()
        df_to_load['asset_id'] = asset_id
        
        # Asegurarse de que las columnas coincidan con la tabla 'market_data'
        # La columna 'value' de nuestro df corresponde a la columna 'value' en la BBDD
        columns_to_load = ["asset_id", "date", "open", "high", "low", "close", "volume", "value"]
        
        # Filtrar solo las columnas que existen en el DataFrame
        existing_columns = [col for col in columns_to_load if col in df_to_load.columns]
        df_to_load = df_to_load[existing_columns]

        # Asegurar que el 'volume' es un entero para que coincida con el tipo 'bigint' de la BBDD
        if 'volume' in df_to_load.columns:
            df_to_load['volume'] = df_to_load['volume'].astype('int64')

        # Reemplazar NaN de pandas con None de Python, que se traduce a NULL en la BBDD
        df_to_load = df_to_load.replace({pd.NA: None, pd.NaT: None, float('nan'): None})

        # Convertir el DataFrame a una lista de diccionarios, que es lo que espera Supabase
        records = df_to_load.to_dict(orient="records")
        
        # Convertir fechas a string en formato ISO para la API
        for record in records:
            record['date'] = record['date'].isoformat()

        # 3. Realizar el upsert
        logging.info("Iniciando carga de %d registros en 'market_data' para el activo '%s'...", len(records), asset_symbol)
        
        # Usamos on_conflict para evitar duplicados en el par (asset_id, date)
        # Esto asume que tienes una constraint UNIQUE en (asset_id, date) en tu tabla.
        data, count = supabase.table("market_data").upsert(records, on_conflict="asset_id,date").execute()

        if count:
             logging.info("Respuesta de Supabase: %s", count)
        
        logging.info("Carga completada para '%s'.", asset_symbol)
        return True

    except Exception as e:
        logging.error("Error durante la carga de datos para '%s': %s", asset_symbol, e, exc_info=True)
        return False

if __name__ == '__main__':
    # Ejemplo de uso para probar el loader directamente
    logging.basicConfig(level=logging.INFO)
    
    # Supongamos que tenemos un DataFrame transformado
    test_data = {
        'date': [pd.to_datetime('2023-01-05').date()],
        'open': [15000], 'high': [15100], 'low': [14900], 
        'close': [15050], 'volume': [1000000], 'value': [100.33]
    }
    test_df = pd.DataFrame(test_data)
    
    # Para que esta prueba funcione, necesitas:
    # 1. Un fichero .env con las credenciales de Supabase.
    # 2. El activo 'TAIEX' debe existir en tu tabla 'assets'.
    from dotenv import load_dotenv
    load_dotenv()
    
    print("DataFrame de prueba a cargar:")
    print(test_df)
    
    success = load_data(test_df, "TAIEX")
    if success:
        print("\nPrueba de carga finalizada con éxito.")
    else:
        print("\nPrueba de carga ha fallado.") 