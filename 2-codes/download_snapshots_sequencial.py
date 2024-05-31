#snapshots sendo baixados em:
# E:\Mestrado\Ribs\xxxxxxx

import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup


def download_arquivos(url_diretorio, pasta_destino):
    # Enviar uma solicitação GET para o URL do diretório
    resposta = requests.get(url_diretorio)
    
    # Verificar se a solicitação foi bem-sucedida (código de status 200)
    if resposta.status_code == 200:
        # Parsear o HTML da página
        soup = BeautifulSoup(resposta.content, 'html.parser')
        
        # Encontrar todos os links para arquivos .bz2
        links_bz2 = [link.get('href') for link in soup.find_all('a') if link.get('href').endswith('.bz2')]
        
        # Baixar cada arquivo .bz2
        for link_bz2 in links_bz2:
            # Construir o URL completo do arquivo
            url_arquivo = urljoin(url_diretorio, link_bz2)
            
            # Extrair o nome do arquivo do URL
            nome_arquivo = os.path.basename(link_bz2)
            
            # Caminho completo do arquivo
            caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)
            
            # Baixar o arquivo
            download_arquivo(url_arquivo, caminho_arquivo)
    else:
        print("O download falhou. Código de status:", resposta.status_code)

def download_arquivo(url, nome_arquivo):
    # Enviar uma solicitação GET para o URL
    resposta = requests.get(url)
    
    # Verificar se a solicitação foi bem-sucedida (código de status 200)
    if resposta.status_code == 200:
        # Abrir o arquivo em modo de escrita binária e escrever o conteúdo da resposta nele
        with open(nome_arquivo, 'wb') as arquivo:
            arquivo.write(resposta.content)
        print(f"Arquivo baixado com sucesso como {nome_arquivo}")
    else:
        print("O download falhou. Código de status:", resposta.status_code)

# URL do diretório contendo os arquivos .bz2
#url_diretorio = "https://routeviews.org/route-views.linx/bgpdata/2004.12/RIBS/"
url_diretorio = "https://routeviews.org/route-views.saopaulo/bgpdata/2011.03/RIBS/"
# Pasta de destino para salvar os arquivos
pasta_destino = r"E:\Mestrado\Ribs\sp2011"

# Chamar a função para baixar os arquivos
download_arquivos(url_diretorio, pasta_destino)




#url = "https://routeviews.org/route-views.linx/bgpdata/2004.12/RIBS/rib.20041202.0747.bz2"