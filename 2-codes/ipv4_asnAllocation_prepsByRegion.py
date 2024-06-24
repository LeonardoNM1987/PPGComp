# ESSE CODIGO VERIFICA QUAL PORCENTAGEM DE PREPENDS É FEITA EM CADA REGIAO
import os
import pprint
import datetime

############################################## URLs ####################################################


# AQUI É CALCULADO A HORA ATUAL PARA GRAVACAO NO TXT RESULTADO
agora = datetime.datetime.now()
data_hora_str = agora.strftime('%d%m%y.%H%M')

# ##TESTS
# print('# ANALISE DE TESTES EM ANDAMENTO... #')
# url_resourcesFolder = f'validadores/asnAllocation/resources'
# url_savePath_afrinic = f'3-results/ipv4_asnAllocation/v4_asnAllocation_prepsAfrinic_{data_hora_str}.txt'
# url_savePath_apnic = f'3-results/ipv4_asnAllocation/v4_asnAllocation_prepsApnic_{data_hora_str}.txt'
# url_savePath_arin = f'3-results/ipv4_asnAllocation/v4_asnAllocation_prepsArin_{data_hora_str}.txt'
# url_savePath_lacnic = f'3-results/ipv4_asnAllocation/v4_asnAllocation_prepsLacnic_{data_hora_str}.txt'
# url_savePath_ripencc = f'3-results/ipv4_asnAllocation/v4_asnAllocation_prepsRipencc_{data_hora_str}.txt'

# url_dataFolder = 'validadores/asnAllocation/resources/'
# url_appResults = 'validadores/asnAllocation/results'

## ANALYSIS
print('# ANALISE COMPLETA EM ANDAMENTO... #')
url_resourcesFolder = f'1-source/resources'
url_savePath_afrinic = f'3-results/ipv4_asnAllocation/v4_asnAllocation_prepsAfrinic_{data_hora_str}.txt'
url_savePath_apnic = f'3-results/ipv4_asnAllocation/v4_asnAllocation_prepsApnic_{data_hora_str}.txt'
url_savePath_arin = f'3-results/ipv4_asnAllocation/v4_asnAllocation_prepsArin_{data_hora_str}.txt'
url_savePath_lacnic = f'3-results/ipv4_asnAllocation/v4_asnAllocation_prepsLacnic_{data_hora_str}.txt'
url_savePath_ripencc = f'3-results/ipv4_asnAllocation/v4_asnAllocation_prepsRipencc_{data_hora_str}.txt'
url_dataFolder = '1-source/resources/'
url_appResults = '3-results/ipv4_prefixOriginPolicies'

########################################################################################################


# CRIA UMA LISTA COM NOME DE CADA PASTA QUE REPRESENTA UMA DATA DE ANALISE
dateList = []
for folderDate in os.listdir(url_resourcesFolder):
    datePath = os.path.join(url_resourcesFolder, folderDate)
    #print(datePath)
    dateList.append(datePath.split('\\')[-1])

    
#regionByDate = {}

afrinicPrep = {}
apnicPrep = {}
arinPrep = {}
lacnicPrep = {}
ripenccPrep = {}


