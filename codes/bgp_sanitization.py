#Este codigo ira remover as rotas bogon e prefixos menores que /8 do arquivo de entrada
#Do arquivo original de rotas é gerado um novo com o termo '_sanitized' no final do nome do arquivo

import ipaddress
import os
import datetime


caminho_bogons = './codes/bogonsList.txt'
snap01 = 'source/rib.20170320.0000.txt' 
snap02 = 'source/rib.20200320.0000.txt' 
#source = 'validadores/validador_IPv4_01.txt'   # ARQUIVO PARA VALIDAÇÃO  

def sanitizar(input):

    source = input

    inicio = datetime.datetime.now() # Marca o início da execução

    print(f'\n Iniciando sanitização do arquivo: {source}.....\n')

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
    caminho_saida = f"{nome_base}_sanitized{extensao}"



    # Processa o arquivo de dados de rede
    with open(source, 'r') as arquivo_entrada, open(caminho_saida, 'w') as arquivo_saida:
        for linha in arquivo_entrada:
            if filtrar_rotas(linha, bogons):
                arquivo_saida.write(linha)

    print("\nProcessamento concluído. As rotas válidas foram salvas em:", caminho_saida,"\n")

    fim = datetime.datetime.now() # Marca o fim da execução
    tempo_execucao = fim - inicio
    tempo_formatado = str(tempo_execucao).split('.')[0] # Remove a parte dos microssegundos
    print(f"Tempo de execução: {tempo_formatado}\n")


sanitizar(snap01)
sanitizar(snap02)