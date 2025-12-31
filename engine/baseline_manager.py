"""
System Baseline Module
Creates and manages system state snapshots
"""

import json
import logging
from typing import Dict
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class BaselineManager:
    """
    Manages system baseline snapshots
    Saves clean system state for later comparison
    """
    
    def __init__(self, baseline_file: str = 'baseline.json'):
        """
        Initialize baseline manager
        
        Args:
            baseline_file: Path to baseline JSON file
        """
        self.baseline_file = Path(baseline_file)
        self.baseline_data = None
        
    def create_baseline(self, system_state: Dict) -> bool:
        """
        Create a new baseline snapshot
        
        Args:
            system_state: Dictionary containing current system state
                         (processes, files, etc.)
                         
        Returns:
            True if successful, False otherwise
        """
        try:
            baseline = {
                'created': datetime.now().isoformat(),
                'system_state': system_state,
                'version': '1.0'
            }
            
            with open(self.baseline_file, 'w') as f:
                json.dump(baseline, f, indent=4)
            
            self.baseline_data = baseline
            logger.info(f"Baseline created successfully: {self.baseline_file}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create baseline: {e}")
            return False
    
    def load_baseline(self) -> Dict:
        """
        Load existing baseline from file
        
        Returns:
            Baseline data dictionary or None if not found
        """
        try:
            if not self.baseline_file.exists():
                logger.warning(f"Baseline file not found: {self.baseline_file}")
                return None
            
            with open(self.baseline_file, 'r') as f:
                self.baseline_data = json.load(f)
            
            logger.info(f"Baseline loaded: created on {self.baseline_data.get('created')}")
            return self.baseline_data
            
        except Exception as e:
            logger.error(f"Failed to load baseline: {e}")
            return None
    
    def get_baseline_state(self) -> Dict:
        """Get the system state from baseline"""
        if self.baseline_data:
            return self.baseline_data.get('system_state', {})
        return {}
    
    def baseline_exists(self) -> bool:
        """Check if baseline file exists"""
        return self.baseline_file.exists()
