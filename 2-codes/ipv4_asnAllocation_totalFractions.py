# ESSE CODIGO VERIFICA O QUANTITATIVO E PERCENTAGEM DE ASES ENCONTRADOS POR REGIAO

import os
import pprint
import datetime

#################### URLs ##########################


# AQUI É CALCULADO A HORA ATUAL PARA GRAVACAO NO TXT RESULTADO
agora = datetime.datetime.now()
data_hora_str = agora.strftime('%d%m%y.%H%M')

# # TESTS
# url_resourcesFolder = f'validadores/asnAllocation/resources' # URL PARA TESTES
# url_savePath_quantitative = f'3-results/ipv4_asnAllocation/v4_asnAllocation_quantitative_{data_hora_str}.txt' # URL PARA TESTES
# url_savePath_percentage = f'3-results/ipv4_asnAllocation/v4_asnAllocation_percentage_{data_hora_str}.txt' # URL PARA TESTES
# url_dataFolder = 'validadores/asnAllocation/resources/'
# url_appResults = 'validadores/asnAllocation/results'

## ANALYSIS
url_resourcesFolder = f'1-source/resources' # URL PARA ANALISE 
url_savePath_quantitative = f'3-results/ipv4_asnAllocation/v4_asnAllocation_quantitative_{data_hora_str}.txt'
url_savePath_percentage = f'3-results/ipv4_asnAllocation/v4_asnAllocation_percentage_{data_hora_str}.txt' 
url_dataFolder = '1-source/resources/'
url_appResults = '3-results/ipv4_prefixOriginPolicies'




# CRIA UMA LISTA COM NOME DE CADA PASTA QUE REPRESENTA UMA DATA DE ANALISE
dateList = []
for folderDate in os.listdir(url_resourcesFolder):
    datePath = os.path.join(url_resourcesFolder, folderDate)
    #print(datePath)
    dateList.append(datePath.split('\\')[-1])

    
resultsByDate = {}

#HEADER FOR CONSOLE DEBUG
# print('\nASes identificados por região:\n')
# print('#Date|Afrinic|Apnic|Arin|Lacnic|RipeNCC|totalLocated|notFound ')


