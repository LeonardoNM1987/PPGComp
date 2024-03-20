import datetime
import os


conjPrepNivel1 = set()                         # listar prepends de nivel 1
conjPrepNivel2 = set()                         # listar prepends de nivel 2
conjPrepNivel3 = set()                         # listar prepends de nivel 3
conjPrepNivel4plus = set()                     # listar prepends de nivel 4 ou superior
conjPrepOrigem = set()                         # listar prepends de conjPrepOrigem
conjPrepIntermed = set()                       # listar prepends conjPrepIntermediarios
conjAsesUnicos = set()                         # listar todos ASes unicos vistos na análise
asPathUnico = set()                            # conjunto para armazenar AS_PATHs únicos e eliminar rotas duplicadas
qtdePrependTotais = 0                          # quantitativo de visualizações de prepend em geral(apenas debug)    
dictVizinhos = {}                              # listar todos dictVizinhos que cada ASN teve
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

def contaPrepend(aspath): 
    #print(f'AS Path em análise: {aspath}\n')                          # DEBUG    
    asn = aspath                                                       # quebra em vários asn   
    
    conjPrepOrigem                                               # conta os de conjPrepOrigem
    conjPrepIntermed                                             # conta os conjPrepIntermediarios
    qtdePrependTotais                                               # conta aspp em geral(apenas debug)
    i=1                                                                # indica posição do asn no path analisado
    trigger = True ; 
    for item in range(len(asn)):                                       #aqui começa a verificação no path    
        while(i<len(asn)):          
            if (asn[-i] == asn[-(i+1)]):                               #compara os ASes de trás para frente                 
                #qtdePrependTotais+=1  
                if (trigger==True):                                    #trata como conjPrepOrigem
                    conjPrepOrigem.add(asn[-i])                        
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
    #conjPrepNivel1, conjPrepNivel2, conjPrepNivel3, conjPrepNivel4plus = [], [], [], []
    for asn, nivel in nivel_prepend_temp.items():
        if nivel == 1:
            conjPrepNivel1.add(asn)
        elif nivel == 2:
            conjPrepNivel2.add(asn)
        elif nivel == 3:
            conjPrepNivel3.add(asn)
        else:
            conjPrepNivel4plus.add(asn)


################################################ ARQUIVOS PARA ANALISE #################################################

bogonsList = './codes/bogonsList.txt'                                  # lista de rotas bogon

# lote de snapshots para análise sequencial
sourceBatch = [
    'source/rib.20110320.0000.txt',
    'source/rib.20130320.0000.txt',
    'source/rib.20150320.0000.txt',
    'source/rib.20170320.0000.txt',
    'source/rib.20200320.0000.txt'    
]
# sourceBatch = [
#     'source/rib.20110320.0000.txt'        
# ]
# sourceBatch = ['validadores/validador_IPv4_01.txt',
#                'validadores/validador_IPv4_02.txt', 
#                'validadores/validador_IPv4_03.txt']
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
                    contaAsesUnicos(asPath)
                    contaPrepend(asPath)                           # >>>>>>>>> AQUI PODE SER UTIL USAR HPC
                    identificar_prepend_nivel(asPath)               # >>>>>>>>> AQUI PODE SER UTIL USAR HPC
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


######################## OUTPUT PARA PASTA RESULTS #########################
    nomeOriginal = os.path.basename(snapshot)
    nomeSemExtensao, extensao = os.path.splitext(nomeOriginal)
    output = (f'./results/{nomeSemExtensao}_results.txt')
    with open(output, 'w') as arquivoResultados:
        arquivoResultados.write(f'{len(conjAsesUnicos)}\n')                          # 1 - Total de ASes unicos visualizados
        arquivoResultados.write(f'{len(conjPrepOrigem)+len(conjPrepIntermed)}\n')    # 2 - Total de prepends contabilizados
        arquivoResultados.write(f'{len(conjPrepOrigem)}\n')                          # 3 - Total de prepends na origem
        arquivoResultados.write(f'{len(conjPrepIntermed)}\n')                        # 4 - Total de prepends intermed
        arquivoResultados.write(f'{len(conjPrepNivel1)}\n')                          # 5 - Total de ASes que fazem prepend nivel 1
        arquivoResultados.write(f'{len(conjPrepNivel2)}\n')                          # 6 - Total de ASes que fazem prepend nivel 2
        arquivoResultados.write(f'{len(conjPrepNivel3)}\n')                          # 7 - Total de ASes que fazem prepend nivel 3
        arquivoResultados.write(f'{len(conjPrepNivel4plus)}\n')                      # 8 - Total de ASes que fazem prepend nivel 4+        
        arquivoResultados.write(f'{conjAsesUnicos}\n')                               # 9 - Lista de ASes unicos visualizados        
        arquivoResultados.write(f'{conjPrepOrigem}\n')                               # 10 - Lista de ASes com prepend na conjPrepOrigem
        arquivoResultados.write(f'{conjPrepIntermed}\n')                             # 11 - Lista de ASes com prepend conjPrepIntermediario
        arquivoResultados.write(f'{conjPrepNivel1}\n')                               # 12 - Lista de ASes que fazem prepend nivel 1
        arquivoResultados.write(f'{conjPrepNivel2}\n')                               # 13 - Lista de ASes que fazem prepend nivel 2
        arquivoResultados.write(f'{conjPrepNivel3}\n')                               # 14 - Lista de ASes que fazem prepend nivel 3
        arquivoResultados.write(f'{conjPrepNivel4plus}\n')                           # 15 - Lista de ASes que fazem prepend nivel 4 ou +        
        arquivoResultados.write(f'{dictVizinhos}\n')                                 # 16 - Lista de ASes com seus respectivos dictVizinhos
    print(f"Os resultados foram salvos em: {output}")

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