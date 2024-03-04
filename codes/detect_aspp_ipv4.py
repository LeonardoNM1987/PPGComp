#Sanitizar o arquivo de entrada com o 'bgp_sanitization.py' antes das etapas abaixo;
#
# OPERAÇÕES REALIZADAS COM ESTE CÓDIGO:
# 1. Listar ASes que fazem prepend na prependOrigem 
# 2. Listar ASes que fazem prepend prependIntermediário 
# 3. Listar ASes únicos visualizados no arquivo de entrada 
# 4. Listar vizinhos que cada AS possui
#
# ESTE CÓDIGO ANALISA APENAS ROTAS IPv4
# PARA ANALISE DE ROTAS IPv6, EXECUTAR O 'detect_aspp_ipv6.py'

import datetime
import os

bogonsList = './codes/bogonsList.txt'                                  # lista de rotas bogon
#source = 'validadores/validador_IPv4_01.txt'                           # ARQUIVO PARA VALIDAÇÃO
source = 'source/rib.20231001.0000_rotasReduzidas.txt'      # ARQUIVO PARA ANÁLISE

prependOrigem = []                                                     # contabiliza prepends de prependOrigem
prependIntermed = []                                                   # contabiliza prepends prependIntermediarios
prependTotais = 0                                                      # contabiliza visualizações de prepend em geral(apenas debug)
vizinhos = {}                                                          # contabiliza todos vizinhos que cada ASN teve
asesTotais = []                                                        # contabiliza todos ASes unicos vistos na análise
asPathUnico = set()                                                    # conjunto para armazenar AS_PATHs únicos


################################################ FUNCOES ################################################

def listaVizinhos(dicionario, chave, valor):                           # Aqui a funcao analisa quem é vizinho de quem
    if chave != valor:                                                 # Ignorar o próprio ASN como vizinho dele mesmo
        if chave in dicionario:
            dicionario[chave].add(valor)                               # Adicionar em um conjunto para evitar duplicatas
        else:
            dicionario[chave] = {valor} 



def contaPrepend(aspath): 
    #print(f'AS Path em análise: {aspath}\n')                          # DEBUG    
    asn = aspath                                                       # quebra em vários asn   
    global asesTotais
    global prependOrigem                                               # conta os de prependOrigem
    global prependIntermed                                             # conta os prependIntermediarios
    global prependTotais                                               # conta aspp em geral(apenas debug)
    i=1                                                                # indica posição do asn no path analisado
    trigger = True ;                                                   #enquanto ligado contabiliza o asn como de prependOrigem/ se desligado contabiliza como prependIntermediario
    for item in range(len(asn)):                                       #aqui começa a verificação no path    

        while(i<len(asn)):    
            
            if (asn[-i] not in asesTotais):                    
                asesTotais.append(asn[-i])            
            #print(f'Testando : {asn[-i]} com {asn[-(i+1)]}...')  
            if (asn[-i] == asn[-(i+1)]):                               #compara asn de trás para frente 
                #print(f'Comparando {asn[-i]} com {asn[-(i+1)]}...')   # DEBUG
                prependTotais+=1
                #print(f'{asn[-i]} é igual à {asn[-(i+1)]}')           # DEBUG 
                if (trigger==True):                                    #trata como prependOrigem
                    if (asn[-i] not in prependOrigem):                    
                        prependOrigem.append(asn[-i])
                        #print(f'{asn[-i]} adicionado à lista de Prepends de prependOrigem') # DEBUG
                else:                                                  #trata como prependIntermediario
                    if (asn[-i] not in prependIntermed):
                        prependIntermed.append(asn[-i])
                        #print(f'{asn[-i]} adicionado à lista de Prepends prependIntermediarios') # DEBUG
            else:
                #print(f'Comparando {asn[-i]} com {asn[-(i+1)]}...')   # DEBUG
                if(trigger):
                    trigger = False
                    #print('\n>>Trigger agora virou false<<')          # DEBUG
            i+=1
            # print('----------------------------------------------')  # DEBUG

################################################ EXECUÇÃO #################################################

inicio = datetime.datetime.now()                                       # Marca o início da execução


