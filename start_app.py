import subprocess
import os
import time
import sys
import platform
import shutil

def kill_port(port: int):
    """Kills any process listening on the given port."""
    print(f"Checking port {port}...")
    system = platform.system()
    
    if system == "Windows":
        # PowerShell command to find and kill the process
        ps_command = f"Get-NetTCPConnection -LocalPort {port} -ErrorAction SilentlyContinue | ForEach-Object {{ Stop-Process -Id $_.OwningProcess -Force }}"
        try:
            subprocess.run(["powershell", "-Command", ps_command], check=False)
            print(f"Cleaned port {port}.")
        except Exception as e:
            print(f"Error cleaning port {port}: {e}")
    else:
        # Unix-like (macOS/Linux)
        killed = False
        # Try lsof (macOS standard, Linux common)
        if shutil.which("lsof"):
            try:
                # Check if anything is listening first to avoid xargs errors
                check = subprocess.run(f"lsof -t -i:{port}", shell=True, capture_output=True, text=True)
                if check.stdout.strip():
                    subprocess.run(f"lsof -t -i:{port} | xargs kill -9", shell=True, check=False, stderr=subprocess.DEVNULL)
                    print(f"Cleaned port {port} using lsof.")
                    killed = True
            except Exception:
                pass
        
        if not killed and shutil.which("fuser"):
             # Try fuser (Linux common)
             try:
                 subprocess.run(f"fuser -k {port}/tcp", shell=True, check=False, stderr=subprocess.DEVNULL)
                 print(f"Cleaned port {port} using fuser.")
                 killed = True
             except Exception:
                 pass

def start_server(name: str, command: str, cwd: str):
    """Starts a server in a new terminal window."""
    print(f"Starting {name}...")
    system = platform.system()
    
    if system == "Windows":
        # 'start' is a Windows shell command to open a new window
        # /k keeps the window open so you can see errors
        full_command = f'start "{name}" cmd /k "{command}"'
        subprocess.Popen(full_command, shell=True, cwd=cwd)
    
    elif system == "Darwin": # macOS
        # Use AppleScript to open Terminal
        safe_cmd = command.replace('"', '\\"')
        safe_cwd = cwd.replace('"', '\\"')
        apple_script = f'''
        tell application "Terminal"
            do script "cd \\"{safe_cwd}\\" && {safe_cmd}"
            activate
        end tell
        '''
        subprocess.Popen(["osascript", "-e", apple_script])
        
    elif system == "Linux":
        # Try common terminal emulators
        terminals = ["gnome-terminal", "konsole", "xfce4-terminal", "x-terminal-emulator", "terminator", "tilix", "alacritty"]
        found = False
        for term in terminals:
            if shutil.which(term):
                if term == "gnome-terminal":
                    subprocess.Popen([term, "--", "bash", "-c", f"{command}; exec bash"], cwd=cwd)
                else:
                    subprocess.Popen([term, "-e", f"bash -c '{command}; exec bash'"], cwd=cwd)
                found = True
                break
        if not found:
            print(f"Warning: Could not find a supported terminal emulator for {name}. Running in background...")
            subprocess.Popen(command, shell=True, cwd=cwd)

def setup_backend(backend_dir: str) -> str:
    """Sets up Python venv, installs requirements, and inits DB."""
    print("--- Setting up Backend ---")
    
    # 1. Virtual Environment
    venv_dir = os.path.join(backend_dir, ".venv")
    if platform.system() == "Windows":
        python_exe = os.path.join(venv_dir, "Scripts", "python.exe")
    else:
        python_exe = os.path.join(venv_dir, "bin", "python")

    if not os.path.exists(venv_dir):
        print(f"Creating virtual environment in {venv_dir}...")
        try:
            subprocess.check_call([sys.executable, "-m", "venv", venv_dir])
        except subprocess.CalledProcessError:
            print("Error creating venv. Ensure python is installed.")
            raise
    
    if not os.path.exists(python_exe):
        print("Warning: Virtual environment python not found. Using system python.")
        python_exe = sys.executable

    # 2. Install Requirements
    req_file = os.path.join(backend_dir, "requirements.txt")
    if os.path.exists(req_file):
        print("Installing/Updating Python dependencies...")
        try:
            subprocess.check_call([python_exe, "-m", "pip", "install", "-r", req_file])
        except subprocess.CalledProcessError:
            print("Error installing requirements.")
            raise
    
    # 3. Initialize Database
    init_script = os.path.join(backend_dir, "init_db.py")
    if os.path.exists(init_script):
        print("Initializing database (if needed)...")
        try:
            subprocess.check_call([python_exe, init_script], cwd=backend_dir)
        except subprocess.CalledProcessError:
            print("Error initializing database. Ensure MySQL is running.")
            # Don't raise here, maybe they just want to start the server and DB is already fine?
            pass
    
    return python_exe

def setup_frontend(frontend_dir: str):
    """Installs Node modules if missing."""
    print("--- Setting up Frontend ---")

    if not shutil.which("npm"):
        print("Error: Node.js (npm) is not installed or not in PATH.")
        raise Exception("npm not found")

    node_modules = os.path.join(frontend_dir, "node_modules")
    if not os.path.exists(node_modules):
        print("Installing Node.js dependencies (npm install)...")
        try:
            # shell=True required on Windows for npm
            subprocess.check_call("npm install", shell=True, cwd=frontend_dir)
        except subprocess.CalledProcessError:
            print("Error installing frontend dependencies. Ensure Node.js/npm is installed.")
            raise
    else:
        print("Frontend dependencies found.")

def main():
    # Paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(base_dir, "backend")
    frontend_dir = os.path.join(base_dir, "frontend")

    # --- Setup Phase ---
    python_exe = sys.executable
    try:
        python_exe = setup_backend(backend_dir)
        setup_frontend(frontend_dir)
    except Exception as e:
        print(f"Setup failed: {e}")
        print("Attempting to start servers anyway...")

    # --- Launch Phase ---
    print("\n--- Starting Servers ---")

    # 1. Kill existing processes
    kill_port(5000)
    kill_port(5173)
    
    time.sleep(2) # Wait for ports to free up

    # 2. Start Backend
    backend_cmd = f'"{python_exe}" run.py'
    start_server("Flask Backend (Port 5000)", backend_cmd, backend_dir)

    # 3. Start Frontend
    start_server("Vite Frontend (Port 5173)", "npm run dev", frontend_dir)

    print("\nDone! Servers are launching in new windows.")

if __name__ == "__main__":
    main()
