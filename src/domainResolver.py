import socket

def resolveIps(domain):
    ipv4List = set()
    ipv6List = set()
    try:
        for res in socket.getaddrinfo(domain, None):
            family, _, _, _, sockaddr = res
            if family == socket.AF_INET:
                ipv4List.add(sockaddr[0])
            elif family == socket.AF_INET6:
                ipv6List.add(sockaddr[0])
    except socket.gaierror:
        print(f"Could not resolve domain: {domain}")
    return ipv4List, ipv6List