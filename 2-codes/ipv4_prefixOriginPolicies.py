# dict_example = {
#     '103.240.84.0/22': {
#         'asn anunciante': '4837',
#         'monitores': 293,
#         'tamanhos de prepend': {0, 1, 2, 5, 10....},
#         'politica': 0, 1, 2 ou 3 (4 politicas)
#     },
#parPrefiXAsn = {'103.240.84.0/22':{56000, 100, {0,4,5}, 3}}

# =|5.41.200.0/24|28186 3356 39386 25019 39891|187.16.219.51|i||||187.16.219.51 28186|1694803584|1

# ipv4_policy
# ipv4_prefixes_policies


#from pprint import pprint
import datetime
import os
import pytricia

inicioTotal = datetime.datetime.now()

datas = [
20180415,
20180515,
20180615,
20180715,
20180815,
20180915,
20181015,
20181115,
20181215,
20190115,
20190215,
20190315,
20190415,
20190515,
20190615,
20190715,
20190815,
20190915,
20191015,
20191115,
20191215,
20200115,
20200215,
20200315,
20200415
]

#teste
# datas = [
# 20180415
# ]


outputPrefixosInfo = []

################ URLs #########################


#source = '3-source_files/3.3-validadores'
#bogonsList = '3-source_files/bogonsList.txt'


#source = '3-source_files/3.3-validadores/cropped_snapshots/20190815' # teste


############### BOGONS ######################

bogonPrefixesIgnored = set()
prefixesUsed = set()
bogon_file_path = '1-source/fullbogons-ipv4.txt'

# Função para ler os prefixos bogon do arquivo
def carregar_prefixos_bogon(arquivo):
    with open(arquivo, 'r') as f:
        linhas = f.readlines()
    prefixos = [linha.strip() for linha in linhas if not linha.startswith('#') and linha.strip()]
    return prefixos

# Carregar os prefixos bogon
bogon_prefixes = carregar_prefixos_bogon(bogon_file_path)

# Inicializar a árvore Patricia
trie = pytricia.PyTricia()

# Adicionar os prefixos bogon na árvore
for prefix in bogon_prefixes:
    trie.insert(prefix, "bogon")

# Função para verificar se um prefixo é bogon
def is_bogon(prefix):
    return trie.has_key(prefix) or trie.get_key(prefix) is not None






