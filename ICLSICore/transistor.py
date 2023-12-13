import os
import re

##### FUNÇÕES ISOLADAS #####

# Função getTransistorParams: Recebe o path do arquivo e extrai os parâmetros base.
# Retorno: - cascata
#          - l
#          - w

def getTransistorParams(filename):
    basename = os.path.basename(filename)
    dims = basename[3:]
    cascata = None
    if basename[0] == "C":
        cascata = basename[1:3]

    # Extrair o número entre 'L' e 'W'
    l_match = re.search(r'L(\d+)', dims)
    l = int(l_match.group(1)) if l_match else None

    # Extrair o número após 'W'
    w_match = re.search(r'W(\d+)', dims)
    w = int(w_match.group(1)) if w_match else None

    # Extrair a curva
    curva_match = re.search(r'CURVA_([A-Za-z]+)', dims)
    curva = str(curva_match.group(1)) if curva_match else None
    if curva:
        curva = curva.upper()
    return cascata, l, w, curva, basename