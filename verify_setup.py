"""
Setup Verification Script
Checks if all dependencies and prerequisites are correctly installed
"""

import sys
import subprocess
from pathlib import Path


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def print_status(check_name, status, details=""):
    """Print check status"""
    symbol = "✅" if status else "❌"
    print(f"{symbol} {check_name:<40} {details}")


def check_python_version():
    """Check Python version"""
    version = sys.version_info
    is_ok = version.major == 3 and version.minor >= 8
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    print_status("Python Version", is_ok, f"v{version_str}")
    return is_ok


def check_admin_rights():
    """Check for administrator privileges"""
    try:
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        print_status("Administrator Rights", is_admin, 
                    "Running as Admin" if is_admin else "Not Admin")
        if not is_admin:
            print("   ⚠️  Warning: Some features may not work without admin rights")
        return True  # Not critical
    except:
        print_status("Administrator Rights", False, "Check failed")
        return False


def check_module(module_name, import_name=None):
    """Check if a Python module is installed"""
    if import_name is None:
        import_name = module_name
    
    try:
        __import__(import_name)
        print_status(f"Module: {module_name}", True, "Installed")
        return True
    except ImportError:
        print_status(f"Module: {module_name}", False, "Not installed")
        return False


def check_directories():
    """Check if required directories exist"""
    dirs_to_check = ['scanners', 'engine', 'utils']
    all_ok = True
    
    for dir_name in dirs_to_check:
        exists = Path(dir_name).exists()
        print_status(f"Directory: {dir_name}", exists)
        all_ok = all_ok and exists
    
    return all_ok


def check_files():
    """Check if main files exist"""
    files_to_check = [
        'main.py',
        'requirements.txt',
        'README.md',
        'TESTING.md',
        'ROOTKIT_EXPLAINED.md'
    ]
    all_ok = True
    
    for file_name in files_to_check:
        exists = Path(file_name).exists()
        print_status(f"File: {file_name}", exists)
        all_ok = all_ok and exists
    
    return all_ok


def main():
    """Main verification function"""
    print_header("ROOTKIT DETECTION SYSTEM - SETUP VERIFICATION")
    
    print("\n🔍 Checking Prerequisites...")
    
    # Track overall status
    checks = []
    
    # Python version
    print_header("Python Environment")
    checks.append(check_python_version())
    
    # Administrator rights
    print_header("System Permissions")
    check_admin_rights()
    
    # Required modules
    print_header("Required Python Packages")
    checks.append(check_module("psutil"))
    checks.append(check_module("win32api", "win32api"))
    checks.append(check_module("wmi"))
    checks.append(check_module("colorama"))
    
    # Project structure
    print_header("Project Structure")
    checks.append(check_directories())
    checks.append(check_files())
    
    # Summary
    print_header("VERIFICATION SUMMARY")
    
    if all(checks):
        print("\n✅ ALL CHECKS PASSED!")
        print("   Your system is ready to run the Rootkit Detection System")
        print("\n📌 Next Steps:")
        print("   1. Review TERMS_AND_CONDITIONS.md")
        print("   2. Read QUICKSTART.md for usage instructions")
        print("   3. Run your first scan: python main.py --scan --no-files")
        print("\n")
        return True
    else:
        print("\n❌ SOME CHECKS FAILED")
        print("   Please install missing dependencies:")
        print("   pip install -r requirements.txt")
        print("\n")
        return False


if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Verification cancelled by user\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during verification: {e}\n")
        sys.exit(1)
