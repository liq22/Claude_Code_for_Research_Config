#!/usr/bin/env python3
"""
Claude Code Research Template - One-Click Setup Script
=====================================================

This script automatically initializes your research environment with all
necessary dependencies and directory structures.

Usage:
    python setup.py           # Full setup with all features
    python setup.py --minimal # Minimal setup (core features only)
    python setup.py --check   # Check system requirements only

Author: Claude Code Research System
License: MIT
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path
from typing import List, Tuple, Optional

# ============================================================================
# Configuration
# ============================================================================

REQUIRED_PYTHON = (3, 9)
PROJECT_ROOT = Path(__file__).parent.absolute()

CORE_DEPENDENCIES = [
    "psutil>=5.9.0",
    "PyYAML>=6.0",
]

RECOMMENDED_DEPENDENCIES = [
    "pandas>=2.0.0",
    "matplotlib>=3.7.0", 
    "seaborn>=0.12.0",
    "numpy>=1.24.0",
    "requests>=2.31.0",
    "beautifulsoup4>=4.12.0",
]

REQUIRED_DIRECTORIES = [
    "workspace/papers",
    "workspace/data", 
    "workspace/figures",
    "logs/executions",
    "logs/sessions",
    "logs/agents",
    "logs/analytics",
    "dev/cache",
]

# ============================================================================
# Utility Functions
# ============================================================================

def print_header(title: str) -> None:
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"🚀 {title}")
    print(f"{'='*60}")

def print_step(step: str, status: str = "⏳") -> None:
    """Print a setup step with status."""
    print(f"{status} {step}")

def print_success(message: str) -> None:
    """Print a success message."""
    print(f"✅ {message}")

def print_error(message: str) -> None:
    """Print an error message."""
    print(f"❌ {message}")

def print_warning(message: str) -> None:
    """Print a warning message."""
    print(f"⚠️ {message}")

def print_info(message: str) -> None:
    """Print an info message."""
    print(f"ℹ️ {message}")

# ============================================================================
# System Checks
# ============================================================================

def check_python_version() -> bool:
    """Check if Python version meets requirements."""
    print_step("Checking Python version...")
    
    current_version = sys.version_info[:2]
    if current_version >= REQUIRED_PYTHON:
        print_success(f"Python {sys.version.split()[0]} is supported")
        return True
    else:
        print_error(f"Python {REQUIRED_PYTHON[0]}.{REQUIRED_PYTHON[1]}+ required, found {current_version[0]}.{current_version[1]}")
        return False

def check_pip_available() -> bool:
    """Check if pip is available."""
    print_step("Checking pip availability...")
    
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                              capture_output=True, text=True, check=True)
        print_success("pip is available")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_error("pip is not available. Please install pip first.")
        return False

def check_git_available() -> bool:
    """Check if git is available (optional)."""
    try:
        result = subprocess.run(["git", "--version"], 
                              capture_output=True, text=True, check=True)
        print_success("Git is available (optional)")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_warning("Git not found (optional for version control)")
        return False

def check_system_requirements() -> bool:
    """Check all system requirements."""
    print_header("System Requirements Check")
    
    python_ok = check_python_version()
    pip_ok = check_pip_available()
    git_ok = check_git_available()
    
    print_step("Checking system information...")
    print_info(f"Operating System: {platform.system()} {platform.release()}")
    print_info(f"Architecture: {platform.machine()}")
    print_info(f"Python Path: {sys.executable}")
    
    return python_ok and pip_ok

# ============================================================================
# Directory Setup
# ============================================================================

def create_directory_structure() -> bool:
    """Create required directory structure."""
    print_header("Creating Directory Structure")
    
    success = True
    for directory in REQUIRED_DIRECTORIES:
        dir_path = PROJECT_ROOT / directory
        try:
            dir_path.mkdir(parents=True, exist_ok=True)
            print_success(f"Created: {directory}/")
        except Exception as e:
            print_error(f"Failed to create {directory}/: {e}")
            success = False
    
    return success

def create_gitkeep_files() -> bool:
    """Create .gitkeep files for empty directories."""
    print_step("Creating .gitkeep files...")
    
    gitkeep_dirs = [
        ("workspace/papers", "Research papers and academic writing drafts"),
        ("workspace/data", "Research data files (CSV, JSON, etc.)"), 
        ("workspace/figures", "Research figures and visualization files"),
        ("logs/executions", "Claude Code execution logs"),
        ("logs/sessions", "Claude Code session logs"),
        ("logs/agents", "AI agent execution logs"),
        ("logs/analytics", "Analytics and performance metrics"),
    ]
    
    success = True
    for directory, description in gitkeep_dirs:
        gitkeep_path = PROJECT_ROOT / directory / ".gitkeep"
        if not gitkeep_path.exists():
            try:
                content = f"# Keep this directory in Git\n# {description}\n"
                gitkeep_path.write_text(content)
                print_success(f"Created: {directory}/.gitkeep")
            except Exception as e:
                print_error(f"Failed to create {directory}/.gitkeep: {e}")
                success = False
    
    return success

# ============================================================================
# Dependency Installation
# ============================================================================

def install_dependencies(dependencies: List[str], name: str) -> bool:
    """Install Python dependencies."""
    print_header(f"Installing {name}")
    
    if not dependencies:
        print_info(f"No {name.lower()} to install")
        return True
    
    print_step(f"Installing {len(dependencies)} packages...")
    
    try:
        cmd = [sys.executable, "-m", "pip", "install"] + dependencies
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print_success(f"{name} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to install {name.lower()}: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False

def setup_environment_file() -> bool:
    """Set up environment configuration file."""
    print_step("Setting up environment configuration...")
    
    env_example = PROJECT_ROOT / ".env.example"
    env_file = PROJECT_ROOT / ".env"
    
    if env_example.exists() and not env_file.exists():
        try:
            shutil.copy2(env_example, env_file)
            print_success("Created .env file from template")
            print_info("Edit .env file to configure your API keys and settings")
        except Exception as e:
            print_warning(f"Could not create .env file: {e}")
    elif env_file.exists():
        print_info(".env file already exists")
    else:
        print_warning(".env.example not found, skipping environment setup")
    
    return True

# ============================================================================
# Validation
# ============================================================================

def validate_installation() -> bool:
    """Validate the installation."""
    print_header("Validating Installation")
    
    # Check if core modules can be imported
    core_modules = ["psutil", "yaml"]
    
    for module in core_modules:
        try:
            print_step(f"Testing {module} import...")
            __import__(module)
            print_success(f"{module} imported successfully")
        except ImportError:
            print_error(f"Failed to import {module}")
            return False
    
    # Check directory structure
    print_step("Validating directory structure...")
    for directory in REQUIRED_DIRECTORIES:
        dir_path = PROJECT_ROOT / directory
        if dir_path.exists():
            print_success(f"✓ {directory}/")
        else:
            print_error(f"✗ {directory}/ missing")
            return False
    
    return True

# ============================================================================
# Main Setup Functions
# ============================================================================

def setup_minimal() -> bool:
    """Perform minimal setup."""
    print_header("Claude Code Research Template - Minimal Setup")
    
    success = True
    success &= check_system_requirements()
    success &= create_directory_structure()
    success &= create_gitkeep_files()
    success &= install_dependencies(CORE_DEPENDENCIES, "Core Dependencies")
    success &= setup_environment_file()
    success &= validate_installation()
    
    return success

def setup_full() -> bool:
    """Perform full setup with all features."""
    print_header("Claude Code Research Template - Full Setup")
    
    success = True
    success &= check_system_requirements()
    success &= create_directory_structure()
    success &= create_gitkeep_files()
    success &= install_dependencies(CORE_DEPENDENCIES, "Core Dependencies")
    success &= install_dependencies(RECOMMENDED_DEPENDENCIES, "Recommended Dependencies")
    success &= setup_environment_file()
    success &= validate_installation()
    
    return success

def print_welcome_message(setup_type: str) -> None:
    """Print welcome message after successful setup."""
    print_header("Setup Complete! 🎉")
    
    print(f"""
