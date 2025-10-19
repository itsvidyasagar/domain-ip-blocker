import os
import shutil
from utils.filePermissions import change_permissions

class dnsManger:
    def __init__(self,hosts_file_path,hosts_backup_file_path,domains_folder_path):
        self.hosts_file_path = hosts_file_path
        self.hosts_backup_file_path = hosts_backup_file_path
        self.domains_folder_path = domains_folder_path

    def _backup_hosts_file(self):
        if not os.path.exists(self.hosts_backup_file_path):
            shutil.copy(self.hosts_file_path, self.hosts_backup_file_path)
            print(f"Hosts Backup created at {self.hosts_backup_file_path}")
            change_permissions(self.hosts_backup_file_path,0o644)
        else:
            print("Backup already exists.")

    def block_hosts_dns(self):
        try:
            self._backup_hosts_file()
            shutil.copy(self.hosts_backup_file_path, self.hosts_file_path)
            change_permissions(self.hosts_file_path,0o644)
            txt_files = [f for f in os.listdir(self.domains_folder_path) if f.endswith(".txt")]
            with open(self.hosts_file_path, "a") as hosts:
                hosts.write("\n# The following hosts are listed by DNS & IP website blocking tool.\n")
                for file_name in txt_files:
                    file_path = os.path.join(self.domains_folder_path, file_name)
                    with open(file_path, "r") as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith("#"):
                                hosts.write(line + "\n")
                    print(f"Applied blocking from {file_name}")
            change_permissions(self.hosts_file_path,0o644)
        except PermissionError:
            print("Permission denied. Run the script as Administrator/with sudo.")
        except FileNotFoundError:
            print(f"Folder not found: {self.domains_folder_path}")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def restore_hosts_dns(self):
        try:
            if os.path.exists(self.hosts_backup_file_path):
                shutil.copy(self.hosts_backup_file_path, self.hosts_file_path)
                change_permissions(self.hosts_file_path,0o644)
                os.remove(self.hosts_backup_file_path)
                print(f"Hosts file restored successfully.")
            else:
                print("No backup found! Cannot restore.")
        except PermissionError:
            print("Permission denied. Run the script as Administrator/with sudo.")
        except Exception as e:
            print(f"An error occurred while restoring hosts: {e}")