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
    
    # Convertir 'date' a datetime si no lo es ya
    df_clean['date'] = pd.to_datetime(df_clean['date'])

    # Si la fecha no tiene zona horaria (es 'naive'), la localizamos a UTC.
    # Si ya la tiene, nos aseguramos de que sea UTC.
    if df_clean['date'].dt.tz is None:
        df_clean['date'] = df_clean['date'].dt.tz_localize('UTC')
    else:
        df_clean['date'] = df_clean['date'].dt.tz_convert('UTC')
    
    # Finalmente, nos quedamos solo con la fecha, sin la hora.
    # Esto elimina la información de zona horaria, pero ya hemos estandarizado todo a UTC.
    df_clean['date'] = df_clean['date'].dt.date
    
    # Eliminar filas donde el precio de cierre es nulo, ya que no podemos trabajar con ellas
    original_rows = len(df_clean)
    df_clean.dropna(subset=['close'], inplace=True)
    if len(df_clean) < original_rows:
        logging.warning("Se eliminaron %d filas con precios de cierre nulos.", original_rows - len(df_clean))

    return df_clean

def forward_fill_missing_dates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rellena los días sin datos (fines de semana, festivos) con el último valor conocido.
    """
    if df.empty:
        return df

    df_filled = df.copy()
    
    # Asegurarse de que la columna 'date' es del tipo correcto para el reindexado
    df_filled['date'] = pd.to_datetime(df_filled['date'])
    df_filled.set_index('date', inplace=True)

    # Crear un rango de fechas completo desde el primer día hasta el último
    full_date_range = pd.date_range(start=df_filled.index.min(), end=df_filled.index.max(), freq='D')
    
    # Reindexar el DataFrame. Los días que no estaban se llenarán con NaN.
    df_filled = df_filled.reindex(full_date_range)
    
    # Usar forward-fill para rellenar los valores NaN.
    # No rellenamos 'volume' ya que un volumen 0 es más representativo para un día no bursátil.
    columns_to_fill = ['open', 'high', 'low', 'close']
    df_filled[columns_to_fill] = df_filled[columns_to_fill].ffill()
    
    # Rellenar el volumen con 0 y el símbolo del activo
    df_filled['volume'].fillna(0, inplace=True)
    
    # Resetear el índice para que 'date' vuelva a ser una columna
    df_filled.reset_index(inplace=True)
    df_filled.rename(columns={'index': 'date'}, inplace=True)

    logging.info("Se han rellenado los días no bursátiles. El total de filas ahora es: %d", len(df_filled))
    
    return df_filled

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

    # Encontrar el precio de cierre en la fecha base o en el siguiente día hábil disponible
    df_sorted = df_transformed.sort_values('date').set_index('date')
    base_row = df_sorted.loc[base_date:]

    if base_row.empty:
        logging.error("La fecha base %s o una posterior no se encuentra en los datos. No se puede normalizar.", base_date)
        df_transformed['value'] = None
        return df_transformed
    
    base_value = base_row['close'].iloc[0]
    actual_base_date = base_row.index[0]

    if base_value == 0:
        logging.error("El valor base en la fecha %s es 0. No se puede dividir por cero.", actual_base_date)
        df_transformed['value'] = None
        return df_transformed
        
    # Calcular la columna 'value' normalizada a base 100
    df_transformed['value'] = (df_transformed['close'] / base_value) * 100
    
    logging.info("Normalización a base 100 completada usando el valor %.2f del %s.", base_value, actual_base_date)
    
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