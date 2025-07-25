import yaml, sys, logging, importlib
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [%(module)s.%(funcName)s] %(message)s")

# Cargar variables de entorno desde .env si existe
load_dotenv()

def run_pipeline(pipeline_config: dict):
    """Ejecuta un único pipeline de ETL definido en la configuración."""
    pipeline_id = pipeline_config.get('id', 'N/A')
    if not pipeline_config.get('enabled', False):
        logging.info("Pipeline '%s' está deshabilitado. Saltando.", pipeline_id)
        return True, pipeline_id

    logging.info("--- Iniciando pipeline: %s ---", pipeline_id)

    try:
        # --- EXTRACCIÓN ---
        extractor_cfg = pipeline_config['extractor']
        extractor_module = importlib.import_module(extractor_cfg['module'])
        extractor_func = getattr(extractor_module, extractor_cfg['function'])
        logging.info("Ejecutando extractor: %s.%s", extractor_cfg['module'], extractor_cfg['function'])
        df = extractor_func(**extractor_cfg.get('params', {}))

        if df.empty:
            logging.warning("El extractor no devolvió datos para el pipeline '%s'. Finalizando.", pipeline_id)
            return True, pipeline_id

        # --- TRANSFORMACIÓN ---
        transform_cfg = pipeline_config['transform']
        transform_module = importlib.import_module(transform_cfg['module'])
        for transform_step in transform_cfg.get('functions', []):
            transform_func = getattr(transform_module, transform_step['name'])
            logging.info("Aplicando transformación: %s.%s", transform_cfg['module'], transform_step['name'])
            df = transform_func(df, **transform_step.get('params', {}))

        # --- CARGA ---
        loader_cfg = pipeline_config['loader']
        loader_module = importlib.import_module(loader_cfg['module'])
        loader_func = getattr(loader_module, loader_cfg['function'])
        logging.info("Ejecutando cargador: %s.%s", loader_cfg['module'], loader_cfg['function'])
        
        # El cargador necesita el símbolo del activo para buscar su ID
        asset_symbol = pipeline_config['asset_symbol']
        success = loader_func(df, asset_symbol=asset_symbol)

        if not success:
            raise RuntimeError("El paso de carga falló.")

        logging.info("--- Pipeline '%s' finalizado con éxito ---", pipeline_id)
        return True, pipeline_id

    except Exception as e:
        logging.error("!!! Pipeline '%s' ha fallado: %s !!!", pipeline_id, e, exc_info=True)
        return False, pipeline_id

def main():
    """Punto de entrada principal del orquestador ETL."""
    config_path = Path(__file__).resolve().parent / "config.yaml"
    
    if not config_path.exists():
        logging.error("Fichero de configuración no encontrado: %s", config_path)
        sys.exit(1)
    
    config = yaml.safe_load(config_path.read_text())
    pipelines = config.get("pipelines", [])
    
    if not pipelines:
        logging.warning("No se han encontrado pipelines en el fichero de configuración.")
        sys.exit(0)

    logging.info("Orquestador ETL iniciado. Encontrados %d pipelines.", len(pipelines))
    
    results = [run_pipeline(p) for p in pipelines]
    
    successful_pipelines = [pid for success, pid in results if success]
    failed_pipelines = [pid for success, pid in results if not success]

    logging.info("--- Resumen de la ejecución ---")
    logging.info("Pipelines exitosos (%d): %s", len(successful_pipelines), ', '.join(successful_pipelines))
    if failed_pipelines:
        logging.error("Pipelines fallidos (%d): %s", len(failed_pipelines), ', '.join(failed_pipelines))
        sys.exit(1)
    
    logging.info("Todos los pipelines se ejecutaron con éxito.")
    sys.exit(0)

if __name__ == "__main__":
    main() 