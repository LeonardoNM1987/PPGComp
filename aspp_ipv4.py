# INFORMAÇÕES OBTIDAS COM ESTE CÓDIGO ATÉ O MOMENTO:
#  1)[X]Lista de ASes que fazem prepend na origem;
#  2)[X]Lista de ASes que fazem prepend Intermediário;
#  3)[X]Lista de ASes totais visualizados na análise;
#  4)[X]Lista de vizinhos que cada AS possui;
#  5)[ ]Detecta o nível do prepend
#  6)[ ]Verifica se é prefixo Bogon
#  7)[ ]Diferencia rotas IPv4 de IPv6





origem = [] #contabiliza prepends de origem
intermed = [] #contabiliza prepends intermediarios
conta_prep = 0 #contabiliza visualizações de prepend em geral(apenas debug)
vizinhos = {} #contabiliza todos vizinhos que cada ASN teve
asesTotais = [] #contabiliza todos ASes unicos vistos na análise

def listaVizinhos(dicionario, chave, valor): # Função para adicionar vizinhos
    if chave != valor:  # Excluir o próprio número
        if chave in dicionario:
            dicionario[chave].add(valor)  # Adicionar em um conjunto para evitar duplicatas
        else:
            dicionario[chave] = {valor} 


def contaPrepend(aspath): 
    print(f'AS Path em análise: {aspath}\n')
    
    asn = aspath # quebra em vários asn
    
    global asesTotais
    global origem #conta os de origem
    global intermed #conta os intermediarios
    global conta_prep #conta aspp em geral(apenas debug)

    i=1 # indica posição do asn no path analisado
    trigger = True ; #enquanto ligado contabiliza o asn como de origem/desligado contabiliza como intermediario
    for item in range(len(asn)): #aqui começa a verificação no path    

        while(i<len(asn)):    
            
            if (asn[-i] not in asesTotais):                    
                asesTotais.append(asn[-i])
            
            #print(f'Testando : {asn[-i]} com {asn[-(i+1)]}...')    

            if (asn[-i] == asn[-(i+1)]):#compara asn de trás para frente 
                print(f'Comparando {asn[-i]} com {asn[-(i+1)]}...')
                conta_prep+=1
                print(f'{asn[-i]} é igual à {asn[-(i+1)]}')        

                if (trigger==True): #trata como origem
                    if (asn[-i] not in origem):                    
                        origem.append(asn[-i])
                        print(f'{asn[-i]} adicionado à lista de Prepends de Origem')
                else:  #trata como intermediario
                    if (asn[-i] not in intermed):
                        intermed.append(asn[-i])
                        print(f'{asn[-i]} adicionado à lista de Prepends Intermediarios')
            else:
                print(f'Comparando {asn[-i]} com {asn[-(i+1)]}...')
                if(trigger):
                    trigger = False;
                    print('\n>>Trigger agora virou false<<') 
            i+=1
            print('----------------------------------------------')


            
with open('rib_validador01.txt', 'r') as arquivo: #abertura do arquivo para análise
    
       
    linhas = 0 #contador de linhas
    for linha in arquivo: #ler linha por linha          
                   
        linhas +=1;
        coluna = linha.split('|')   # separa as colunas de cada linha        
        
        if len(coluna)>=3:             
            asPath = coluna[2].split()  #divide os ases no as-path                    
            
            contaPrepend(asPath)

            asn = asPath # quebra em vários asn   
            # Iterar pela lista de números
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


print(f'\n\nQuantas vezes se viu prepend: {conta_prep}\n')
print(f'Ases que fazem prepend na origem: {origem}\n')
print(f'ASes que fazem prepend de forma intermediária: {intermed}\n')
print(f'ASes únicos visualizados: {asesTotais}\n')
vizinhos_formatados = {k: list(v) for k, v in vizinhos.items()} # Convertendo conjuntos para listas para melhor visualização
print(f'Lista de ASN e seus respectivos vizinhos: {vizinhos_formatados}\n')
print(f'Linhas no arquivo: {linhas}')