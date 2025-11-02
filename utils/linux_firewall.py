from src.constants import IPV4_SET_NAME,IPV6_SET_NAME
from utils.command_runner import run_command
from utils.progress_bar import progress_bar

class LinuxFirewall:
    def __init__(self):
        self.ipv4_set_name = IPV4_SET_NAME
        self.ipv6_set_name = IPV6_SET_NAME

    def block_ips(self,ipv4_list,ipv6_list):
        try:
            run_command(f"sudo ipset create {self.ipv4_set_name} hash:ip family inet -exist")
            run_command(f"sudo ipset create {self.ipv6_set_name} hash:ip family inet6 -exist")
            total = len(ipv4_list)
            title = "Applying IPv4 rules"
            for i,ipv4 in enumerate(ipv4_list,1):
                run_command(f"sudo ipset add {self.ipv4_set_name} {ipv4} -exist")
                progress_bar(title,i,total)
            total = len(ipv6_list)
            title = "Applying IPv6 rules"
            for i,ipv6 in enumerate(ipv6_list,1):
                run_command(f"sudo ipset add {self.ipv6_set_name} {ipv6} -exist")
                progress_bar(title,i,total)
            run_command(f"sudo iptables -C INPUT -m set --match-set {self.ipv4_set_name} src -j DROP || sudo iptables -I INPUT -m set --match-set {self.ipv4_set_name} src -j DROP")
            run_command(f"sudo ip6tables -C INPUT -m set --match-set {self.ipv6_set_name} src -j DROP || sudo ip6tables -I INPUT -m set --match-set {self.ipv6_set_name} src -j DROP")
            run_command("sudo netfilter-persistent save")
        except PermissionError:
            raise PermissionError("Permission denied. Run the script with sudo.")
        except Exception as e:
            raise Exception(f"{e}")
    
    def unblock_ips(self):
        try:
            run_command(f"sudo iptables -D INPUT -m set --match-set {self.ipv4_set_name} src -j DROP",[0,1,2])
            run_command(f"sudo ip6tables -D INPUT -m set --match-set {self.ipv6_set_name} src -j DROP",[0,1,2])
            run_command(f"sudo ipset destroy {self.ipv4_set_name}",[0,1])
            run_command(f"sudo ipset destroy {self.ipv6_set_name}",[0,1])
            run_command("sudo netfilter-persistent save")
        except PermissionError:
            raise PermissionError("Permission denied. Run the script with sudo.")
        except Exception as e:
            raise Exception(f"{e}")
