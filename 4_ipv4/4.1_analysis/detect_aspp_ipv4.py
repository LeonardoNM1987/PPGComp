import datetime
import os
import ipaddress

#Todas URLs do codigo
bogonsList = '4_ipv4/4.1_analysis/bogonsList.txt'
source = r'C:\Ribs\2ndsp2018a2020'   # AJUSTAR source DE OUTPUT TAMBÉM!!

#RESULTADOS A APRESENTAR
asnPrepTam1 = set()                           # conjunto de ASes que fazem prepends de tamanho 1
asnPrepTam2 = set()                           # conjunto de ASes que fazem prepends de tamanho 2
asnPrepTam3 = set()                           # conjunto de ASes que fazem prepends de tamanho 3
asnPrepTam4Plus = set()                       # conjunto de ASes que fazem prepends de tamanho 4 ou +
prefixPrepTam1 = set()                        # conjunto de Prefixos que fazem prepends de tamanho 1
prefixPrepTam2 = set()                        # conjunto de Prefixos que fazem prepends de tamanho 2
prefixPrepTam3 = set()                        # conjunto de Prefixos que fazem prepends de tamanho 3
prefixPrepTam4Plus = set()                    # conjunto de Prefixos que fazem prepends de tamanho 4 +  
conjPrepOrigem = set()                         # conjunto de todos ASes que fazem prepend na Origem 
conjPrepIntermed = set()                       # conjunto de todos ASes que fazem prepend de forma Intermediária
conjPrepOrigemANDintermed = set()              # conjunto de ASes que fazem prepend Origem e Intermed
conjPrepOnlyOrigem = set() 
conjPrepOnlyIntermed = set() 
conjAsesUnicos = set()                         # conjunto de todos ASes unicos vistos na análise
conjPrefixosUnicos = set()                     # prefixos visualizados no snapshot
dictVizinhos = {}                              # dicionario com todos vizinhos de cada AS
dictPrefixAsnPrep = {}                         # dicionario com prefixos anunciados apenas por ASN que faz prepend
dictPrefixASN = {}                             # dicionario com prefixos anunciados por cada ASN relacionando-os
prefixPrepOrigem = set()                       # conjunto de prefixos que fazem prep na Origem
qtdePrependTotais = 0                          # quantitativo dos prep apenas na origem, apenas Intermediario e que fazem os dois   

#OBJETOS TEMPORARIOS E DEBUG
asPathUnico = set()                            # conjunto de AS_PATHs únicos, usados para eliminar rotas duplicadas

bogonPrefixes = set()                                # identificacao das rotas bogon para debug
qtdeRotasIgnoradas = 0                         # identificacao das rotas bogon para debug
qtdeRotasValidas = 0                           # identificacao das rotas validas para debug
numeroDaLinha = 0                              # qtde de linhas verificadas no arquivo


################################################ FUNCOES ################################################


def is_not_bogon(prefix, bogon_list):    
    if prefix not in bogon_list:
        return True
    else:
        bogonPrefixes.add(prefix)
        return False

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

            
def identificar_prepend_nivel(as_path, prefix):
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
    #asnPrepTam1, asnPrepTam2, asnPrepTam3, asnPrepTam4Plus = [], [], [], []
    for asn, nivel in nivel_prepend_temp.items():
        if nivel == 1:
            asnPrepTam1.add(asn)
            prefixPrepTam1.add(prefix)
        elif nivel == 2:
            asnPrepTam2.add(asn)
            prefixPrepTam2.add(prefix)
        elif nivel == 3:
            asnPrepTam3.add(asn)
            prefixPrepTam3.add(prefix)
        else:
            asnPrepTam4Plus.add(asn)
            prefixPrepTam4Plus.add(prefix)

def prefixosAnunciados(asPath, prefixo):        
    try:
        asn = asPath[-1]
        if asn not in dictPrefixASN:
            dictPrefixASN.update({asn:[prefixo]})    
        else:
            if prefixo not in dictPrefixASN[asn]:
                dictPrefixASN[asn].append(prefixo)
    except:
        pass


################################################ ARQUIVOS PARA ANALISE #################################################


## PREPARA LISTA BOGON ##

bogon_list = []
with open(bogonsList, 'r') as arquivo:
    for line in arquivo:
        bogon_list.append(line.strip())
