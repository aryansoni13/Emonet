#!/usr/bin/env python3
"""
Launcher script for Real-Time Face Emotion Avatar
Provides setup checks and better error handling
"""

import sys
import os
import subprocess
import importlib.util

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['cv2', 'mediapipe', 'numpy']
    missing_packages = []
    
    for package in required_packages:
        if package == 'cv2':
            spec = importlib.util.find_spec('cv2')
        else:
            spec = importlib.util.find_spec(package)
        
        if spec is None:
            missing_packages.append(package)
        else:
            print(f"✅ {package} is installed")
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            return False
    
    return True

def check_webcam():
    """Check if webcam is available"""
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            cap.release()
            print("✅ Webcam is available")
            return True
        else:
            print("❌ Webcam not detected")
            return False
    except Exception as e:
        print(f"❌ Error checking webcam: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ['screenshots', 'logs']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def main():
    """Main launcher function"""
    print("🎭 Real-Time Face Emotion Avatar Launcher")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return 1
    
    # Check dependencies
    if not check_dependencies():
        return 1
    
    # Check webcam
    if not check_webcam():
        print("⚠️  Webcam not available, but continuing...")
    
    # Create directories
    create_directories()
    
    print("\n🚀 Starting Emotion Avatar...")
    print("=" * 50)
    
    try:
        # Import and run the main application
        from avatar import EmotionAvatar
        avatar = EmotionAvatar()
        avatar.run()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error running application: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 