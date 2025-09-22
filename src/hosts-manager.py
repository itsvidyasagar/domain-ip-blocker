import platform
import os
import shutil


# Determine OS-specific hosts file path and backup
if platform.system() == "Windows":
    HOSTS_FILE = r"C:\Windows\System32\drivers\etc\hosts"
    HOSTS_BACKUP_FILE = r"C:\Windows\System32\drivers\etc\hosts.backup"
else:
    HOSTS_FILE = "/etc/hosts"
    HOSTS_BACKUP_FILE = "/etc/hosts.backup"


def create_backup():
    """Create a single primary backup if it doesn't exist."""
    if not os.path.exists(HOSTS_BACKUP_FILE):
        shutil.copy(HOSTS_FILE, HOSTS_BACKUP_FILE)
        print(f"Backup created at {HOSTS_BACKUP_FILE}")
    else:
        print("Backup already exists. Skipping.")


def apply_hosts(folder_path):
    """
    Apply website blocking using all .txt files in the folder.
    Each file should have lines like: '0.0.0.0    domain.com'
    """
    try:
        create_backup()
        shutil.copy(HOSTS_BACKUP_FILE, HOSTS_FILE)  # restore original

        txt_files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]

        with open(HOSTS_FILE, "a") as hosts:
            hosts.write("\n# The following hosts are listed by DNS & IP website blocking tool.\n")

            for file_name in txt_files:
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, "r") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            hosts.write(line + "\n")
                print(f"Applied blocking from {file_name}")

    except PermissionError:
        print("Permission denied. Run the script as Administrator/with sudo.")
    except FileNotFoundError:
        print(f"Folder not found: {folder_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

    
def restore_hosts():
    """Restore the original hosts file from backup."""
    try:
        if os.path.exists(HOSTS_BACKUP_FILE):
            shutil.copy(HOSTS_BACKUP_FILE, HOSTS_FILE)
            print(f"Hosts file restored from {HOSTS_BACKUP_FILE}")
        else:
            print("No backup found! Cannot revert.")
    except PermissionError:
        print("Permission denied. Run the script as Administrator/with sudo.")
    except Exception as e:
        print(f"An error occurred while restoring hosts: {e}")
