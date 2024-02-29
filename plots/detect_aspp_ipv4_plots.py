import matplotlib.pyplot as plt





# Supondo que você leu esses dados do seu arquivo txt
# Estes são apenas dados de exemplo
total_prepends = 100  # Valor hipotético
origem_prepends = [10, 20, 5, 40]  # Lista hipotética ao longo do tempo
intermed_prepends = [5, 1, 2, 5]  # Lista hipotética ao longo do tempo
unique_ases = [1, 3, 2, 4]  # Lista hipotética ao longo do tempo

# Datas correspondentes aos seus dados
dates = ['2010', '2013', '2016', '2020']  # As datas devem corresponder aos seus dados

# Criando o gráfico
plt.plot(dates, origem_prepends, marker='o', label='Prepends Totais')
plt.plot(dates, intermed_prepends, marker='s', label='Prep.Origem')
plt.plot(dates, unique_ases, marker='x', label='Prep.Intermed.')

# Adicionando título e rótulos
plt.title('Fração de ASes utilizando ASPP')
plt.xlabel('Período (Mensal, Jan2010-Abr2020)')
plt.ylabel('Fração de Ases Unicos')

# Adicionando legenda
plt.legend()

# Mostrando o gráfico
plt.show()

#plt.savefig('plots/plot01.png')
