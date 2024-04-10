# 1 - Total de prepends contabilizados (prependTotais)
# 2 - Lista de ASes com prepend na prependOrigem (prependOrigem)
# 3 - Lista de ASes com prepend prependIntermediario (prependIntermed)
# 4 - Lista de ASes que fazem prepend nivel 1 (prepNivel1)
# 5 - Lista de ASes que fazem prepend nivel 2 (prepNivel2)
# 6 - Lista de ASes que fazem prepend nivel 3 (prepNivel3)
# 7 - Lista de ASes que fazem prepend nivel 4 ou + (prepNivel4plus)
# 8 - Lista de ASes unicos visualizados (asesTotais)
# 9 - ASes com seus respectivos vizinhos listados (vizinhos)

import matplotlib.pyplot as plt

totalPrepends2011ate2020 = []  # 5 valores correspondetes a 2011, 2013, 2015, 2017 e 2020
asesUnicos = []
totalASes2011ate2020 = []
prepOrigem2011ate2020 = []
prepIntermed2011ate2020 = []
prepOrig_Intermed2011ate2020 = []


prependTotalTemp = []
prependTotal = []
dates = ['2011', '2013', '2015', '2017', '2020']  # As datas devem corresponder aos seus dados
fractionTotalPreps = []
fractionPrepsOrigem = []
fractionPrepsIntermed = []
fractionPrepsOrigIntermed = []

sourceBatch = [
    'results/rib.20110320.0000_ipv4_results.txt',
    'results/rib.20130320.0000_ipv4_results.txt',
    'results/rib.20150320.0000_ipv4_results.txt',
    'results/rib.20170320.0000_ipv4_results.txt',
    'results/rib.20200320.0000_ipv4_results.txt'    
]

for resultado in sourceBatch:    
    with open(resultado, 'r') as arquivo:                                                                       
        linhaEspecifica = arquivo.readlines()        
        #totalPrepends2011ate2020.append(linhaEspecifica[0].strip())
        asesUnicos.append(int(linhaEspecifica[0]))
        prependTotal.append(int(linhaEspecifica[1]))
        prepOrigem2011ate2020.append(int(linhaEspecifica[2]))
        prepIntermed2011ate2020.append(int(linhaEspecifica[3]))  
        prepOrig_Intermed2011ate2020.append(int(linhaEspecifica[4]))  
        #prependTotalTemp = len(linhaEspecifica[2].strip()) + len(linhaEspecifica[2].strip())
        #totalPrepends2011ate2020.append(prependTotalTemp)
        #prependTotalTemp = ''

############  PROMPT PARA DEBUG #################
print(f'Anos analisados: {dates}')
print(f'ASes únicos visualizados em cada ano: {asesUnicos}')
print(f'Prepends totais observados em cada ano: {prependTotal}')
print(f'Prepends na Origem em cada ano: {prepOrigem2011ate2020}')
print(f'Prepends Intermediarios em cada ano: {prepIntermed2011ate2020}')
print(f'Prepends em Ambas posições em cada ano: {prepOrig_Intermed2011ate2020}')
# for x in range(5):
#     print(f'No ano de {dates[x]}, dos {asesUnicos[x]} ASes totais, {totalPrepends2011ate2020[x]} realizam prepend, sendo {prepOrigem2011ate2020[x]} na Origem e {prepIntermed2011ate2020[x]} de forma Intermediaria.')

for item in range(5):    
    fractionTotalPreps.append("{:.2f}".format((prependTotal[item]/asesUnicos[item])*100))
    fractionPrepsOrigem.append("{:.2f}".format((prepOrigem2011ate2020[item]/asesUnicos[item])*100))
    fractionPrepsIntermed.append("{:.2f}".format((prepIntermed2011ate2020[item]/asesUnicos[item])*100))
    fractionPrepsOrigIntermed.append("{:.2f}".format((prepOrig_Intermed2011ate2020[item]/asesUnicos[item])*100))

for x in range(5):
    print(f'-----------------------------------------------------')
    print(f'{dates[x]}:')
    print(f'{asesUnicos[x]}  ases observados ')
    print(f'{prependTotal[x]} ({fractionTotalPreps[x]}%) - executam algum tipo de prepend(orig, interm ou Ambos) ')
    print(f'{prepOrigem2011ate2020[x]} ({fractionPrepsOrigem[x]}%) - executam apenas na origem.')
    print(f'{prepIntermed2011ate2020[x]} ({fractionPrepsIntermed[x]}%) - executam apenas intermediaria.')
    print(f'{prepOrig_Intermed2011ate2020[x]} ({fractionPrepsOrigIntermed[x]}%) - executam em ambas as posições')

    

# # print(fractionTotalPreps)
# # print(fractionPrepsOrigem)
# # print(fractionPrepsIntermed)


# ############ PLOT #################

fractionTotalPreps = [float(x) for x in fractionTotalPreps]
fractionPrepsOrigem = [float(x) for x in fractionPrepsOrigem]
fractionPrepsIntermed = [float(x) for x in fractionPrepsIntermed]

# Convertendo as porcentagens em frações
fractionTotalPreps = [x / 100 for x in fractionTotalPreps]
fractionPrepsOrigem = [x / 100 for x in fractionPrepsOrigem]
fractionPrepsIntermed = [x / 100 for x in fractionPrepsIntermed]

# Ordenando os dados pelo ano, pois parece haver um erro na ordem de 'dates'
sorted_data = sorted(zip(dates, fractionTotalPreps, fractionPrepsOrigem, fractionPrepsIntermed))
dates, fractionTotalPreps, fractionPrepsOrigem, fractionPrepsIntermed = zip(*sorted_data)

# Criando a figura e o eixo para o gráfico
plt.figure(figsize=(10, 6))

# Plotando os dados
plt.plot(dates, fractionTotalPreps, 'o-', label='Total de Prepends')
plt.plot(dates, fractionPrepsOrigem, 's-', label='Prepends na Origem')
plt.plot(dates, fractionPrepsIntermed, '^-', label='Prepends Intermediários')

# Adicionando título e rótulos aos eixos
plt.title('ASPP de 2011 to 2020')
plt.xlabel('Ano')
plt.ylabel('Fração de ASes Únicos Observados')

# Definindo os ticks no eixo x e eixo y
plt.xticks(sorted(dates))
#plt.yticks([i / asesUnicos[0] for i in range(0, int(max(asesUnicos)) + 1)])
plt.yticks([i * 0.1 for i in range(0, 11)])

# Habilitando a legenda e a grade
plt.legend()
plt.grid(True)

# Exibindo o gráfico
plt.show()

#plt.savefig('plots/plot01.png')
