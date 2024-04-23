#!/bin/bash

# Diretório onde os arquivos .bz2 estão localizados
DIRECTORY="/path/to/your/files"

# Navega para o diretório
cd "$DIRECTORY"

# Loop para processar cada arquivo .bz2
for bz2_file in *.bz2
do
    # Remove a extensão .bz2 para obter a base do nome do arquivo
    base_name=${bz2_file%.bz2}

    # Executa bgpscanner e redireciona a saída para um arquivo .txt
    bgpscanner $bz2_file >> "${base_name}.txt"

    echo "Converted $bz2_file to ${base_name}.txt"
done

echo "All files have been converted."
