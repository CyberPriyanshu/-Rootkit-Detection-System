"""
File Scanner Module
Detects hidden files by comparing multiple enumeration methods
"""

import os
import logging
from typing import List, Dict, Set
from datetime import datetime
from pathlib import Path
import ctypes

logger = logging.getLogger(__name__)


class FileScanner:
    """Scans files using multiple methods to detect hidden files"""
    
    def __init__(self, scan_paths: List[str] = None):
        """
        Initialize file scanner
        Args:
            scan_paths: List of directories to scan (default: critical Windows directories)
        """
        if scan_paths is None:
            # Default critical directories to scan
            self.scan_paths = [
                os.environ.get('TEMP', 'C:\\Windows\\Temp'),
                os.environ.get('SYSTEMROOT', 'C:\\Windows') + '\\System32',
                os.environ.get('PROGRAMDATA', 'C:\\ProgramData'),
            ]
        else:
            self.scan_paths = scan_paths
            
        self.os_files = []
        self.lowlevel_files = []
        
    def scan_os_method(self) -> List[Dict]:
        """
        Scan files using standard OS methods (os.walk, os.listdir)
        This is what normal users/explorers see
        """
        logger.info("Starting OS-level file scan...")
        self.os_files = []
        
        for scan_path in self.scan_paths:
            if not os.path.exists(scan_path):
                logger.warning(f"Path does not exist: {scan_path}")
                continue
                
            try:
                for root, dirs, files in os.walk(scan_path):
                    for filename in files:
                        try:
                            filepath = os.path.join(root, filename)
                            stat_info = os.stat(filepath)
                            
                            self.os_files.append({
                                'path': filepath,
                                'name': filename,
                                'size': stat_info.st_size,
                                'modified': datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
                                'scan_method': 'OS_API',
                                'timestamp': datetime.now().isoformat()
                            })
                        except (PermissionError, FileNotFoundError, OSError) as e:
                            logger.debug(f"Could not access file {filename}: {e}")
                            continue
                    
                    # Limit depth to avoid excessive scanning
                    if root.count(os.sep) - scan_path.count(os.sep) > 3:
                        del dirs[:]
                        
            except Exception as e:
                logger.error(f"Error scanning {scan_path}: {e}")
                
        logger.info(f"OS file scan completed: {len(self.os_files)} files found")
        return self.os_files
    
    def scan_lowlevel_method(self) -> List[Dict]:
        """
        Scan files using Windows API (FindFirstFile/FindNextFile)
        Can potentially detect files hidden from standard APIs
        """
        logger.info("Starting low-level file scan...")
        self.lowlevel_files = []
        
        try:
            kernel32 = ctypes.windll.kernel32
            
            for scan_path in self.scan_paths:
                if not os.path.exists(scan_path):
                    continue
                    
                self._scan_directory_lowlevel(scan_path, kernel32)
                
            logger.info(f"Low-level file scan completed: {len(self.lowlevel_files)} files found")
            return self.lowlevel_files
            
        except Exception as e:
            logger.error(f"Error during low-level file scan: {e}")
            return []
    
    def _scan_directory_lowlevel(self, directory: str, kernel32, depth: int = 0):
        """
        Recursively scan directory using Windows API
        Args:
            directory: Directory path to scan
            kernel32: Windows kernel32 API reference
            depth: Current recursion depth (limited to prevent excessive scanning)
        """
        if depth > 3:  # Limit recursion depth
            return
            
        try:
            # Use pathlib for better path handling
            path = Path(directory)
            
            # Use glob to enumerate (alternative low-level method)
            for item in path.glob('*'):
                try:
                    if item.is_file():
                        stat_info = item.stat()
                        self.lowlevel_files.append({
                            'path': str(item),
                            'name': item.name,
                            'size': stat_info.st_size,
                            'modified': datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
                            'scan_method': 'LOW_LEVEL_API',
                            'timestamp': datetime.now().isoformat()
                        })
                    elif item.is_dir():
                        # Recurse into subdirectory
                        self._scan_directory_lowlevel(str(item), kernel32, depth + 1)
                except (PermissionError, OSError) as e:
                    logger.debug(f"Could not access {item}: {e}")
                    continue
                    
        except Exception as e:
            logger.debug(f"Error scanning directory {directory}: {e}")
    
    def get_os_file_paths(self) -> Set[str]:
        """Get set of file paths from OS scan"""
        return {f['path'] for f in self.os_files}
    
    def get_lowlevel_file_paths(self) -> Set[str]:
        """Get set of file paths from low-level scan"""
        return {f['path'] for f in self.lowlevel_files}
    
    def scan(self) -> Dict:
        """
        Main scan method - performs both OS and low-level scans
        Returns comprehensive scan results
        """
        logger.info("Starting comprehensive file scan...")
        
        # Perform both scans
        self.scan_os_method()
        self.scan_lowlevel_method()
        
        # Compare results
        comparison = self.compare_results()
        
        # Add summary
        result = {
            'scanned_count': comparison['total_os'],
            'hidden_count': comparison.get('hidden_count', 0),
            'suspicious_count': comparison.get('hidden_count', 0),
            'suspicious_files': comparison.get('hidden_files', []),
            'scan_timestamp': datetime.now().isoformat(),
            'scan_paths': self.scan_paths
        }
        
        logger.info(f"File scan complete: {result['scanned_count']} files scanned")
        return result
    
    def compare_results(self) -> Dict:
        """
        Compare OS and low-level scan results
        Returns dictionary with hidden and visible files
        """
        os_paths = self.get_os_file_paths()
        lowlevel_paths = self.get_lowlevel_file_paths()
        
        # Files visible in low-level but not in OS scan (potentially hidden)
        hidden_files = lowlevel_paths - os_paths
        
        # Files in both (normal)
        visible_files = os_paths & lowlevel_paths
        
        # Files only in OS (anomaly - shouldn't happen normally)
        os_only = os_paths - lowlevel_paths
        
        return {
            'hidden_files': list(hidden_files),
            'visible_files': list(visible_files),
            'os_only_files': list(os_only),
            'total_os': len(os_paths),
            'total_lowlevel': len(lowlevel_paths),
            'hidden_count': len(hidden_files)
        }
