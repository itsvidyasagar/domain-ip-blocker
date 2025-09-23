import os
import subprocess
import pwd
import grp
import src.domain-resolver import resolve_ips


BLOCKED_FILE = "/etc/ip.blocked"


def secure_file(path):
    """
    Ensure file is owned by root:root and has 644 permissions (rw-r--r--).
    Only root can write, others can only read.
    """
    root_uid = pwd.getpwnam("root").pw_uid
    root_gid = grp.getgrnam("root").gr_gid
    os.chown(path, root_uid, root_gid)
    os.chmod(path, 0o644)


def create_blocked_file():
    """
    Always create (overwrite) /etc/ip.blocked as an empty file,
    with secure ownership and permissions.
    """
    try:
        with open(BLOCKED_FILE, "w") as f:
            pass
        secure_file(BLOCKED_FILE)
        print(f"Created empty blocked IP file at {BLOCKED_FILE} with secure permissions.")
    except PermissionError:
        print("Permission denied. Run this script with sudo.")
    except Exception as e:
        print(f"Error creating {BLOCKED_FILE}: {e}")


def block_ip(ip):
    """
    Block a single IP using iptables (IPv4) or ip6tables (IPv6).
    """
    try:
        subprocess.run(["sudo", "iptables", "-A", "OUTPUT", "-d", ip, "-j", "REJECT"], check=True)
        print(f"Blocked IPv4: {ip}")
    except subprocess.CalledProcessError:
        try:
            subprocess.run(["sudo", "ip6tables", "-A", "OUTPUT", "-d", ip, "-j", "REJECT"], check=True)
            print(f"Blocked IPv6: {ip}")
        except subprocess.CalledProcessError:
            print(f"Failed to block IP: {ip}")


def unblock_ip(ip):
    """
    Remove a single IP block rule (both IPv4 and IPv6).
    """
    try:
        subprocess.run(["sudo", "iptables", "-D", "OUTPUT", "-d", ip, "-j", "REJECT"], check=True)
        print(f"Unblocked IPv4: {ip}")
    except subprocess.CalledProcessError:
        try:
            subprocess.run(["sudo", "ip6tables", "-D", "OUTPUT", "-d", ip, "-j", "REJECT"], check=True)
            print(f"Unblocked IPv6: {ip}")
        except subprocess.CalledProcessError:
            print(f"Failed to unblock IP: {ip}")


def revert_ip_block():
    """
    Revert all IPs stored in /etc/ip.blocked if the file exists.
    If the file does not exist, do nothing.
    """
    if not os.path.exists(BLOCKED_FILE):
        print("No blocked IPs to revert.")
        return

    try:
        with open(BLOCKED_FILE, "r") as f:
            ips = [line.strip() for line in f if line.strip()]

        for ip in ips:
            unblock_ip(ip)

        # Clear the file after reverting
        with open(BLOCKED_FILE, "w") as f:
            pass
        secure_file(BLOCKED_FILE)

        print("Reverted all IP blocks.")
    except Exception as e:
        print(f"Error reverting IP blocks: {e}")


def apply_ip_block(folder_path):
    """
    Block all domains listed in .txt files in the given folder.
    If blocked IP file exists, revert first. Otherwise, create the file.
    """
    if os.path.exists(BLOCKED_FILE):
        revert_ip_block()
    else:
        create_blocked_file()

    blocked_ips = set()

    try:
        txt_files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
    except Exception as e:
        print(f"Error listing .txt files in {folder_path}: {e}")
        return

    for file_name in txt_files:
        file_path = os.path.join(folder_path, file_name)
        try:
            with open(file_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        domain = line.split()[-1]
                        try:
                            ipv4_list, ipv6_list = resolve_ips(domain)
                            for ip in ipv4_list | ipv6_list:
                                block_ip(ip)
                                blocked_ips.add(ip)
                        except Exception as e:
                            print(f"Error resolving IPs for {domain}: {e}")
            print(f"Applied IP blocking for {file_name}")
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")

    # Save blocked IPs to /etc/ip.blocked
    try:
        with open(BLOCKED_FILE, "w") as f:
            for ip in blocked_ips:
                f.write(ip + "\n")
        secure_file(BLOCKED_FILE)
        print(f"Updated {BLOCKED_FILE} with current blocked IPs (secure permissions).")
    except Exception as e:
        print(f"Error writing to {BLOCKED_FILE}: {e}")


if __name__ == "__main__":
    apply_ip_block("/config")