#!/usr/bin/env python3
"""
Build script for ESM VR Patcher
Creates a distributable package for Nexus Mods
"""

import os
import sys
import shutil
import zipfile
import subprocess
from pathlib import Path

# Configuration
PROJECT_NAME = "ESM_Patcher"
VERSION = "1.0.0"
MAIN_SCRIPT = "esm_patcher.py"

def create_directories():
    """Create necessary directories"""
    dirs = ["build", "dist", "assets"]
    for d in dirs:
        Path(d).mkdir(exist_ok=True)
    print("✓ Created directories")

def check_requirements():
    """Check and install required packages"""
    required = ["pyinstaller"]
    
    print("Checking requirements...")
    for package in required:
        try:
            __import__(package)
            print(f"  ✓ {package} installed")
        except ImportError:
            print(f"  ✗ {package} not found, installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"  ✓ {package} installed")

def prepare_assets():
    """Prepare asset files"""
    print("\nPreparing assets...")
    
    # Create placeholder files for assets that would come from the installer
    assets_needed = {
        "xdelta3.exe": "Download from: https://github.com/jmacd/xdelta-gpl/releases",
        "fallout4_323025.xdelta": "Extract from Fallout: London VR installer",
        "fallout4_322806.xdelta": "Extract from Fallout: London VR installer",
        "icon.ico": "Optional: Add custom icon"
    }
    
    for asset, source in assets_needed.items():
        asset_path = Path("assets") / asset
        if not asset_path.exists():
            print(f"  ⚠ {asset} not found")
            print(f"    Source: {source}")
            
            # Create placeholder for icon
            if asset == "icon.ico":
                # We'll proceed without icon
                continue
            else:
                print(f"    ERROR: Required file {asset} is missing!")
                print("\n    Please obtain the required files:")
                print("    1. xdelta3.exe from the xdelta project")
                print("    2. Patch files from the Fallout: London VR installer")
                return False
        else:
            print(f"  ✓ {asset} found")
    
    return True

def build_executable():
    """Build the executable using PyInstaller"""
    print("\nBuilding executable...")
    
    # Try to find pyinstaller in different locations
    pyinstaller_cmd = None
    possible_paths = [
        "pyinstaller",  # System PATH
        sys.executable.replace("python.exe", "Scripts\\pyinstaller.exe"),  # Same dir as Python
        os.path.join(os.path.dirname(sys.executable), "Scripts", "pyinstaller.exe"),  # Scripts folder
        os.path.expanduser("~\\AppData\\Roaming\\Python\\Python312\\Scripts\\pyinstaller.exe"),  # User install Python 3.12
        os.path.expanduser("~\\AppData\\Roaming\\Python\\Python311\\Scripts\\pyinstaller.exe"),  # User install Python 3.11
        os.path.expanduser("~\\AppData\\Roaming\\Python\\Python310\\Scripts\\pyinstaller.exe"),  # User install Python 3.10
        os.path.expanduser("~\\AppData\\Local\\Programs\\Python\\Python312\\Scripts\\pyinstaller.exe"),  # Local Python 3.12
        os.path.expanduser("~\\AppData\\Local\\Programs\\Python\\Python311\\Scripts\\pyinstaller.exe"),  # Local Python 3.11
    ]
    
    # Find the first working pyinstaller
    for path in possible_paths:
        if os.path.exists(path) or shutil.which(path):
            pyinstaller_cmd = path
            print(f"Found PyInstaller at: {path}")
            break
    
    if not pyinstaller_cmd:
        # Try running with python -m
        try:
            subprocess.check_output([sys.executable, "-m", "PyInstaller", "--version"], stderr=subprocess.DEVNULL)
            pyinstaller_cmd = [sys.executable, "-m", "PyInstaller"]
            print("Using PyInstaller via python -m")
        except:
            print("ERROR: Could not find PyInstaller executable!")
            print("\nTry one of these solutions:")
            print("1. Run: python -m pip install --upgrade pyinstaller")
            print("2. Add PyInstaller to your PATH")
            print("3. Run PyInstaller directly:")
            print(f"   python -m PyInstaller --onefile --windowed --name {PROJECT_NAME} --add-data \"assets;assets\" {MAIN_SCRIPT}")
            return False
    
    # Build PyInstaller command
    if isinstance(pyinstaller_cmd, list):
        cmd = pyinstaller_cmd + [
            "--onefile",
            "--windowed",
            "--name", PROJECT_NAME,
            "--add-data", "assets;assets",
            "--distpath", "dist",
            "--workpath", "build/work",
            "--specpath", "build",
            "--clean",
            "--noconfirm"
        ]
    else:
        cmd = [
            pyinstaller_cmd,
            "--onefile",
            "--windowed",
            "--name", PROJECT_NAME,
            "--add-data", "assets;assets",
            "--distpath", "dist",
            "--workpath", "build/work",
            "--specpath", "build",
            "--clean",
            "--noconfirm"
        ]
    
    # Add icon if it exists
    icon_path = Path("assets/icon.ico")
    if icon_path.exists():
        cmd.extend(["--icon", str(icon_path)])
    
    cmd.append(MAIN_SCRIPT)
    
    try:
        print(f"Running command: {' '.join(cmd if isinstance(cmd[0], str) else [str(c) for c in cmd])}")
        subprocess.check_call(cmd)
        print("✓ Executable built successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed: {e}")
        return False
    except FileNotFoundError:
        print("✗ PyInstaller not found in PATH")
        print("\nTry running manually:")
        print(f"python -m PyInstaller --onefile --windowed --name {PROJECT_NAME} --add-data \"assets;assets\" --icon assets/icon.ico {MAIN_SCRIPT}")
        return False

def create_package():
    """Create the final distribution package"""
    print("\nCreating distribution package...")
    
    # Create package directory
    package_dir = Path(f"dist/{PROJECT_NAME}_v{VERSION}")
    package_dir.mkdir(exist_ok=True)
    
    # Copy executable
    exe_source = Path(f"dist/{PROJECT_NAME}.exe")
    if not exe_source.exists():
        print("✗ Executable not found!")
        return False
    
    shutil.copy2(exe_source, package_dir / f"{PROJECT_NAME}.exe")
    print(f"  ✓ Copied executable")
    
    # Copy assets folder
    assets_dest = package_dir / "assets"
    if assets_dest.exists():
        shutil.rmtree(assets_dest)
    shutil.copytree("assets", assets_dest)
    print(f"  ✓ Copied assets")
    
    # Copy README
    readme_source = Path("README.md")
    if readme_source.exists():
        shutil.copy2(readme_source, package_dir / "README.md")
        print(f"  ✓ Copied README")
    
    # Create ZIP archive
    zip_name = f"{PROJECT_NAME}_v{VERSION}.zip"
    zip_path = Path("dist") / zip_name
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(package_dir.parent)
                zipf.write(file_path, arcname)
    
    print(f"  ✓ Created {zip_name}")
    
    # Calculate file size
    size_mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"  ✓ Package size: {size_mb:.2f} MB")
    
    return True

