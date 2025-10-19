from src.constants import HOSTS_FILE_PATH,HOSTS_BACKUP_FILE_PATH,DOMAINS_FOLDER_PATH
from src.dnsManager import dnsManger

def main():
    hm =dnsManger(HOSTS_FILE_PATH,HOSTS_BACKUP_FILE_PATH,DOMAINS_FOLDER_PATH)
    hm.restore_hosts_dns()

if __name__ == "__main__":
    main()