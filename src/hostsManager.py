import platform
import os
import shutil

# Determine OS-specific hosts file path and backup
if platform.system() == "Windows":
    HOSTS_FILE_PATH = r"C:\Windows\System32\drivers\etc\hosts"
    HOSTS_BACKUP_FILE_PATH = r"C:\Windows\System32\drivers\etc\hosts.backup"
else:
    HOSTS_FILE_PATH = "/etc/hosts"
    HOSTS_BACKUP_FILE_PATH = "/etc/hosts.backup"

def createBackup():
    if not os.path.exists(HOSTS_BACKUP_FILE_PATH):
        shutil.copy(HOSTS_FILE_PATH, HOSTS_BACKUP_FILE_PATH)
        print(f"Backup created at {HOSTS_BACKUP_FILE_PATH}")
    else:
        print("Backup already exists.")

def applyHosts(folderPath):
    try:
        createBackup()
        shutil.copy(HOSTS_BACKUP_FILE_PATH, HOSTS_FILE_PATH)  # restore original
        txtFiles = [f for f in os.listdir(folderPath) if f.endswith(".txt")]
        with open(HOSTS_FILE_PATH, "a") as hosts:
            hosts.write("\n# The following hosts are listed by DNS & IP website blocking tool.\n")
            for fileName in txtFiles:
                filePath = os.path.join(folderPath, fileName)
                with open(filePath, "r") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            hosts.write(line + "\n")
                print(f"Applied blocking from {fileName}")
    except PermissionError:
        print("Permission denied. Run the script as Administrator/with sudo.")
    except FileNotFoundError:
        print(f"Folder not found: {folderPath}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
def restoreHosts():
    try:
        if os.path.exists(HOSTS_BACKUP_FILE_PATH):
            shutil.copy(HOSTS_BACKUP_FILE_PATH, HOSTS_FILE_PATH)
            os.remove(HOSTS_BACKUP_FILE_PATH)
            print(f"Hosts file restored successfully.")
        else:
            print("No backup found! Cannot restore.")
    except PermissionError:
        print("Permission denied. Run the script as Administrator/with sudo.")
    except Exception as e:
        print(f"An error occurred while restoring hosts: {e}")