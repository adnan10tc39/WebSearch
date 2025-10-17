
from pathlib import Path
import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CFG_PATH = PROJECT_ROOT / "configs" / "app_config.yml"

class LoadConfig:
    def __init__(self):
        with open(CFG_PATH, "r") as f:
            self.data = yaml.safe_load(f)
        self.gpt_model = self.data["gpt_model"]
        self.temperature = self.data["temperature"]
        self.llm_system_role = self.data["llm_system_role"]
        self.llm_function_caller_system_role = self.data["llm_function_caller_system_role"]

