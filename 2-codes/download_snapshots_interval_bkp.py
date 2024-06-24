# Este codigo baixa todos snapshots de:
# URL personalizável
# Abril de 2018 até Abril 2020 / Todo dia 15/ Todo horario 2200 - Aprox. 25 snapshots

import requests
import os
from datetime import datetime
import time

def download_ribs_files(start_year, start_month, end_year, end_month, download_dir):
    #base_url = 'https://routeviews.org/route-views.amsix/bgpdata/'  #amsterdam
    base_url = 'https://routeviews.org/route-views.sg/bgpdata/' #singapura
    day = 15
    hour = 2200
    current_date = datetime(start_year, start_month, 1)
    end_date = datetime(end_year, end_month, 1)

    # Certifique-se de que o diretório para os arquivos existe
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    while current_date <= end_date:
        time.sleep(5) # isso deve evitar algum bloqueio do meu ip no routeviews por excesso de conexões
        year = current_date.year
        month = current_date.month
        formatted_date = current_date.strftime('%Y.%m')
        file_name = f"rib.{year}{month:02d}{day}.{hour}.bz2"
        full_url = f"{base_url}/{formatted_date}/RIBS/{file_name}"

        # Tente fazer o download do arquivo
        try:
            response = requests.get(full_url, stream=True)
            if response.status_code == 200:
                file_path = os.path.join(download_dir, file_name)
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                print(f"Downloaded {file_name}")
            else:
                print(f"Failed to download {file_name} - HTTP status {response.status_code}")
        except Exception as e:
            print(f"An error occurred: {e}")

        # Avança para o próximo mês
        if month == 12:
            current_date = datetime(year + 1, 1, 1)
        else:
            current_date = datetime(year, month + 1, 1)

# Define o diretório de destino
download_directory = '0_bz2/singapore'

# Chamada da função para o intervalo desejado
download_ribs_files(2018, 4, 2020, 4, download_directory)
