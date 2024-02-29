import matplotlib.pyplot as plt

# Supondo que você leu esses dados do seu arquivo txt
# Estes são apenas dados de exemplo
total_prepends = 100  # Valor hipotético
origem_prepends = [10, 20, 30, 40]  # Lista hipotética ao longo do tempo
intermed_prepends = [5, 15, 25, 35]  # Lista hipotética ao longo do tempo
unique_ases = [1, 3, 2, 4]  # Lista hipotética ao longo do tempo

# Datas correspondentes aos seus dados
dates = ['2010', '2013', '2016', '2020']  # As datas devem corresponder aos seus dados

# Criando o gráfico
plt.plot(dates, origem_prepends, marker='o', label='Prepended')
plt.plot(dates, intermed_prepends, marker='s', label='Origin-Prep.')
plt.plot(dates, unique_ases, marker='x', label='Interm.-Prep.')

# Adicionando título e rótulos
plt.title('Fraction of ASes deploying ASPP')
plt.xlabel('Time (monthly, Jan2010-Apr2020)')
plt.ylabel('Fraction of unique ASes')

# Adicionando legenda
plt.legend()

# Mostrando o gráfico
plt.show()
