
import matplotlib.pyplot as plt
import numpy as np
import os

pasta = 'ipv4/5_policy/results/main'   # AJUSTAR PASTA DE OUTPUT TAMBÉM!!
lista_snapshots = []

# Listar os arquivos na pasta
for nome_arquivo in os.listdir(pasta):
    caminho_completo = os.path.join(pasta, nome_arquivo)
    lista_snapshots.append(caminho_completo)

# Checagem de quantidade de arquivos
print(f'Pasta com Ribs localizada e possui {len(lista_snapshots)} itens.')



uniquePrefix = []  
noPrepenPrefix = []
uniformPrefix = []
binaryPrefix = []
diversePrefix = []

for snapshot in lista_snapshots:
    with open(snapshot, 'r') as arquivo:
        linhaEspecifica = arquivo.readlines()
        uniquePrefix.append(int(linhaEspecifica[4].strip()))
        noPrepenPrefix.append(int(linhaEspecifica[5].strip()))
        uniformPrefix.append(int(linhaEspecifica[6].strip()))
        binaryPrefix.append(int(linhaEspecifica[7].strip()))
        diversePrefix.append(int(linhaEspecifica[8].strip()))

# Dados fornecidos
Amostra_Total = np.array(uniquePrefix)
Prepend = np.array(noPrepenPrefix)
Uniform = np.array(uniformPrefix)
Binary = np.array(binaryPrefix)
Diverse = np.array(diversePrefix)

# Calculando as porcentagens
Prepend_percent = Prepend / Amostra_Total
Uniform_percent = Uniform / Amostra_Total
Binary_percent = Binary / Amostra_Total
Diverse_percent = Diverse / Amostra_Total

print(uniquePrefix)
print(noPrepenPrefix)
print(uniformPrefix)
print(binaryPrefix)
print(diversePrefix)

print(Prepend_percent)
print(Uniform_percent)
print(Binary_percent)
print(Diverse_percent)



# Rótulos para o eixo x
#rótulos = ["Abril '18", "Out '18", "Abril '19", "Out '19"]  # Certifique-se de que este array tenha o tamanho adequado

# Rótulos para o eixo x
#rotulos = ["Abril '18", "Out '18", "Abril '19", "Out '19", "Abril '20"]
rotulos = ['Apr/18', 'May/18', 'Jun/18', 'Aug/18', 'Sep/18', 'Oct/18', 'Nov/18', 'Dec/18', 'Jan/19', 'Feb/19', 'Mar/19', 'Apr/19', 'May/19', 'Jun/19', 'Jun/19', 'Aug/19', 'Sep/19', 'Oct/19', 'Dec/19', 'Jan/20', 'Feb/20', 'Mar/20', 'Apr/20']
#print(len(rotulos))
posicoes_x = np.arange(len(rotulos))
if len(lista_snapshots) != len(rotulos):  # Ajuste o número conforme a quantidade esperada de pontos de dados
    print(f'Erro: Número de arquivos difere do esperado! {len(lista_snapshots)} x {len(rotulos)} ')


# Criando o gráfico
plt.figure(figsize=(10, 6))
plt.plot(Prepend_percent, label='No Prepend',color='blue')
plt.plot(Uniform_percent, label='Uniform', color='yellow')
plt.plot(Binary_percent, label='Binary', color='purple')
plt.plot(Diverse_percent, label='Diverse', color='green')

# Configurando o título e os labels dos eixos
plt.title('Prefix-origin: Fractions through time of visible prefixes per ASPP policy.')
plt.xlabel('Time')
plt.ylabel('Fraction of fully visible prefixes')
plt.xticks(range(len(rotulos)), rotulos)  # Usando range para garantir a correspondência com o número de pontos
plt.xticks(rotation=45)
plt.ylim(0, 1)

# Adicionando a legenda
plt.legend()

# Exibindo o gráfico
plt.grid(True)
plt.savefig('ipv4/4_plots/Figure5.jpg')
plt.show()


