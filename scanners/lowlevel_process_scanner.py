"""
Process Scanner Module - Low Level
Scans processes using Windows API directly (the truth)
"""

import ctypes
import logging
from typing import List, Dict
from datetime import datetime
import sys

logger = logging.getLogger(__name__)

# Windows API constants
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010
MAX_PATH = 260

# Windows API structures
class PROCESSENTRY32(ctypes.Structure):
    _fields_ = [
        ("dwSize", ctypes.c_ulong),
        ("cntUsage", ctypes.c_ulong),
        ("th32ProcessID", ctypes.c_ulong),
        ("th32DefaultHeapID", ctypes.c_void_p),
        ("th32ModuleID", ctypes.c_ulong),
        ("cntThreads", ctypes.c_ulong),
        ("th32ParentProcessID", ctypes.c_ulong),
        ("pcPriClassBase", ctypes.c_long),
        ("dwFlags", ctypes.c_ulong),
        ("szExeFile", ctypes.c_char * MAX_PATH)
    ]


class LowLevelProcessScanner:
    """Scans processes using Windows API directly"""
    
    def __init__(self):
        self.processes = []
        self.kernel32 = None
        self._initialize_api()
        
    def _initialize_api(self):
        """Initialize Windows API access"""
        try:
            if sys.platform == 'win32':
                self.kernel32 = ctypes.windll.kernel32
                logger.info("Windows API initialized successfully")
            else:
                logger.warning("Not running on Windows - low-level scan unavailable")
        except Exception as e:
            logger.error(f"Failed to initialize Windows API: {e}")
    
    def scan(self) -> List[Dict]:
        """
        Scan all processes using Windows API (CreateToolhelp32Snapshot)
        This can detect processes that might be hidden from standard APIs
        """
        logger.info("Starting low-level process scan...")
        self.processes = []
        
        if not self.kernel32:
            logger.error("Windows API not available")
            return []
        
        try:
            # Create snapshot of all processes
            TH32CS_SNAPPROCESS = 0x00000002
            snapshot = self.kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
            
            if snapshot == -1:
                logger.error("Failed to create process snapshot")
                return []
            
            # Initialize process entry structure
            pe32 = PROCESSENTRY32()
            pe32.dwSize = ctypes.sizeof(PROCESSENTRY32)
            
            # Get first process
            if self.kernel32.Process32First(snapshot, ctypes.byref(pe32)):
                while True:
                    try:
                        proc_name = pe32.szExeFile.decode('utf-8', errors='ignore')
                        
                        self.processes.append({
                            'pid': pe32.th32ProcessID,
                            'name': proc_name,
                            'parent_pid': pe32.th32ParentProcessID,
                            'threads': pe32.cntThreads,
                            'scan_method': 'LOW_LEVEL_API',
                            'timestamp': datetime.now().isoformat()
                        })
                        
                    except Exception as e:
                        logger.warning(f"Error processing entry: {e}")
                    
                    # Move to next process
                    if not self.kernel32.Process32Next(snapshot, ctypes.byref(pe32)):
                        break
            
            # Close snapshot handle
            self.kernel32.CloseHandle(snapshot)
            
            logger.info(f"Low-level scan completed: {len(self.processes)} processes found")
            return self.processes
            
        except Exception as e:
            logger.error(f"Error during low-level process scan: {e}")
            return []
    
    def get_pids(self) -> List[int]:
        """Get list of all PIDs"""
        return [proc['pid'] for proc in self.processes]
    
    def get_process_names(self) -> List[str]:
        """Get list of all process names"""
        return [proc['name'] for proc in self.processes]
    
    def get_process_by_pid(self, pid: int) -> Dict:
        """Get process info by PID"""
        for proc in self.processes:
            if proc['pid'] == pid:
                return proc
        return None
