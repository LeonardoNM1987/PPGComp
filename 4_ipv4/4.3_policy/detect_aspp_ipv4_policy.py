
#O que procurar?
# 1º: Quais pares prefixo não fazem prepend? (Ver Quais ases não fazem)
# 2º: Quais fazem sempre o mesmo prepend na amostragem
# 3º: 

#Dados que preciso, nos resultados e nas respectivas linhas:
# 18 - Conjunto de prefixos que fazem prepend na Origem
# 19 - Dicionario que associa ASes com os prefixos anunciados que fazem prepend na Origem
# 20 - Dicionario que lista quais ASes anunciam quais prefixos

import os
import datetime
import sys
import ast #modulo de conversao de str para dict
from collections import Counter

inicioTotal = datetime.datetime.now()

#  sourceBatch = [
#     '3_results/rib.20110320.0000_ipv4_results.txt'
# ]
# sourceBatch = [
#     '3_results/rib.20110320.0000_ipv4_results.txt',        
#     '3_results/rib.20130320.0000_ipv4_results.txt',        
#     '3_results/rib.20150320.0000_ipv4_results.txt',        
#     '3_results/rib.20170320.0000_ipv4_results.txt',        
#     '3_results/rib.20200320.0000_ipv4_results.txt'        
# ]

pasta = 'ipv4/3_results/main'   # AJUSTAR PASTA DE OUTPUT TAMBÉM!!
#pasta = r'C:\Ribs\2ndsp2011a2020'    # AJUSTAR PASTA DE OUTPUT TAMBÉM!!
# Lista para armazenar os caminhos dos arquivos
sourceBatch = []

# Listar os arquivos na pasta
for nome_arquivo in os.listdir(pasta):
    # Criar o caminho completo para o arquivo
    caminho_completo = os.path.join(pasta, nome_arquivo)
    # Adicionar o caminho à lista
    sourceBatch.append(caminho_completo)

# Exibir a lista de caminhos
print(f'Pasta com Ribs localizada e possui {len(sourceBatch)} arquivos.\n')



#dados já obtidos:
uniquePrefixes = set()          # todos prefixos unicos observados
prepPrefixAll = set()           # todos prefixos com algum prepend
prepPrefixLen1 = set()          # prefixos que fizeram prep tamanho 1
prepPrefixLen2 = set()          # prefixos que fizeram prep tamanho 2
prepPrefixLen3 = set()          # prefixos que fizeram prep tamanho 3
prepPrefixLen4Plus = set()      # prefixos que fizeram prep tamanho 4+
noPrependPrefixes = set()       # prefixos sem Prepend (prefixos unicos subtraindo os com algum prepend)

#dados para descobrir:
uniformPrefix = set()           # prefixos de politica uniforme
binaryPrefix = set()            # prefixos de politica binaria
diversePrefix = set()           # prefixos de politica diversa  


# 1: no-prepend: no visible prepended route; 
# 2: uniform: the only visible prepend size is 𝑁, where 𝑁 > 0;
# 3: binary: visible routes either have prepend size 𝑀 or 𝑁, where 𝑀, 𝑁 ≥ 0 and 𝑀 ≠ 𝑁; 
# 4: diverse: the number of different prepend sizes in the visible routes exceeds two.



def classificar_prefixos(*conjuntos):
    # Criar um contador para todos os prefixos nos conjuntos
    contador_prefixos = Counter()

    # Atualizar o contador com cada prefixo encontrado em cada conjunto
    for conjunto in conjuntos:
        for prefixo in conjunto:
            contador_prefixos[prefixo] += 1

    # Classificar os prefixos com base na contagem de frequência
    politica_uniforme = {p for p, count in contador_prefixos.items() if count == 1}
    prefixos_binarios = {p for p, count in contador_prefixos.items() if count == 2}
    prefixos_diversos = {p for p, count in contador_prefixos.items() if count > 2}

    return politica_uniforme, prefixos_binarios, prefixos_diversos


for resultado in sourceBatch: 
    inicio = datetime.datetime.now() 
    print(f'ANALISANDO SNAPSHOT: {resultado}......')    
    with open(resultado, 'r') as arquivo:                                                                       
        linhaEspecifica = arquivo.readlines()        
        prepPrefixAll = ast.literal_eval(linhaEspecifica[17])
        uniquePrefixes = ast.literal_eval(linhaEspecifica[21])        
        prepPrefixLen1 = ast.literal_eval(linhaEspecifica[22])
        prepPrefixLen2 = ast.literal_eval(linhaEspecifica[23])
        prepPrefixLen3 = ast.literal_eval(linhaEspecifica[24])
        prepPrefixLen4Plus = ast.literal_eval(linhaEspecifica[25])
        noPrependPrefixes = uniquePrefixes - prepPrefixAll
      
        # Chamar a função com os conjuntos de dados
        politica_uniforme, prefixos_binarios, prefixos_diversos = classificar_prefixos(
            prepPrefixAll, 
            prepPrefixLen1, 
            prepPrefixLen2, 
            prepPrefixLen3, 
            prepPrefixLen4Plus)

        # print('Política noPrepend:',len(noPrependPrefixes))
        # print("Política Uniforme:", len(politica_uniforme))
        # print("Prefixos Binários:", len(prefixos_binarios))
        # print("Prefixos Diversos:", len(prefixos_diversos))
        # print("-------------------------------------------")

       
    nomeOriginal = os.path.basename(resultado)
    nomeSemExtensao, extensao = os.path.splitext(nomeOriginal)
    output = (f'ipv4/5_policy/results/main/{nomeSemExtensao}_policyResults.txt')
    #output = (f'ipv4/5_policy/resultados_teste/{nomeSemExtensao}_policyResults.txt')
    with open(output, 'w') as arquivoResultados:                      
        arquivoResultados.write(f'{noPrependPrefixes}\n')       #0    
        arquivoResultados.write(f'{politica_uniforme}\n')       #1
        arquivoResultados.write(f'{prefixos_binarios}\n')       #2
        arquivoResultados.write(f'{prefixos_diversos}\n')       #3
        arquivoResultados.write(f'{len(uniquePrefixes)}\n')     #5
        arquivoResultados.write(f'{len(noPrependPrefixes)}\n')  #6
        arquivoResultados.write(f'{len(politica_uniforme)}\n')  #7
        arquivoResultados.write(f'{len(prefixos_binarios)}\n')  #8
        arquivoResultados.write(f'{len(prefixos_diversos)}\n')  #9

    


    fim = datetime.datetime.now()                                       #Marca o fim da execução
    tempo_execucao = fim - inicio
    tempo_formatado = str(tempo_execucao).split('.')[0]                 #Remove a parte dos microssegundos
    print(f"Os resultados foram salvos em: {output}")
    print(f'Análise concluída com duranção de: {tempo_formatado}')   
    print('--------------------------------------------------------------')
    
#fim_for
#print('##########################################################')
fimTotal = datetime.datetime.now()  
tempo_execucao_total = fimTotal - inicioTotal
tempo_execucao_total_format = str(tempo_execucao_total).split('.')[0]
print(f"Tempo de execução total das {len(sourceBatch)} análises: {tempo_execucao_total_format}")