#ESSE 'FOR' É GERAL E ANALISA UMA DATA POR VEZ, BASEADO NA LISTA CRIADA ANTERIORMENTE
for date in dateList:
    print(f'\nAnalisando {date}')    
    resultsByDate[date] = {
        'afrinic':0,
        'apnic':0,
        'arin':0,
        'lacnic':0,
        'ripencc':0,
        'totalLocated':0,
        'notFound':0,
        'totalAnalyzed':0
        }
   

    dateFolder = f'{url_dataFolder}{date}' # URL PARA TESTES
    asppResults = f'{url_appResults}/v4_sane_policies_{date}.txt'  # URL PARA TESTES

    # dateFolder = f'{date}' # URL PARA ANALISE    
    # asppResults = f'/v4_sane_policies_{date}.txt'  # URL PARA ANALISE


    afrinic = {}
    apnic = {}
    arin = {}
    lacnic = {}
    ripencc = {}

    #DEFINE NOMES PARA CADA DICT, PARA TRABALHAR EM FORMA DE STR
    region_dicts = {
        'afrinic': afrinic,
        'apnic': apnic,
        'arin': arin,
        'lacnic': lacnic,
        'ripencc': ripencc
    }


    for delegatedFile in os.listdir(dateFolder):
        filePath = os.path.join(dateFolder, delegatedFile)
        fileName = filePath.split('\\')[-1]
        regionName = fileName.split('-')[1] 
        with open(filePath, 'r') as readDelegated:
            #totalASes = ''
            #print(f'{regionName}...')
            for linha in readDelegated:
                try:
                    coluna = linha.split('|')
                  
                    if (coluna[2] == 'asn') and (coluna[3] != '*'):                    
                        if coluna[3] not in region_dicts[regionName] and coluna[4]=='1':                            
                            region_dicts[regionName][coluna[3]] = set()
                        else:
                            startAsn = int(coluna[3])                        
                            somarAsn = int(coluna[4])                        
                            endAsn = startAsn + somarAsn
                            # print(f'ASN Inicial:{startAsn}')
                            # print(f'Somar X vezes:{somarAsn}')
                            # print(f'ASN Final:{endAsn}')
                            for item in range(startAsn, endAsn):
                                region_dicts[regionName][str(item)] = set()

                except Exception as e:
                    #print(f"Erro ao processar linha: {linha}\nErro: {e}")
                    pass


    # # JUST DEBUG                    
    # print('\nAlocação de ASNs por região: \n')
    # print(f'afrinic: {len(afrinic)}')
    # print(f'arin: {len(arin)}')
    # print(f'lacnic: {len(lacnic)}')
    # print(f'apnic: {len(apnic)}')
    # print(f'ripencc: {len(ripencc)}')

    

    asesNotFound = set()

    with open(asppResults, 'r') as readSanePolicies:
        next(readSanePolicies)
        numLinha = 0
        try:
            for line in readSanePolicies:
                #print(line)
                numLinha+=1
                coluna = line.split('|')    
                if (coluna[1] in afrinic):                                      
                    observedPrepends = coluna[3].replace(',', ';').split(';')                 
                    for valor in observedPrepends:
                        afrinic[coluna[1]].add(int(valor))
                elif (coluna[1] in arin):                                    
                    observedPrepends = coluna[3].replace(',', ';').split(';')                 
                    for valor in observedPrepends:
                        arin[coluna[1]].add(int(valor))
                elif (coluna[1] in lacnic):                                    
                    observedPrepends = coluna[3].replace(',', ';').split(';')                 
                    for valor in observedPrepends:
                        lacnic[coluna[1]].add(int(valor))
                elif (coluna[1] in apnic):                                    
                    observedPrepends = coluna[3].replace(',', ';').split(';')                 
                    for valor in observedPrepends:
                        apnic[coluna[1]].add(int(valor))                      
                elif (coluna[1] in ripencc):                                    
                    observedPrepends = coluna[3].replace(',', ';').split(';')                 
                    for valor in observedPrepends:
                        ripencc[coluna[1]].add(int(valor))
                else:
                    asesNotFound.add(coluna[1])  
        except:
            pass

            
    
    # AQUI SERÁ CALCULADO QUANTOS ASES FORAM ALOCADOS EM CADA DICIONARIO DE REGIAO
    afrinic_Detected = sum(1 for key, value in afrinic.items() if len(value) > 0)
    apnic_Detected = sum(1 for key, value in apnic.items() if len(value) > 0)
    arin_Detected = sum(1 for key, value in arin.items() if len(value) > 0)
    lacnic_Detected = sum(1 for key, value in lacnic.items() if len(value) > 0)
    ripe_Detected = sum(1 for key, value in ripencc.items() if len(value) > 0)
    
    

    totalLocated = afrinic_Detected+apnic_Detected+arin_Detected+lacnic_Detected+ripe_Detected
    totalAnalyzed = totalLocated + len(asesNotFound)

    #print(f'{date}|{afrinic_Detected}|{apnic_Detected}|{arin_Detected}|{lacnic_Detected}|{ripe_Detected}|{totalLocated}|{len(asesNotFound)}')
    
    resultsByDate[date]['afrinic'] = afrinic_Detected
    resultsByDate[date]['apnic'] = apnic_Detected
    resultsByDate[date]['arin'] = arin_Detected
    resultsByDate[date]['lacnic'] = lacnic_Detected
    resultsByDate[date]['ripencc'] = ripe_Detected
    resultsByDate[date]['totalLocated'] = totalLocated
    resultsByDate[date]['notFound'] = len(asesNotFound)
    resultsByDate[date]['totalAnalyzed'] = totalAnalyzed



    # resultsByDate[date]=[]
    # resultsByDate[date].append(apnic_Detected)
    # resultsByDate[date].append(arin_Detected)
    # resultsByDate[date].append(lacnic_Detected)
    # resultsByDate[date].append(ripe_Detected)
    # resultsByDate[date].append(totalLocated)
    # resultsByDate[date].append(len(asesNotFound))

