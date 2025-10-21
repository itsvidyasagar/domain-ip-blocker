from src.constants import IPV4_RULE_NAME,IPV6_RULE_NAME
from utils.command_runner import run_command

class WindowsFirewall:
    def __init__(self):
        self.ipv4_rule_name = IPV4_RULE_NAME
        self.ipv6_rule_name = IPV6_RULE_NAME

    def block_ips(self,ipv4_list,ipv6_list):
        try:
            for ipv4 in ipv4_list:
                run_command(f'netsh advfirewall firewall add rule name="{self.ipv4_rule_name}" dir=in action=block remoteip={ipv4} enable=yes',[0,1])
            for ipv6 in ipv6_list:
                run_command(f'netsh advfirewall firewall add rule name="{self.ipv6_rule_name}" dir=in action=block remoteip={ipv6} enable=yes',[0,1])
        except PermissionError:
            raise PermissionError("Permission denied. Run the script as Administrator/with sudo.")
        except Exception as e:
            raise Exception(f"{e}")

    def unblock_ips(self):
        try:
            run_command(f'netsh advfirewall firewall delete rule name="{self.ipv4_rule_name}"',[0,1])
            run_command(f'netsh advfirewall firewall delete rule name="{self.ipv6_rule_name}"',[0,1])
        except PermissionError:
            raise PermissionError("Permission denied. Run the script as Administrator/with sudo.")
        except Exception as e:
            raise Exception(f"{e}")
