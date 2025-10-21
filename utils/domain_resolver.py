import dns.resolver
from src.constants import DNS_RESOLVER_LIFE_TIME

def resolve_ips(domain):
    ipv4_list = set()
    ipv6_list = set()
    try:
        try:
            answers = dns.resolver.resolve(domain, 'A', lifetime = DNS_RESOLVER_LIFE_TIME)
            for rdata in answers:
                ipv4_list.add(rdata.address)
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            pass
        try:
            answers = dns.resolver.resolve(domain, 'AAAA',lifetime=DNS_RESOLVER_LIFE_TIME)
            for rdata in answers:
                ipv6_list.add(rdata.address)
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            pass
    except dns.exception.DNSException:
        raise RuntimeError(f"Could not resolve domain: {domain}")

    return ipv4_list, ipv6_list