
#O que procurar?
# 1º: Quais pares prefixo não fazem prepend? (Ver Quais ases não fazem)
# 2º: Quais fazem sempre o mesmo prepend na amostragem
# 3º: 

#Dados que preciso, nos resultados e nas respectivas linhas:
# 18 - Conjunto de prefixos que fazem prepend na Origem
# 19 - Dicionario que associa ASes com os prefixos anunciados que fazem prepend na Origem
# 20 - Dicionario que lista quais ASes anunciam quais prefixos

import ast #modulo de conversao de str para dict

# sourceBatch = [
#     'results/rib.20110320.0000_ipv4_results.txt',
#     'results/rib.20130320.0000_ipv4_results.txt',
#     'results/rib.20150320.0000_ipv4_results.txt',
#     'results/rib.20170320.0000_ipv4_results.txt',
#     'results/rib.20200320.0000_ipv4_results.txt'    
# ]
sourceBatch = [
    '3_results/rib.20170320.0000_ipv4_results.txt'        
]

prefixOrigin = {}

noPrependPrefixes = set()
uniformPrefixes = set()
binaryPrefixes = set()
diversePrefixes = set()

conjPrefixosUnicos = set()          # todos prefixos unicos detectados
conjPrependedOrigPrefix = set()     # todos prefixos com prepend
conjNoPrependPrefix = set()         # todos prefixos sem Prepend


for resultado in sourceBatch:    
    with open(resultado, 'r') as arquivo:                                                                       
        linhaEspecifica = arquivo.readlines()
        conjPrefixosUnicos = ast.literal_eval(linhaEspecifica[21])
        conjPrependedOrigPrefix = ast.literal_eval(linhaEspecifica[17])  
        conjNoPrependPrefix = conjPrefixosUnicos -  conjPrependedOrigPrefix
        
        #prefixOrigin = ast.literal_eval(linhaEspecifica[19])   #prefixos anunciados que fazem prepend na Origem
        
        

        # for asn, prefixes in prefixOrigin.items():
        #     # Verifica se o ASN está no conjunto de ASes únicos
        #     if asn in conjAsesUnicos:
        #         # Adiciona os prefixos associados ao ASN ao conjunto 'conjNoPrependPrefix'
        #         conjNoPrependPrefix.update(prefixes)

print(len(conjPrefixosUnicos))
print(len(conjPrependedOrigPrefix))
print(len(conjNoPrependPrefix))

# Exibe os prefixos que não têm prepend
#print("Prefixos sem prepend:", conjNoPrependPrefix)

        
        #print(linhaEspecifica[19])
        # v2.append(int(linhaEspecifica[1]))
        # v3.append(int(linhaEspecifica[2]))
        # v4.append(int(linhaEspecifica[3]))  
        # v5.append(int(linhaEspecifica[4]))  

        




        #asesNoPrepend = conjAsesUnicos - conjPrepOrigemANDintermed
            

            # Itera sobre as chaves do dicionário prefixOrigin