def create_nexus_description():
    """Create a formatted description for Nexus Mods"""
    description = """
[size=6][b]Fallout 4 ESM Patcher[/b][/size]
[size=4]Version 1.0.0[/size]

[size=4][b]Description[/b][/size]
A standalone tool to patch Next-Gen Fallout4.esm files for mod compatibility. Essential for running Fallout: London, VR mods, and other mods that require the older ESM format.

[size=4][b]Features[/b][/size]
[list]
[*]Auto-detects Fallout 4 installations
[*]Identifies if patching is needed
[*]Creates automatic backups
[*]One-click restore function
[*]GUI and command-line support
[*]Detailed logging
[/list]

[size=4][b]Installation[/b][/size]
1. Download and extract the archive
2. Run ESM_Patcher.exe
3. Click "Auto-Detect" or browse to your Fallout4.esm
4. Click "Apply Patch" if needed

[size=4][b]Requirements[/b][/size]
[list]
[*]Windows 7/8/10/11
[*]Fallout 4 with Next-Gen update
[*]100 MB free disk space
[/list]

[size=4][b]Supported Versions[/b][/size]
[list]
[*]Next-Gen ESM: 330,777,465 bytes (323,025 KB variant)
[*]Next-Gen ESM: 330,553,163 bytes (322,806 KB variant)
[/list]

[size=4][b]Credits[/b][/size]
[list]
[*]xdelta3 by Joshua MacDonald
[*]Fallout: London Team for original patches
[*]Fallout 4 Modding Community
[/list]
"""
    
    with open("dist/nexus_description.txt", "w") as f:
        f.write(description)
    
    print("\n✓ Created Nexus description file")

def main():
    """Main build process"""
    print(f"Building {PROJECT_NAME} v{VERSION}")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("ERROR: Python 3.7+ required")
        return 1
    
    # Create directories
    create_directories()
    
    # Check requirements
    check_requirements()
    
    # Prepare assets
    if not prepare_assets():
        print("\n⚠ WARNING: Missing required assets!")
        print("The build will fail without the xdelta3.exe and patch files.")
        response = input("\nContinue anyway? (y/n): ")
        if response.lower() != 'y':
            return 1
    
    # Build executable
    if not build_executable():
        print("\n✗ Build failed!")
        return 1
    
    # Create package
    if not create_package():
        print("\n✗ Package creation failed!")
        return 1
    
    # Create Nexus description
    create_nexus_description()
    
    print("\n" + "=" * 50)
    print(f"✓ Build complete!")
    print(f"\nOutput files in dist/:")
    print(f"  - {PROJECT_NAME}_v{VERSION}.zip (Upload to Nexus)")
    print(f"  - nexus_description.txt (Copy to Nexus description)")
    print(f"  - {PROJECT_NAME}_v{VERSION}/ (Extracted package for testing)")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())