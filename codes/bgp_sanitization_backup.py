#Este codigo ira remover as rotas bogon e prefixos menores que /8 do arquivo de entrada
#Do arquivo original de rotas é gerado um novo com o termo '_sanitized' no final do nome do arquivo

import ipaddress
import os

caminho_bogons = 'bogons_list.txt'
#source = 'source/rib.20231001.0000_rotasReduzidas.txt' 


# Carrega a lista de rotas bogon do arquivo
def carregar_bogons(caminho_bogons):
    with open(caminho_bogons, 'r') as arquivo:
        bogons = [linha.strip() for linha in arquivo.readlines()]
    return bogons

# Carrega a lista de bogons
carregar_bogons('bogons_list.txt')


#print("Processamento concluído. As rotas válidas foram salvas em:", caminho_saida)
