import datetime
import os

#folder URL
policiesFolder = '3-results\ipv4_prefixOriginPolicies'


for file in os.listdir(policiesFolder):

    if file.startswith('v4_sane_policies_'):        
        
        # Files URLs
        #source = '3-results/ipv4_prefixOriginPolicies/v4_sane_policies_20180415.txt'
        source = os.path.join(policiesFolder, file)
        currentDate  = file[len('v4_sane_policies_'):-len('.txt')]
        
        agora = datetime.datetime.now()
        data_hora_str = agora.strftime('%d%m%y.%H%M')
        output = f'3-results/ipv4_asesPolicies/v4_asesPolicies_{currentDate}.txt'

        # Inicializar o dicionário
        asesPolicies = {}

        # Função para processar o arquivo
        def processar_arquivo(arquivo, num_linhas=None):
            with open(arquivo, 'r') as f:
                # Ignorar a primeira linha (cabeçalho)
                next(f)
                linha_contador = 0
                for linha in f:
                    if num_linhas and linha_contador >= num_linhas:
                        break
                    
                    partes = linha.strip().split('|')
                    sistema_autonomo = partes[1]
                    politica = partes[4]

                    # Se a chave já existe no dicionário, adiciona a política se não estiver presente
                    if sistema_autonomo in asesPolicies:
                        if politica not in asesPolicies[sistema_autonomo]['policies']:
                            asesPolicies[sistema_autonomo]['policies'].append(politica)
                    else:
                        # Se a chave não existe, cria uma nova entrada com a política
                        asesPolicies[sistema_autonomo] = {'policies': [politica], 'geral_policy': ''}

                    linha_contador += 1

        # Função para determinar a Política Geral
        def determinar_politica_geral(policies):
            if len(policies) == 1:
                if policies[0] == '0':
                    return 'NoPrepend'
                elif policies[0] == '1':
                    return 'Uniform'
                elif policies[0] == '2':
                    return 'Binary'
                elif policies[0] == '3':
                    return 'Diverse'
            else:
                return 'Mixed'

        qtdeLinhas = 999999999

        ######################## EXECUCAO #############################



        # Processar o arquivo
        print(f'Analisando arquivo {file}...')
        processar_arquivo(source, qtdeLinhas)

        # Determinar a Política Geral para cada AS
        for asn, data in asesPolicies.items():
            geral_policy = determinar_politica_geral(data['policies'])
            asesPolicies[asn]['geral_policy'] = geral_policy

        # Escrever o resultado no arquivo de saída
        with open(output, 'w') as outputLinhas:
            outputLinhas.write(f'# AS|ObservedPolicies|GeralPolicy\n')
            for key, data in asesPolicies.items():
                politicasFormated = ';'.join(data['policies'])
                outputLinhas.write(f'{key}|{politicasFormated}|{data["geral_policy"]}\n')
        print(f'Analise concluída. Salvo em {output}...')
    #fim if startwiths
#fim for folder