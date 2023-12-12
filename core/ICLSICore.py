# ICLSICore.py
# author: Felipe Cesar Cuellar da Silva <felipecesar@usp.br>
# description: Biblioteca com código compartilhado entre diversos módulos do sitema de automação da IC-LSI-2023

import os
import re
import tkinter as tk
from tkinter import simpledialog
from tkinter import filedialog
from tkinter import ttk


##### CAIXAS DE DIÁLOGO #####

font_config = {
    "font": "Helvetica",
    "size": "12"
}

# Classe da caixa de diálogo de Cascata, W e L de transistor.
# Atributos públicos: - cascata_var: Nome da cascata
#                     - l_var: Tamanho de L em microns
#                     - w_var: Tamanho de W em microns


class CmosDialog(simpledialog.Dialog):
    def __init__(self, parent, title="Adicionar Transistor", basename="", cascata_var=None, w_var=None, l_var=None, curva_var=None):
        self.cascata_var = cascata_var or tk.StringVar()
        self.w_var = w_var or tk.StringVar()
        self.l_var = l_var or tk.StringVar()
        self.curva_var = curva_var or tk.StringVar()
        self.basename = basename
        print(f"[INFO] Mapeamento manual do arquivo '{basename}'")
        super().__init__(parent, title)
    
    def body(self, master):

        style = ttk.Style()
        style.configure("Styled.TButton", padding=2, relief="flat", background="#F0F0F0", foreground="#000000")
        style.configure("Styled.TEntry" , padding=2, relief="flat", background="#F0F0F0", foreground="#000000")

        title_label = tk.Label(master, text="Informações básicas do transistor", font=(font_config["font"], 14, "bold"))
        file_label  = tk.Label(master, text=f"Arquivo: {self.basename}", font=(font_config["font"], 10, "italic"))
        title_label.grid(row=0, columnspan=2, pady=[10, 2])
        file_label.grid(row=1, columnspan=2, pady=[0, 10])

        tk.Label(master, text="Cascata:", font=(font_config["font"], font_config["size"])).grid(row=2)
        tk.Label(master, text="W:"      , font=(font_config["font"], font_config["size"])).grid(row=3)
        tk.Label(master, text="L:"      , font=(font_config["font"], font_config["size"])).grid(row=4)
        tk.Label(master, text="Curva:"  , font=(font_config["font"], font_config["size"])).grid(row=5)

        self.cascata_entry = ttk.Entry(master, textvariable=self.cascata_var, font=(font_config["font"], font_config["size"]), style="Styled.TEntry")
        self.w_entry       = ttk.Entry(master, textvariable=self.w_var      , font=(font_config["font"], font_config["size"]), style="Styled.TEntry")
        self.l_entry       = ttk.Entry(master, textvariable=self.l_var      , font=(font_config["font"], font_config["size"]), style="Styled.TEntry")
        self.curva_entry   = ttk.Entry(master, textvariable=self.curva_var  , font=(font_config["font"], font_config["size"]), style="Styled.TEntry")

        self.cascata_entry.grid(row=2, column=1, padx=5, pady=5)
        self.w_entry.grid(row=3, column=1, padx=5, pady=5)
        self.l_entry.grid(row=4, column=1, padx=5, pady=5)
        self.curva_entry.grid(row=5, column=1, padx=5, pady=5)

        return self.cascata_entry # Foco inicial

    def buttonbox(self):
        box = tk.Frame(self)

        # Botão OK personalizado
        ok_button = ttk.Button(box, text="OK", width=10, command=self.ok, style="Styled.TButton")
        ok_button.grid(row=0, column=0, padx=5, pady=5)

        # Botão Cancel personalizado
        cancel_button = ttk.Button(box, text="Cancelar", width=10, command=self.cancel, style="Styled.TButton")
        cancel_button.grid(row=0, column=1, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def apply(self):
        uppercased_curva = self.curva_var.get().upper()
        self.curva_var.set(uppercased_curva)

# Classe da caixa de diálogo que importa os arquivos de uma pasta
# Atributos públicos: - path_var: Caminho para a pasta dos arquivos

class FolderInputDialog(simpledialog.Dialog):
    def __init__(self, parent, title="Selecionar Pasta", path_var=None):
        self.path_var = path_var or tk.StringVar()
        super().__init__(parent, title)
    
    def body(self, master):
        style = ttk.Style()
        style.configure("Styled.TButton", padding=2, relief="flat", background="#F0F0F0", foreground="#000000")
        style.configure("Styled.TEntry" , padding=2, relief="flat", background="#F0F0F0", foreground="#000000")
        
        title_label = tk.Label(master, text="Indique a pasta de origem dos dados", font=(font_config["font"], 14, "bold"))
        title_label.grid(row=0, columnspan=2, pady=10)

        self.path_entry = ttk.Entry(master, textvariable=self.path_var, style="Styled.TEntry", width=60)
        self.path_entry.grid(row=1, column=0, padx=10, pady=10)

        self.select_button = ttk.Button(master, text="Buscar...", command=self.select_folder, style="Styled.TButton")
        self.select_button.grid(row=1, column=1, padx=0, pady=0)

        return self.path_entry # Foco inicial

    def buttonbox(self):
        box = tk.Frame(self)

        ok_button = ttk.Button(box, text="OK", width=10, command=self.ok, style="Styled.TButton")
        ok_button.grid(row=0, column=0, padx=5, pady=5)

        cancel_button = ttk.Button(box, text="Cancelar", width=10, command=self.cancel, style="Styled.TButton")
        cancel_button.grid(row=0, column=1, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()
    
    def select_folder(self):
        folder_selected = filedialog.askdirectory(title="Selecionar Pasta")
        if folder_selected:
            self.path_var.set(folder_selected)

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