#print(bogon_list)
######


# lote de snapshots para análise sequencial

# sourceBatch = ['validadores/validador_IPv4_01.txt',
#                'validadores/validador_IPv4_02.txt', 
#                'validadores/validador_IPv4_03.txt']


# pasta onde estão os arquivos 
source = r'C:\Ribs\2ndsp2018a2020'   # AJUSTAR pasta DE OUTPUT TAMBÉM!!
#pasta = r'C:\Ribs\2ndsp2011a2020'    # AJUSTAR pasta DE OUTPUT TAMBÉM!!
# Lista para armazenar os caminhos dos arquivos
caminhos = []

# Listar os arquivos na pasta
for nome_arquivo in os.listdir(source):
    # Criar o caminho completo para o arquivo
    caminho_completo = os.path.join(source, nome_arquivo)
    # Adicionar o caminho à lista
    caminhos.append(caminho_completo)

# Exibir a lista de caminhos
print(f'source com Ribs localizada e possui {len(caminhos)} arquivos.\n')


# sourceBatch = [r'C:\Ribs\2ndsp2011a2020\rib.20110320.0000.txt',
#                r'C:\Ribs\2ndsp2011a2020\rib.20130320.0000.txt',
#                r'C:\Ribs\2ndsp2011a2020\rib.20150320.0000.txt',
#                r'C:\Ribs\2ndsp2011a2020\rib.20170320.0000.txt',
#                r'C:\Ribs\2ndsp2011a2020\rib.20200320.0000.txt']
#sourceBatch = ['1_source/rib.20110320.0000.txt']
#sourceBatch = ['validadores/validador_IPv4_01_reduzido.txt']

################################################ EXECUÇÃO #################################################

inicioTotal = datetime.datetime.now()

for snapshot in caminhos:                                               # esse for analisa snapshots em lote
    inicio = datetime.datetime.now()                                       # Marca o início da execução       
    
    print(f'ANALISANDO SNAPSHOT: {snapshot}......')
    with open(snapshot, 'r') as arquivo:    
                                                                  
        for linha in arquivo:                                               #ler linha por linha    
            numeroDaLinha+=1
            coluna = linha.split('|')                                       #quebra a linha em colunas
            
            if is_not_bogon(coluna[1], bogon_list) and (':' not in coluna[1]) and (len(coluna)>=3):                                                   
                qtdeRotasValidas +=1           
                conjPrefixosUnicos.add(coluna[1])
                asPath = coluna[2].split()                         #divide os ases no as-path                    
                as_path_str = ' '.join(asPath)                     #Cria uma string única para o AS_PATH                
                if as_path_str not in asPathUnico:                 #Verifica se o AS_PATH é único(evita contar rotas duplicadas em coletores diferentes)
                    asPathUnico.add(as_path_str)                   #Adiciona o AS_PATH ao conjunto de únicos
                    contaAsesUnicos(asPath)                        # >>>>>>>>> AQUI PODE SER UTIL USAR HPC
                    contaPrepend(asPath, coluna[1])                # >>>>>>>>> AQUI PODE SER UTIL USAR HPC
                    identificar_prepend_nivel(asPath, coluna[1])              # >>>>>>>>> AQUI PODE SER UTIL USAR HPC
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
    


#end_for



