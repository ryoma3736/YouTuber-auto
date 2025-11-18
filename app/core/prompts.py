"""
Prompt management module
Loads prompts from prompts.yaml
"""
import yaml
from pathlib import Path

def load_prompts(file_path: str = "prompts.yaml") -> dict:
    """Load prompts from YAML file"""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Prompts file not found: {file_path}")

    with open(path, 'r', encoding='utf-8') as f:
        prompts = yaml.safe_load(f)

    return prompts

def get_prompt(name: str, prompts: dict = None) -> str:
    """Get a specific prompt by name"""
    if prompts is None:
        prompts = load_prompts()

    if name not in prompts:
        raise KeyError(f"Prompt '{name}' not found in prompts.yaml")

    return prompts[name]
