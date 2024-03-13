import datetime
import os

         
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
            if (asn[-i] == asn[-(i+1)]):                               #compara os ASes de trás para frente                 
                prependTotais+=1  
                if (trigger==True):                                    #trata como prependOrigem
                    if (asn[-i] not in prependOrigem):                    
                        prependOrigem.append(asn[-i])
                        
                else:                                                  #trata como prependIntermediario
                    if (asn[-i] not in prependIntermed):
                        prependIntermed.append(asn[-i])                       
            else:
                if(trigger):
                    trigger = False
            i+=1

def contabilizar_duplicidade(as_path):
    as_contagem = {}
    as_set = set()    
    for asn in as_path:
        if asn in as_set:
            as_contagem[asn] = as_contagem.get(asn, 0) + 1
        else:
            as_set.add(asn)    
    return as_contagem


################################################ INPUTS #################################################

bogonsList = './codes/bogonsList.txt'                                  # lista de rotas bogon
#source = 'validadores/validador_IPv4_01.txt'                           # ARQUIVO PARA VALIDAÇÃO
#source = 'source/rib.20200320.0000.txt'                  # ARQUIVO PARA ANÁLISE

# sourceBatch = [
#     'source/rib.20110320.0000.txt',
#     'source/rib.20130320.0000.txt',
#     'source/rib.20150320.0000.txt',
#     'source/rib.20170320.0000.txt',
#     'source/rib.20200320.0000.txt'    
# ]
# sourceBatch = ['validadores/validador_IPv4_01.txt',
#                'validadores/validador_IPv4_02.txt', 
#                'validadores/validador_IPv4_03.txt']
sourceBatch = ['validadores/validador_IPv4_01.txt']

################################################ EXECUÇÃO #################################################

for snapshot in sourceBatch:                                               #esse for replica diversas analises sequenciais

    inicio = datetime.datetime.now()                                       # Marca o início da execução

    prependOrigem = []                                                     # contabiliza prepends de prependOrigem
    prependIntermed = []                                                   # contabiliza prepends prependIntermediarios
    prependTotais = 0                                                      # contabiliza visualizações de prepend em geral(apenas debug)
    vizinhos = {}                                                          # contabiliza todos vizinhos que cada ASN teve
    asesTotais = []                                                        # contabiliza todos ASes unicos vistos na análise
    asPathUnico = set()                                                    # conjunto para armazenar AS_PATHs únicos
    rotasBogon = []
    rotasRemovidas = 0
    rotaValida = 0
    numLinha = 0
    
    with open(bogonsList, 'r') as arquivoBogon:                              #abertura e conversão do arquivo bogon para uma lista
        for linha in arquivoBogon.readlines():
            rotasBogon.append(linha.strip())

    print('ANALISANDO SNAPSHOT...')
    with open(snapshot, 'r') as arquivo:    
                                                                  
        for linha in arquivo:                                               #ler linha por linha    
            numLinha+=1
            coluna = linha.split('|')                                       #quebra a linha em colunas
            
            if coluna[1] not in rotasBogon:
                if ':' not in coluna[1]:                                   #Esse if verifica se é rota ipv4. Senão for, pula linha. 
                    if len(coluna)>=3:
                        rotaValida +=1           
                        asPath = coluna[2].split()                         #divide os ases no as-path                    
                        as_path_str = ' '.join(asPath)                     #Cria uma string única para o AS_PATH                
                        if as_path_str not in asPathUnico:                 #Verifica se o AS_PATH é único(evita contar rotas duplicadas em coletores diferentes)
                            asPathUnico.add(as_path_str)                   #Adiciona o AS_PATH ao conjunto de únicos
                            contaPrepend(asPath)                           # >>>>>>>>> AQUI PODE SER UTIL USAR HPC
                            #contabilizar_duplicidade(asPath)                  # >>>>>>>>> AQUI PODE SER UTIL USAR HPC
                            asn = asPath                                   #quebra o path em vários asn 
                            for i, num in enumerate(asn):                  #Iterar pela lista de ASes
                                if i > 0:                                  #Certificar de não ser o primeiro elemento
                                    listaVizinhos(vizinhos, num, asn[i-1])    
                                # Vizinho seguinte
                                if i < len(asn)-1:                         #Certificar de não ser o último elemento
                                    listaVizinhos(vizinhos, num, asn[i+1])              
                    
                    else:
                        print(f'\nErro ao ler linha: {rotaValida}! Passando para a próxima...\n')
                else:            
                    #print(f'Rota não é IPv4:{coluna[1]} | linha {numLinha}')  #Aqui só é avisado no prompt a rota ignorada
                    pass
            else:
                print(f'Rota bogon na linha:{numLinha} | Prefixo: {coluna[1]}')
                rotasRemovidas+=1


    ######################## OUTPUT PARA PASTA RESULTS #########################
    nomeOriginal = os.path.basename(snapshot)
    nomeSemExtensao, extensao = os.path.splitext(nomeOriginal)
    output = (f'./results/{nomeSemExtensao}_results.txt')
    with open(output, 'w') as arquivoResultados:
        arquivoResultados.write(f'{prependTotais}\n')               # 1 - Total de prepends contabilizados
        arquivoResultados.write(f'{prependOrigem}\n')               # 2 - Lista de ASes com prepend na prependOrigem
        arquivoResultados.write(f'{prependIntermed}\n')             # 3 - Lista de ASes com prepend prependIntermediario
        arquivoResultados.write(f'{asesTotais}\n')                  # 4 - Lista de ASes unicos visualizados
        arquivoResultados.write(f'{vizinhos}\n')                    # 5 - ASes com seus respctivos vizinhos listados
    print(f"Os resultados foram salvos em: {output}")

    #duplicados_contagem = contabilizar_duplicidade(asPath)

    fim = datetime.datetime.now()                                       #Marca o fim da execução
    tempo_execucao = fim - inicio
    tempo_formatado = str(tempo_execucao).split('.')[0]                 #Remove a parte dos microssegundos

    ############################### SAIDAS NO PROMPT ##############################

    print('Análise concluída com sucesso!')
    print(f'Rotas IPv4 inválidas e ignoradas: {rotasRemovidas}') 
    print(f'Rotas IPv4 analisadas: {rotaValida}')
    #print(f"ASes com prepend: {duplicados_contagem}")
    print(f"Tempo de execução: {tempo_formatado}")





############ NÃO UTILIZADO ###########

# print('--------------------------  RESULTADOS DA ANALISE  --------------------------')
# print(f'\nQuantas vezes se viu prepend: {prependTotais}\n')
# print(f'Ases que fazem prepend na prependOrigem: {sorted(prependOrigem, key=int)}\n')
# print(f'ASes que fazem prepend de forma prependIntermediária: {sorted(prependIntermed,key=int)}\n')
# print(f'ASes únicos visualizados: {sorted(asesTotais, key=int)}\n')
# print(f'ASes únicos visualizados: {asesTotais}\n')
# vizinhos_formatados = {k: list(v) for k, v in vizinhos.items()} # Convertendo conjuntos para listas para melhor visualização
# print(f'Lista de ASN e seus respectivos vizinhos: {vizinhos}\n')
# print(f'rotaValida no arquivo: {rotaValida}') 