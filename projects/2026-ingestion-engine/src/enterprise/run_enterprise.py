import os
import sys
import yaml
import json
import importlib
import argparse
from datetime import datetime
from pathlib import Path

# Ensure src/ modules are reachable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.logger import get_logger
from src.enterprise.base_client import RestAPIClient
from src.enterprise.transform_v2 import DataTransformerV2
from src.enterprise.senior_eda import EnterpriseEDAEngine

logger = get_logger(__name__)

def run(config_path: Path) -> None:
    """Enterprise Pipeline Orchestrator. Completely decoupled from specific APIs."""
    if not config_path.exists():
        logger.error(f"Config file not found: {config_path}")
        return
        
    with open(config_path, "r") as f:
        spec = yaml.safe_load(f)
        
    out_dir = Path("data") / "landing"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    for source in spec["sources"]:
        name = source["name"]
        logger.info(f"=== Starting Ingestion: {name} ===")
        
        try:
            # 1. Instantiate varying strategies
            if source.get("type") == "custom_plugin":
                logger.info(f"Delegating to custom plugin: {source['plugin_module']}")
                module = importlib.import_module(source["plugin_module"])
                PluginClass = getattr(module, source["plugin_class"])
                # Fallback to dev mode so we don't need real FCC creds during execution demos
                client = PluginClass(output_dir=out_dir)
                data = client.fetch(env="dev") 
            else:
                client = RestAPIClient(config=source)
                data = client.fetch()
            
            # 2. Universal Landing Zone Dump
            file_path = out_dir / f"{name}_v2_{timestamp}.json"
            with open(file_path, "w") as f:
                json.dump(data, f, indent=2)
                
            logger.info(f"Success. Landed payload at {file_path}")
            
        except Exception as e:
            logger.error(f"Failed to ingest {name}: {e}")

    # 3. Bronze to Silver Orchestration
    logger.info("=== Starting V2 Schema Transformations ===")
    transformer = DataTransformerV2()
    silver_ready = True
    for source in spec["sources"]:
        name = source["name"]
        file_path = out_dir / f"{name}_v2_{timestamp}.json"
        
        try:
            if not file_path.exists(): continue
            with open(file_path, "r") as f:
                raw_data = json.load(f)
            
            if name == "nces_grade3":
                transformer.load_grade3_to_silver(raw_data)
            elif name == "broadband":
                transformer.load_broadband_to_silver(raw_data)
            elif name == "census_hps":
                transformer.load_hps_to_silver(raw_data)
            elif name == "fcc_broadband":
                transformer.load_broadband_to_silver(raw_data)
            elif name == "census_income":
                transformer.load_income_to_silver(raw_data)
        except Exception as e:
            logger.error(f"Silver transform failed for {name}: {e}")
            silver_ready = False
            
    transformer.close()
    
    # 4. Gold Data Quality Pipeline (The Real Enterprise Value)
    if silver_ready:
        logger.info("=== Starting V2 Advanced Analytical Engine ===")
        eda = EnterpriseEDAEngine()
        try:
            eda.materialize_analytical_gold()
            eda.check_ecological_fallacy()
            eda.generate_descriptive_stats()
            eda.calculate_effect_sizes()
            
            bias_detected = eda.run_simpsons_paradox_check()
            eda.plot_stratified_variance(out_dir)
            
            if bias_detected:
                logger.critical("🛑 PIPELINE HALTED: Correlation artifact invalid. ML export aborted.")
                eda.plot_real_income_control(out_dir)
            else:
                logger.info("✅ Pipeline cleared structural DQ gates. Exporting Gold...")
        finally:
            eda.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enterprise Data Ingestion Engine")
    parser.add_argument(
        "--config", 
        type=str, 
        default=str(Path(__file__).parent / "config.yaml"),
        help="Path to the ingestion configuration YAML"
    )
    args = parser.parse_args()
    run(Path(args.config))
