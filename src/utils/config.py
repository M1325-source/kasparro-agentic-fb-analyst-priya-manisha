import os
import yaml

def load_config():
    """
    Load YAML config based on ENV env var. Defaults to 'dev'.
    """
    env = os.environ.get("ENV", "dev")
    path = os.path.join("config", f"{env}.yaml")
    if not os.path.exists(path):
        # fallback to dev
        path = os.path.join("config", "dev.yaml")
    with open(path, "r", encoding="utf8") as f:
        cfg = yaml.safe_load(f)
    cfg["_env"] = env
    return cfg
