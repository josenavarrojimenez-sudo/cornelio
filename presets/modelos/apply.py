#!/usr/bin/env python3
"""
Apply Model Presets to OpenClaw Agents

Usage:
    python3 apply.py <preset> <agent>
    
Examples:
    python3 apply.py coding cornelio
    python3 apply.py frontend cleo
    python3 apply.py chat magnum
"""

import json
import sys
import os
from pathlib import Path

PRESETS_DIR = Path(__file__).parent
AGENTS_DIR = Path("/root/.openclaw/agents")

def load_preset(preset_name):
    """Load a preset JSON file"""
    preset_path = PRESETS_DIR / f"{preset_name}.json"
    if not preset_path.exists():
        print(f"❌ Preset '{preset_name}' not found")
        print(f"Available presets: {[p.stem for p in PRESETS_DIR.glob('*.json')]}")
        return None
    
    with open(preset_path) as f:
        return json.load(f)

def apply_to_agent(preset_data, agent_id):
    """Apply preset to an agent's models.json"""
    agent_models = AGENTS_DIR / agent_id / "agent" / "models.json"
    
    if not agent_models.exists():
        print(f"❌ Agent '{agent_id}' not found")
        return False
    
    # Load current models.json
    with open(agent_models) as f:
        models_data = json.load(f)
    
    # Build new models list from preset
    new_models = []
    
    # Add primary
    primary = preset_data['models']['primary']
    provider, model_id = parse_model_id(primary)
    if provider and model_id:
        new_models.append({
            "id": model_id,
            "name": f"{preset_data['name']} Primary",
            "reasoning": True,
            "input": ["text", "image"],
            "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0},
            "contextWindow": 262144,
            "maxTokens": 16384
        })
    
    # Add fallbacks
    for fallback in preset_data['models']['fallbacks']:
        provider, model_id = parse_model_id(fallback)
        if provider and model_id:
            new_models.append({
                "id": model_id,
                "name": model_id,
                "reasoning": True,
                "input": ["text", "image"],
                "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0},
                "contextWindow": 262144,
                "maxTokens": 16384
            })
    
    # Update provider configs
    if 'ollama' not in models_data['providers']:
        models_data['providers']['ollama'] = {
            "baseUrl": "https://ollama.com/v1",
            "api": "ollama",
            "apiKey": "ollama-local",
            "models": []
        }
    
    if 'openrouter' not in models_data['providers']:
        models_data['providers']['openrouter'] = {
            "baseUrl": "https://openrouter.ai/v1",
            "api": "openai-completions",
            "apiKey": "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",
            "models": []
        }
    
    # Clear and repopulate models
    models_data['providers']['ollama']['models'] = [m for m in new_models if ':' in m['id'] and 'cloud' in m['id']]
    models_data['providers']['openrouter']['models'] = [m for m in new_models if '/' in m['id']]
    
    # Save
    with open(agent_models, 'w') as f:
        json.dump(models_data, f, indent=2)
    
    print(f"✅ Applied preset '{preset_data['name']}' to agent '{agent_id}'")
    print(f"   Primary: {preset_data['models']['primary']}")
    print(f"   Fallbacks: {len(preset_data['models']['fallbacks'])} models")
    return True

def parse_model_id(model_string):
    """Parse model string into provider and model ID"""
    if model_string.startswith('ollama/'):
        return 'ollama', model_string.replace('ollama/', '')
    elif model_string.startswith('openrouter/'):
        return 'openrouter', model_string.replace('openrouter/', '')
    elif ':cloud' in model_string:
        return 'ollama', model_string
    else:
        return None, model_string

def list_presets():
    """List all available presets"""
    print("📦 Available Presets:\n")
    for preset_file in sorted(PRESETS_DIR.glob('*.json')):
        with open(preset_file) as f:
            data = json.load(f)
        print(f"  • {data['name']:15} - {data['description']}")
    print()

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 apply.py <preset> [agent]")
        print("       python3 apply.py --list")
        print()
        list_presets()
        return
    
    if sys.argv[1] == '--list':
        list_presets()
        return
    
    if len(sys.argv) < 3:
        print("❌ Missing agent ID")
        print("Usage: python3 apply.py <preset> <agent>")
        return
    
    preset_name = sys.argv[1]
    agent_id = sys.argv[2]
    
    preset_data = load_preset(preset_name)
    if preset_data:
        apply_to_agent(preset_data, agent_id)

if __name__ == '__main__':
    main()
