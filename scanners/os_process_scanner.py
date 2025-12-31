"""
Process Scanner Module - OS Level
Scans processes using standard OS APIs (what users normally see)
"""

import psutil
import logging
from typing import List, Dict
from datetime import datetime

logger = logging.getLogger(__name__)


class OSProcessScanner:
    """Scans processes using OS-level APIs (psutil)"""
    
    def __init__(self):
        self.processes = []
        
    def scan(self) -> List[Dict]:
        """
        Scan all processes visible through OS APIs
        Returns list of process information dictionaries
        """
        logger.info("Starting OS-level process scan...")
        self.processes = []
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'exe', 'username', 'status']):
                try:
                    proc_info = proc.info
                    self.processes.append({
                        'pid': proc_info['pid'],
                        'name': proc_info['name'],
                        'exe': proc_info['exe'],
                        'username': proc_info['username'],
                        'status': proc_info['status'],
                        'scan_method': 'OS_API',
                        'timestamp': datetime.now().isoformat()
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
                    logger.warning(f"Could not access process: {e}")
                    continue
                    
            logger.info(f"OS scan completed: {len(self.processes)} processes found")
            return self.processes
            
        except Exception as e:
            logger.error(f"Error during OS process scan: {e}")
            return []
    
    def get_process_by_pid(self, pid: int) -> Dict:
        """Get process info by PID"""
        for proc in self.processes:
            if proc['pid'] == pid:
                return proc
        return None
    
    def get_process_names(self) -> List[str]:
        """Get list of all process names"""
        return [proc['name'] for proc in self.processes]
    
    def get_pids(self) -> List[int]:
        """Get list of all PIDs"""
        return [proc['pid'] for proc in self.processes]
