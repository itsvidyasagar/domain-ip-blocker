from src.constants import IPV4_SET_NAME,IPV6_SET_NAME
from utils.command_runner import run_command

class LinuxFirewall:
    def __init__(self):
        self.ipv4_set_name = IPV4_SET_NAME
        self.ipv6_set_name = IPV6_SET_NAME

    def block_ips(self,ipv4_list,ipv6_list):
        try:
            run_command(f"sudo ipset create {self.ipv4_set_name} hash:ip family inet -exist")
            run_command(f"sudo ipset create {self.ipv6_set_name} hash:ip family inet6 -exist")
            for ipv4 in ipv4_list:
                run_command(f"sudo ipset add {self.ipv4_set_name} {ipv4} -exist")
            for ipv6 in ipv6_list:
                run_command(f"sudo ipset add {self.ipv6_set_name} {ipv6} -exist")
            run_command(f"sudo iptables -C INPUT -m set --match-set {self.ipv4_set_name} src -j DROP || sudo iptables -I INPUT -m set --match-set {self.ipv4_set_name} src -j DROP")
            run_command(f"sudo ip6tables -C INPUT -m set --match-set {self.ipv6_set_name} src -j DROP || sudo ip6tables -I INPUT -m set --match-set {self.ipv6_set_name} src -j DROP")
            run_command("sudo netfilter-persistent save")
        except PermissionError:
            raise PermissionError("Permission denied. Run the script as Administrator/with sudo.")
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
            raise PermissionError("Permission denied. Run the script as Administrator/with sudo.")
        except Exception as e:
            raise Exception(f"{e}")
