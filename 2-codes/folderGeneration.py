# ESTE CODIGO GERA PASTAS AUTOMATICAMENTE PERSOINALIZAVEL, DE 01/2011 ATÉ 03/2018
import os
from datetime import datetime, timedelta

# Função para gerar as datas
def generate_dates(start_year, start_month, end_year, end_month):
    dates = []
    current_date = datetime(start_year, start_month, 15)
    end_date = datetime(end_year, end_month, 15)
    
    while current_date <= end_date:
        dates.append(current_date.strftime('%Y%m%d'))
        # Adiciona um mês
        next_month = current_date.month + 2
        next_year = current_date.year + (next_month // 13)
        next_month = next_month % 12 or 12
        current_date = datetime(next_year, next_month, 15)
    
    return dates

# Diretório base onde as pastas serão criadas
#base_dir = 'C:\\caminho\\para\\diretorio\\base'
base_dir = 'C:\\Mestrado\\PPGComp\\1-source\\snapshots'

# Gera as datas
dates = generate_dates(2011, 1, 2018, 3)

# Cria as pastas para cada data
for date in dates:
    path = os.path.join(base_dir, date)
    os.makedirs(path, exist_ok=True)
    print(f'Pasta criada: {path}')
