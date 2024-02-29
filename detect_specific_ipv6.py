import ipaddress

def analisar_ipv6(arquivo):
    with open(arquivo, 'r') as f:
        for linha in f:
            try:
                partes = linha.strip().split('|')
                prefixo = partes[1]
                ip_network = ipaddress.ip_network(prefixo, strict=False)

                if ip_network.version == 6:
                    print(linha.strip())
            except ValueError:
                continue

arquivo_ipv6 = 'validadores/rib_IPv4_IPv6_validador02_sanitized.txt'
analisar_ipv6(arquivo_ipv6)



