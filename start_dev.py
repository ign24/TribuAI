#!/usr/bin/env python3
"""
TribuAI Development Server

This script starts both the backend API server and the frontend development server.
It provides a convenient way to run the full TribuAI application in development mode.
"""

import os
import sys
import subprocess
import time
import signal
import threading
from pathlib import Path
from typing import List, Optional

# Add the backend directory to Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

def print_banner():
    """Print the TribuAI development banner."""
    print("\n" + "="*60)
    print("🎭 TribuAI Development Server")
    print("="*60)
    print("Starting both backend API and frontend development servers...")
    print("="*60)

def check_dependencies():
    """Check if required dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    # Check Python dependencies
    try:
        import fastapi
        import uvicorn
        print("✅ Backend dependencies found")
    except ImportError as e:
        print(f"❌ Backend dependency missing: {e}")
        print("Please run: pip install -r backend/requirements.txt")
        return False
    
    # Check Node.js and npm
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Node.js found")
        else:
            print("❌ Node.js not found")
            return False
    except FileNotFoundError:
        print("❌ Node.js not found")
        return False
    
    try:
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ npm found")
        else:
            print("❌ npm not found")
            return False
    except FileNotFoundError:
        print("❌ npm not found")
        return False
    
    return True

def install_frontend_dependencies():
    """Install frontend dependencies if needed."""
    frontend_dir = Path(__file__).parent / "frontend"
    node_modules = frontend_dir / "node_modules"
    
    if not node_modules.exists():
        print("📦 Installing frontend dependencies...")
        try:
            subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
            print("✅ Frontend dependencies installed")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install frontend dependencies: {e}")
            return False
    
    return True

def start_backend_server():
    """Start the FastAPI backend server."""
    print("🚀 Starting backend server...")
    
    backend_dir = Path(__file__).parent / "backend"
    api_file = backend_dir / "app" / "api.py"
    
    try:
        # Start the FastAPI server
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "app.api:app", 
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--reload"
        ], cwd=backend_dir)
        
        print("✅ Backend server started on http://localhost:8000")
        return process
        
    except Exception as e:
        print(f"❌ Failed to start backend server: {e}")
        return None

def start_frontend_server():
    """Start the Vue frontend development server."""
    print("🎨 Starting frontend server...")
    
    frontend_dir = Path(__file__).parent / "frontend"
    
    try:
        # Start the Vue dev server
        process = subprocess.Popen([
            "npm", "run", "dev"
        ], cwd=frontend_dir)
        
        print("✅ Frontend server started on http://localhost:5173")
        return process
        
    except Exception as e:
        print(f"❌ Failed to start frontend server: {e}")
        return None

def wait_for_backend():
    """Wait for backend to be ready."""
    import requests
    
    print("⏳ Waiting for backend to be ready...")
    max_attempts = 30
    attempt = 0
    
    while attempt < max_attempts:
        try:
            response = requests.get("http://localhost:8000/health", timeout=2)
            if response.status_code == 200:
                print("✅ Backend is ready!")
                return True
        except:
            pass
        
        attempt += 1
        time.sleep(1)
        if attempt % 5 == 0:
            print(f"   Still waiting... ({attempt}/{max_attempts})")
    
    print("❌ Backend failed to start within timeout")
    return False

def main():
    """Main development server startup function."""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Dependency check failed. Please install missing dependencies.")
        sys.exit(1)
    
    # Install frontend dependencies if needed
    if not install_frontend_dependencies():
        print("\n❌ Failed to install frontend dependencies.")
        sys.exit(1)
    
    # Start backend server
    backend_process = start_backend_server()
    if not backend_process:
        print("\n❌ Failed to start backend server.")
        sys.exit(1)
    
    # Wait for backend to be ready
    if not wait_for_backend():
        print("\n❌ Backend server is not responding.")
        backend_process.terminate()
        sys.exit(1)
    
    # Start frontend server
    frontend_process = start_frontend_server()
    if not frontend_process:
        print("\n❌ Failed to start frontend server.")
        backend_process.terminate()
        sys.exit(1)
    
    print("\n" + "="*60)
    print("🎉 TribuAI Development Environment Ready!")
    print("="*60)
    print("📱 Frontend: http://localhost:5173")
    print("🔧 Backend API: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("="*60)
    print("Press Ctrl+C to stop all servers")
    print("="*60)
    
    # Signal handler for graceful shutdown
    def signal_handler(signum, frame):
        print("\n🛑 Shutting down servers...")
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        print("✅ Servers stopped")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Wait for processes to complete
    try:
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)

if __name__ == "__main__":
    main() 