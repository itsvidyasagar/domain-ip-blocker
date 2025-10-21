import argparse
from src.constants import DOMAINS_FOLDER_PATH
from src.domain_manager import DomainManager
from src.ip_manager import IpManager

def main():
    domain_manager =DomainManager()
    ip_manager = IpManager()
    domains_folder_path = DOMAINS_FOLDER_PATH

    parser = argparse.ArgumentParser(
        description="web-domain-ip-blocking-tool"
    )
    parser.add_argument(
        "action",
        choices=["block", "unblock"],
        default="block",
        help="Choose whether to block or unblock"
    )
    parser.add_argument(
        "--domain",
        action="store_true",
        help="Apply the action to Domain entries"
    )

    args = parser.parse_args()

    if args.action == "block":
        if args.domain:
            ip_manager.unblock_ips()
            domain_manager.block_domains(domains_folder_path)
        else:
            domain_manager.unblock_domains()
            ip_manager.block_ips(domains_folder_path)
            # domain_manager.block_domains(domains_folder_path)
    elif args.action == "unblock":
            ip_manager.unblock_ips()
            domain_manager.unblock_domains()
    else:
        raise RuntimeError("An error occurred proccessing the request. Try again.")

if __name__ == "__main__":
    main()