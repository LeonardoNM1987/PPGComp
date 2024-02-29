#Sanitizar o arquivo de entrada com o 'bgp_sanitization.py' antes das etapas abaixo;
#
# OPERAÇÕES REALIZADAS COM ESTE CÓDIGO:
# 1. Listar ASes que fazem prepend na Origem 
# 2. Listar ASes que fazem prepend Intermediário 
# 3. Listar ASes únicos visualizados no arquivo de entrada 
# 4. Listar vizinhos que cada AS possui
#
# ESTE CÓDIGO ANALISA APENAS ROTAS IPv6
# PARA ANALISE DE ROTAS IPv6, EXECUTAR O 'detect_aspp_ipv4.py'




origem = [] #contabiliza prepends de origem
intermed = [] #contabiliza prepends intermediarios
conta_prep = 0 #contabiliza visualizações de prepend em geral(apenas debug)
vizinhos = {} #contabiliza todos vizinhos que cada ASN teve
asesTotais = [] #contabiliza todos ASes unicos vistos na análise

# Função para adicionar vizinhos
def listaVizinhos(dicionario, chave, valor): 
    if chave != valor:  #Ignorar o próprio ASN como vizinho dele mesmo
        if chave in dicionario:
            dicionario[chave].add(valor)  # Adicionar em um conjunto para evitar duplicatas
        else:
            dicionario[chave] = {valor} 


def contaPrepend(aspath): 
    #print(f'AS Path em análise: {aspath}\n') # DEBUG
    
    asn = aspath # quebra em vários asn
    
    global asesTotais
    global origem #conta os de origem
    global intermed #conta os intermediarios
    global conta_prep #conta aspp em geral(apenas debug)

    i=1 # indica posição do asn no path analisado
    trigger = True ; #enquanto ligado contabiliza o asn como de origem/ se desligado contabiliza como intermediario
    for item in range(len(asn)): #aqui começa a verificação no path    

        while(i<len(asn)):    
            
            if (asn[-i] not in asesTotais):                    
                asesTotais.append(asn[-i])
            
            #print(f'Testando : {asn[-i]} com {asn[-(i+1)]}...')    

            if (asn[-i] == asn[-(i+1)]):#compara asn de trás para frente 
                #print(f'Comparando {asn[-i]} com {asn[-(i+1)]}...') # DEBUG
                conta_prep+=1
                #print(f'{asn[-i]} é igual à {asn[-(i+1)]}') # DEBUG       

                if (trigger==True): #trata como origem
                    if (asn[-i] not in origem):                    
                        origem.append(asn[-i])
                        #print(f'{asn[-i]} adicionado à lista de Prepends de Origem') # DEBUG
                else:  #trata como intermediario
                    if (asn[-i] not in intermed):
                        intermed.append(asn[-i])
                        #print(f'{asn[-i]} adicionado à lista de Prepends Intermediarios') # DEBUG
            else:
                #print(f'Comparando {asn[-i]} com {asn[-(i+1)]}...') # DEBUG
                if(trigger):
                    trigger = False;
                    #print('\n>>Trigger agora virou false<<') # DEBUG
            i+=1
            # print('----------------------------------------------') # DEBUG



######################## EXECUÇÃO #########################
            

try:
     # TESTAR O ARQUIVO DA PASTA RIB AQUI      
    with open('validadores/rib_IPv4_IPv6_validador02_sanitized.txt', 'r') as arquivo:           
        linhas = 0 #contador de linhas
    
        for linha in arquivo: #ler linha por linha          

            
            

            #busca a coluna de ASes para análise
            linhas +=1
            coluna = linha.split('|')

            #A condição abaixo verifica se é rota IPv4 e a ignora
            if ':' not in coluna[1]:
                print(f'Rota ignorada:{coluna[1]} | linha {linhas}')
                continue

            if len(coluna)>=3:             
                asPath = coluna[2].split()  #divide os ases no as-path                    
                
                contaPrepend(asPath)

                asn = asPath # quebra em vários asn   
                # Iterar pela lista de ASes
                for i, num in enumerate(asn):
                    # Vizinho anterior
                    if i > 0:  # Certificar de não estar no primeiro elemento
                        listaVizinhos(vizinhos, num, asn[i-1])    
                    # Vizinho seguinte
                    if i < len(asn)-1:  # Certificar de não estar no último elemento
                        listaVizinhos(vizinhos, num, asn[i+1])              
            
            else:
                print("ERRO: Não foi possível ler a linha! Passando para a próxima..")
     
    
    ######################## RESULTADOS #########################

    print("\n\n[AVISO!] ANTES DE ANALISAR O ARQUIVO DE ENTRADA, FILTRE ELE COM O 'bgp_sanitization.py'!")
    print(f'\nQuantas vezes se viu prepend: {conta_prep}\n')
    print(f'Ases que fazem prepend na origem: {sorted(origem, key=int)}\n')
    print(f'ASes que fazem prepend de forma intermediária: {sorted(intermed,key=int)}\n')
    print(f'ASes únicos visualizados: {sorted(asesTotais, key=int)}\n')
    vizinhos_formatados = {k: list(v) for k, v in vizinhos.items()} # Convertendo conjuntos para listas para melhor visualização
    print(f'Lista de ASN e seus respectivos vizinhos: {vizinhos_formatados}\n')
    print(f'Linhas no arquivo: {linhas}') 

except:
  print("[AVISO!] OCORREU UM ERRO AO LER O ARQUIVO. VERIFIQUE O ARQUIVO DE ENTRADA E TENTE NOVAMENTE!")

