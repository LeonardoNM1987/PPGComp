#!/bin/bash

# Diretório onde os arquivos .bz2 estão localizados
DIRECTORY="/path/to/your/files"

# Nova string para substituir 'rib'
NEW_STRING="nova_string" # Substitua 'nova_string' pela string desejada

# Navega para o diretório
cd "$DIRECTORY"

# Loop para processar cada arquivo .bz2
for bz2_file in *.bz2
do
    # Remove a extensão .bz2 para obter a base do nome do arquivo
    base_name=${bz2_file%.bz2}
    
    # Substitui 'rib' pela nova string na base do nome do arquivo
    new_base_name=${base_name/rib/$NEW_STRING}

    # Executa bgpscanner e redireciona a saída para um arquivo .txt
    bgpscanner $bz2_file >> "${new_base_name}.txt"

    echo "Converted $bz2_file to ${new_base_name}.txt"
done

echo "All files have been converted."
