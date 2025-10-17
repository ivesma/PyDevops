"""
Configuration management utilities for DevOps operations
"""

import json
import yaml
from pathlib import Path
from typing import Any, Dict, Optional


class ConfigManager:
    """Manage configuration files in various formats"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize ConfigManager
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = Path(config_path) if config_path else None
        self.config: Dict[str, Any] = {}
        
        if self.config_path and self.config_path.exists():
            self.load()
    
    def load(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if not self.config_path or not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        suffix = self.config_path.suffix.lower()
        
        if suffix == '.json':
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
        elif suffix in ['.yaml', '.yml']:
            with open(self.config_path, 'r') as f:
                self.config = yaml.safe_load(f)
        else:
            raise ValueError(f"Unsupported config format: {suffix}")
        
        return self.config
    
    def save(self, path: Optional[str] = None) -> None:
        """Save configuration to file"""
        target_path = Path(path) if path else self.config_path
        
        if not target_path:
            raise ValueError("No config path specified")
        
        suffix = target_path.suffix.lower()
        
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        if suffix == '.json':
            with open(target_path, 'w') as f:
                json.dump(self.config, f, indent=2)
        elif suffix in ['.yaml', '.yml']:
            with open(target_path, 'w') as f:
                yaml.dump(self.config, f, default_flow_style=False)
        else:
            raise ValueError(f"Unsupported config format: {suffix}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def update(self, updates: Dict[str, Any]) -> None:
        """Update configuration with dictionary"""
        self.config.update(updates)
