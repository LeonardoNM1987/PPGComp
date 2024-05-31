import os
import matplotlib.pyplot as plt
from datetime import datetime


source = '5-ipv4_policy/results'
#source = '5-ipv4_policy/results_validadores'


dates = {}
source_folder = []
for nome_arquivo in os.listdir(source):
    # Criar o caminho completo para o arquivo
    caminho_completo = os.path.join(source, nome_arquivo)    
    
    # Adicionar o caminho à lista
    source_folder.append(caminho_completo)

#o tamanho do conjunto abaixo será a amostragem total para o eixo y
uniquePrefixes = set()


for snapshot in source_folder:
    countPrefixes = 0
    dateReference = snapshot.split('_policies_')[1].split('.')[0]
    dates[dateReference] = {
            'prefixes':0,
            'noprep':0, 
            'uniform':0, 
            'binary':0,
            'diverse':0            
            }

    with open(snapshot, 'r') as arquivo:
        #linha abaixo lê e ignora o cabecalho
        arquivo.readline() 
        
        for linha in arquivo:
            countPrefixes+=1
            coluna = linha.split('|')
            uniquePrefixes.add(coluna[0])
            if(int(coluna[4])==0):
                dates[dateReference]['noprep']+=1
            if(int(coluna[4])==1):
                dates[dateReference]['uniform']+=1
            if(int(coluna[4])==2):
                dates[dateReference]['binary']+=1
            if(int(coluna[4])==3):
                dates[dateReference]['diverse']+=1
    dates[dateReference]['prefixes'] = countPrefixes
    print(f'{dateReference} concluída.')    
        

#print(dates)
print(f'\nQuantidade de prefixos únicos: {len(uniquePrefixes)}')
for key, value in dates.items():
    print(f'{key}: {value}')


############### GERANDO GRÁFICO ########

#Essa function irá padronizar as datas na legenda do eixo x
def formatar_data(data_str):
    data = datetime.strptime(data_str, "%Y%m%d")
    return data.strftime("%b/%y")


datas = []
noprep_percent = []
uniform_percent = []
binary_percent = []
diverse_percent = []

# Extraindo os dados do dicionário e calculando as porcentagens
for data, valores in dates.items():
    total_prefixes = valores['prefixes']
    datas.append(formatar_data(data))
    noprep_percent.append(valores['noprep'] / total_prefixes * 100)
    uniform_percent.append(valores['uniform'] / total_prefixes * 100)
    binary_percent.append(valores['binary'] / total_prefixes * 100)
    diverse_percent.append(valores['diverse'] / total_prefixes * 100)



# Plotando os dados
plt.figure(figsize=(10, 6))
plt.plot(datas, noprep_percent, marker='.' ,label='No-prepend', color='blue')
plt.plot(datas, uniform_percent, marker='.' ,label='Uniform', color='yellow')
plt.plot(datas, binary_percent, marker='.' ,label='Binary', color='purple')
plt.plot(datas, diverse_percent, marker='.' ,label='Diverse', color='green')

# Configurando o gráfico
plt.xlabel('Período (Mensal, Todo dia 15 de Abr/2018 até Abr/2020)')
plt.ylabel('Prefixos Visíveis (%)', fontsize='8')
plt.suptitle('Prefixos categorizados de acordo com as políticas de ASPP\n ao longo do tempo.', fontsize='14')
plt.title('Coletores: São Paulo, Amsterdam e Singapura', fontsize='10', pad=25)
plt.legend()
plt.grid(True)

#formatar eixo x com intervalos
#Explicação:
    #intervalo = 6: Define o intervalo para os ticks no eixo x (a cada 6 meses).
    #ticks = [i for i in range(0, len(datas), intervalo)]: Gera uma lista de índices que representam os pontos no eixo x onde os ticks serão colocados.
    #tick_labels = [datas[i] for i in ticks]: Cria os rótulos dos ticks com base nos índices.
    #plt.xticks(ticks, tick_labels, rotation=45): Define os ticks e os rótulos no eixo x, rotacionando-os em 45 graus para melhor legibilidade.

intervalo = 4
ticks = [i for i in range(0, len(datas), intervalo)]
tick_labels = [datas[i] for i in ticks]
plt.xticks(ticks, tick_labels, fontsize='8')
#plt.xticks(rotation=45) #eixo basico, com todas datas

plt.ylim(0, 100)  # Ajuste os valores conforme necessário
plt.yticks(range(0, 101, 10))  # Define ticks de 10 em 10

# Exibindo o gráfico
plt.tight_layout()
# plt.show()




#salvando gráfico

agora = datetime.now()
data_hora_str = agora.strftime('%d%m%y.%H%M')

pltSaveName = f'./plot{data_hora_str}.jpg'
diretorio_script = os.path.dirname(os.path.abspath(__file__))
caminho_completo = os.path.join(diretorio_script, pltSaveName)

plt.savefig(caminho_completo, format='jpg')
print(f'Gráfico salvo como: {pltSaveName}')