import subprocess
import os
import time
import sys

def kill_port(port):
    """Kills any process listening on the given port using PowerShell."""
    print(f"Checking port {port}...")
    # PowerShell command to find and kill the process
    ps_command = f"Get-NetTCPConnection -LocalPort {port} -ErrorAction SilentlyContinue | ForEach-Object {{ Stop-Process -Id $_.OwningProcess -Force }}"
    try:
        subprocess.run(["powershell", "-Command", ps_command], check=False)
        print(f"Cleaned port {port}.")
    except Exception as e:
        print(f"Error cleaning port {port}: {e}")

def start_server(name, command, cwd):
    """Starts a server in a new command prompt window."""
    print(f"Starting {name}...")
    # 'start' is a Windows shell command to open a new window
    # /k keeps the window open so you can see errors
    full_command = f'start "{name}" cmd /k "{command}"'
    subprocess.Popen(full_command, shell=True, cwd=cwd)

def main():
    # Paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(base_dir, "backend")
    frontend_dir = os.path.join(base_dir, "frontend")

    # 1. Kill existing processes
    kill_port(5000)
    kill_port(5173)
    
    time.sleep(2) # Wait for ports to free up

    # 2. Start Backend
    # Activate venv if it exists
    venv_script = os.path.join(backend_dir, ".venv", "Scripts", "activate.bat")
    if os.path.exists(venv_script):
        backend_cmd = f'"{venv_script}" && python run.py'
    else:
        backend_cmd = "python run.py"
    
    start_server("Flask Backend (Port 5000)", backend_cmd, backend_dir)

    # 3. Start Frontend
    start_server("Vite Frontend (Port 5173)", "npm run dev", frontend_dir)

    print("\nDone! Servers are launching in new windows.")

if __name__ == "__main__":
    main()
