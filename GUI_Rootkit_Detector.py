"""
GUI Rootkit Detection Tool
Professional graphical interface for rootkit detection and testing
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import json
from pathlib import Path
from datetime import datetime
import sys
import os

# Add current directory to path to import rootkit_detector
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rootkit_detector import RootkitDetector


class RootkitDetectorGUI:
    """Professional GUI for Rootkit Detection System"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🛡️ Rootkit Detection System - Professional Edition")
        self.root.geometry("1000x700")
        self.root.configure(bg="#1e1e1e")
        
        # Force window to front and center
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after_idle(self.root.attributes, '-topmost', False)
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1000 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f'1000x700+{x}+{y}')
        
        # Initialize detector
        self.detector = None
        self.scanning = False
        
        # Color scheme
        self.colors = {
            'bg': '#1e1e1e',
            'fg': '#ffffff',
            'accent': '#007acc',
            'success': '#4ec9b0',
            'warning': '#ce9178',
            'danger': '#f48771',
            'button': '#0e639c',
            'button_hover': '#1177bb'
        }
        
        # Setup GUI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        
        # Title Bar
        title_frame = tk.Frame(self.root, bg=self.colors['accent'], height=60)
        title_frame.pack(fill=tk.X, side=tk.TOP)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="🛡️ ROOTKIT DETECTION SYSTEM",
            font=("Segoe UI", 20, "bold"),
            bg=self.colors['accent'],
            fg=self.colors['fg']
        )
        title_label.pack(pady=15)
        
        # Main Container
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left Panel - Controls
        self.setup_control_panel(main_container)
        
        # Right Panel - Output
        self.setup_output_panel(main_container)
        
        # Bottom Status Bar
        self.setup_status_bar()
        
    def setup_control_panel(self, parent):
        """Setup the control panel with buttons"""
        control_frame = tk.Frame(parent, bg=self.colors['bg'], width=280)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        control_frame.pack_propagate(False)
        
        # System Status Card
        status_card = tk.LabelFrame(
            control_frame,
            text="📊 SYSTEM STATUS",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['success'],
            bd=2,
            relief=tk.GROOVE
        )
        status_card.pack(fill=tk.X, pady=(0, 15))
        
        # Status indicators
        self.status_labels = {}
        status_items = [
            ("Processes:", "---"),
            ("Hidden:", "---"),
            ("Files Scanned:", "---"),
            ("Threat Level:", "---")
        ]
        
        for label, value in status_items:
            frame = tk.Frame(status_card, bg=self.colors['bg'])
            frame.pack(fill=tk.X, padx=10, pady=5)
            
            tk.Label(
                frame,
                text=label,
                font=("Segoe UI", 9),
                bg=self.colors['bg'],
                fg=self.colors['fg'],
                anchor='w'
            ).pack(side=tk.LEFT)
            
            value_label = tk.Label(
                frame,
                text=value,
                font=("Segoe UI", 9, "bold"),
                bg=self.colors['bg'],
                fg=self.colors['success'],
                anchor='e'
            )
            value_label.pack(side=tk.RIGHT)
            self.status_labels[label] = value_label
        
        # Action Buttons Card
        actions_card = tk.LabelFrame(
            control_frame,
            text="🎯 ACTIONS",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['accent'],
            bd=2,
            relief=tk.GROOVE
        )
        actions_card.pack(fill=tk.X, pady=(0, 15))
        
        # Buttons
        buttons = [
            ("🚀 Quick Scan", self.quick_scan, self.colors['success']),
            ("🔍 Full Scan", self.full_scan, self.colors['accent']),
            ("📸 Create Baseline", self.create_baseline, self.colors['warning']),
            ("🔄 Compare Baseline", self.compare_baseline, self.colors['button']),
            ("🧪 Run All Tests", self.run_all_tests, self.colors['button']),
            ("📄 Generate Report", self.generate_report, self.colors['button']),
        ]
        
        self.button_widgets = {}
        for text, command, color in buttons:
            btn = tk.Button(
                actions_card,
                text=text,
                command=command,
                font=("Segoe UI", 10, "bold"),
                bg=color,
                fg=self.colors['fg'],
                activebackground=self.colors['button_hover'],
                activeforeground=self.colors['fg'],
                relief=tk.FLAT,
                cursor="hand2",
                height=2
            )
            btn.pack(fill=tk.X, padx=10, pady=5)
            self.button_widgets[text] = btn
            
            # Hover effects
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.colors['button_hover']))
            btn.bind("<Leave>", lambda e, b=btn, c=color: b.configure(bg=c))
        
        # Progress Bar
        progress_card = tk.LabelFrame(
            control_frame,
            text="⏳ PROGRESS",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['accent'],
            bd=2,
            relief=tk.GROOVE
        )
        progress_card.pack(fill=tk.X, pady=(0, 15))
        
        self.progress = ttk.Progressbar(
            progress_card,
            mode='indeterminate',
            length=260
        )
        self.progress.pack(padx=10, pady=10)
        
        # Clear/Exit Buttons
        bottom_buttons = tk.Frame(control_frame, bg=self.colors['bg'])
        bottom_buttons.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        tk.Button(
            bottom_buttons,
            text="🗑️ Clear Output",
            command=self.clear_output,
            font=("Segoe UI", 9),
            bg="#444444",
            fg=self.colors['fg'],
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        tk.Button(
            bottom_buttons,
            text="❌ Exit",
            command=self.exit_app,
            font=("Segoe UI", 9),
            bg=self.colors['danger'],
            fg=self.colors['fg'],
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0))
    
    def setup_output_panel(self, parent):
        """Setup the output display panel"""
        output_frame = tk.Frame(parent, bg=self.colors['bg'])
        output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Output Header
        header = tk.Label(
            output_frame,
            text="📝 SCAN OUTPUT & RESULTS",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['accent'],
            anchor='w'
        )
        header.pack(fill=tk.X, pady=(0, 10))
        
        # Scrolled Text Output
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="#0d1117",
            fg="#c9d1d9",
            insertbackground=self.colors['fg'],
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for colored output
        self.output_text.tag_config("success", foreground="#4ec9b0")
        self.output_text.tag_config("warning", foreground="#ce9178")
        self.output_text.tag_config("error", foreground="#f48771")
        self.output_text.tag_config("info", foreground="#569cd6")
        self.output_text.tag_config("header", foreground="#dcdcaa", font=("Consolas", 10, "bold"))
        
        # Welcome message
        self.log_message("="*80, "header")
        self.log_message("🛡️  ROOTKIT DETECTION SYSTEM - PROFESSIONAL EDITION", "header")
        self.log_message("="*80, "header")
        self.log_message("\n✅ System initialized successfully!", "success")
        self.log_message("📌 Select an action from the left panel to begin\n", "info")
        self.log_message("="*80 + "\n", "header")
    
    def setup_status_bar(self):
        """Setup the status bar at the bottom"""
        status_bar = tk.Frame(self.root, bg=self.colors['accent'], height=30)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        status_bar.pack_propagate(False)
        
        self.status_text = tk.Label(
            status_bar,
            text="⚡ Ready",
            font=("Segoe UI", 9),
            bg=self.colors['accent'],
            fg=self.colors['fg'],
            anchor='w',
            padx=10
        )
        self.status_text.pack(side=tk.LEFT)
        
        time_label = tk.Label(
            status_bar,
            text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            font=("Segoe UI", 9),
            bg=self.colors['accent'],
            fg=self.colors['fg'],
            anchor='e',
            padx=10
        )
        time_label.pack(side=tk.RIGHT)
    
    def log_message(self, message, tag=""):
        """Add message to output with optional color tag"""
        self.output_text.insert(tk.END, message + "\n", tag)
        self.output_text.see(tk.END)
        self.root.update_idletasks()
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_text.config(text=f"⚡ {message}")
        self.root.update_idletasks()
    
    def update_system_status(self, processes=None, hidden=None, files=None, threat=None):
        """Update system status indicators"""
        if processes is not None:
            self.status_labels["Processes:"].config(text=str(processes))
        if hidden is not None:
            color = self.colors['success'] if hidden == 0 else self.colors['danger']
            self.status_labels["Hidden:"].config(text=str(hidden), fg=color)
        if files is not None:
            self.status_labels["Files Scanned:"].config(text=str(files))
        if threat is not None:
            color = {
                'LOW': self.colors['success'],
                'MEDIUM': self.colors['warning'],
                'HIGH': self.colors['danger'],
                'CRITICAL': self.colors['danger']
            }.get(threat, self.colors['fg'])
            self.status_labels["Threat Level:"].config(text=threat, fg=color)
    
    def disable_buttons(self):
        """Disable all action buttons during scan"""
        for btn in self.button_widgets.values():
            btn.config(state=tk.DISABLED)
        self.progress.start(10)
    
    def enable_buttons(self):
        """Enable all action buttons after scan"""
        for btn in self.button_widgets.values():
            btn.config(state=tk.NORMAL)
        self.progress.stop()
    
    def run_in_thread(self, func):
        """Run function in separate thread to prevent GUI freeze"""
        thread = threading.Thread(target=func, daemon=True)
        thread.start()
    
    def quick_scan(self):
        """Perform quick process scan"""
        self.run_in_thread(self._quick_scan)
    
    def _quick_scan(self):
        """Internal quick scan implementation"""
        self.disable_buttons()
        self.update_status("Running quick scan...")
        
        self.log_message("\n" + "="*80, "header")
        self.log_message("🚀 QUICK SCAN - Process Detection Only", "header")
        self.log_message("="*80, "header")
        
        try:
            # Initialize detector
            if not self.detector:
                self.detector = RootkitDetector()
            
            self.log_message("\n[1/2] Scanning processes...", "info")
            result = self.detector.run_full_scan(enable_file_scan=False)
            
            # Display results
            processes = result['processes']
            self.log_message("\n" + "="*80, "header")
            self.log_message("📊 SCAN RESULTS", "header")
            self.log_message("="*80, "header")
            
            self.log_message(f"\n⏱️  Duration: {result['duration']:.2f} seconds", "info")
            self.log_message(f"📦 Processes scanned: {processes['total_lowlevel_processes']}", "info")
            self.log_message(f"🔍 Hidden processes: {processes['hidden_count']}", 
                            "error" if processes['hidden_count'] > 0 else "success")
            
            # Update status display
            self.update_system_status(
                processes=processes['total_lowlevel_processes'],
                hidden=processes['hidden_count'],
                threat='LOW' if processes['hidden_count'] == 0 else 'HIGH'
            )
            
            if processes['hidden_count'] == 0:
                self.log_message("\n✅ CLEAN - No hidden processes detected!", "success")
            else:
                self.log_message(f"\n⚠️  WARNING - {processes['hidden_count']} hidden process(es) found!", "error")
            
            self.log_message("\n" + "="*80 + "\n", "header")
            self.update_status("Quick scan completed")
            
        except Exception as e:
            self.log_message(f"\n❌ ERROR: {str(e)}", "error")
            self.update_status("Scan failed")
        finally:
            self.enable_buttons()
    
    def full_scan(self):
        """Perform full system scan"""
        self.run_in_thread(self._full_scan)
    
    def _full_scan(self):
        """Internal full scan implementation"""
        self.disable_buttons()
        self.update_status("Running full scan...")
        
        self.log_message("\n" + "="*80, "header")
        self.log_message("🔍 FULL SYSTEM SCAN - Processes + Files", "header")
        self.log_message("="*80, "header")
        
        try:
            if not self.detector:
                self.detector = RootkitDetector()
            
            self.log_message("\n[1/2] Scanning processes...", "info")
            self.log_message("[2/2] Scanning file system...", "info")
            
            result = self.detector.run_full_scan(enable_file_scan=True)
            
            # Display results
            processes = result['processes']
            files = result.get('files', {})
            
            self.log_message("\n" + "="*80, "header")
            self.log_message("📊 FULL SCAN RESULTS", "header")
            self.log_message("="*80, "header")
            
            self.log_message(f"\n⏱️  Duration: {result['duration']:.2f} seconds", "info")
            self.log_message(f"📦 Processes scanned: {processes['total_lowlevel_processes']}", "info")
            self.log_message(f"📁 Files scanned: {files.get('scanned_count', 0)}", "info")
            self.log_message(f"🔍 Hidden processes: {processes['hidden_count']}", 
                            "error" if processes['hidden_count'] > 0 else "success")
            self.log_message(f"📄 Suspicious files: {files.get('suspicious_count', 0)}", "warning")
            
            # Update status
            self.update_system_status(
                processes=processes['total_lowlevel_processes'],
                hidden=processes['hidden_count'],
                files=files.get('scanned_count', 0),
                threat='LOW' if processes['hidden_count'] == 0 else 'HIGH'
            )
            
            if processes['hidden_count'] == 0:
                self.log_message("\n✅ SYSTEM CLEAN - No threats detected!", "success")
            else:
                self.log_message(f"\n⚠️  THREATS DETECTED - {processes['hidden_count']} hidden items!", "error")
            
            self.log_message("\n" + "="*80 + "\n", "header")
            self.update_status("Full scan completed")
            
        except Exception as e:
            self.log_message(f"\n❌ ERROR: {str(e)}", "error")
            self.update_status("Scan failed")
        finally:
            self.enable_buttons()
    
    def create_baseline(self):
        """Create system baseline"""
        self.run_in_thread(self._create_baseline)
    
    def _create_baseline(self):
        """Internal baseline creation"""
        self.disable_buttons()
        self.update_status("Creating baseline...")
        
        self.log_message("\n" + "="*80, "header")
        self.log_message("📸 CREATING SYSTEM BASELINE", "header")
        self.log_message("="*80, "header")
        
        try:
            if not self.detector:
                self.detector = RootkitDetector()
            
            self.log_message("\n[1/2] Scanning processes...", "info")
            self.log_message("[2/2] Scanning files...", "info")
            
            self.detector.create_baseline()
            
            self.log_message("\n✅ Baseline created successfully!", "success")
            self.log_message("📁 Saved to: baseline.json", "info")
            self.log_message("\nYou can now use 'Compare Baseline' to detect changes.", "info")
            self.log_message("\n" + "="*80 + "\n", "header")
            self.update_status("Baseline created")
            
        except Exception as e:
            self.log_message(f"\n❌ ERROR: {str(e)}", "error")
            self.update_status("Baseline creation failed")
        finally:
            self.enable_buttons()
    
    def compare_baseline(self):
        """Compare current system with baseline"""
        self.run_in_thread(self._compare_baseline)
    
    def _compare_baseline(self):
        """Internal baseline comparison"""
        self.disable_buttons()
        self.update_status("Comparing with baseline...")
        
        self.log_message("\n" + "="*80, "header")
        self.log_message("🔄 COMPARING WITH BASELINE", "header")
        self.log_message("="*80, "header")
        
        try:
            if not self.detector:
                self.detector = RootkitDetector()
            
            if not Path("baseline.json").exists():
                self.log_message("\n❌ No baseline found. Create one first!", "error")
                self.update_status("No baseline found")
                return
            
            self.log_message("\n[1/2] Loading baseline...", "info")
            self.log_message("[2/2] Scanning current system...", "info")
            
            result = self.detector.compare_with_baseline()
            
            if result:
                self.log_message("\n✅ Comparison completed!", "success")
                self.log_message("\nCheck the output above for detailed changes.", "info")
            else:
                self.log_message("\n⚠️  Comparison completed with warnings", "warning")
            
            self.log_message("\n" + "="*80 + "\n", "header")
            self.update_status("Baseline comparison completed")
            
        except Exception as e:
            self.log_message(f"\n❌ ERROR: {str(e)}", "error")
            self.update_status("Comparison failed")
        finally:
            self.enable_buttons()
    
    def run_all_tests(self):
        """Run complete automated testing"""
        response = messagebox.askyesno(
            "Run All Tests",
            "This will run all 7 automated tests.\nThis may take 5-10 minutes.\n\nContinue?"
        )
        if response:
            self.run_in_thread(self._run_all_tests)
    
    def _run_all_tests(self):
        """Internal test runner"""
        self.disable_buttons()
        self.update_status("Running automated tests...")
        
        self.log_message("\n" + "="*80, "header")
        self.log_message("🧪 AUTOMATED TESTING WORKFLOW", "header")
        self.log_message("="*80, "header")
        
        try:
            if not self.detector:
                self.detector = RootkitDetector()
            
            self.log_message("\n⚠️  Running complete test suite...", "warning")
            self.log_message("This may take several minutes.\n", "info")
            
            # Note: run_automated_testing requires user input, so show message
            self.log_message("❌ Automated testing requires terminal interaction.", "error")
            self.log_message("Please run: python rootkit_detector.py --test-all", "info")
            
            self.log_message("\n" + "="*80 + "\n", "header")
            self.update_status("Tests require terminal mode")
            
        except Exception as e:
            self.log_message(f"\n❌ ERROR: {str(e)}", "error")
            self.update_status("Tests failed")
        finally:
            self.enable_buttons()
    
    def generate_report(self):
        """Generate security report"""
        self.run_in_thread(self._generate_report)
    
    def _generate_report(self):
        """Internal report generation"""
        self.disable_buttons()
        self.update_status("Generating report...")
        
        self.log_message("\n" + "="*80, "header")
        self.log_message("📄 GENERATING SECURITY REPORT", "header")
        self.log_message("="*80, "header")
        
        try:
            if not self.detector:
                self.detector = RootkitDetector()
            
            self.log_message("\n[1/2] Scanning system...", "info")
            result = self.detector.run_full_scan(enable_file_scan=True)
            
            self.log_message("[2/2] Generating reports...", "info")
            reports = self.detector.generate_report(result)
            
            self.log_message("\n✅ Reports generated successfully!", "success")
            self.log_message(f"\n📄 JSON: {reports['json']}", "info")
            self.log_message(f"📄 TXT:  {reports['txt']}", "info")
            self.log_message("\n" + "="*80 + "\n", "header")
            self.update_status("Reports generated")
            
        except Exception as e:
            self.log_message(f"\n❌ ERROR: {str(e)}", "error")
            self.update_status("Report generation failed")
        finally:
            self.enable_buttons()
    
    def clear_output(self):
        """Clear the output display"""
        self.output_text.delete(1.0, tk.END)
        self.log_message("="*80, "header")
        self.log_message("🛡️  OUTPUT CLEARED", "header")
        self.log_message("="*80 + "\n", "header")
        self.update_status("Output cleared")
    
    def exit_app(self):
        """Exit the application"""
        response = messagebox.askyesno("Exit", "Are you sure you want to exit?")
        if response:
            self.root.quit()


