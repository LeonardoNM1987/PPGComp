# ESSE CODIGO BAIXA OS ARQUIVOS DE RECURSOS DE ALOCAÇÃO INTERVALADOS TODO DIA 15 DE CADA MES..
# USANDO DATA E URL PERSONALIZAVEL PELO USUARIO
# SERA BAIXADO SEMPRE O ARQUIVO SEM EXTENSAO, COM O .TXT INSERIDO AO FINAL(opcional)

import os
import requests
from datetime import datetime, timedelta

def download_files(start_date, end_date, base_url, save_dir):
    # Criar o diretório de salvamento se ele não existir
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    current_date = start_date

    # Garantir que o start_date seja o dia 15
    if current_date.day != 15:
        current_date = current_date.replace(day=15)
    
    while current_date <= end_date:
        year = current_date.strftime('%Y')
        date_str = current_date.strftime('%Y%m%d')
        
        # Construir a URL do arquivo
        file_url = f"{base_url}/{year}/delegated-apnic-extended-{date_str}.gz"
        #file_url = f"{base_url}/delegated-lacnic-{date_str}"
        
        try:
            # Fazer o download do arquivo sem extensão
            response = requests.get(file_url)
            if response.status_code == 200:
                file_path = os.path.join(save_dir, f"delegated-apnic-extended-{date_str}.gz")
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                print(f"Arquivo {file_url} baixado com sucesso e salvo em {file_path}.")
            else:
                print(f"Arquivo {file_url} não encontrado.")
        
        except Exception as e:
            print(f"Erro ao baixar o arquivo {file_url}: {e}")
        
        # Avançar para o próximo mês
        next_month = current_date.month % 12 + 1
        next_year = current_date.year + (current_date.month // 12)
        current_date = current_date.replace(year=next_year, month=next_month)

# Datas de início e fim
start_date = datetime(2018, 4, 15)
end_date = datetime(2020, 4, 15)

# URL base
base_url = "https://ftp.lacnic.net/pub/stats/apnic"

# Diretório de salvamento
save_dir = "1-source/snapshots/resources/apnic"  # Substitua pelo caminho desejado

# Baixar os arquivos
download_files(start_date, end_date, base_url, save_dir)




















# Diretório de salvamento
save_dir = "1-source/snapshots/resources_temp"  # Substitua pelo caminho desejado

# Baixar os arquivos
download_files(start_date, end_date, base_url, save_dir)

