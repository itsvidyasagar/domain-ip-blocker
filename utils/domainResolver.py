import socket

def resolve_ips(domain):
    ipv4_list = set()
    ipv6_list = set()
    try:
        for res in socket.getaddrinfo(domain, None):
            family, _, _, _, sockaddr = res
            if family == socket.AF_INET:
                ipv4_list.add(sockaddr[0])
            elif family == socket.AF_INET6:
                ipv6_list.add(sockaddr[0])
    except socket.gaierror:
        print(f"Could not resolve domain: {domain}")
    return ipv4_list, ipv6_list