🚀 Your Claude Code Research Template is ready!

Setup Type: {setup_type}
Project Root: {PROJECT_ROOT}

📋 Next Steps:
1. Open Claude Code and load this directory
2. Edit .env file with your API keys (optional)
3. Start a conversation: "I want to research [your topic]"
4. Check out examples/ folder for inspiration

📖 Quick Start:
• README.md - Overview and usage guide
• QUICKSTART.md - 3-minute tutorial
• examples/ - Real usage scenarios
• templates/ - Paper formats (Nature, IEEE, etc.)

💡 First conversation ideas:
• "Help me write a Nature paper about [your topic]"
• "Search recent papers on [your research area]"
• "Analyze my experiment data in workspace/data/"

🔗 Resources:
• Documentation: Read INSTALLATION.md for detailed setup
• Templates: Check templates/ for academic formats
• Examples: See examples/ for usage scenarios

Happy researching! 📚✨
    """)

# ============================================================================
# Command Line Interface
# ============================================================================

def main():
    """Main setup function."""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--check":
            # Only check requirements
            success = check_system_requirements()
            sys.exit(0 if success else 1)
        elif sys.argv[1] == "--minimal":
            # Minimal setup
            success = setup_minimal()
            if success:
                print_welcome_message("Minimal")
        elif sys.argv[1] == "--help":
            print(__doc__)
            sys.exit(0)
        else:
            print_error(f"Unknown option: {sys.argv[1]}")
            print("Usage: python setup.py [--minimal|--check|--help]")
            sys.exit(1)
    else:
        # Full setup (default)
        success = setup_full()
        if success:
            print_welcome_message("Full")
    
    if success:
        print_success("Setup completed successfully!")
        sys.exit(0)
    else:
        print_error("Setup failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()