#ESSE 'FOR' É GERAL E ANALISA UMA DATA POR VEZ, BASEADO NA LISTA CRIADA ANTERIORMENTE
for date in dateList:
    print(f'Analisando {date}\n')    
    
    
    #ESSES DICTS IRAO SALVAR OS RESULTADOS EM CADA DATA    
    afrinicPrep[date] = {'totalases':0,'geralprep':0,'noprep':0}
    apnicPrep[date]   = {'totalases':0,'geralprep':0,'noprep':0}
    arinPrep[date]    = {'totalases':0,'geralprep':0,'noprep':0}
    lacnicPrep[date]  = {'totalases':0,'geralprep':0,'noprep':0}
    ripenccPrep[date] = {'totalases':0,'geralprep':0,'noprep':0}
   

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

    #AQUI SAO CRIADOS OS DICTS DE CADA REGIAO COM OS ASES ALOCADOS
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
    # print('\nAlocação de ASNs por região:')
    # print(f'afrinic: {len(afrinic)}')
    # print(f'arin: {len(arin)}')
    # print(f'lacnic: {len(lacnic)}')
    # print(f'apnic: {len(apnic)}')
    # print(f'ripencc: {len(ripencc)}')

    
    #AQUI SERÁ FEITA DE FORMA QUE CADA LINHA SEJA COMPARADO COM CADA DICT DE REGIAO PREVIAMENTE CRIADO
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
 

    # print(f'\nAfrinic:{afrinic}')
    # print(f'Apnic:{apnic}')
    # print(f'Arin:{arin}')
    # print(f'Lacnic:{lacnic}')
    # print(f'Ripe:{ripencc}')

    # AQUI COMEÇA O CALCULO DE PREPS GERAL EM CADA REGIAO
    #regionListPrep = [afrinicPrep,apnicPrep,arinPrep,lacnicPrep,ripenccPrep]


    #DEFINIR A REGIAO 
    #regiao = ripencc
    ############# AFRINIC #################

    prep = 0
    NoPrep = 0
    NotDetected = 0
    
    for key, value in afrinic.items():
        if not value:
            NotDetected += 1
        elif value == {0}:
            NoPrep += 1
        else:
            prep += 1 

    afrinicPrep[date]['totalases'] = prep+NoPrep
    afrinicPrep[date]['geralprep'] = prep
    afrinicPrep[date]['noprep'] = NoPrep

    ############# APNIC #################

    prep = 0
    NoPrep = 0
    NotDetected = 0
    
    for key, value in apnic.items():
        if not value:
            NotDetected += 1
        elif value == {0}:
            NoPrep += 1
        else:
            prep += 1 

    apnicPrep[date]['totalases'] = prep+NoPrep
    apnicPrep[date]['geralprep'] = prep
    apnicPrep[date]['noprep'] = NoPrep

    ############# ARIN #################

    prep = 0
    NoPrep = 0
    NotDetected = 0
    
    for key, value in arin.items():
        if not value:
            NotDetected += 1
        elif value == {0}:
            NoPrep += 1
        else:
            prep += 1 

    arinPrep[date]['totalases'] = prep+NoPrep
    arinPrep[date]['geralprep'] = prep
    arinPrep[date]['noprep'] = NoPrep

    ############# LACNIC #################

    prep = 0
    NoPrep = 0
    NotDetected = 0
    
    for key, value in lacnic.items():
        if not value:
            NotDetected += 1
        elif value == {0}:
            NoPrep += 1
        else:
            prep += 1 

    lacnicPrep[date]['totalases'] = prep+NoPrep
    lacnicPrep[date]['geralprep'] = prep
    lacnicPrep[date]['noprep'] = NoPrep


    ############# RIPENCC #################

    prep = 0
    NoPrep = 0
    NotDetected = 0
    
    for key, value in ripencc.items():
        if not value:
            NotDetected += 1
        elif value == {0}:
            NoPrep += 1
        else:
            prep += 1 

    ripenccPrep[date]['totalases'] = prep+NoPrep
    ripenccPrep[date]['geralprep'] = prep
    ripenccPrep[date]['noprep'] = NoPrep
    
    

#end for separated by dates

#print(ripenccPrep)


#################################################### AFRINIC ####################################################

with open(url_savePath_afrinic, 'w') as afrinicFile:
    afrinicFile.write('        # QUANTITATIVE #')
    afrinicFile.write('\n# Date|totalases|geralprep|noprep')
    for date, values in afrinicPrep.items():
        afrinicFile.write(f'\n{date}|{values['totalases']}|{values['geralprep']}|{values['noprep']}')
    afrinicFile.write('\n        # PERCENTAGE #')
    afrinicFile.write('\n# Date|totalases|geralprep|noprep')
    for date, values in afrinicPrep.items():
        geralPrep_percent = 100 * (float(values['geralprep']))/(float(values['totalases']))
        noprep_percent    = 100 * (float(values['noprep']))/(float(values['totalases']))
        afrinicFile.write(f'\n{date}|{values['totalases']}|{geralPrep_percent:.2f}|{noprep_percent:.2f}')      
    
    print(f'File saved: v4_asnAllocation_prepsAfrinic_{data_hora_str}.txt')