######################## OUTPUT PARA source RESULTS #########################
    nomeOriginal = os.path.basename(snapshot)
    nomeSemExtensao, extensao = os.path.splitext(nomeOriginal)
    #output = (f'ipv4/3_results/resultados_teste/{nomeSemExtensao}_results.txt')
    output = (f'ipv4/3_results/{nomeSemExtensao}_results.txt')
    with open(output, 'w') as arquivoResultados:
        arquivoResultados.write(f'{len(conjAsesUnicos)}\n')              #0
        arquivoResultados.write(f'{qtdePrependTotais}\n')                #1   
        arquivoResultados.write(f'{len(conjPrepOnlyOrigem)}\n')          #2  
        arquivoResultados.write(f'{len(conjPrepOnlyIntermed)}\n')        #3
        arquivoResultados.write(f'{len(conjPrepOrigemANDintermed)}\n')   #4          
        arquivoResultados.write(f'{len(asnPrepTam1)}\n')                 #5  
        arquivoResultados.write(f'{len(asnPrepTam2)}\n')                 #6  
        arquivoResultados.write(f'{len(asnPrepTam3)}\n')                 #7  
        arquivoResultados.write(f'{len(asnPrepTam4Plus)}\n')             #8 
        arquivoResultados.write(f'{conjAsesUnicos}\n')                   #9     
        arquivoResultados.write(f'{conjPrepOnlyOrigem}\n')               #10 
        arquivoResultados.write(f'{conjPrepOnlyIntermed}\n')             #11 
        arquivoResultados.write(f'{conjPrepOrigemANDintermed}\n')        #12  
        arquivoResultados.write(f'{asnPrepTam1}\n')                      #13
        arquivoResultados.write(f'{asnPrepTam2}\n')                      #14
        arquivoResultados.write(f'{asnPrepTam3}\n')                      #15
        arquivoResultados.write(f'{asnPrepTam4Plus}\n')                  #16
        arquivoResultados.write(f'{prefixPrepOrigem}\n')                 #17
        arquivoResultados.write(f'{dictPrefixAsnPrep}\n')                #18
        arquivoResultados.write(f'{dictPrefixASN}\n')                    #19
        arquivoResultados.write(f'{dictVizinhos}\n')                     #20        
        # PARA ANALISE DAS POLITICAS DE PREFIXOS
        arquivoResultados.write(f'{conjPrefixosUnicos}\n')               #21
        arquivoResultados.write(f'{prefixPrepTam1}\n')                   #22
        arquivoResultados.write(f'{prefixPrepTam2}\n')                   #23
        arquivoResultados.write(f'{prefixPrepTam3}\n')                   #24
        arquivoResultados.write(f'{prefixPrepTam4Plus}\n')               #25
        arquivoResultados.write(f'{bogonPrefixes}\n')                    #26
    print(f"Os resultados foram salvos em: {output}")

 
# 0 - Quantitativo de ASes unicos visualizados
# 1 - Quantitativo de prepends no geral (apenas origem, apenas intermed e que fazem os dois) 
# 2 - Quantitativo de prepends apenas de origem
# 3 - Quantitativo de prepends apenas intermediário
# 4 - Quantitativo de prepends que fazem Origem e Intermediário
# 5 - Quantitativo de ASes que fazem prepend tamanho 1  
# 6 - Quantitativo de ASes que fazem prepend tamanho 2
# 7 - Quantitativo de ASes que fazem prepend tamanho 3
# 8 - Quantitativo de ASes que fazem prepend tamanho 4+            
# 9 - Conjunto de ASes unicos visualizados        
# 10 - Conjunto de ASes com prepend apenas na Origem
# 11 - Conjunto de ASes com prepend apenas Intermediário
# 12 - Conjunto de ASes que fazem na Origem e também Intermediário 
# 13 - Conjunto de ASes que fazem prepend tamanho 1
# 14 - Conjunto de ASes que fazem prepend tamanho 2
# 15 - Conjunto de ASes que fazem prepend tamanho 3
# 16 - Conjunto de ASes que fazem prepend tamanho 4+                
# 17 - Conjunto de prefixos que fazem prepend na Origem
# 18 - Dicionario que associa ASes com os prefixos anunciados que fazem prepend na Origem
# 19 - Dicionario que lista quais ASes anunciam quais prefixos
# 20 - Dicionario que relaciona ASes com seus respectivos vizinhos
# 21 - Conjunto de prefixos unicos visualizados no snapshot
# 22 - Conjunto de prefixos com prepend tamanho 1
# 23 - Conjunto de prefixos com prepend tamanho 2
# 24 - Conjunto de prefixos com prepend tamanho 3
# 25 - Conjunto de prefixos com prepend tamanho 4 +





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
    if (len(conjAsesUnicos) > 110000):
        print ('ATENÇÃO, QTDE DE ASES UNICOS É MUITO SUPERIOR A 110.000. VERIFIQUE A ANÁLISE!')



print('##########################################################')
fimTotal = datetime.datetime.now()  
tempo_execucao_total = fimTotal - inicioTotal
tempo_execucao_total_format = str(tempo_execucao_total).split('.')[0]
print(f"Tempo de execução total das análises: {tempo_execucao_total_format}")