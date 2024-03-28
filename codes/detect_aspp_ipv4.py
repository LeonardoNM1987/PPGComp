import datetime
import os

#RESULTADOS A APRESENTAR
conjPrepTam1 = set()                           # conjunto de ASes que fazem prepends de tamanho 1
conjPrepTam2 = set()                           # conjunto de ASes que fazem prepends de tamanho 2
conjPrepTam3 = set()                            # conjunto de ASes que fazem prepends de tamanho 3
conjPrepTam4plus = set()                       # conjunto de ASes que fazem prepends de tamanho 4 ou +
conjPrepOrigem = set()                         # conjunto de todos ASes que fazem prepend na Origem 
conjPrepIntermed = set()                       # conjunto de todos ASes que fazem prepend de forma Intermediária
conjPrepOrigemANDintermed = set()              # conjunto de ASes que fazem prepend Origem e Intermed
conjPrepOnlyOrigem = set() 
conjPrepOnlyIntermed = set() 
conjAsesUnicos = set()                         # conjunto de todos ASes unicos vistos na análise
dictVizinhos = {}                              # dicionario com todos vizinhos de cada AS
dictPrefixAsnPrep = {}                         # dicionario com prefixos anunciados apenas por ASN que faz prepend
dictPrefixASN = {}                             # dicionario com prefixos anunciados por cada ASN
prefixPrepOrigem = set()                       # conjunto de prefixos que fazem prep na Origem
qtdePrependTotais = 0                          # quantitativo dos prep apenas na origem, apenas Intermediario e que fazem os dois   

#OBJETOS TEMPORARIOS E DEBUG
asPathUnico = set()                            # conjunto de AS_PATHs únicos, usados para eliminar rotas duplicadas

rotasBogon = []                                # identificacao das rotas bogon para debug
qtdeRotasIgnoradas = 0                         # identificacao das rotas bogon para debug
qtdeRotasValidas = 0                           # identificacao das rotas validas para debug
numeroDaLinha = 0                              # qtde de linhas verificadas no arquivo


################################################ FUNCOES ################################################

def contaAsesUnicos(path):    
    for item in path:        
        conjAsesUnicos.add(item)

def listadictVizinhos(dicionario, chave, valor):                           # Aqui a funcao analisa quem é vizinho de quem
    if chave != valor:                                                 # Ignorar o próprio ASN como vizinho dele mesmo
        if chave in dicionario:
            dicionario[chave].add(valor)                               # Adicionar em um conjunto para evitar duplicatas
        else:
            dicionario[chave] = {valor} 

def contaPrepend(aspath, prefixo): 
    #print(f'AS Path em análise: {aspath}\n')                          # DEBUG    
    asn = aspath                                                       # quebra em vários asn   
     

    conjPrepOrigem                                                    # conta os de conjPrepOrigem
    conjPrepIntermed                                                  # conta os conjPrepIntermediarios                                                                     
    i=1                                                               # indica posição do asn no path analisado
    trigger = True ; 
    for item in range(len(asn)):                                       #aqui começa a verificação no path    
        while(i<len(asn)):          
            if (asn[-i] == asn[-(i+1)]):                               #compara os ASes de trás para frente                 
                  
                if (trigger==True):                                    #trata como conjPrepOrigem
                    conjPrepOrigem.add(asn[-i])
                    prefixPrepOrigem.add(prefixo)
                    if asn[-i] not in dictPrefixAsnPrep:
                        dictPrefixAsnPrep.update({asn[-i]:[prefixo]})
                    else:
                        dictPrefixAsnPrep[asn[-i]].append(prefixo)
                else:                                                  #trata como conjPrepIntermediario
                    conjPrepIntermed.add(asn[-i])                       
            else:
                if(trigger):
                    trigger = False
            i+=1

            
def identificar_prepend_nivel(as_path):
    """
    Identifica o nível de AS-Path prepend para cada ASN repetido no AS-Path fornecido,
    organizando-os em listas por nível de prepend.
    """
    # Dicionário temporário para contar os prepends
    nivel_prepend_temp = {}
    contador_temp = 1  # Contador para acompanhar repetições consecutivas

    for i in range(1, len(as_path)):
        if as_path[i] == as_path[i-1]:
            contador_temp += 1
        else:
            if contador_temp > 1:
                nivel_prepend_temp[as_path[i-1]] = contador_temp - 1
            contador_temp = 1

    if contador_temp > 1:
        nivel_prepend_temp[as_path[-1]] = contador_temp - 1

    # Organiza os ASNs em listas por nível de prepend
    #conjPrepTam1, conjPrepTam2, conjPrepTam3, conjPrepTam4plus = [], [], [], []
    for asn, nivel in nivel_prepend_temp.items():
        if nivel == 1:
            conjPrepTam1.add(asn)
        elif nivel == 2:
            conjPrepTam2.add(asn)
        elif nivel == 3:
            conjPrepTam3.add(asn)
        else:
            conjPrepTam4plus.add(asn)

