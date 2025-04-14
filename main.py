import os
import subprocess
import regex

# Define the path to the Documents folder
documents_folder = os.path.expanduser("~/Documents")

# Define the name of the .sh file you want to execute
sh_file_name = "your_script.sh"  # replace with your actual script name

# Change the current working directory to the Documents folder
os.chdir(documents_folder)

# Execute the .sh file
try
    subprocess.run(['bash', sh_file_name], check=True)  # or use ['./' + sh_file_name] if it's executable
    print(f"{sh_file_name} executed successfully.")
except subprocess.CalledProcessError as e:
    print(f"An error occurred while executing the script: {e}")