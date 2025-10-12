import os
import subprocess
import pwd
import grp
from domainResolver import resolveIps


BLOCKED_FILE = "/etc/ip.blocked"

def secureFile(path):
    root_uid = pwd.getpwnam("root").pw_uid
    root_gid = grp.getgrnam("root").gr_gid
    os.chown(path, root_uid, root_gid)
    os.chmod(path, 0o644)

def createBlockedFile():
    try:
        with open(BLOCKED_FILE, "w") as f:
            pass
        secureFile(BLOCKED_FILE)
        print(f"Created empty blocked IP file at {BLOCKED_FILE} with secure permissions.")
    except PermissionError:
        print("Permission denied. Run this script with sudo.")
    except Exception as e:
        print(f"Error creating {BLOCKED_FILE}: {e}")


def blockIp(ip):
    try:
        subprocess.run(["sudo", "iptables", "-A", "OUTPUT", "-d", ip, "-j", "REJECT"], check=True)
        print(f"Blocked IPv4: {ip}")
    except subprocess.CalledProcessError:
        try:
            subprocess.run(["sudo", "ip6tables", "-A", "OUTPUT", "-d", ip, "-j", "REJECT"], check=True)
            print(f"Blocked IPv6: {ip}")
        except subprocess.CalledProcessError:
            print(f"Failed to block IP: {ip}")


def unblockIp(ip):
    try:
        subprocess.run(["sudo", "iptables", "-D", "OUTPUT", "-d", ip, "-j", "REJECT"], check=True)
        print(f"Unblocked IPv4: {ip}")
    except subprocess.CalledProcessError:
        try:
            subprocess.run(["sudo", "ip6tables", "-D", "OUTPUT", "-d", ip, "-j", "REJECT"], check=True)
            print(f"Unblocked IPv6: {ip}")
        except subprocess.CalledProcessError:
            print(f"Failed to unblock IP: {ip}")


def revertIpBlock():
    if not os.path.exists(BLOCKED_FILE):
        print("No blocked IPs to revert.")
        return
    try:
        with open(BLOCKED_FILE, "r") as f:
            ips = [line.strip() for line in f if line.strip()]

        for ip in ips:
            unblockIp(ip)

        # Clear the file after reverting
        with open(BLOCKED_FILE, "w") as f:
            pass
        secureFile(BLOCKED_FILE)

        print("Reverted all IP blocks.")
    except Exception as e:
        print(f"Error reverting IP blocks: {e}")


def applyIpBlock(folderPath):
    if os.path.exists(BLOCKED_FILE):
        revertI
    pBlock()
    else:
        createBlockedFile()

    blockedIps = set()

    try:
        txtFiles = [f for f in os.listdir(folderPath) if f.endswith(".txt")]
    except Exception as e:
        print(f"Error listing .txt files in {folderPath}: {e}")
        return

    for fileName in txtFiles:
        filePath = os.path.join(folderPath, fileName)
        try:
            with open(filePath, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        domain = line.split()[-1]
                        try:
                            ipv4List, ipv6List = resolveIps(domain)
                            for ip in ipv4List | ipv6List:
                                blockIp(ip)
                                blockedIps.add(ip)
                        except Exception as e:
                            print(f"Error resolving IPs for {domain}: {e}")
            print(f"Applied IP blocking for {fileName}")
        except Exception as e:
            print(f"Error reading file {filePath}: {e}")

    # Save blocked IPs to /etc/ip.blocked
    try:
        with open(BLOCKED_FILE, "w") as f:
            for ip in blockedIps:
                f.write(ip + "\n")
        secureFile(BLOCKED_FILE)
        print(f"Updated {BLOCKED_FILE} with current blocked IPs (secure permissions).")
    except Exception as e:
        print(f"Error writing to {BLOCKED_FILE}: {e}")