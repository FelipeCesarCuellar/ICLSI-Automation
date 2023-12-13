# DataExtractionModule.py
# author: Felipe Cesar Cuellar da Silva <felipecesar@usp.br>
# description: Módulo para a extração automática dos arquivos dos transistores

from tkinter import messagebox
import tkinter as tk
import pandas as pd
import originpro as op
import glob

from ICLSICore.dialogs import CmosDialog, FolderInputDialog
from ICLSICore.transistor import getTransistorParams

root = tk.Tk()
root.withdraw()

path = ""

while True:
    dialog = FolderInputDialog(root)
    path = dialog.path_var.get()
        
    if not path:
        messagebox.showwarning("Pasta inválida", "Preencha corretamente o caminho para a pasta e clique em OK.")
        
    else:
        break

wildcard = path + "/*.txt"
files = glob.glob(wildcard)

print(f"[INFO] Files: {files}")

for file in files:
    cascata, l, w, curva, basename = getTransistorParams(file) # Extrai os parâmetros automaticamente
    if any(param is None for param in [cascata, l, w, curva]): # Se algo deu errado
        while True:
            dialog = CmosDialog(root, basename=basename) # Usar caixa manual
            cascata = dialog.cascata_var.get()
            l = dialog.l_var.get()
            w = dialog.w_var.get()
            curva = dialog.curva_var.get()
            
            if any(param is None for param in [cascata, l, w, curva]): # Enquanto preencher errado, avisar
                messagebox.showwarning("Inforações inválidas", "Preencha corretamente as informações da medida e clique em OK.")
            else:
                break # Preencheu certo, então podemos seguir

    with open(file, 'r', encoding='utf-8') as data: # Leitura dos dados dentro do arquivo. Enviar ele para o módulo principal
        content = data.read()
        print(f"[INFO] Cascata: {cascata} - L: {l} - W: {w} - Curva: {curva}")
        df = pd.read_table(file, delim_whitespace=True)
        df = df.drop(columns=["Vb"])
        print(df)
        wks = op.new_sheet()
        wks.from_df(df)
        wks

root.destroy()
    