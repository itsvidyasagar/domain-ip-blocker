import os
import ipaddress
from utils.ip_set import IpSet
from utils.domain_resolver import resolve_ips
from utils.command_runner import run_command
from utils.file_permissions import change_permissions
from src.constants import SYSTEM

class IpManager:
    def __init__(self):
        self.system = SYSTEM
        self.ipv4_list = []
        self.ipv6_list = []
        if self.system == "linux":
            from src.constants import IPV4_SET_NAME,IPV6_SET_NAME
            self.ipv4_set_name = IPV4_SET_NAME
            self.ipv6_set_name = IPV6_SET_NAME
            self.ipv4_set = IpSet(self.ipv4_set_name,"inet")
            self.ipv6_set = IpSet(self.ipv6_set_name,"inet6")
        elif self.system == "darwin":
            from src.constants import START_MARKER,END_MARKER,IPV4_PF_TABLE_NAME,IPV6_PF_TABLE_NAME,IPV4_PF_TABLE_PATH,IPV6_PF_TABLE_PATH,PF_CONF_FILE_PATH
            self.start_marker = START_MARKER
            self.end_marker = END_MARKER
            self.ipv4_pf_table_name = IPV4_PF_TABLE_NAME
            self.ipv6_pf_table_name = IPV6_PF_TABLE_NAME
            self.ipv4_pf_table_path = IPV4_PF_TABLE_PATH
            self.ipv6_pf_table_path = IPV6_PF_TABLE_PATH
            self.pf_conf_file_path = PF_CONF_FILE_PATH
        elif self.system == "windows":
            from src.constants import IPV4_RULE_NAME,IPV6_RULE_NAME
            self.ipv4_rule_name = IPV4_RULE_NAME
            self.ipv6_rule_name = IPV6_RULE_NAME
        else:
            raise RuntimeError("Unsupported operating system.")

    def _list_domain_ips(self,domains_folder_path):
        try:
            txt_files = [f for f in os.listdir(domains_folder_path) if f.endswith(".txt")]
            for file_name in txt_files:
                file_path = os.path.join(domains_folder_path, file_name)
                with open(file_path, "r") as f:
                    lines = f.readlines()
                    total_lines = len(lines)
                    for line_number, line in enumerate(lines, start=1):
                        line = line.strip()
                        if line and not line.startswith("#"):
                            domain = line.split()[-1]
                            try:
                                ipv4_list, ipv6_list = resolve_ips(domain)
                                for ip in ipv4_list:
                                    try:
                                        ip_obj = ipaddress.ip_address(ip)
                                        if not (ip_obj.is_loopback or ip_obj.is_link_local or ip_obj.is_multicast or ip_obj.is_reserved or ip_obj.is_private):
                                            self.ipv4_list.append(ip)
                                    except ValueError:
                                        # print(f"Invalid IPv4 skipped: {ip}")
                                        pass
                                for ip in ipv6_list:
                                    try:
                                        ip_obj = ipaddress.ip_address(ip)
                                        if not (ip_obj.is_loopback or ip_obj.is_link_local or ip_obj.is_multicast or ip_obj.is_reserved or ip_obj.is_private):
                                            self.ipv6_list.append(ip)
                                    except ValueError:
                                        # print(f"[Invalid IPv6 skipped: {ip}")
                                        pass
                                # print(f"[{line_number}/{total_lines}]: {domain} Resolved : {len(ipv4_list)} IPv4, {len(ipv6_list)} IPv6")
                            except Exception as e:
                                # print(f"[{line_number}/{total_lines}]: {e}")
                                pass
        except PermissionError:
            raise PermissionError("Permission denied. Run the script as Administrator/with sudo.")
        except FileNotFoundError:
            raise FileNotFoundError(f"Folder not found: {domains_folder_path}")
        except Exception as e:
            raise Exception(f"{e}")
    
    def _linux_block_ips(self):
        try:
            self.ipv4_set = IpSet(self.ipv4_set_name,"inet")
            self.ipv6_set = IpSet(self.ipv6_set_name,"inet6")
            for ipv4 in self.ipv4_list:
                self.ipv4_set.add_ip(ipv4)
            for ipv6 in self.ipv6_list:
                self.ipv6_set.add_ip(ipv6)
            run_command(f"sudo iptables -C INPUT -m set --match-set {self.ipv4_set_name} src -j DROP || sudo iptables -I INPUT -m set --match-set {self.ipv4_set_name} src -j DROP")
            run_command(f"sudo ip6tables -C INPUT -m set --match-set {self.ipv6_set_name} src -j DROP || sudo ip6tables -I INPUT -m set --match-set {self.ipv6_set_name} src -j DROP")
            run_command("sudo netfilter-persistent save")
        except PermissionError:
            raise PermissionError("Permission denied. Run the script as Administrator/with sudo.")
        except Exception as e:
            raise Exception(f"{e}")
        
    def _linux_unblock_ips(self):
        try:
            run_command(f"sudo iptables -D INPUT -m set --match-set {self.ipv4_set_name} src -j DROP",[0,1])
            run_command(f"sudo ip6tables -D INPUT -m set --match-set {self.ipv6_set_name} src -j DROP",[0,1])
            self.ipv4_set.destroy()
            self.ipv6_set.destroy()
            run_command("sudo netfilter-persistent save")
        except PermissionError:
            raise PermissionError("Permission denied. Run the script as Administrator/with sudo.")
        except Exception as e:
            raise Exception(f"{e}")

    def _darwin_block_ips(self):
        try:
            for pf_table in [self.ipv4_pf_table_path, self.ipv6_pf_table_path]:
                open(pf_table, "w").close()
                change_permissions(pf_table,0o644)
            if self.ipv4_list:
                with open(self.ipv4_pf_table_path, "w") as f:
                    f.write("\n".join(self.ipv4_list) + "\n")
                change_permissions(self.ipv4_pf_table_path,0o644)
            if self.ipv6_list:
                with open(self.ipv6_pf_table_path, "w") as f:
                    f.write("\n".join(self.ipv6_list) + "\n")
                change_permissions(self.ipv6_pf_table_path,0o644)
            if not os.path.exists(self.pf_conf_file_path):
                open(self.pf_conf_file_path, "w").close()
                change_permissions(self.pf_conf_file_path,0o644)
            with open(self.pf_conf_file_path, "r") as f:
                conf_lines = f.readlines()
            block_rules = [
                self.start_marker,
                f"table <{self.ipv4_pf_table_name}> persist file \"{self.ipv4_pf_table_path}\"\n",
                f"block in quick from <{self.ipv4_pf_table_name}> to any\n",
                f"table <{self.ipv6_pf_table_name}> persist file \"{self.ipv6_pf_table_path}\"\n",
                f"block in quick from <{self.ipv6_pf_table_name}> to any\n",
                self.end_marker
            ]
            conf_lines.extend(block_rules)
            with open(self.pf_conf_file_path, "w") as f:
                f.writelines(conf_lines)
            change_permissions(self.pf_conf_file_path,0o644)
            run_command("sudo pfctl -f /etc/pf.conf")
            run_command("sudo pfctl -e",[0,1])
        except PermissionError:
            raise PermissionError("Permission denied. Run the script as Administrator/with sudo.")
        except Exception as e:
            raise Exception(f"{e}")
        
    def _darwin_unblock_ips(self):
        try:
            for pf_table in [self.ipv4_pf_table_path, self.ipv6_pf_table_path]:
                if os.path.exists(pf_table):
                    os.remove(pf_table)
            if os.path.exists(self.pf_conf_file_path):
                with open(self.pf_conf_file_path, "r") as f:
                    conf_lines = f.readlines()
                inside_snippet = False
                new_conf = []
                for line in conf_lines:
                    if line == self.start_marker:
                        inside_snippet = True
                        continue
                    if line == self.end_marker:
                        inside_snippet = False
                        continue
                    if not inside_snippet:
                        new_conf.append(line)
                with open(self.pf_conf_file_path, "w") as f:
                    f.writelines(new_conf)
                change_permissions(self.pf_conf_file_path,0o644)
                run_command("sudo pfctl -f /etc/pf.conf")
                run_command("sudo pfctl -e",[0,1])
        except PermissionError:
            raise PermissionError("Permission denied. Run the script as Administrator/with sudo.")
        except Exception as e:
            raise Exception(f"{e}")
        
    def _windows_block_ips(self):
        try:
            for ip in self.ipv4_list:
                run_command(f'netsh advfirewall firewall add rule name="{self.ipv4_rule_name}" dir=in action=block remoteip={ip} enable=yes',[0,1])
            for ip in self.ipv6_list:
                run_command(f'netsh advfirewall firewall add rule name="{self.ipv6_rule_name}" dir=in action=block remoteip={ip} enable=yes',[0,1])
        except PermissionError:
            raise PermissionError("Permission denied. Run the script as Administrator/with sudo.")
        except Exception as e:
            raise Exception(f"{e}")

    def _windows_unblock_ips(self):
        try:
            run_command(f'netsh advfirewall firewall delete rule name="{self.ipv4_rule_name}"',[0,1])
            run_command(f'netsh advfirewall firewall delete rule name="{self.ipv6_rule_name}"',[0,1])
        except PermissionError:
            raise PermissionError("Permission denied. Run the script as Administrator/with sudo.")
        except Exception as e:
            raise Exception(f"{e}")


    def block_ips(self,domains_folder_path):
        try:
            self.unblock_ips()
            self._list_domain_ips(domains_folder_path)
            if self.system == "linux":
                self._linux_block_ips()
            elif self.system == "darwin":
                self._darwin_block_ips()
            elif self.system == "windows":
                self._windows_block_ips()
            else:
                raise RuntimeError("Unsupported operating system.")
        except PermissionError:
            raise PermissionError("Permission denied. Run the script as Administrator/with sudo.")
        except Exception as e:
            raise Exception(f"{e}")

    def unblock_ips(self):
        try:
            if self.system == "linux":
                self._linux_unblock_ips()
            elif self.system == "darwin":
                self._darwin_unblock_ips()
            elif self.system == "windows":
                self._windows_unblock_ips()
            else:
                raise RuntimeError("Unsupported operating system.")
        except PermissionError:
            raise PermissionError("Permission denied. Run the script as Administrator/with sudo.")
        except Exception as e:
            raise Exception(f"{e}")