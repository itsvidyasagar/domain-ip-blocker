import platform

TOOL_NAME = "domain-ip-blocker"
START_MARKER = f"# >>> {TOOL_NAME.upper()} START <<< (don't edit this comment) \n"
END_MARKER = f"# >>> {TOOL_NAME.upper()} END <<< (don't edit this comment) \n"
SYSTEM = platform.system().lower()
if SYSTEM == "windows":
    HOSTS_FILE_PATH = r"C:\Windows\System32\drivers\etc\hosts"
else:
    HOSTS_FILE_PATH = "/etc/hosts"
DOMAINS_FOLDER_PATH = "config"
DNS_RESOLVER_LIFE_TIME = 0.5
IPV4_SET_NAME = f"{TOOL_NAME}-ipv4-set"
IPV6_SET_NAME = f"{TOOL_NAME}-ipv6-set"
IPV4_PF_TABLE_NAME = f"{TOOL_NAME}-ipv4-pf-table"
IPV6_PF_TABLE_NAME = f"{TOOL_NAME}-ipv6-pf-table"
IPV4_PF_TABLE_PATH = f"/etc/{IPV4_PF_TABLE_NAME}.txt"
IPV6_PF_TABLE_PATH = f"/etc/{IPV6_PF_TABLE_NAME}.txt"
PF_CONF_FILE_PATH = "/etc/pf.conf"
IPV4_RULE_NAME = f"{TOOL_NAME}-ipv4-rule-name"
IPV6_RULE_NAME = f"{TOOL_NAME}-ipv6-rule-name"