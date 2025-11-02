import os
import ipaddress
from utils.domain_resolver import resolve_domain
from utils.progress_bar import progress_bar
from src.constants import SYSTEM
from utils.linux_firewall import LinuxFirewall
from utils.darwin_firewall import DarwinFirewall
from utils.windows_firewall import WindowsFirewall

class IpManager:
    def __init__(self):
        self.system = SYSTEM
        self.ipv4_list = []
        self.ipv6_list = []
        if self.system == "linux":
            self.linux_firewall = LinuxFirewall()
        elif self.system == "darwin":
            self.darwin_firewall = DarwinFirewall()
        elif self.system == "windows":
            self.windows_firewall = WindowsFirewall()
        else:
            raise RuntimeError("Unsupported operating system.")

    def _collect_ip_addresses(self,domains_folder_path):
        try:
            txt_files = [f for f in os.listdir(domains_folder_path) if f.endswith(".txt")]
            for file_name in txt_files:
                file_path = os.path.join(domains_folder_path, file_name)
                with open(file_path, "r") as f:
                    lines = f.readlines()
                    total = len(lines)
                    title = f"Resolving {file_name}"
                    for i,line in enumerate(lines,1):
                        line = line.strip()
                        if line and not line.startswith("#"):
                            domain = line.split()[-1]
                            try:
                                ipv4_list, ipv6_list = resolve_domain(domain)
                                for ip in ipv4_list:
                                    try:
                                        ip_obj = ipaddress.ip_address(ip)
                                        if not (ip_obj.is_loopback or ip_obj.is_link_local or ip_obj.is_multicast or ip_obj.is_reserved or ip_obj.is_private):
                                            self.ipv4_list.append(ip)
                                    except ValueError:
                                        pass
                                for ip in ipv6_list:
                                    try:
                                        ip_obj = ipaddress.ip_address(ip)
                                        if not (ip_obj.is_loopback or ip_obj.is_link_local or ip_obj.is_multicast or ip_obj.is_reserved or ip_obj.is_private):
                                            self.ipv6_list.append(ip)
                                    except ValueError:
                                        pass
                            except Exception as e:
                                pass
                        progress_bar(title,i,total)
        except PermissionError:
            raise PermissionError("Permission denied. Run the script as Administrator/with sudo.")
        except FileNotFoundError:
            raise FileNotFoundError(f"Folder not found: {domains_folder_path}")
        except Exception as e:
            raise Exception(f"{e}")

    def block_ips(self,domains_folder_path):
        try:
            self._collect_ip_addresses(domains_folder_path)
            if self.system == "linux":
                self.linux_firewall.block_ips(self.ipv4_list,self.ipv6_list)
            elif self.system == "darwin":
                self.darwin_firewall.block_ips(self.ipv4_list,self.ipv6_list)
            elif self.system == "windows":
                self.windows_firewall.block_ips(self.ipv4_list,self.ipv6_list)
            else:
                raise RuntimeError("Unsupported operating system.")
        except PermissionError:
            raise PermissionError("Permission denied. Run the script as Administrator/with sudo.")
        except Exception as e:
            raise Exception(f"{e}")

    def unblock_ips(self):
        try:
            if self.system == "linux":
                self.linux_firewall.unblock_ips()
            elif self.system == "darwin":
                self.darwin_firewall.unblock_ips()
            elif self.system == "windows":
                self.windows_firewall.unblock_ips()
            else:
                raise RuntimeError("Unsupported operating system.")
        except PermissionError:
            raise PermissionError("Permission denied. Run the script as Administrator/with sudo.")
        except Exception as e:
            raise Exception(f"{e}")