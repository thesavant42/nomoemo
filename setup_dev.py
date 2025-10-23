#!/usr/bin/env python3
"""
Development setup script for NoMoEmo.

This script sets up a development environment with all dependencies
and development tools installed.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and print status."""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    """Main setup function."""
    print("🚀 Setting up NoMoEmo development environment...")
    print("=" * 50)

    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        sys.exit(1)

    print(f"✅ Python {sys.version.split()[0]} detected")

    # Upgrade pip
    if not run_command("python -m pip install --upgrade pip", "Upgrading pip"):
        sys.exit(1)

    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        sys.exit(1)

    # Install development dependencies if available
    dev_requirements = Path("requirements-dev.txt")
    if dev_requirements.exists():
        if not run_command("pip install -r requirements-dev.txt", "Installing development dependencies"):
            sys.exit(1)
    else:
        print("ℹ️  No requirements-dev.txt found, skipping development dependencies")

    # Verify installation
    print("\n🔍 Verifying installation...")
    if not run_command("python nomoemo.py --version", "Testing NoMoEmo installation"):
        sys.exit(1)

    # Run basic test
    print("\n🧪 Running basic functionality test...")
    test_file = Path("test_emoji.txt")
    try:
        # Create a test file with emoji
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("Test file with 😀 emoji")

        # Test dry run
        result = subprocess.run([sys.executable, "nomoemo.py", "--dry-run", "--quiet", str(test_file)],
                              capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ Basic functionality test passed")
        else:
            print(f"⚠️  Basic functionality test had issues (exit code: {result.returncode})")
            print(f"Output: {result.stdout}")
            print(f"Errors: {result.stderr}")

    except Exception as e:
        print(f"⚠️  Could not run basic test: {e}")
    finally:
        # Clean up test file
        if test_file.exists():
            test_file.unlink()

    print("\n🎉 Development environment setup complete!")
    print("\n📖 Quick start:")
    print("  python nomoemo.py --help              # Show help")
    print("  python nomoemo.py --dry-run .         # Scan current directory")
    print("  python nomoemo.py --dry-run --verbose file.py  # Detailed scan")

    print("\n📚 Documentation:")
    print("  README.md                              # Complete guide")
    print("  TROUBLESHOOTING.md                     # Common issues")
    print("  TODO.md                               # Development progress")

if __name__ == "__main__":
    main()