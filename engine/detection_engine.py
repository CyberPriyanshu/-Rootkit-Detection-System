"""
Detection Engine Module
Core logic for comparing scan results and identifying anomalies
"""

import logging
from typing import Dict, List, Set
from datetime import datetime

logger = logging.getLogger(__name__)


class DetectionEngine:
    """
    Core detection engine that compares scan results
    to identify hidden processes and files (rootkit indicators)
    """
    
    def __init__(self):
        self.detections = []
        self.severity_levels = {
            'CRITICAL': 'Hidden process or file detected',
            'HIGH': 'Suspicious process behavior',
            'MEDIUM': 'Anomalous system activity',
            'LOW': 'Informational finding'
        }
        
    def compare_processes(self, os_processes: List[Dict], 
                         lowlevel_processes: List[Dict]) -> Dict:
        """
        Compare OS-level vs low-level process scans
        
        Args:
            os_processes: Processes from OS API scan
            lowlevel_processes: Processes from low-level API scan
            
        Returns:
            Dictionary containing detection results
        """
        logger.info("Comparing process scan results...")
        
        # Extract PIDs from both scans
        os_pids = {proc['pid'] for proc in os_processes}
        lowlevel_pids = {proc['pid'] for proc in lowlevel_processes}
        
        # Find hidden processes (in low-level but not in OS)
        hidden_pids = lowlevel_pids - os_pids
        
        # Find visible processes (in both)
        visible_pids = os_pids & lowlevel_pids
        
        # Find OS-only processes (anomaly - shouldn't happen)
        os_only_pids = os_pids - lowlevel_pids
        
        # Build detailed results
        hidden_processes = []
        for pid in hidden_pids:
            proc = self._find_process_by_pid(lowlevel_processes, pid)
            if proc:
                detection = {
                    'type': 'HIDDEN_PROCESS',
                    'severity': 'CRITICAL',
                    'pid': pid,
                    'name': proc.get('name', 'Unknown'),
                    'description': f"Process {proc.get('name')} (PID: {pid}) is hidden from OS APIs",
                    'details': proc,
                    'timestamp': datetime.now().isoformat()
                }
                hidden_processes.append(detection)
                self.detections.append(detection)
                logger.warning(f"CRITICAL: Hidden process detected - {proc.get('name')} (PID: {pid})")
        
        results = {
            'hidden_processes': hidden_processes,
            'hidden_count': len(hidden_pids),
            'visible_count': len(visible_pids),
            'os_only_count': len(os_only_pids),
            'total_os_processes': len(os_pids),
            'total_lowlevel_processes': len(lowlevel_pids),
            'scan_timestamp': datetime.now().isoformat()
        }
        
        if hidden_processes:
            logger.critical(f"ROOTKIT ALERT: {len(hidden_processes)} hidden process(es) detected!")
        else:
            logger.info("No hidden processes detected - system appears clean")
            
        return results
    
    def compare_files(self, os_files: Set[str], lowlevel_files: Set[str]) -> Dict:
        """
        Compare OS-level vs low-level file scans
        
        Args:
            os_files: Set of file paths from OS scan
            lowlevel_files: Set of file paths from low-level scan
            
        Returns:
            Dictionary containing detection results
        """
        logger.info("Comparing file scan results...")
        
        # Find hidden files (in low-level but not in OS)
        hidden_files = lowlevel_files - os_files
        
        # Find visible files (in both)
        visible_files = os_files & lowlevel_files
        
        # Build detailed results
        hidden_file_detections = []
        for filepath in hidden_files:
            detection = {
                'type': 'HIDDEN_FILE',
                'severity': 'HIGH',
                'path': filepath,
                'description': f"File {filepath} is hidden from standard file explorers",
                'timestamp': datetime.now().isoformat()
            }
            hidden_file_detections.append(detection)
            self.detections.append(detection)
            logger.warning(f"HIGH: Hidden file detected - {filepath}")
        
        results = {
            'hidden_files': list(hidden_files),
            'hidden_count': len(hidden_files),
            'visible_count': len(visible_files),
            'total_os_files': len(os_files),
            'total_lowlevel_files': len(lowlevel_files),
            'detections': hidden_file_detections,
            'scan_timestamp': datetime.now().isoformat()
        }
        
        if hidden_file_detections:
            logger.warning(f"ALERT: {len(hidden_file_detections)} hidden file(s) detected!")
        else:
            logger.info("No hidden files detected - file system appears clean")
            
        return results
    
    def analyze_baseline_drift(self, current_state: Dict, baseline_state: Dict) -> Dict:
        """
        Compare current system state against baseline snapshot
        
        Args:
            current_state: Current system scan results
            baseline_state: Previously saved baseline state
            
        Returns:
            Dictionary containing changes detected
        """
        logger.info("Analyzing system drift from baseline...")
        
        changes = {
            'new_processes': [],
            'removed_processes': [],
            'new_files': [],
            'removed_files': [],
            'timestamp': datetime.now().isoformat()
        }
        
        # Compare processes
        if 'processes' in baseline_state and 'processes' in current_state:
            baseline_pids = {p['pid'] for p in baseline_state['processes']}
            current_pids = {p['pid'] for p in current_state['processes']}
            
            new_pids = current_pids - baseline_pids
            removed_pids = baseline_pids - current_pids
            
            for pid in new_pids:
                proc = self._find_process_by_pid(current_state['processes'], pid)
                if proc:
                    changes['new_processes'].append(proc)
                    logger.info(f"New process since baseline: {proc.get('name')} (PID: {pid})")
            
            for pid in removed_pids:
                proc = self._find_process_by_pid(baseline_state['processes'], pid)
                if proc:
                    changes['removed_processes'].append(proc)
        
        return changes
    
    def get_all_detections(self) -> List[Dict]:
        """Get all detections from current session"""
        return self.detections
    
    def get_critical_detections(self) -> List[Dict]:
        """Get only critical severity detections"""
        return [d for d in self.detections if d.get('severity') == 'CRITICAL']
    
    def clear_detections(self):
        """Clear all stored detections"""
        self.detections = []
        logger.info("Detection history cleared")
    
    def _find_process_by_pid(self, processes: List[Dict], pid: int) -> Dict:
        """Helper method to find process by PID in a list"""
        for proc in processes:
            if proc.get('pid') == pid:
                return proc
        return None
    
    def generate_summary(self) -> Dict:
        """
        Generate summary of all detections
        
        Returns:
            Dictionary with detection statistics and summary
        """
        summary = {
            'total_detections': len(self.detections),
            'critical_count': len([d for d in self.detections if d.get('severity') == 'CRITICAL']),
            'high_count': len([d for d in self.detections if d.get('severity') == 'HIGH']),
            'medium_count': len([d for d in self.detections if d.get('severity') == 'MEDIUM']),
            'low_count': len([d for d in self.detections if d.get('severity') == 'LOW']),
            'hidden_processes': len([d for d in self.detections if d.get('type') == 'HIDDEN_PROCESS']),
            'hidden_files': len([d for d in self.detections if d.get('type') == 'HIDDEN_FILE']),
            'timestamp': datetime.now().isoformat()
        }
        
        # Determine overall threat level
        if summary['critical_count'] > 0:
            summary['threat_level'] = 'CRITICAL'
            summary['recommendation'] = 'Immediate action required - possible rootkit detected'
        elif summary['high_count'] > 0:
            summary['threat_level'] = 'HIGH'
            summary['recommendation'] = 'Investigation recommended - suspicious activity detected'
        elif summary['medium_count'] > 0:
            summary['threat_level'] = 'MEDIUM'
            summary['recommendation'] = 'Monitor system - anomalous behavior observed'
        else:
            summary['threat_level'] = 'LOW'
            summary['recommendation'] = 'System appears clean'
        
        return summary