print('---------------------------  ANALISANDO SNAPSHOT... ---------------------------')
with open(source, 'r') as arquivo:    
    linhas = 0                                                    #contador de linhas
    for linha in arquivo:                                         #ler linha por linha    
        linhas +=1
        coluna = linha.split('|')                                 #quebra a linha em colunas
        if ':' not in coluna[1]:                                  #Esse if verifica se é rota ipv4. Senão for, pula linha. 
            if len(coluna)>=3:             
                asPath = coluna[2].split()                         #divide os ases no as-path                    
                as_path_str = ' '.join(asPath)                     #Cria uma string única para o AS_PATH                
                if as_path_str not in asPathUnico:                 #Verifica se o AS_PATH é único(evita contar rotas duplicadas em coletores diferentes)
                    asPathUnico.add(as_path_str)                   #Adiciona o AS_PATH ao conjunto de únicos
                    contaPrepend(asPath)                           #Processa o AS_PATH
                    asn = asPath                                   #quebra o path em vários asn 
                    for i, num in enumerate(asn):                  #Iterar pela lista de ASes
                        if i > 0:                                  #Certificar de não ser o primeiro elemento
                            listaVizinhos(vizinhos, num, asn[i-1])    
                        # Vizinho seguinte
                        if i < len(asn)-1:                         #Certificar de não ser o último elemento
                            listaVizinhos(vizinhos, num, asn[i+1])              
            
            else:
                print(f'\nERRO: Não foi possível ler a linha {linhas}! Passando para a próxima...\n')
        #else:            
            #print(f'Rota ignorada:{coluna[1]} | linha {linhas}')  #Aqui só é avisado no prompt a rota ignorada
            


fim = datetime.datetime.now()                                       #Marca o fim da execução
tempo_execucao = fim - inicio
tempo_formatado = str(tempo_execucao).split('.')[0]                 #Remove a parte dos microssegundos

############################### RESULTADOS NO PROMPT ##############################
print('Análise concluída com sucesso!')
print(f"Tempo de execução: {tempo_formatado}")
# print('--------------------------  RESULTADOS DA ANALISE  --------------------------')
# print(f'\nQuantas vezes se viu prepend: {prependTotais}\n')
# print(f'Ases que fazem prepend na prependOrigem: {sorted(prependOrigem, key=int)}\n')
# print(f'ASes que fazem prepend de forma prependIntermediária: {sorted(prependIntermed,key=int)}\n')
# print(f'ASes únicos visualizados: {sorted(asesTotais, key=int)}\n')
# print(f'ASes únicos visualizados: {asesTotais}\n')
# vizinhos_formatados = {k: list(v) for k, v in vizinhos.items()} # Convertendo conjuntos para listas para melhor visualização
# print(f'Lista de ASN e seus respectivos vizinhos: {vizinhos}\n')
# print(f'Linhas no arquivo: {linhas}') 



######################## OUTPUT PARA PASTA RESULTS #########################

# Agora será criado o arquivo results com toda análise

# Ordem dos dados no arquivo results: 
# 1 - Total de prepends contabilizados
# 2 - Lista de ASes com prepend na prependOrigem
# 3 - Lista de ASes com prepend prependIntermediario
# 4 - Lista de ASes unicos visualizados
# 5 - ASes com seus respctivos vizinhos listados

nomeOriginal = os.path.basename(source)
output = (f'./results/{nomeOriginal}_results.txt')
with open(output, 'w') as arquivoResultados:
    arquivoResultados.write(f'{prependTotais}\n')               # 1 - Total de prepends contabilizados
    arquivoResultados.write(f'{prependOrigem}\n')               # 2 - Lista de ASes com prepend na prependOrigem
    arquivoResultados.write(f'{prependIntermed}\n')             # 3 - Lista de ASes com prepend prependIntermediario
    arquivoResultados.write(f'{asesTotais}\n')                  # 4 - Lista de ASes unicos visualizados
    arquivoResultados.write(f'{vizinhos}\n')                    # 5 - ASes com seus respctivos vizinhos listados
print(f"Os resultados foram salvos em: {output}")

