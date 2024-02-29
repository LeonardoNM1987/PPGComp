#Este codigo ira remover as rotas bogon e prefixos menores que /8 do arquivo de entrada
#Do arquivo original de rotas é gerado um novo com o termo '_sanitized' no final do nome do arquivo

import ipaddress
import os

caminho_bogons = 'bogons_list.txt'
source = 'source/rib.20231001.0000_rotasReduzidas.txt' 


# Carrega a lista de rotas bogon do arquivo
def carregar_bogons(caminho_bogons):
    with open(caminho_bogons, 'r') as arquivo:
        bogons = [linha.strip() for linha in arquivo.readlines()]
    return bogons

# Carrega a lista de bogons
bogons = carregar_bogons(caminho_bogons)

# Verifica se a rota é bogon ou tem prefixo menor que /8
def filtrar_rotas(rota, bogons):
    try:
        # Extrai o prefixo da rota
        prefixo = rota.split('|')[1]
        rede = ipaddress.ip_network(prefixo, strict=False)
        
        # Verifica se o prefixo é menor que /8
        if rede.prefixlen < 8:
            return False
        
        # Verifica se a rota é bogon
        for bogon in bogons:
            if rede.overlaps(ipaddress.ip_network(bogon, strict=False)):
                return False
        return True
    except ValueError:
        # Em caso de erro na conversão para rede IP, considera inválido
        return False
  

# Gerando o caminho do arquivo de saída
nome_base, extensao = os.path.splitext(source)
caminho_saida = f"source/{nome_base}_sanitized{extensao}"



# Processa o arquivo de dados de rede
with open(source, 'r') as arquivo_entrada, open(caminho_saida, 'w') as arquivo_saida:
    for linha in arquivo_entrada:
        if filtrar_rotas(linha, bogons):
            arquivo_saida.write(linha)

print("Processamento concluído. As rotas válidas foram salvas em:", caminho_saida)