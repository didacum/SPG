import pandas as pd
import logging

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia y estandariza el DataFrame de datos de mercado.

    - Se asegura de que la columna 'date' sea de tipo datetime y consciente de UTC.
    - Elimina filas con 'close' nulo.
    """
    if df.empty:
        return df

    df_clean = df.copy()
    
    # Convertir 'date' a datetime y localizar a UTC
    # El .dt.date lo convierte a solo fecha, eliminando la hora
    df_clean['date'] = pd.to_datetime(df_clean['date']).dt.tz_convert(None).dt.date
    
    # Eliminar filas donde el precio de cierre es nulo, ya que no podemos trabajar con ellas
    original_rows = len(df_clean)
    df_clean.dropna(subset=['close'], inplace=True)
    if len(df_clean) < original_rows:
        logging.warning("Se eliminaron %d filas con precios de cierre nulos.", original_rows - len(df_clean))

    return df_clean

def calculate_base100(df: pd.DataFrame, base_date_str: str = None) -> pd.DataFrame:
    """
    Calcula una nueva columna 'value' normalizada a base 100.

    Args:
        df (pd.DataFrame): El DataFrame limpio, debe contener 'date' y 'close'.
        base_date_str (str): La fecha base en formato 'YYYY-MM-DD'. Si es None,
                             se usará la primera fecha disponible en los datos.

    Returns:
        pd.DataFrame: El DataFrame original con una columna adicional 'value'.
    """
    if df.empty:
        return df

    df_transformed = df.copy()
    
    # Asegurarse de que la fecha base es un objeto date
    if base_date_str:
        base_date = pd.to_datetime(base_date_str).date()
    else:
        base_date = df_transformed['date'].min()
        logging.info("No se especificó fecha base, usando la primera disponible: %s", base_date)

    # Encontrar el precio de cierre en la fecha base
    base_row = df_transformed[df_transformed['date'] == base_date]

    if base_row.empty:
        logging.error("La fecha base %s no se encuentra en los datos. No se puede normalizar.", base_date)
        df_transformed['value'] = None
        return df_transformed
    
    base_value = base_row['close'].iloc[0]

    if base_value == 0:
        logging.error("El valor base en la fecha %s es 0. No se puede dividir por cero.", base_date)
        df_transformed['value'] = None
        return df_transformed
        
    # Calcular la columna 'value' normalizada a base 100
    df_transformed['value'] = (df_transformed['close'] / base_value) * 100
    
    logging.info("Normalización a base 100 completada usando el valor %.2f del %s.", base_value, base_date)
    
    return df_transformed

if __name__ == '__main__':
    # Ejemplo de uso para probar las transformaciones
    logging.basicConfig(level=logging.INFO)
    test_data = {
        'date': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04']),
        'close': [100, 105, 110, 95]
    }
    test_df = pd.DataFrame(test_data)
    
    print("DataFrame Original:")
    print(test_df)
    
    cleaned_df = clean_data(test_df)
    print("\nDataFrame Limpio:")
    print(cleaned_df)
    
    transformed_df = calculate_base100(cleaned_df, base_date_str='2023-01-02')
    print("\nDataFrame Transformado (base 100):")
    print(transformed_df) 