# resultsByDate[date] = {
#         'afrinic':0,
#         'apnic':0,
#         'arin':0,
#         'lacnic':0,
#         'ripencc':0,
#         'totalLocated':0,
#         'notFound':0
#         }

    # #ESSE FOR CONTA APENAS OS PREPENDS EM CADA REGIAO EM CADA DATA DO 'FOR' PAI
    # for nome, item in region_dicts.items():    
    #     NoPrep = 0
    #     Prep = 0
    #     notDetected = 0 # nao usado    
    #     for key, value in item.items():       
    #         if len(value) > 1:
    #             Prep+=1
    #     resultsByDate[date][nome] = Prep
        

#end for by dates




#print(resultsByDate)
for key, value in resultsByDate.items():
    print(f'{key}:{value}')    


# QUANTITATIVE RESULTS
with open(url_savePath_quantitative, 'w') as saveFile:
    saveFile.write('# Date|afrinic|apnic|arin|lacnic|ripencc|totalLocated|notFound|totalAnalyzed\n')
    for date, data in resultsByDate.items():
        line = f"{date}|{data['totalAnalyzed']}|{data['afrinic']}|{data['apnic']}|{data['arin']}|{data['lacnic']}|{data['ripencc']}|{data['totalLocated']}|{data['notFound']}\n"
        saveFile.write(line) 
        

# PERCENTAGE RESULTS

with open(url_savePath_percentage, 'w') as saveFile:
    saveFile.write('# Date|afrinic|apnic|arin|lacnic|ripencc|totalLocated|notFound|totalAnalyzed\n')
    for date, data in resultsByDate.items():
        afrinic_percent = 100 *(float(data['afrinic']) / float(data['totalAnalyzed']))
        apnic_percent = 100 *(float(data['apnic']) / float(data['totalAnalyzed']))
        arin_percent = 100 *(float(data['arin']) / float(data['totalAnalyzed']))
        lacnic_percent = 100 *(float(data['lacnic']) / float(data['totalAnalyzed']))
        ripencc_percent = 100 *(float(data['ripencc']) / float(data['totalAnalyzed']))
        notFound_percent = 100 * (float(data['notFound']) / float(data['totalAnalyzed']))
        totalLocated_percent = afrinic_percent + apnic_percent + arin_percent + lacnic_percent + ripencc_percent         
        line = f"{date}|{data['totalAnalyzed']}|{afrinic_percent:.2f}|{apnic_percent:.2f}|{arin_percent:.2f}|{lacnic_percent:.2f}|{ripencc_percent:.2f}|{totalLocated_percent:.2f}|{notFound_percent:.2f}\n"
        saveFile.write(line) 












# # ESSE FOR CALCULA E PRINTA APENAS QUEM FEZ PREP POR REGIAO
# for date, values in resultsByDate.items():
#         formatted_values = '|'.join(str(values[region]) for region in ['afrinic', 'apnic', 'arin', 'lacnic', 'ripencc'])
#         print('\nFrações de ASes observados por região:')
#         print('#date|afrinic|apnic|arin|lacnic|ripencc\n')
#         print(f'{date}|{formatted_values}\n')










#########################################################
#
#    CRIAR CALCULO AUTOMATICO DE PORCENTAGENS
#
#########################################################





# for nome, item in region_dicts.items():


# print('Local -> NoPrep|Prep')
# for nome, item in region_dicts.items():
#     NoPrep = 0
#     Prep = 0
#     notDetected = 0 # nao usado
#     for key, value in item.items():
#         if len(value) == 0:
#             notDetected+=1
#         elif len(value) == 1 and 0 in value:
#             NoPrep+=1
#         elif len(value) > 1:
#             Prep+=1
#     print(f'{nome} -> {NoPrep}|{Prep}')



# for key, value in region_dicts.items():
#     print(f'{key}:{value}')  


# for key, value in afrinic.items():
#     print(f'{key}:{value}')    
# for key, value in arin.items():
#     print(f'{key}:{value}')  
# for key, value in ripencc.items():
#     print(f'{key}:{value}')  
# for key, value in lacnic.items():
#     print(f'{key}:{value}')  
# for key, value in apnic.items():
#     print(f'{key}:{value}')  