#################################################### APNIC ####################################################

with open(url_savePath_apnic, 'w') as apnicFile:
    apnicFile.write('        # QUANTITATIVE #')
    apnicFile.write('\n# Date|totalases|geralprep|noprep')
    for date, values in apnicPrep.items():
        apnicFile.write(f'\n{date}|{values['totalases']}|{values['geralprep']}|{values['noprep']}')
    apnicFile.write('\n        # PERCENTAGE #')
    apnicFile.write('\n# Date|totalases|geralprep|noprep')
    for date, values in apnicPrep.items():
        geralPrep_percent = 100 * (float(values['geralprep']))/(float(values['totalases']))
        noprep_percent    = 100 * (float(values['noprep']))/(float(values['totalases']))
        apnicFile.write(f'\n{date}|{values['totalases']}|{geralPrep_percent:.2f}|{noprep_percent:.2f}')      
    
    print(f'File saved: v4_asnAllocation_prepsApnic_{data_hora_str}.txt')

#################################################### ARIN ####################################################

with open(url_savePath_arin, 'w') as arinFile:
    arinFile.write('        # QUANTITATIVE #')
    arinFile.write('\n# Date|totalases|geralprep|noprep')
    for date, values in arinPrep.items():
        arinFile.write(f'\n{date}|{values['totalases']}|{values['geralprep']}|{values['noprep']}')
    arinFile.write('\n        # PERCENTAGE #')
    arinFile.write('\n# Date|totalases|geralprep|noprep')
    for date, values in arinPrep.items():
        geralPrep_percent = 100 * (float(values['geralprep']))/(float(values['totalases']))
        noprep_percent    = 100 * (float(values['noprep']))/(float(values['totalases']))
        arinFile.write(f'\n{date}|{values['totalases']}|{geralPrep_percent:.2f}|{noprep_percent:.2f}')      
    
    print(f'File saved: v4_asnAllocation_prepsArin_{data_hora_str}.txt')

#################################################### LACNIC ####################################################

with open(url_savePath_lacnic, 'w') as lacnicFile:
    lacnicFile.write('        # QUANTITATIVE #')
    lacnicFile.write('\n# Date|totalases|geralprep|noprep')
    for date, values in lacnicPrep.items():
        lacnicFile.write(f'\n{date}|{values['totalases']}|{values['geralprep']}|{values['noprep']}')
    lacnicFile.write('\n        # PERCENTAGE #')
    lacnicFile.write('\n# Date|totalases|geralprep|noprep')
    for date, values in lacnicPrep.items():
        geralPrep_percent = 100 * (float(values['geralprep']))/(float(values['totalases']))
        noprep_percent    = 100 * (float(values['noprep']))/(float(values['totalases']))
        lacnicFile.write(f'\n{date}|{values['totalases']}|{geralPrep_percent:.2f}|{noprep_percent:.2f}')      
    
    print(f'File saved: v4_asnAllocation_prepsLacnic_{data_hora_str}.txt')


#################################################### RIPENCC ####################################################

with open(url_savePath_ripencc, 'w') as ripenccFile:
    ripenccFile.write('        # QUANTITATIVE #')
    ripenccFile.write('\n# Date|totalases|geralprep|noprep')
    for date, values in ripenccPrep.items():
        ripenccFile.write(f'\n{date}|{values['totalases']}|{values['geralprep']}|{values['noprep']}')
    ripenccFile.write('\n        # PERCENTAGE #')
    ripenccFile.write('\n# Date|totalases|geralprep|noprep')
    for date, values in ripenccPrep.items():
        geralPrep_percent = 100 * (float(values['geralprep']))/(float(values['totalases']))
        noprep_percent    = 100 * (float(values['noprep']))/(float(values['totalases']))
        ripenccFile.write(f'\n{date}|{values['totalases']}|{geralPrep_percent:.2f}|{noprep_percent:.2f}')      
    
    print(f'File saved: v4_asnAllocation_prepsRipencc_{data_hora_str}.txt')