def prefixosAnunciados(asPath, prefixo):        
    asn = asPath[-1]
    if asn not in dictPrefixASN:
        dictPrefixASN.update({asn:[prefixo]})    
    else:
        if prefixo not in dictPrefixASN[asn]:
            dictPrefixASN[asn].append(prefixo)



################################################ ARQUIVOS PARA ANALISE #################################################

bogonsList = './codes/bogonsList.txt'                                  # lista de rotas bogon

# lote de snapshots para análise sequencial

# sourceBatch = ['validadores/validador_IPv4_01.txt',
#                'validadores/validador_IPv4_02.txt', 
#                'validadores/validador_IPv4_03.txt']

sourceBatch = ['source/rib.20110320.0000.txt','source/rib.20130320.0000.txt','source/rib.20150320.0000.txt','source/rib.20170320.0000.txt','source/rib.20200320.0000.txt']
#sourceBatch = ['validadores/validador_IPv4_01_reduzido.txt']

################################################ EXECUÇÃO #################################################

inicioTotal = datetime.datetime.now()

for snapshot in sourceBatch:                                               # esse for analisa snapshots em lote

    inicio = datetime.datetime.now()                                       # Marca o início da execução

       
    with open(bogonsList, 'r') as arquivoBogon:                              #abertura e conversão do arquivo bogon para uma lista
        for linha in arquivoBogon.readlines():
            rotasBogon.append(linha.strip())

    print(f'ANALISANDO SNAPSHOT: {snapshot}......')
    with open(snapshot, 'r') as arquivo:    
                                                                  
        for linha in arquivo:                                               #ler linha por linha    
            numeroDaLinha+=1
            coluna = linha.split('|')                                       #quebra a linha em colunas
            
            if (coluna[1] not in rotasBogon) and (':' not in coluna[1]) and (len(coluna)>=3):
                qtdeRotasValidas +=1           
                asPath = coluna[2].split()                         #divide os ases no as-path                    
                as_path_str = ' '.join(asPath)                     #Cria uma string única para o AS_PATH                
                if as_path_str not in asPathUnico:                 #Verifica se o AS_PATH é único(evita contar rotas duplicadas em coletores diferentes)
                    asPathUnico.add(as_path_str)                   #Adiciona o AS_PATH ao conjunto de únicos
                    contaAsesUnicos(asPath)                        # >>>>>>>>> AQUI PODE SER UTIL USAR HPC
                    contaPrepend(asPath, coluna[1])                # >>>>>>>>> AQUI PODE SER UTIL USAR HPC
                    identificar_prepend_nivel(asPath)              # >>>>>>>>> AQUI PODE SER UTIL USAR HPC
                    prefixosAnunciados(asPath, coluna[1])          # >>>>>>>>> AQUI PODE SER UTIL USAR HPC                    
                    asn = asPath                                   #quebra o path em vários asn 
                    for i, num in enumerate(asn):                  #Iterar pela lista de ASes
                        if i > 0:                                  #Certificar de não ser o primeiro elemento
                            listadictVizinhos(dictVizinhos, num, asn[i-1])    
                        # Vizinho seguinte
                        if i < len(asn)-1:                         #Certificar de não ser o último elemento
                            listadictVizinhos(dictVizinhos, num, asn[i+1])
                    
                    
            else:
                #print(f'Rota inválida na linha: {numeroDaLinha} | Prefixo: {coluna[1]}')
                qtdeRotasIgnoradas+=1

    conjPrepOrigemANDintermed = conjPrepOrigem & conjPrepIntermed                                               # O que consta nos dois conjuntos - intersecção
    conjPrepOnlyOrigem = conjPrepOrigem - conjPrepIntermed                                                  # o que consta apenas no de origem
    conjPrepOnlyIntermed = conjPrepIntermed - conjPrepOrigem                                                # o que consta apenas no intermed
    qtdePrependTotais = len(conjPrepOnlyOrigem)+len(conjPrepOnlyIntermed)+len(conjPrepOrigemANDintermed)    #soma de todos prepends 


