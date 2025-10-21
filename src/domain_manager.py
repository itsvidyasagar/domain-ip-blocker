import os
import shutil
from utils.file_permissions import change_permissions
from src.constants import HOSTS_FILE_PATH,START_MARKER,END_MARKER

class DomainManager:
    def __init__(self):
        self.hosts_file_path = HOSTS_FILE_PATH
        self.start_marker = START_MARKER
        self.end_marker = END_MARKER

    def block_domains(self,domains_folder_path):
        try:
            self.unblock_domains()
            txt_files = [f for f in os.listdir(domains_folder_path) if f.endswith(".txt")]
            with open(self.hosts_file_path, "a") as hosts:
                hosts.write("\n"+self.start_marker)
                for file_name in txt_files:
                    file_path = os.path.join(domains_folder_path, file_name)
                    with open(file_path, "r") as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith("#"):
                                hosts.write(line + "\n")
                hosts.write(self.end_marker)
            change_permissions(self.hosts_file_path,0o644)
        except PermissionError:
            raise PermissionError("Permission denied. Run the script as Administrator/with sudo.")
        except FileNotFoundError:
            raise FileNotFoundError(f"Folder not found: {domains_folder_path}")
        except Exception as e:
            raise Exception(f"{e}")
    
    def unblock_domains(self):
        try:
            if os.path.exists(self.hosts_file_path):
                with open(self.hosts_file_path, "r") as f:
                    lines = f.readlines()
                inside_snippet = False
                new_lines = []
                for line in lines:
                    if line == self.start_marker:
                        inside_snippet = True
                        continue
                    if line == self.end_marker:
                        inside_snippet = False
                        continue
                    if not inside_snippet:
                        new_lines.append(line)
                new_lines.reverse()
                while new_lines != [] and new_lines[0] == "\n":
                    new_lines.remove("\n")
                new_lines.reverse()
                with open(self.hosts_file_path, "w") as f:
                    f.writelines(new_lines)
                change_permissions(self.hosts_file_path,0o644)
            else:
                # print("Hosts file does not exist! Cannot Unblock domains.")
                pass
        except PermissionError:
            raise PermissionError("Permission denied. Run the script as Administrator/with sudo.")
        except Exception as e:
            raise Exception(f"{e}")