for currentDate in datas:


    print(f'Analisando {currentDate}...')
    source = f'2-source/snapshots/{currentDate}' # teste
    folder_name = os.path.basename(source)
    save_name = f'3-results/ipv4_prefixOriginPolicies/v4_sane_policies_{folder_name}.txt'  # FINAL              
    #save_name = f'5-ipv4_prefixes_policies/results_validadores/v4_policies_{folder_name}.txt'  # FINAL              



    #original_name = source.split('/')[-1]
    #date_file = original_name.split('.')[1]
    #save_name = '3-results/ipv4_prefixOriginPolicies/test_results_20190815fast.txt'   # TESTE
    #save_name = '3-results/ipv4_prefixOriginPolicies/test_results_validadores.txt'   # TESTE



    # ler varios arquivos sequenciais em uma pasta
    source_folder = []
    for nome_arquivo in os.listdir(source):
        # Criar o caminho completo para o arquivo
        caminho_completo = os.path.join(source, nome_arquivo)
        # Adicionar o caminho à lista
        source_folder.append(caminho_completo)





    parPrefixoASN = {}
    policy = 0 
    #prepend = set()





    ############## FUNCTIONS ##########################

    def tamanho_prepend(path):      
        path.reverse() 
        tamanho = 0
        for i in range(len(path) - 1):
            if path[i] == path[i+1]:
                tamanho += 1
            else:
                break  
        
        return tamanho
        


    #O dict associa prefixo aos valores: [asn anunciante, monitores, tamanho prepend, politica]
    def prefixoAnunciado(prefixo, aspath):
        prefix = prefixo 
        path = aspath.split(' ')                                                       # quebra em vários asn              
        anunciante = path[-1]
        
        tam_prep = tamanho_prepend(path)
        #print(f'O tamanho do prepend do prefixo {prefixo} anunciado por {anunciante} é {tam_prep}')
        #prepend.add(tam_prep)
        if prefix not in parPrefixoASN:
            parPrefixoASN[prefix] = [anunciante, 1, {tam_prep}, policy]       
        else:        
            if parPrefixoASN[prefix][0] == anunciante:
                parPrefixoASN[prefix][1] += 1
                parPrefixoASN[prefix][2].add(tam_prep)



    def politica(conjunto):
        # Verificar se o conjunto tem um elemento
        if len(conjunto) == 1:
            # Extrair o único elemento do conjunto
            elemento = next(iter(conjunto))
            # Verificar se o elemento é zero
            if elemento == 0:
                return 0
            else:
                return 1
        # Verificar se o conjunto tem dois elementos
        elif len(conjunto) == 2:
            return 2
        # Verificar se o conjunto tem mais de dois elementos
        elif len(conjunto) > 2:
            return 3




    ###################### EXECUCAO #####################


    for snapshot in source_folder:
        inicio = datetime.datetime.now()

        with open(snapshot, 'r') as arquivo:

            for linha in arquivo:
                coluna = linha.split('|') 
                #prepend.clear()
                try:
                    if(':' not in coluna[1]):                           
                        if is_bogon(coluna[1]) or coluna[1] == '0.0.0.0/0':
                            bogonPrefixesIgnored.add(coluna[1])
                        else:
                            prefixesUsed.add(coluna[1])
                            prefixoAnunciado(coluna[1], coluna[2])
                except:
                    print('Erro ao ler linha!')
                    pass
                



        ############ CALCULO DE BLOCO ################
        fim = datetime.datetime.now()                                       
        tempo_execucao = fim - inicio
        tempo_formatado = str(tempo_execucao).split('.')[0]
        corte = snapshot.split('\\')
        snap = corte[-1]
        print(f'Análise concluída! Snapshot: {snap} | Duracao: {tempo_formatado}')


    with open(save_name, 'w') as gravar_linhas:
        gravar_linhas.write('# Prefix | Origin | NumMonitors | list(;):ObservedPrepends | resultingPolicy\n')
        for key, value in parPrefixoASN.items():
            tam_prep_str = ';'.join(map(str, value[2]))
            gravar_linhas.write(f'{key}|{value[0]}|{value[1]}|{tam_prep_str}|{politica(value[2])}\n')
    
    # for key, value in parPrefixoASN.items():
    #     print(f'{key}|{value[0]}|{value[1]}|{value[2]}|{value[3]}')
    # for key, value in parPrefixoASN.items():
    #     # Converta o conjunto em uma string separada por ';'
    #     tam_prep_str = ';'.join(map(str, value[2]))
    #     print(f'{key}|{value[0]}|{value[1]}|{tam_prep_str}|{politica(value[2])}')

    
    totalPrefixesTemp = len(prefixesUsed) + len(bogonPrefixesIgnored)
    outputPrefixosInfo.append(f'{currentDate}|{totalPrefixesTemp}|{len(prefixesUsed)}|{len(bogonPrefixesIgnored)}')


############# USED AND IGNORED PREFIXES[DEBUG] #############


# Esse aqui é o arquivo de output com prefixos validos e invalidos em cada dia
agora = datetime.datetime.now()
data_hora_str = agora.strftime('%d%m%y.%H%M')
prefixesResults = f'3-results/ipv4_diverseInformations/v4ValidPrefixesInfo_{data_hora_str}.txt'

with open(prefixesResults, 'w') as writeLines:
    writeLines.write(f'# Time|Total_Prefixes|Valid_Prefixes|Bogon_Prefixes\n')
    for posicao in outputPrefixosInfo:
        writeLines.write(f'{posicao}\n')





############ CALCULO TOTAL ################
fimTotal = datetime.datetime.now()  
tempo_execucao_total = fimTotal - inicioTotal
tempo_execucao_total_format = str(tempo_execucao_total).split('.')[0]
print(f"Tempo de execução total das análises: {tempo_execucao_total_format}")



