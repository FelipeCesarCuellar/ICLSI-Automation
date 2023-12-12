# input_window.py
# author: Felipe Cesar Cuellar da Silva <felipecesar@usp.br>
# description: Script para o teste de janelas no origin

import sys
import os
import re
from tkinter import messagebox
import originpro as op
import tkinter as tk
from ICLSICore import CmosDialog, FolderInputDialog
import glob

def getTransistorParams(filename):
    basename = os.path.basename(filename)
    dims = basename[3:-1]
    print(f"DIMS: {dims}")
    cascata = None
    if basename[0] == "C":
        cascata = basename[1:3]

    # Extrair o número entre 'L' e 'W'
    l_match = re.search(r'L(\d+)', dims)
    l = int(l_match.group(1)) if l_match else None

    # Extrair o número após 'W'
    w_match = re.search(r'W(\d+)', dims)
    w = int(w_match.group(1)) if w_match else None
    print(f"[INFO] Extracted - Cascata: {cascata}, L: {l}, W: {w}")
    return cascata, l, w





print(f"[INFO] Quantidade de argumentos: {len(sys.argv)}")
for i in range(len(sys.argv)):
    print(f"[INFO] Argumento {i+1}: {sys.argv[i]}")

root = tk.Tk()
root.withdraw()

path = ""

while True:
    dialog = FolderInputDialog(root)

    path = dialog.path_var.get()

    if not path:
        print("[WARN] Pasta inexistente")
        messagebox.showwarning("Pasta inválida", "Preencha corretamente o caminho para a pasta e clique em OK.")
    else:
        print(f"[INFO] Path selecionado: {path}")
        break

root.destroy() # Destroi o root após executar a janela
root.mainloop() # Só executa se o root n foi destruído (posso fazer outro método aqui. E se eu jogasse um while com condicional (root)?
print("[INFO] Saindo do loop de janela")

wildcard = path + "/*.txt"

files = glob.glob(wildcard)

print(f"FILES IS {files}")

for file in files:
    print(f"[INFO] Arquivo identificado: {file}")
    getTransistorParams(file)
    with open(file, 'r', encoding='utf-8') as data:
        content = data.read()
        print(f"[INFO] Message: {content}")