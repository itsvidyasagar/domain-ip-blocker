import os
from utils.command_runner import run_command
from utils.file_permissions import change_permissions
from src.constants import START_MARKER,END_MARKER,IPV4_PF_TABLE_NAME,IPV6_PF_TABLE_NAME,IPV4_PF_TABLE_PATH,IPV6_PF_TABLE_PATH,PF_CONF_FILE_PATH


class DarwinFirewall:
    def __init__(self):
        self.start_marker = START_MARKER
        self.end_marker = END_MARKER
        self.ipv4_pf_table_name = IPV4_PF_TABLE_NAME
        self.ipv6_pf_table_name = IPV6_PF_TABLE_NAME
        self.ipv4_pf_table_path = IPV4_PF_TABLE_PATH
        self.ipv6_pf_table_path = IPV6_PF_TABLE_PATH
        self.pf_conf_file_path = PF_CONF_FILE_PATH

    def block_ips(self,ipv4_list,ipv6_list):
        try:
            for pf_table in [self.ipv4_pf_table_path, self.ipv6_pf_table_path]:
                open(pf_table, "w").close()
                change_permissions(pf_table,0o644)
            if ipv4_list:
                with open(self.ipv4_pf_table_path, "w") as f:
                    f.write("\n".join(ipv4_list) + "\n")
                change_permissions(self.ipv4_pf_table_path,0o644)
            if ipv6_list:
                with open(self.ipv6_pf_table_path, "w") as f:
                    f.write("\n".join(ipv6_list) + "\n")
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
            raise PermissionError("Permission denied. Run the script with sudo.")
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
            raise PermissionError("Permission denied. Run the script with sudo.")
        except Exception as e:
            raise Exception(f"{e}")