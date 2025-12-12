"""Service for saving and loading pivot configurations."""

import json
from typing import Optional

from pivot_builder.models.pivot_model import PivotConfig
from pivot_builder.config.logging_config import logger


class PivotConfigService:
    """Service for persisting pivot configurations to JSON."""

    def save(self, config: PivotConfig, path: str) -> bool:
        """
        Save pivot configuration to JSON file.

        Args:
            config: PivotConfig instance to save
            path: File path to save to

        Returns:
            True if successful, False otherwise
        """
        try:
            config_dict = config.to_dict()
            with open(path, 'w') as f:
                json.dump(config_dict, f, indent=2)
            logger.info(f"Saved pivot configuration to {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save pivot configuration: {e}")
            return False

    def load(self, path: str) -> Optional[PivotConfig]:
        """
        Load pivot configuration from JSON file.

        Args:
            path: File path to load from

        Returns:
            PivotConfig instance if successful, None otherwise
        """
        try:
            with open(path, 'r') as f:
                config_dict = json.load(f)
            config = PivotConfig.from_dict(config_dict)
            logger.info(f"Loaded pivot configuration from {path}")
            return config
        except Exception as e:
            logger.error(f"Failed to load pivot configuration: {e}")
            return None
