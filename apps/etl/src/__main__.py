import argparse, yaml, sys, logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

def main():
    p = argparse.ArgumentParser(description="SPG ETL Orchestrator")
    p.add_argument("-c", "--config", default="config.yaml", help="path to config file")
    args = p.parse_args()

    cfg_path = Path(__file__).resolve().parent / args.config
    if not cfg_path.exists():
        logging.error("Config file not found: %s", cfg_path)
        sys.exit(1)

    cfg = yaml.safe_load(cfg_path.read_text())
    logging.info("Loaded %d pipelines", len(cfg.get("pipelines", [])))
    # por ahora no hacemos más
    logging.info("ETL scaffold finished OK")
    sys.exit(0)

if __name__ == "__main__":
    main() 