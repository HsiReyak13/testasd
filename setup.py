#!/usr/bin/env python3
"""
Setup script for Sales Data Processing Script

This script handles the installation of dependencies and setup of the environment
for the sales data processing application.

Usage:
    python setup.py install    # Install dependencies
    python setup.py check      # Check if dependencies are installed
    python setup.py clean      # Clean up installation files
"""

import subprocess
import sys
import os
import importlib.util
from pathlib import Path


def run_pip_command(command, description):
    """
    Run a pip command with error handling.
    
    Args:
        command (list): Pip command as a list of arguments
        description (str): Description of what the command does
    
    Returns:
        bool: True if successful, False otherwise
    """
    print(f"📦 {description}...")
    try:
        result = subprocess.run(
            command, 
            capture_output=True, 
            text=True, 
            check=True
        )
        print(f"✓ {description} completed successfully")
        if result.stdout.strip():
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed")
        print(f"   Error: {e.stderr.strip() if e.stderr else str(e)}")
        return False
    except FileNotFoundError:
        print(f"✗ pip command not found. Please ensure Python and pip are installed.")
        return False


def check_python_version():
    """Check if Python version meets requirements."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} is supported")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} is not supported")
        print("   Please upgrade to Python 3.7 or higher")
        return False


def check_pip_installed():
    """Check if pip is available."""
    print("📦 Checking pip availability...")
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                              capture_output=True, text=True, check=True)
        print(f"✓ pip is available: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ pip is not available")
        print("   Please install pip: https://pip.pypa.io/en/stable/installation/")
        return False


def upgrade_pip():
    """Upgrade pip to the latest version."""
    command = [sys.executable, "-m", "pip", "install", "--upgrade", "pip"]
    return run_pip_command(command, "Upgrading pip")


def install_requirements():
    """Install packages from requirements.txt."""
    requirements_file = Path("requirements.txt")
    
    if not requirements_file.exists():
        print("✗ requirements.txt not found")
        return False
    
    command = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
    return run_pip_command(command, "Installing requirements from requirements.txt")


def install_optional_packages():
    """Install optional development packages."""
    optional_packages = [
        "pytest>=7.0.0",      # For testing
        "flake8>=5.0.0",       # For linting
        "black>=22.0.0",       # For code formatting
        "jupyter>=1.0.0",      # For data analysis notebooks
    ]
    
    print("\n🔧 Installing optional development packages...")
    success = True
    
    for package in optional_packages:
        command = [sys.executable, "-m", "pip", "install", package]
        if not run_pip_command(command, f"Installing {package.split('>=')[0]}"):
            success = False
    
    return success


def check_package_installed(package_name):
    """Check if a specific package is installed."""
    try:
        spec = importlib.util.find_spec(package_name)
        if spec is not None:
            # Try to import to ensure it's working
            module = importlib.import_module(package_name)
            version = getattr(module, '__version__', 'unknown')
            print(f"✓ {package_name} {version} is installed")
            return True
        else:
            print(f"✗ {package_name} is not installed")
            return False
    except ImportError as e:
        print(f"✗ {package_name} import failed: {e}")
        return False


def check_all_dependencies():
    """Check if all required dependencies are installed."""
    print("\n🔍 Checking installed dependencies...")
    
    required_packages = ['pandas']
    optional_packages = ['pytest', 'flake8', 'black', 'jupyter']
    
    all_required_installed = True
    for package in required_packages:
        if not check_package_installed(package):
            all_required_installed = False
    
    print("\n🔧 Optional packages:")
    for package in optional_packages:
        check_package_installed(package)
    
    return all_required_installed


def create_virtual_environment():
    """Create a virtual environment for the project."""
    venv_name = "sales_env"
    print(f"🏠 Creating virtual environment '{venv_name}'...")
    
    try:
        command = [sys.executable, "-m", "venv", venv_name]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(f"✓ Virtual environment '{venv_name}' created successfully")
        
        # Provide activation instructions
        if os.name == 'nt':  # Windows
            activate_cmd = f"{venv_name}\\Scripts\\activate"
        else:  # Unix-like
            activate_cmd = f"source {venv_name}/bin/activate"
        
        print(f"\n📋 To activate the virtual environment, run:")
        print(f"   {activate_cmd}")
        print(f"\n📋 Then install dependencies with:")
        print(f"   pip install -r requirements.txt")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to create virtual environment: {e}")
        return False


def clean_installation():
    """Clean up installation files and cache."""
    print("🧹 Cleaning up installation files...")
    
    # Clean pip cache
    command = [sys.executable, "-m", "pip", "cache", "purge"]
    run_pip_command(command, "Cleaning pip cache")
    
    # Remove __pycache__ directories
    for root, dirs, files in os.walk("."):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                cache_path = os.path.join(root, dir_name)
                try:
                    import shutil
                    shutil.rmtree(cache_path)
                    print(f"✓ Removed {cache_path}")
                except Exception as e:
                    print(f"✗ Failed to remove {cache_path}: {e}")
    
    print("✓ Cleanup completed")


def main():
    """Main setup function."""
    print("="*60)
    print("🚀 Sales Data Processing Script Setup")
    print("="*60)
    
    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  python setup.py install    # Install dependencies")
        print("  python setup.py check      # Check dependencies")
        print("  python setup.py venv       # Create virtual environment")
        print("  python setup.py dev        # Install with dev dependencies")
        print("  python setup.py clean      # Clean installation files")
        return 1
    
    command = sys.argv[1].lower()
    
    # Always check Python version and pip availability first
    if not check_python_version():
        return 1
    
    if command in ['install', 'dev', 'check']:
        if not check_pip_installed():
            return 1
    
    if command == 'install':
        print("\n🔧 Installing dependencies...")
        success = True
        
        if not upgrade_pip():
            print("⚠ Warning: Failed to upgrade pip, continuing anyway...")
        
        if not install_requirements():
            success = False
        
        if success:
            print("\n✅ Installation completed successfully!")
            print("\n📋 Next steps:")
            print("   1. Run: python process_sales_data.py")
            print("   2. Make sure you have 'sales_data.csv' in the current directory")
        else:
            print("\n❌ Installation failed. Please check the errors above.")
            return 1
    
    elif command == 'dev':
        print("\n🔧 Installing with development dependencies...")
        success = True
        
        if not upgrade_pip():
            print("⚠ Warning: Failed to upgrade pip, continuing anyway...")
        
        if not install_requirements():
            success = False
        
        if not install_optional_packages():
            print("⚠ Warning: Some optional packages failed to install")
        
        if success:
            print("\n✅ Development installation completed!")
        else:
            print("\n❌ Installation failed. Please check the errors above.")
            return 1
    
    elif command == 'check':
        print("\n🔍 Checking installation...")
        if check_all_dependencies():
            print("\n✅ All required dependencies are installed!")
        else:
            print("\n❌ Some required dependencies are missing.")
            print("   Run: python setup.py install")
            return 1
    
    elif command == 'venv':
        create_virtual_environment()
    
    elif command == 'clean':
        clean_installation()
    
    else:
        print(f"✗ Unknown command: {command}")
        print("   Available commands: install, check, venv, dev, clean")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)