######################## OUTPUT PARA PASTA RESULTS #########################
    nomeOriginal = os.path.basename(snapshot)
    nomeSemExtensao, extensao = os.path.splitext(nomeOriginal)
    output = (f'./results/{nomeSemExtensao}_ipv4_results.txt')
    with open(output, 'w') as arquivoResultados:
        arquivoResultados.write(f'{len(conjAsesUnicos)}\n')               #1
        arquivoResultados.write(f'{qtdePrependTotais}\n')                 #2   
        arquivoResultados.write(f'{len(conjPrepOnlyOrigem)}\n')           #3  
        arquivoResultados.write(f'{len(conjPrepOnlyIntermed)}\n')         #4
        arquivoResultados.write(f'{len(conjPrepOrigemANDintermed)}\n')    #5          
        arquivoResultados.write(f'{len(conjPrepTam1)}\n')                 #6  
        arquivoResultados.write(f'{len(conjPrepTam2)}\n')                 #7  
        arquivoResultados.write(f'{len(conjPrepTam3)}\n')                 #8  
        arquivoResultados.write(f'{len(conjPrepTam4plus)}\n')             #9 
        arquivoResultados.write(f'{conjAsesUnicos}\n')                    #10     
        arquivoResultados.write(f'{conjPrepOnlyOrigem}\n')                #11 
        arquivoResultados.write(f'{conjPrepOnlyIntermed}\n')              #12 
        arquivoResultados.write(f'{conjPrepOrigemANDintermed}\n')         #13  
        arquivoResultados.write(f'{conjPrepTam1}\n')                      #14
        arquivoResultados.write(f'{conjPrepTam2}\n')                      #15
        arquivoResultados.write(f'{conjPrepTam3}\n')                      #16
        arquivoResultados.write(f'{conjPrepTam4plus}\n')                  #17
        arquivoResultados.write(f'{prefixPrepOrigem}\n')                  #18
        arquivoResultados.write(f'{dictPrefixAsnPrep}\n')                 #19
        arquivoResultados.write(f'{dictPrefixASN}\n')                     #20
        arquivoResultados.write(f'{dictVizinhos}\n')                      #21
    print(f"Os resultados foram salvos em: {output}")

 
# 1 - Quantitativo de ASes unicos visualizados
# 2 - Quantitativo de prepends no geral (apenas origem, apenas intermed e que fazem os dois) 
# 3 - Quantitativo de prepends apenas de origem
# 4 - Quantitativo de prepends apenas intermediário
# 5 - Quantitativo de prepends que fazem Origem e Intermediário
# 6 - Quantitativo de ASes que fazem prepend tamanho 1  
# 7 - Quantitativo de ASes que fazem prepend tamanho 2
# 8 - Quantitativo de ASes que fazem prepend tamanho 3
# 9 - Quantitativo de ASes que fazem prepend tamanho 4+            
# 10 - Conjunto de ASes unicos visualizados        
# 11 - Conjunto de ASes com prepend apenas na Origem
# 12 - Conjunto de ASes com prepend apenas Intermediário
# 13 - Conjunto de ASes que fazem na Origem e também Intermediário 
# 14 - Conjunto de ASes que fazem prepend tamanho 1
# 15 - Conjunto de ASes que fazem prepend tamanho 2
# 16 - Conjunto de ASes que fazem prepend tamanho 3
# 17 - Conjunto de ASes que fazem prepend tamanho 4+                
# 18 - Conjunto de prefixos que fazem prepend na Origem
# 19 - Dicionario que associa ASes com os prefixos anunciados que fazem prepend na Origem
# 20 - Dicionario que lista quais ASes anunciam quais prefixos
# 21 - Dicionario que relaciona ASes com seus respectivos vizinhos






    #duplicados_contagem = contabilizar_duplicidade(asPath)

    fim = datetime.datetime.now()                                       #Marca o fim da execução
    tempo_execucao = fim - inicio
    tempo_formatado = str(tempo_execucao).split('.')[0]                 #Remove a parte dos microssegundos

    ############################### SAIDAS NO PROMPT ##############################

    print('Análise concluída com sucesso!')
    print(f'Rotas IPv4 inválidas e ignoradas: {qtdeRotasIgnoradas}') 
    print(f'Rotas IPv4 analisadas: {qtdeRotasValidas}')
    #print(f"ASes com prepend: {contabilizar_duplicidade}")    
    print(f"Tempo de execução: {tempo_formatado}")
    if (len(conjAsesUnicos) > 102000):
        print ('ATENÇÃO, QTDE DE ASES UNICOS É MUITO SUPERIOR A 102.000. VERIFIQUE A ANÁLISE!')



print('##########################################################')
fimTotal = datetime.datetime.now()  
tempo_execucao_total = fimTotal - inicioTotal
tempo_execucao_total_format = str(tempo_execucao_total).split('.')[0]
print(f"Tempo de execução total das análises: {tempo_execucao_total_format}")