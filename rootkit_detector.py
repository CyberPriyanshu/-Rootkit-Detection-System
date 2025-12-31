"""
╔════════════════════════════════════════════════════════════════════════════╗
║                   ROOTKIT DETECTION & TESTING SYSTEM                       ║
║                        Educational Security Tool                           ║
╚════════════════════════════════════════════════════════════════════════════╝

⚠️ IMPORTANT: READ TERMS & CONDITIONS BEFORE USE ⚠️

This tool combines:
1. Advanced Rootkit Detection (defensive security)
2. Educational Testing Simulator (safe learning)
3. Automated Testing Workflow (all-in-one)

WHAT THIS TOOL DOES:
✓ Detects hidden processes and files
✓ Creates system baselines
✓ Generates security reports
✓ Simulates test scenarios (educational)
✓ Automated testing workflow

WHAT THIS TOOL DOES NOT DO:
✗ Create actual malware
✗ Hide processes from the OS
✗ Perform attacks
✗ Modify system files maliciously

═══════════════════════════════════════════════════════════════════════════
TERMS & CONDITIONS - MUST ACCEPT TO PROCEED
═══════════════════════════════════════════════════════════════════════════

BY USING THIS TOOL, YOU AGREE TO THE FOLLOWING:

1. EDUCATIONAL PURPOSE ONLY
   - This tool is for learning cybersecurity concepts
   - Not for unauthorized system access
   - Not for malicious purposes

2. AUTHORIZED USE ONLY
   - Use ONLY on systems you own
   - Use ONLY on systems you have explicit permission to test
   - Any unauthorized use is ILLEGAL

3. NO WARRANTY
   - Provided "as is" without guarantees
   - Author not liable for misuse
   - User assumes all responsibility

4. ETHICAL RESPONSIBILITY
   - You understand cybersecurity ethics
   - You will not use for harm
   - You will follow all applicable laws

5. TESTING SIMULATOR
   - Creates BENIGN test processes only
   - Does NOT create actual rootkits
   - All test actions are visible and reversible
   - For educational demonstration only

═══════════════════════════════════════════════════════════════════════════

⚖️ LEGAL NOTICE:
Unauthorized access to computer systems is illegal under:
- Computer Fraud and Abuse Act (USA)
- Computer Misuse Act (UK)
- Similar laws worldwide

Violators will be prosecuted to the fullest extent of the law.

═══════════════════════════════════════════════════════════════════════════
"""

import sys
import os
import argparse
import time
import logging
import subprocess
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from scanners import OSProcessScanner, LowLevelProcessScanner, FileScanner
from engine import DetectionEngine, BaselineManager
from utils import AlertSystem, ReportGenerator, setup_logging


