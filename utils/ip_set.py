import ipaddress
from utils.command_runner import run_command

class IpSet:
    def __init__(self,ip_set_name,ip_family):
        self.ip_set_name = ip_set_name
        self.ip_family = ip_family
        try:
            run_command(f"sudo ipset create {self.ip_set_name} hash:ip family {self.ip_family} -exist")
        except PermissionError:
            raise PermissionError("Permission denied. Run the script as Administrator/with sudo.")
        except Exception as e:
            raise Exception(f"{e}")

    def add_ip(self,ip):
        try:
            run_command(f"sudo ipset add {self.ip_set_name} {ip} -exist")
            print(ip)
        except PermissionError:
            raise PermissionError("Permission denied. Run the script as Administrator/with sudo.")
        except Exception as e:
            raise Exception(f"{e}")
    
    def flush(self):
        try:
            run_command(f"sudo ipset flush {self.ip_set_name}")
        except RuntimeError:
            # print(f"Ipset '{self.ip_set_name}' does not exist, skipping.")
            pass
        except PermissionError:
            raise PermissionError("Permission denied. Run the script as Administrator/with sudo.")
        except Exception as e:
            raise Exception(f"{e}")
    
    def destroy(self):
        try:
            run_command(f"sudo ipset destroy {self.ip_set_name}")
        except RuntimeError:
            # print(f"Ipset '{self.ip_set_name}' does not exist, skipping.")
            pass
        except PermissionError:
            raise PermissionError("Permission denied. Run the script as Administrator/with sudo.")
        except Exception as e:
            raise Exception(f"{e}")