def show_terms_and_conditions():
    """Show terms and conditions dialog before starting GUI"""
    print("\n" + "="*60)
    print("📋 SHOWING TERMS & CONDITIONS DIALOG...")
    print("="*60)
    
    # Create root window
    root = tk.Tk()
    root.title("⚖️ Educational Terms & Conditions")
    root.geometry("750x650")
    root.configure(bg="#1e1e1e")
    
    # Center the window
    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (750 // 2)
    y = (screen_height // 2) - (650 // 2)
    root.geometry(f'750x650+{x}+{y}')
    
    # Force to front
    root.lift()
    root.attributes('-topmost', True)
    root.after(100, lambda: root.attributes('-topmost', False))
    root.focus_force()
    
    print("✅ Terms window created and positioned")
    print("📌 LOOK FOR THE WINDOW - It should be visible now!")
    print("📌 Orange/Red header with white text")
    print("📌 Two buttons: GREEN (Accept) and RED (Decline)\n")
    
    # Result variable
    accepted = [False]
    
    # Header with warning color
    header = tk.Frame(root, bg="#d83b01", height=70)
    header.pack(fill=tk.X)
    header.pack_propagate(False)
    
    tk.Label(
        header,
        text="⚠️ EDUCATIONAL USE ONLY",
        font=("Segoe UI", 18, "bold"),
        bg="#d83b01",
        fg="#ffffff"
    ).pack(pady=5)
    
    tk.Label(
        header,
        text="Read Terms & Conditions Before Use",
        font=("Segoe UI", 11),
        bg="#d83b01",
        fg="#ffffff"
    ).pack()
    
    # Main frame
    main_frame = tk.Frame(root, bg="#1e1e1e")
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Terms text area
    terms_text = scrolledtext.ScrolledText(
        main_frame,
        wrap=tk.WORD,
        font=("Consolas", 10),
        bg="#2d2d30",
        fg="#ffffff",
        relief=tk.SOLID,
        bd=2,
        padx=15,
        pady=15
    )
    terms_text.pack(fill=tk.BOTH, expand=True)
    
    # Simplified terms content
    terms_content = """
╔══════════════════════════════════════════════════════════════════════╗
║                    EDUCATIONAL USE ONLY                              ║
║                     LEGAL DISCLAIMER                                 ║
╚══════════════════════════════════════════════════════════════════════╝

BY USING THIS SOFTWARE, YOU AGREE TO ALL TERMS BELOW:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. EDUCATIONAL PURPOSE ONLY
   ✓ This tool is for learning cybersecurity concepts ONLY
   ✓ NOT for hacking, attacking, or unauthorized access
   ✓ Designed to demonstrate defensive security techniques

2. AUTHORIZED USE ONLY
   ✓ Use ONLY on systems you own
   ✓ Use ONLY on systems where you have written permission
   ✗ Unauthorized use is ILLEGAL and PROHIBITED

3. LEGAL COMPLIANCE
   ⚖️  Laws you must follow:
   • Computer Fraud and Abuse Act (CFAA) - USA
   • Computer Misuse Act - United Kingdom  
   • Similar laws worldwide
   
   ⚠️  Violations will be prosecuted!

4. DISCLAIMER OF LIABILITY - IMPORTANT!

   ⚠️  IF YOU MISUSE THIS TOOL:
   
   ✗ The AUTHOR is NOT responsible
   ✗ The CREATOR is NOT liable  
   ✗ YOU accept ALL responsibility
   ✗ YOU face ALL legal consequences
   ✗ YOU cannot hold the author liable

5. NO WARRANTY
   • Software provided "AS IS"
   • No guarantees of any kind
   • Author not liable for damages
   • User assumes all risk

6. YOU ACKNOWLEDGE THAT:
   ✓ This is a defensive security tool (detection only)
   ✓ It does NOT create malware or attacks
   ✓ You understand cybersecurity ethics
   ✓ You will follow all applicable laws
   ✓ You accept full responsibility

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  CRITICAL: THE AUTHOR IS NOT RESPONSIBLE FOR YOUR ACTIONS!

If you misuse this tool, YOU (not the author) are legally liable.

By clicking "I ACCEPT", you confirm:
• You will use this for educational purposes only
• You will only test your own systems or authorized systems
• You understand and accept full legal responsibility
• The author is not liable for your misuse

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    terms_text.insert(1.0, terms_content)
    terms_text.config(state=tk.DISABLED)
    
    # Warning message
    warning = tk.Label(
        main_frame,
        text="⚠️ You MUST accept these terms to use this software",
        font=("Segoe UI", 11, "bold"),
        bg="#1e1e1e",
        fg="#ce9178",
        pady=10
    )
    warning.pack()
    
    # Buttons frame
    button_frame = tk.Frame(root, bg="#1e1e1e")
    button_frame.pack(fill=tk.X, padx=20, pady=20)
    
    def on_accept():
        print("\n✅ USER ACCEPTED TERMS")
        accepted[0] = True
        root.quit()
        root.destroy()
    
    def on_decline():
        print("\n❌ USER DECLINED TERMS")
        accepted[0] = False
        root.quit()
        root.destroy()
    
    # Accept button (GREEN)
    accept_btn = tk.Button(
        button_frame,
        text="✓ I ACCEPT\nI will use this for educational purposes only",
        command=on_accept,
        font=("Segoe UI", 12, "bold"),
        bg="#4ec9b0",
        fg="#000000",
        activebackground="#6ed9c0",
        relief=tk.RAISED,
        bd=3,
        cursor="hand2",
        height=3,
        width=30
    )
    accept_btn.pack(side=tk.LEFT, expand=True, padx=5)
    
    # Decline button (RED)
    decline_btn = tk.Button(
        button_frame,
        text="✗ I DECLINE\nExit Application",
        command=on_decline,
        font=("Segoe UI", 12, "bold"),
        bg="#f48771",
        fg="#000000",
        activebackground="#ff9781",
        relief=tk.RAISED,
        bd=3,
        cursor="hand2",
        height=3,
        width=30
    )
    decline_btn.pack(side=tk.RIGHT, expand=True, padx=5)
    
    # Handle window close
    root.protocol("WM_DELETE_WINDOW", on_decline)
    
    print("⏳ Waiting for user response...")
    print("   (Click 'I ACCEPT' to continue)\n")
    
    # Run the dialog
    root.mainloop()
    
    print(f"📊 Result: {'ACCEPTED' if accepted[0] else 'DECLINED'}\n")
    
    return accepted[0]


def main():
    """Main entry point"""
    try:
        print("="*60)
        print("🛡️  ROOTKIT DETECTION SYSTEM - GUI STARTING...")
        print("="*60)
        print("\n[1/2] Loading Terms & Conditions...")
        
        # Show terms and conditions first
        if not show_terms_and_conditions():
            # User declined - show exit message and quit
            print("\n❌ Terms declined. Exiting...")
            root = tk.Tk()
            root.withdraw()
            messagebox.showinfo(
                "Application Closed",
                "You must accept the terms and conditions to use this software.\n\n"
                "Application will now exit."
            )
            root.destroy()
            return
        
        print("\n[2/2] Starting main GUI...")
        print("✅ Terms accepted. Launching application...\n")
        
        # User accepted - start main GUI
        root = tk.Tk()
        app = RootkitDetectorGUI(root)
        
        print("✅ GUI window created successfully!")
        print("📌 If you don't see the window, check your taskbar.\n")
        
        root.mainloop()
        
        print("\n✅ Application closed normally.")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nPress Enter to exit...")
        input()


if __name__ == "__main__":
    main()
