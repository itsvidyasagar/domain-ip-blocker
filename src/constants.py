import platform

SYSTEM = platform.system().lower()
DOMAINS_FOLDER_PATH = "config"
if SYSTEM == "windows":
    HOSTS_FILE_PATH = r"C:\Windows\System32\drivers\etc\hosts"
    HOSTS_BACKUP_FILE_PATH = r"C:\Windows\System32\drivers\etc\hosts.backup"
else:
    HOSTS_FILE_PATH = "/etc/hosts"
    HOSTS_BACKUP_FILE_PATH = "/etc/hosts.backup"