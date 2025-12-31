"""
Report Generator Module
Generates detailed security reports in various formats
"""

import json
import logging
from typing import Dict, List
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class ReportGenerator:
    """
    Generates detailed security reports
    Supports JSON and text formats
    """
    
    def __init__(self, output_dir: str = 'reports'):
        """
        Initialize report generator
        
        Args:
            output_dir: Directory to save reports
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def generate_full_report(self, scan_results: Dict, 
                           detections: List[Dict],
                           summary: Dict) -> str:
        """
        Generate comprehensive security report
        
        Args:
            scan_results: Raw scan results
            detections: List of all detections
            summary: Detection summary
            
        Returns:
            Path to generated report file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        report_data = {
            'report_info': {
                'generated': datetime.now().isoformat(),
                'report_version': '1.0',
                'tool': 'Rootkit Detection System'
            },
            'scan_results': scan_results,
            'detections': detections,
            'summary': summary
        }
        
        # Generate JSON report
        json_file = self.output_dir / f'security_report_{timestamp}.json'
        try:
            with open(json_file, 'w') as f:
                json.dump(report_data, f, indent=4)
            logger.info(f"JSON report generated: {json_file}")
        except Exception as e:
            logger.error(f"Failed to generate JSON report: {e}")
        
        # Generate text report
        txt_file = self.output_dir / f'security_report_{timestamp}.txt'
        try:
            with open(txt_file, 'w') as f:
                self._write_text_report(f, report_data)
            logger.info(f"Text report generated: {txt_file}")
        except Exception as e:
            logger.error(f"Failed to generate text report: {e}")
        
        return str(json_file)
    
    def _write_text_report(self, file, report_data: Dict):
        """Write formatted text report"""
        file.write("=" * 80 + "\n")
        file.write("  ROOTKIT DETECTION SYSTEM - SECURITY REPORT\n")
        file.write("=" * 80 + "\n\n")
        
        # Report info
        file.write(f"Generated: {report_data['report_info']['generated']}\n")
        file.write(f"Tool Version: {report_data['report_info']['report_version']}\n\n")
        
        # Summary
        summary = report_data.get('summary', {})
        file.write("-" * 80 + "\n")
        file.write("EXECUTIVE SUMMARY\n")
        file.write("-" * 80 + "\n")
        file.write(f"Threat Level: {summary.get('threat_level', 'UNKNOWN')}\n")
        file.write(f"Total Detections: {summary.get('total_detections', 0)}\n")
        file.write(f"  - Critical: {summary.get('critical_count', 0)}\n")
        file.write(f"  - High: {summary.get('high_count', 0)}\n")
        file.write(f"  - Medium: {summary.get('medium_count', 0)}\n")
        file.write(f"  - Low: {summary.get('low_count', 0)}\n\n")
        file.write(f"Hidden Processes: {summary.get('hidden_processes', 0)}\n")
        file.write(f"Hidden Files: {summary.get('hidden_files', 0)}\n\n")
        file.write(f"Recommendation: {summary.get('recommendation', 'N/A')}\n\n")
        
        # Detections
        detections = report_data.get('detections', [])
        if detections:
            file.write("-" * 80 + "\n")
            file.write("DETAILED FINDINGS\n")
            file.write("-" * 80 + "\n\n")
            
            for i, detection in enumerate(detections, 1):
                file.write(f"Finding #{i}\n")
                file.write(f"  Severity: {detection.get('severity')}\n")
                file.write(f"  Type: {detection.get('type')}\n")
                file.write(f"  Description: {detection.get('description')}\n")
                file.write(f"  Timestamp: {detection.get('timestamp')}\n")
                
                details = detection.get('details', {})
                if details:
                    file.write(f"  Details:\n")
                    for key, value in details.items():
                        file.write(f"    {key}: {value}\n")
                file.write("\n")
        
        # Scan statistics
        scan_results = report_data.get('scan_results', {})
        if scan_results:
            file.write("-" * 80 + "\n")
            file.write("SCAN STATISTICS\n")
            file.write("-" * 80 + "\n")
            
            if 'process_comparison' in scan_results:
                pc = scan_results['process_comparison']
                file.write(f"\nProcess Scan:\n")
                file.write(f"  Total OS Processes: {pc.get('total_os_processes', 0)}\n")
                file.write(f"  Total Low-Level Processes: {pc.get('total_lowlevel_processes', 0)}\n")
                file.write(f"  Hidden Count: {pc.get('hidden_count', 0)}\n")
            
            if 'file_comparison' in scan_results:
                fc = scan_results['file_comparison']
                file.write(f"\nFile Scan:\n")
                file.write(f"  Total OS Files: {fc.get('total_os_files', 0)}\n")
                file.write(f"  Total Low-Level Files: {fc.get('total_lowlevel_files', 0)}\n")
                file.write(f"  Hidden Count: {fc.get('hidden_count', 0)}\n")
        
        file.write("\n" + "=" * 80 + "\n")
        file.write("END OF REPORT\n")
        file.write("=" * 80 + "\n")
    
    def generate_quick_summary(self, summary: Dict) -> str:
        """
        Generate quick text summary
        
        Args:
            summary: Summary dictionary
            
        Returns:
            Summary text string
        """
        text = "\n" + "=" * 70 + "\n"
        text += "QUICK SUMMARY\n"
        text += "=" * 70 + "\n"
        text += f"Threat Level: {summary.get('threat_level', 'UNKNOWN')}\n"
        text += f"Total Detections: {summary.get('total_detections', 0)}\n"
        text += f"Critical: {summary.get('critical_count', 0)} | "
        text += f"High: {summary.get('high_count', 0)} | "
        text += f"Medium: {summary.get('medium_count', 0)} | "
        text += f"Low: {summary.get('low_count', 0)}\n"
        text += "=" * 70 + "\n"
        
        return text