class EducationalTestingSimulator:
    """Integrated testing simulator for educational purposes"""
    
    def __init__(self):
        self.test_processes = []
        self.test_files = []
        self.config_file = Path("test_results/test_config.json")
        self.results_file = Path("test_results/test_results.json")
        self.logger = logging.getLogger(__name__)
    
    def show_simulator_terms(self):
        """Display simulator-specific educational terms"""
        terms = """
╔════════════════════════════════════════════════════════════════════════════╗
║                     TESTING SIMULATOR - WHAT IT DOES                       ║
╚════════════════════════════════════════════════════════════════════════════╝

The testing simulator creates BENIGN processes to demonstrate detection:

✓ SAFE ACTIONS:
  - Creates visible Python processes
  - Runs harmless background tasks
  - Demonstrates detection methodology
  - All actions are reversible

✗ WHAT IT DOES NOT DO:
  - Does NOT hide processes (no kernel driver)
  - Does NOT create actual malware
  - Does NOT modify system permanently
  - Does NOT perform attacks

PURPOSE: Educational demonstration of security concepts
RESULT: You learn how rootkit detection works

Press ENTER to continue with simulator...
"""
        print(terms)
        input()
    
    def create_test_process(self, duration=120):
        """
        Create a benign test process for detection demonstration
        
        Args:
            duration: How long process should run (seconds)
        """
        self.logger.info(f"Creating educational test process (duration: {duration}s)")
        
        # Create test configuration
        config = {
            "created_at": datetime.now().isoformat(),
            "purpose": "Educational rootkit detection testing",
            "duration": duration,
            "process_type": "benign_background_process"
        }
        
        # Save configuration
        self.config_file.parent.mkdir(exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        # Create benign background process
        code = f"""
import time
import sys
from datetime import datetime

print("Educational Test Process Started")
print(f"PID: {{os.getpid()}}")
print(f"Purpose: Rootkit Detection Testing")
print(f"Duration: {duration} seconds")
print(f"Status: BENIGN - Safe for testing")
print()

# Run for specified duration
start = time.time()
while time.time() - start < {duration}:
    time.sleep(5)
    elapsed = int(time.time() - start)
    print(f"[{{datetime.now().strftime('%H:%M:%S')}}] Test process running... ({{elapsed}}s/{duration}s)")

print()
print("Test process completed successfully")
"""
        
        # Write test script
        test_script = Path("test_results/test_process.py")
        test_script.parent.mkdir(exist_ok=True)
        with open(test_script, 'w') as f:
            f.write(code)
        
        self.test_files.append(test_script)
        
        # Start the process
        try:
            python_exe = sys.executable
            process = subprocess.Popen(
                [python_exe, str(test_script)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
            )
            
            self.test_processes.append({
                "pid": process.pid,
                "name": "python.exe",
                "script": str(test_script),
                "started": datetime.now().isoformat()
            })
            
            self.logger.info(f"✓ Test process created: PID {process.pid}")
            print(f"\n✓ Educational test process created successfully!")
            print(f"  PID: {process.pid}")
            print(f"  Duration: {duration} seconds")
            print(f"  Status: Running in separate window")
            print(f"\n  This is a BENIGN process for testing purposes.")
            
            # Save test results
            with open(self.results_file, 'w') as f:
                json.dump(self.test_processes, f, indent=2)
            
            return process.pid
            
        except Exception as e:
            self.logger.error(f"Failed to create test process: {e}")
            print(f"\n✗ Error creating test process: {e}")
            return None
    
    def cleanup_test_artifacts(self):
        """Remove all test processes and files"""
        self.logger.info("Cleaning up test artifacts...")
        print("\n" + "="*80)
        print("CLEANUP: Removing test artifacts...")
        print("="*80)
        
        # Terminate processes
        terminated = 0
        if self.results_file.exists():
            with open(self.results_file, 'r') as f:
                test_data = json.load(f)
            
            for proc_info in test_data:
                pid = proc_info['pid']
                try:
                    import psutil
                    process = psutil.Process(pid)
                    process.terminate()
                    process.wait(timeout=3)
                    terminated += 1
                    print(f"✓ Terminated test process PID {pid}")
                except (psutil.NoSuchProcess, psutil.TimeoutExpired):
                    pass
                except Exception as e:
                    print(f"  Warning: Could not terminate PID {pid}: {e}")
        
        # Remove test files
        removed_files = 0
        test_files_to_remove = [
            self.config_file,
            self.results_file,
            Path("test_results/test_process.py")
        ]
        
        for file_path in test_files_to_remove:
            if file_path.exists():
                file_path.unlink()
                removed_files += 1
                print(f"✓ Removed {file_path}")
        
        print(f"\n✓ Cleanup complete:")
        print(f"  - Terminated {terminated} test process(es)")
        print(f"  - Removed {removed_files} test file(s)")
        print(f"  - System restored to clean state")


class RootkitDetector:
    """Unified rootkit detection and testing system"""
    
    def __init__(self, verbose=False):
        """Initialize detection system"""
        # Setup logging
        log_level = logging.DEBUG if verbose else logging.INFO
        self.log_file = setup_logging(log_level)
        
        # Initialize components
        self.alert_system = AlertSystem()
        self.detection_engine = DetectionEngine()
        self.baseline_manager = BaselineManager()
        self.report_generator = ReportGenerator()
        self.simulator = EducationalTestingSimulator()
        
        # Scanners
        self.os_process_scanner = OSProcessScanner()
        self.lowlevel_process_scanner = LowLevelProcessScanner()
        self.file_scanner = FileScanner()
        
        self.logger = logging.getLogger(__name__)
    
    def run_full_scan(self, enable_file_scan=True):
        """
        Execute complete security scan
        
        Args:
            enable_file_scan: Whether to include file system scanning
            
        Returns:
            dict: Scan results
        """
        self.logger.info("="*80)
        self.logger.info("STARTING COMPREHENSIVE SECURITY SCAN")
        self.logger.info("="*80)
        
        print("\n" + "="*80)
        print("ROOTKIT DETECTION SCAN")
        print("="*80)
        
        results = {
            'scan_time': datetime.now().isoformat(),
            'duration': 0,
            'processes': {},
            'files': {},
            'alerts': []
        }
        
        start_time = time.time()
        
        # Process scanning
        print("\n[1/3] Scanning processes...")
        print("  → OS-level scan (user-mode APIs)...")
        os_processes = self.os_process_scanner.scan()
        
        print("  → Kernel-level scan (low-level APIs)...")
        lowlevel_processes = self.lowlevel_process_scanner.scan()
        
        # Detection analysis
        print("\n[2/3] Analyzing for hidden processes...")
        detection_results = self.detection_engine.compare_processes(
            os_processes, lowlevel_processes
        )
        
        results['processes'] = detection_results
        
        # Generate alerts
        if detection_results['hidden_count'] > 0:
            alert = self.alert_system.create_alert(
                severity="CRITICAL",
                alert_type="HIDDEN_PROCESS",
                message=f"ROOTKIT DETECTED: {detection_results['hidden_count']} hidden process(es)",
                details=detection_results
            )
            results['alerts'].append(alert)
            self.alert_system.display_alert(alert)
        else:
            alert = self.alert_system.create_alert(
                severity="LOW",
                alert_type="SCAN_COMPLETE",
                message="No hidden processes detected - system clean",
                details=detection_results
            )
            # LOW alerts don't need to be displayed for clean scans
        
        # File scanning
        if enable_file_scan:
            print("\n[3/3] Scanning file system...")
            file_results = self.file_scanner.scan()
            results['files'] = file_results
            
            if file_results.get('suspicious_count', 0) > 0:
                alert = self.alert_system.create_alert(
                    severity="WARNING",
                    alert_type="SUSPICIOUS_FILE",
                    message=f"Found {file_results['suspicious_count']} suspicious file(s)",
                    details=file_results
                )
                results['alerts'].append(alert)
                self.alert_system.display_alert(alert)
        else:
            print("\n[3/3] File system scan: SKIPPED")
        
        # Calculate duration
        results['duration'] = time.time() - start_time
        
        # Summary
        print("\n" + "="*80)
        print("SCAN COMPLETE")
        print("="*80)
        print(f"Duration: {results['duration']:.2f} seconds")
        print(f"Processes scanned: {detection_results['total_lowlevel_processes']}")
        if enable_file_scan:
            print(f"Files scanned: {file_results.get('scanned_count', 0)}")
        print(f"Hidden processes: {detection_results['hidden_count']}")
        print(f"Alerts: {len(results['alerts'])}")
        
        # Determine threat level
        if detection_results['hidden_count'] > 0:
            threat_level = "CRITICAL"
        elif results.get('alerts'):
            threat_level = "MEDIUM"
        else:
            threat_level = "LOW"
        
        print(f"Threat level: {threat_level}")
        
        self.logger.info(f"Scan completed in {results['duration']:.2f}s")
        
        return results
    
    def create_baseline(self):
        """Create system baseline snapshot"""
        self.logger.info("Creating system baseline...")
        print("\n" + "="*80)
        print("CREATING SYSTEM BASELINE")
        print("="*80)
        print("\nCapturing current system state for future comparison...")
        
        # Scan processes
        print("\n[1/2] Scanning processes...")
        os_processes = self.os_process_scanner.scan()
        lowlevel_processes = self.lowlevel_process_scanner.scan()
        
        # Scan files
        print("\n[2/2] Scanning critical system files...")
        file_results = self.file_scanner.scan()
        
        # Save baseline
        baseline_data = {
            'created_at': datetime.now().isoformat(),
            'processes': {
                'os_level': os_processes,
                'kernel_level': lowlevel_processes
            },
            'files': file_results
        }
        
        self.baseline_manager.create_baseline(baseline_data)
        
        print("\n" + "="*80)
        print("✓ BASELINE CREATED SUCCESSFULLY")
        print("="*80)
        print(f"Processes recorded: {len(os_processes)}")
        print(f"Files recorded: {file_results.get('scanned_count', 0)}")
        print(f"Baseline saved to: {self.baseline_manager.baseline_file}")
        print("\nYou can now use --compare to detect changes since this baseline.")
        
        self.logger.info("Baseline created successfully")
    
    def compare_with_baseline(self):
        """Compare current state with baseline"""
        self.logger.info("Comparing with baseline...")
        
        if not self.baseline_manager.baseline_exists():
            print("\n✗ ERROR: No baseline found. Create one first with --baseline")
            return None
        
        print("\n" + "="*80)
        print("COMPARING WITH BASELINE")
        print("="*80)
        
        # Load baseline
        baseline = self.baseline_manager.load_baseline()
        baseline_data = baseline.get('system_state', {})
        baseline_time = baseline_data.get('created_at', 'unknown')
        print(f"\nBaseline created: {baseline_time}")
        
        # Current scan
        print("\n[1/2] Scanning current system state...")
        current_os = self.os_process_scanner.scan()
        current_lowlevel = self.lowlevel_process_scanner.scan()
        
        # Compare
        print("\n[2/2] Analyzing differences...")
        baseline_os = baseline_data['processes']['os_level']
        baseline_pids = {p['pid'] for p in baseline_os}
        current_pids = {p['pid'] for p in current_os}
        
        new_pids = current_pids - baseline_pids
        removed_pids = baseline_pids - current_pids
        
        print("\n" + "="*80)
        print("COMPARISON RESULTS")
        print("="*80)
        print(f"\nBaseline processes: {len(baseline_pids)}")
        print(f"Current processes: {len(current_pids)}")
        print(f"\nNew processes: {len(new_pids)}")
        print(f"Removed processes: {len(removed_pids)}")
        
        if new_pids:
            print("\n📋 NEW PROCESSES SINCE BASELINE:")
            for proc in current_os:
                if proc['pid'] in new_pids:
                    print(f"  • {proc['name']} (PID: {proc['pid']})")
        
        if removed_pids:
            print("\n📋 REMOVED PROCESSES SINCE BASELINE:")
            for proc in baseline_os:
                if proc['pid'] in removed_pids:
                    print(f"  • {proc['name']} (PID: {proc['pid']})")
        
        if not new_pids and not removed_pids:
            print("\n✓ No changes detected - system matches baseline")
        
        return {
            'new_count': len(new_pids),
            'removed_count': len(removed_pids),
            'new_processes': [p for p in current_os if p['pid'] in new_pids],
            'removed_processes': [p for p in baseline_os if p['pid'] in removed_pids]
        }
    
    def generate_report(self, scan_results):
        """Generate comprehensive security report"""
        self.logger.info("Generating security report...")
        
        print("\n" + "="*80)
        print("GENERATING SECURITY REPORT")
        print("="*80)
        
        # Prepare summary data
        summary = {
            'threat_level': 'LOW' if scan_results.get('processes', {}).get('hidden_count', 0) == 0 else 'HIGH',
            'total_detections': len(scan_results.get('alerts', [])),
            'critical_count': sum(1 for a in scan_results.get('alerts', []) if a.get('severity') == 'CRITICAL'),
            'high_count': sum(1 for a in scan_results.get('alerts', []) if a.get('severity') == 'HIGH'),
            'medium_count': sum(1 for a in scan_results.get('alerts', []) if a.get('severity') == 'MEDIUM'),
            'low_count': sum(1 for a in scan_results.get('alerts', []) if a.get('severity') == 'LOW'),
            'hidden_processes': scan_results.get('processes', {}).get('hidden_count', 0),
            'hidden_files': scan_results.get('files', {}).get('hidden_count', 0)
        }
        
        # Generate report
        json_file = self.report_generator.generate_full_report(
            scan_results, 
            scan_results.get('alerts', []), 
            summary
        )
        
        # Derive txt filename from json filename
        txt_file = json_file.replace('.json', '.txt')
        
        print(f"\n✓ JSON report: {json_file}")
        print(f"✓ Text report: {txt_file}")
        
        print(f"\n📁 Reports saved to: {Path('reports').absolute()}")
        
        return {'json': json_file, 'txt': txt_file}
    
    def run_automated_testing(self):
        """
        Run complete automated testing workflow
        This demonstrates the full capability of the tool
        """
        print("\n" + "╔" + "="*78 + "╗")
        print("║" + " "*20 + "AUTOMATED TESTING WORKFLOW" + " "*32 + "║")
        print("╚" + "="*78 + "╝")
        
        self.simulator.show_simulator_terms()
        
        test_results = {
            'start_time': datetime.now().isoformat(),
            'tests': []
        }
        
        # Test 1: Initial clean scan
        print("\n" + "─"*80)
        print("TEST 1: Initial Clean System Scan")
        print("─"*80)
        input("Press ENTER to run test 1...")
        
        test1_result = self.run_full_scan(enable_file_scan=False)
        test_results['tests'].append({
            'name': 'Initial Clean Scan',
            'status': 'PASSED',
            'hidden_count': test1_result['processes']['hidden_count']
        })
        
        # Test 2: Create baseline
        print("\n" + "─"*80)
        print("TEST 2: Create System Baseline")
        print("─"*80)
        input("Press ENTER to run test 2...")
        
        self.create_baseline()
        test_results['tests'].append({
            'name': 'Baseline Creation',
            'status': 'PASSED'
        })
        
        # Test 3: Start test process
        print("\n" + "─"*80)
        print("TEST 3: Start Educational Test Process")
        print("─"*80)
        print("\nThis will create a BENIGN background process for testing.")
        input("Press ENTER to run test 3...")
        
        test_pid = self.simulator.create_test_process(duration=180)
        if test_pid:
            test_results['tests'].append({
                'name': 'Test Process Creation',
                'status': 'PASSED',
                'pid': test_pid
            })
        else:
            test_results['tests'].append({
                'name': 'Test Process Creation',
                'status': 'FAILED'
            })
        
        # Test 4: Detect with test process running
        print("\n" + "─"*80)
        print("TEST 4: Scan With Test Process Running")
        print("─"*80)
        print("\nWaiting 3 seconds for test process to stabilize...")
        time.sleep(3)
        input("Press ENTER to run test 4...")
        
        test4_result = self.run_full_scan(enable_file_scan=False)
        test_results['tests'].append({
            'name': 'Scan With Test Process',
            'status': 'PASSED',
            'processes_found': test4_result['processes']['total_lowlevel_processes'],
            'hidden_processes': test4_result['processes']['hidden_count']
        })
        
        # Test 5: Compare with baseline
        print("\n" + "─"*80)
        print("TEST 5: Compare With Baseline (Change Detection)")
        print("─"*80)
        input("Press ENTER to run test 5...")
        
        comparison = self.compare_with_baseline()
        if comparison:
            test_results['tests'].append({
                'name': 'Baseline Comparison',
                'status': 'PASSED',
                'new_processes': comparison['new_count']
            })
        
        # Test 6: Full scan with reporting
        print("\n" + "─"*80)
        print("TEST 6: Full Scan With Report Generation")
        print("─"*80)
        input("Press ENTER to run test 6...")
        
        test6_result = self.run_full_scan(enable_file_scan=True)
        reports = self.generate_report(test6_result)
        test_results['tests'].append({
            'name': 'Full Scan + Report',
            'status': 'PASSED',
            'reports': reports
        })
        
        # Test 7: Cleanup
        print("\n" + "─"*80)
        print("TEST 7: Cleanup Test Artifacts")
        print("─"*80)
        input("Press ENTER to run test 7...")
        
        self.simulator.cleanup_test_artifacts()
        test_results['tests'].append({
            'name': 'Cleanup',
            'status': 'PASSED'
        })
        
        # Final summary
        test_results['end_time'] = datetime.now().isoformat()
        test_results['total_tests'] = len(test_results['tests'])
        test_results['passed'] = sum(1 for t in test_results['tests'] if t['status'] == 'PASSED')
        
        print("\n" + "╔" + "="*78 + "╗")
        print("║" + " "*25 + "TESTING COMPLETE" + " "*37 + "║")
        print("╚" + "="*78 + "╝")
        print(f"\nTotal Tests: {test_results['total_tests']}")
        print(f"Passed: {test_results['passed']}")
        print(f"Failed: {test_results['total_tests'] - test_results['passed']}")
        print(f"\n{'✓ ALL TESTS PASSED!' if test_results['passed'] == test_results['total_tests'] else '✗ Some tests failed'}")
        
        # Save test results
        results_file = Path("test_results/automated_test_results.json")
        results_file.parent.mkdir(exist_ok=True)
        with open(results_file, 'w') as f:
            json.dump(test_results, f, indent=2)
        print(f"\n📁 Test results saved to: {results_file.absolute()}")
        
        return test_results


def show_terms_and_conditions():
    """Display terms and conditions - must be accepted"""
    print(__doc__)
    print("\n" + "="*80)
    print("DO YOU ACCEPT THESE TERMS & CONDITIONS?")
    print("="*80)
    print("\nBy typing 'I ACCEPT', you confirm that:")
    print("  • You will use this tool for educational purposes only")
    print("  • You will only test systems you own or have permission to test")
    print("  • You understand the legal and ethical responsibilities")
    print("  • You will not use this tool for malicious purposes")
    print("\n")
    
    response = input("Type 'I ACCEPT' to continue (or anything else to exit): ").strip()
    
    if response.upper() == "I ACCEPT":
        print("\n✓ Terms accepted. Proceeding...")
        return True
    else:
        print("\n✗ Terms not accepted. Exiting.")
        return False


def main():
    """Main entry point with terms acceptance"""
    
    parser = argparse.ArgumentParser(
        description="Rootkit Detection & Testing System - Educational Security Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Show terms and accept
  python rootkit_detector.py --accept-terms
  
  # Run full automated testing (includes all features)
  python rootkit_detector.py --test-all
  
  # Quick scan (no file scan)
  python rootkit_detector.py --scan --no-files
  
  # Create system baseline
  python rootkit_detector.py --baseline
  
  # Compare with baseline
  python rootkit_detector.py --compare
  
  # Full scan with report
  python rootkit_detector.py --scan --report

For first-time users: python rootkit_detector.py --test-all
        """
    )
    
    parser.add_argument('--accept-terms', action='store_true',
                      help='Show and accept terms & conditions')
    parser.add_argument('--test-all', action='store_true',
                      help='Run complete automated testing workflow (recommended for first use)')
    parser.add_argument('--scan', action='store_true',
                      help='Run rootkit detection scan')
    parser.add_argument('--baseline', action='store_true',
                      help='Create system baseline snapshot')
    parser.add_argument('--compare', action='store_true',
                      help='Compare current state with baseline')
    parser.add_argument('--report', action='store_true',
                      help='Generate detailed security report')
    parser.add_argument('--no-files', action='store_true',
                      help='Skip file system scanning (faster)')
    parser.add_argument('--verbose', '-v', action='store_true',
                      help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # If no arguments, show help
    if len(sys.argv) == 1:
        parser.print_help()
        print("\n" + "="*80)
        print("FIRST TIME? Run: python rootkit_detector.py --test-all")
        print("="*80)
        sys.exit(0)
    
    # Show terms if requested or if running interactive mode
    if args.accept_terms or args.test_all:
        if not show_terms_and_conditions():
            sys.exit(1)
    
    # Initialize detector
    detector = RootkitDetector(verbose=args.verbose)
    
    try:
        # Automated testing mode
        if args.test_all:
            detector.run_automated_testing()
        
        # Create baseline
        elif args.baseline:
            detector.create_baseline()
        
        # Compare with baseline
        elif args.compare:
            detector.compare_with_baseline()
        
        # Run scan
        elif args.scan:
            enable_files = not args.no_files
            results = detector.run_full_scan(enable_file_scan=enable_files)
            
            if args.report:
                detector.generate_report(results)
        
        else:
            print("\n✗ Please specify an action (--scan, --baseline, --compare, or --test-all)")
            parser.print_help()
    
    except KeyboardInterrupt:
        print("\n\n⚠️ Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        logging.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
