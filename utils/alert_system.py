"""
Alert System Module
Manages alerts and notifications for detected threats
"""

import logging
from typing import Dict, List
from datetime import datetime
from colorama import Fore, Back, Style, init

# Initialize colorama for colored console output
init(autoreset=True)

logger = logging.getLogger(__name__)


class AlertSystem:
    """
    Manages security alerts and notifications
    Displays warnings for detected rootkit indicators
    """
    
    def __init__(self):
        self.alerts = []
        self.alert_count = {
            'CRITICAL': 0,
            'HIGH': 0,
            'MEDIUM': 0,
            'LOW': 0
        }
        
    def create_alert(self, severity: str, alert_type: str, 
                    message: str, details: Dict = None) -> Dict:
        """
        Create a new security alert
        
        Args:
            severity: Alert severity (CRITICAL, HIGH, MEDIUM, LOW)
            alert_type: Type of alert (HIDDEN_PROCESS, HIDDEN_FILE, etc.)
            message: Alert message
            details: Additional details dictionary
            
        Returns:
            Created alert dictionary
        """
        alert = {
            'id': len(self.alerts) + 1,
            'severity': severity,
            'type': alert_type,
            'message': message,
            'details': details or {},
            'timestamp': datetime.now().isoformat(),
            'acknowledged': False
        }
        
        self.alerts.append(alert)
        self.alert_count[severity] += 1
        
        logger.warning(f"[{severity}] {alert_type}: {message}")
        return alert
    
    def display_alert(self, alert: Dict):
        """
        Display alert with color-coded severity
        
        Args:
            alert: Alert dictionary to display
        """
        severity = alert['severity']
        
        # Color coding based on severity
        if severity == 'CRITICAL':
            color = Fore.RED + Back.WHITE + Style.BRIGHT
            symbol = "🚨"
        elif severity == 'HIGH':
            color = Fore.RED + Style.BRIGHT
            symbol = "⚠️"
        elif severity == 'MEDIUM':
            color = Fore.YELLOW + Style.BRIGHT
            symbol = "⚡"
        else:
            color = Fore.CYAN
            symbol = "ℹ️"
        
        print(f"\n{color}{'=' * 70}")
        print(f"{symbol}  {severity} ALERT - {alert['type']}")
        print(f"{'=' * 70}{Style.RESET_ALL}")
        print(f"Message: {alert['message']}")
        print(f"Time: {alert['timestamp']}")
        
        if alert['details']:
            print(f"\nDetails:")
            for key, value in alert['details'].items():
                print(f"  {key}: {value}")
        
        print(f"{color}{'=' * 70}{Style.RESET_ALL}\n")
    
    def display_all_alerts(self):
        """Display all alerts in the system"""
        if not self.alerts:
            print(f"\n{Fore.GREEN}✓ No alerts - System appears clean{Style.RESET_ALL}\n")
            return
        
        print(f"\n{Style.BRIGHT}📋 SECURITY ALERTS SUMMARY{Style.RESET_ALL}")
        print(f"{'=' * 70}")
        print(f"Total Alerts: {len(self.alerts)}")
        print(f"  🚨 CRITICAL: {self.alert_count['CRITICAL']}")
        print(f"  ⚠️  HIGH: {self.alert_count['HIGH']}")
        print(f"  ⚡ MEDIUM: {self.alert_count['MEDIUM']}")
        print(f"  ℹ️  LOW: {self.alert_count['LOW']}")
        print(f"{'=' * 70}\n")
        
        for alert in self.alerts:
            self.display_alert(alert)
    
    def get_critical_alerts(self) -> List[Dict]:
        """Get all critical severity alerts"""
        return [a for a in self.alerts if a['severity'] == 'CRITICAL']
    
    def get_unacknowledged_alerts(self) -> List[Dict]:
        """Get all unacknowledged alerts"""
        return [a for a in self.alerts if not a['acknowledged']]
    
    def acknowledge_alert(self, alert_id: int) -> bool:
        """
        Mark an alert as acknowledged
        
        Args:
            alert_id: ID of alert to acknowledge
            
        Returns:
            True if successful, False otherwise
        """
        for alert in self.alerts:
            if alert['id'] == alert_id:
                alert['acknowledged'] = True
                logger.info(f"Alert {alert_id} acknowledged")
                return True
        return False
    
    def clear_alerts(self):
        """Clear all alerts"""
        self.alerts = []
        self.alert_count = {
            'CRITICAL': 0,
            'HIGH': 0,
            'MEDIUM': 0,
            'LOW': 0
        }
        logger.info("All alerts cleared")
    
    def display_banner(self):
        """Display application banner"""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}")
        print("=" * 70)
        print("  🔐 ROOTKIT DETECTION AND MONITORING SYSTEM")
        print("  Educational Security Tool - For Authorized Use Only")
        print("=" * 70)
        print(f"{Style.RESET_ALL}")
    
    def display_scan_start(self):
        """Display scan start message"""
        print(f"\n{Fore.YELLOW}🔍 Starting security scan...{Style.RESET_ALL}\n")
    
    def display_scan_complete(self, duration: float):
        """Display scan completion message"""
        print(f"\n{Fore.GREEN}✓ Scan completed in {duration:.2f} seconds{Style.RESET_ALL}\n")
    
    def display_summary(self, summary: Dict):
        """
        Display detection summary
        
        Args:
            summary: Summary dictionary from DetectionEngine
        """
        print(f"\n{Style.BRIGHT}📊 DETECTION SUMMARY{Style.RESET_ALL}")
        print(f"{'=' * 70}")
        print(f"Threat Level: {self._get_colored_threat_level(summary.get('threat_level', 'UNKNOWN'))}")
        print(f"Total Detections: {summary.get('total_detections', 0)}")
        print(f"  🚨 Critical: {summary.get('critical_count', 0)}")
        print(f"  ⚠️  High: {summary.get('high_count', 0)}")
        print(f"  ⚡ Medium: {summary.get('medium_count', 0)}")
        print(f"  ℹ️  Low: {summary.get('low_count', 0)}")
        print(f"\nHidden Processes: {summary.get('hidden_processes', 0)}")
        print(f"Hidden Files: {summary.get('hidden_files', 0)}")
        print(f"\nRecommendation: {summary.get('recommendation', 'N/A')}")
        print(f"{'=' * 70}\n")
    
    def _get_colored_threat_level(self, level: str) -> str:
        """Get colored threat level string"""
        if level == 'CRITICAL':
            return f"{Fore.RED}{Style.BRIGHT}{level}{Style.RESET_ALL}"
        elif level == 'HIGH':
            return f"{Fore.RED}{level}{Style.RESET_ALL}"
        elif level == 'MEDIUM':
            return f"{Fore.YELLOW}{level}{Style.RESET_ALL}"
        elif level == 'LOW':
            return f"{Fore.GREEN}{level}{Style.RESET_ALL}"
        else:
            return level
