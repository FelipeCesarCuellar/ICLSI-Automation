import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

def requirements():
    # Função que verifica se os requisitos para se obter Vt foram cumpridos -> Ainda não implementado
    return True

def configure():
    return

# Extrai Vt pelo método da segunda derivada
def execute(dataframes):
    print("\n ======= Módulo de extração de Vt ========")
    if not requirements(): 
        print("[ERRO] Dados insufientes para se obter Vt")
        return
    print(f"[INFO] Etapa atual: extrair Vt pela segunda derivada")
    for df in dataframes:
        print(f"[INFO] Arquivo: {df.attrs['Filename']} - Cascata: {df.attrs['Cascata']} - W: {df.attrs['W']} - L: {df.attrs['L']}")
        df = df.sort_values(by='VG')

        # Aplicar Savitzky-Golay para suavizar a curva original
        # Script original em LabTalk: Window_size = 24 order = 3
        window_size_smooth = 17
        order_smooth = 3
        window_size_derivative = 17
        order_derivative = 3

        df['Id_smoothed'] = savgol_filter(df['Id'], window_size_smooth, order_smooth)
        df['Id_first_derivative'] = np.gradient(df['Id_smoothed'])
        df['Id_smoothed_derivative'] = savgol_filter(df['Id_first_derivative'], window_size_derivative, order_derivative)
        df['Id_second_derivative'] = np.gradient(df['Id_smoothed_derivative'])
        second_derivative = df['Id_second_derivative']
        original_second_derivative = np.gradient(np.gradient(df['Id']))

        max_index = np.argmax(second_derivative)
        print(f"       Vt estimado: {df['VG'][max_index]} V")

        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(8, 6))

        ax1.plot(df['VG'], df['Id'], label='Curva Original sem filtro', color='green', zorder=1)
        ax1.plot(df['VG'], df['Id_smoothed'], label='Curva Original Suavizada', zorder=1)
        ax1.set_ylabel('Id')
        ax1.set_title('Curva Original Suavizada')

        ax2.plot(df['VG'], original_second_derivative, color='orange', label='Segunda Derivada sem filtro', zorder=1)
        ax2.plot(df['VG'], second_derivative, color='blue', label='Segunda Derivada Suavizada', zorder=1)
        ax2.scatter(df['VG'][max_index], second_derivative[max_index], color='green', label=f'Máximo em: VG={df["VG"][max_index]}', zorder=2)
        ax2.set_xlabel('VG')
        ax2.set_ylabel('Segunda Derivada Suavizada')
        ax2.set_title('Segunda Derivada Suavizada da Curva')

        ax1.legend()
        ax2.legend()

        plt.tight_layout()
        plt.subplots_adjust(top=0.9)
        fig.suptitle(f"Cascata: {df.attrs['Cascata']} - W: {df.attrs['W']} - L: {df.attrs['L']} - Arquivo: {df.attrs['Filename']}")
        plt.savefig(f"report_{df.attrs['Filename']}.pdf")