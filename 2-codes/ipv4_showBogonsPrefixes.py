

# Especificar o caminho do arquivo
#file_path = '3-results/ipv4_prefixOriginPolicies/v4ValidPrefixesInfo__280524.0039.txt'


dados = [
'20180415|742774|739665|3109',
'20180515|761873|758739|3134',
'20180615|777719|774515|3204',
'20180715|789476|786266|3210',
'20180815|804774|801555|3219',
'20180915|818988|815764|3224',
'20181015|833076|829839|3237',
'20181115|869059|865670|3389',
'20181215|899350|895921|3429',
'20190115|920435|916572|3863',
'20190215|933266|929403|3863',
'20190315|945813|941943|3870',
'20190415|961522|957642|3880',
'20190515|977741|973846|3895',
'20190615|992193|988290|3903',
'20190715|1003743|999830|3913',
'20190815|1016060|1012146|3914',
'20190915|1028397|1024478|3919',
'20191015|1041747|1037819|3928',
'20191115|1055829|1051892|3937',
'20191215|1069044|1065106|3938',
'20200115|1079190|1075251|3939',
'20200215|1092108|1088141|3967',
'20200315|1103664|1099584|4080',
'20200415|1119503|1115410|4093',
]
print(f'Data | Prefixos Validos | Bogons')
for item in dados:

    def calcular_porcentagens(linha):
        # Dividir a linha por '|' para extrair os valores
        partes = item.split('|')
        
        # Extrair os valores correspondentes
        data = partes[0]
        prefixos_analisados = int(partes[1])
        prefixos_validos = int(partes[2])
        prefixos_bogon = int(partes[3])
        
        # Calcular as porcentagens
        porcentagem_validos = (prefixos_validos / prefixos_analisados) * 100
        porcentagem_bogon = (prefixos_bogon / prefixos_analisados) * 100
        
        return data, porcentagem_validos, porcentagem_bogon

    # Exemplo de uso
    #linha = '20180715|789476|786266|3210'
    data, porcentagem_validos, porcentagem_bogon = calcular_porcentagens(item)
    
    print(f"{data} | {porcentagem_validos:.2f}% | {porcentagem_bogon:.2f}% ")
    # print(f"Porcentagem de Prefixos Válidos: ")
    # print(f"Porcentagem de Prefixos Bogon: {porcentagem_bogon:.2f}%")
