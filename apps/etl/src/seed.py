import yaml, sys, logging
from pathlib import Path
from dotenv import load_dotenv

# Añadimos el path de 'src' para poder importar 'utils'
sys.path.append(str(Path(__file__).resolve().parent))

from utils.supabase_client import get_supabase

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# Cargar variables de entorno desde .env si existe (para desarrollo local)
load_dotenv()

def seed_assets(config_path: Path):
    """
    Lee la lista de activos de un fichero de configuración YAML y los inserta/actualiza
    en la tabla 'assets' de Supabase.
    """
    if not config_path.exists():
        logging.error("El fichero de configuración no existe: %s", config_path)
        return 1

    try:
        logging.info("Cargando activos desde: %s", config_path)
        config = yaml.safe_load(config_path.read_text())
        assets_to_seed = config.get("assets", [])

        if not assets_to_seed:
            logging.warning("No se han encontrado activos para sembrar en el fichero de configuración.")
            return 0
        
        logging.info("Encontrados %d activos para sembrar/actualizar.", len(assets_to_seed))

        supabase = get_supabase()
        logging.info("Conectado a Supabase. Realizando 'upsert' en la tabla 'assets'...")

        # 'upsert' insertará o actualizará los activos basándose en la constraint UNIQUE del 'symbol'
        data, count = supabase.table("assets").upsert(assets_to_seed, on_conflict="symbol").execute()

        if data and len(data[1]) > 0:
            logging.info("Se han procesado %d activos con éxito.", len(data[1]))
            # for asset in data[1]:
            #     logging.info("  - %s", asset.get('symbol'))
        else:
            logging.info("No hubo cambios o la respuesta de la API fue vacía. Verifique los datos.")
        
        logging.info("Proceso de sembrado de activos finalizado.")
        return 0

    except Exception as e:
        logging.error("Ha ocurrido un error durante el sembrado de activos: %s", e, exc_info=True)
        return 1

def main():
    # La ruta al config.yaml se asume relativa a la localización de este script
    cfg_path = Path(__file__).resolve().parent / "config.yaml"
    sys.exit(seed_assets(cfg_path))

if __name__ == "__main__":
    main() 