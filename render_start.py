#!/usr/bin/env python3
"""
Render deployment runner
This script ensures the app starts correctly on Render
"""

import subprocess
import sys
import os

if __name__ == "__main__":
    # Install requirements
    print("📦 Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements_advanced.txt"])
    
    # Run the main application
    print("🚀 Starting YouTube AI Agents System...")
    subprocess.check_call([sys.executable, "youtube_ai_agents_advanced.py"])
