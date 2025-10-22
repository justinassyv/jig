#!/usr/bin/env python3
import subprocess
import os
import sys

# Path to your .sh file
script_path = "/home/rpi/Documents/sonora/prog.sh"

# Check if the file exists
if not os.path.exists(script_path):
    print(f"Error: File not found -> {script_path}")
    sys.exit(1)

# Make sure the file is executable
os.chmod(script_path, 0o755)

print("Starting firmware programming...")

try:
    # Run the shell script
    subprocess.run(["bash", script_path], check=True)
    print("Programming completed successfully!")
except subprocess.CalledProcessError as e:
    print(f"Error: Script exited with code {e.returncode}")
except Exception as e:
    print(f"Unexpected error: {e}")
