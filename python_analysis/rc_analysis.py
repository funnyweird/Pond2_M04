#!/usr/bin/env python3
"""
Script para análise e visualização dos dados do circuito RC
Gera gráficos de carga do capacitor e descarga do resistor
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import glob
from datetime import datetime

# Configuração do matplotlib para português
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10

def load_data(file_path):
    """Carrega dados do arquivo CSV"""
    try:
        df = pd.read_csv(file_path)
        print(f"Dados carregados: {len(df)} pontos")
        print(f"Colunas: {list(df.columns)}")
        return df
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return None

def find_latest_data_file():
    """Encontra o arquivo de dados mais recente"""
    data_files = glob.glob("../data/rc_data_*.csv")
    if not data_files:
        print("Nenhum arquivo de dados encontrado na pasta ../data/")
        return None
    
    # Retorna o arquivo mais recente
    latest_file = max(data_files, key=os.path.getctime)
    print(f"Arquivo mais recente: {latest_file}")
    return latest_file

def create_individual_plots(df, output_dir="../results"):
    """Cria gráficos individuais de carga e descarga"""
    
    # Cria diretório de resultados se não existir
    os.makedirs(output_dir, exist_ok=True)
    
    # Converte tempo de ms para s para melhor visualização
    time_s = df['Tempo_ms'] / 1000.0
    
    # Gráfico 1: Carga no Capacitor
    plt.figure(figsize=(10, 6))
    plt.plot(time_s, df['Tensao_Capacitor_V'], 'b-', linewidth=2, label='Tensão no C (Vc)')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Tensão (V)')
    plt.title('Carga no Capacitor (C)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    
    # Salva o gráfico
    plt.savefig(f"{output_dir}/carga_capacitor.png", dpi=300, bbox_inches='tight')
    plt.show()
    
    # Gráfico 2: Descarga no Resistor
    plt.figure(figsize=(10, 6))
    plt.plot(time_s, df['Tensao_Resistor_V'], 'r-', linewidth=2, label='Tensão no R (Vr)')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Tensão (V)')
    plt.title('Descarga no Resistor (R)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    
    # Salva o gráfico
    plt.savefig(f"{output_dir}/descarga_resistor.png", dpi=300, bbox_inches='tight')
    plt.show()

def create_comparison_plot(df, output_dir="../results"):
    """Cria gráfico de comparação entre carga e descarga"""
    
    time_s = df['Tempo_ms'] / 1000.0
    
    plt.figure(figsize=(12, 8))
    
    # Plota ambas as tensões
    plt.plot(time_s, df['Tensao_Capacitor_V'], 'b-', linewidth=2, label='Tensão no C (Vc)')
    plt.plot(time_s, df['Tensao_Resistor_V'], 'r-', linewidth=2, label='Tensão no R (Vr)')
    
    # Calcula e plota a soma das tensões
    soma_tensoes = df['Tensao_Capacitor_V'] + df['Tensao_Resistor_V']
    plt.plot(time_s, soma_tensoes, 'g--', linewidth=1, alpha=0.7, label='Soma (Vc + Vr)')
    
    plt.xlabel('Tempo (s)')
    plt.ylabel('Tensão (V)')
    plt.title('Comparação: Carga no C e Descarga no R')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    
    # Salva o gráfico
    plt.savefig(f"{output_dir}/comparacao_rc.png", dpi=300, bbox_inches='tight')
    plt.show()

def create_all_plots_subplot(df, output_dir="../results"):
    """Cria todos os gráficos em uma única figura com subplots"""
    
    time_s = df['Tempo_ms'] / 1000.0
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Análise Completa do Circuito RC', fontsize=16, fontweight='bold')
    
    # Gráfico 1: Carga no Capacitor
    axes[0, 0].plot(time_s, df['Tensao_Capacitor_V'], 'b-', linewidth=2)
    axes[0, 0].set_xlabel('Tempo (s)')
    axes[0, 0].set_ylabel('Tensão (V)')
    axes[0, 0].set_title('Carga no Capacitor (C)')
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].set_ylim(0, 5)
    
    # Gráfico 2: Descarga no Resistor
    axes[0, 1].plot(time_s, df['Tensao_Resistor_V'], 'r-', linewidth=2)
    axes[0, 1].set_xlabel('Tempo (s)')
    axes[0, 1].set_ylabel('Tensão (V)')
    axes[0, 1].set_title('Descarga no Resistor (R)')
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].set_ylim(0, 5)
    
    # Gráfico 3: Comparação
    axes[1, 0].plot(time_s, df['Tensao_Capacitor_V'], 'b-', linewidth=2, label='Vc')
    axes[1, 0].plot(time_s, df['Tensao_Resistor_V'], 'r-', linewidth=2, label='Vr')
    soma_tensoes = df['Tensao_Capacitor_V'] + df['Tensao_Resistor_V']
    axes[1, 0].plot(time_s, soma_tensoes, 'g--', linewidth=1, alpha=0.7, label='Vc + Vr')
    axes[1, 0].set_xlabel('Tempo (s)')
    axes[1, 0].set_ylabel('Tensão (V)')
    axes[1, 0].set_title('Comparação: Carga no C e Descarga no R')
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].legend()
    axes[1, 0].set_ylim(0, 5)
    
    # Gráfico 4: Análise estatística
    axes[1, 1].hist(df['Tensao_Capacitor_V'], bins=20, alpha=0.7, color='blue', label='Vc')
    axes[1, 1].hist(df['Tensao_Resistor_V'], bins=20, alpha=0.7, color='red', label='Vr')
    axes[1, 1].set_xlabel('Tensão (V)')
    axes[1, 1].set_ylabel('Frequência')
    axes[1, 1].set_title('Distribuição das Tensões')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Salva o gráfico
    plt.savefig(f"{output_dir}/analise_completa_rc.png", dpi=300, bbox_inches='tight')
    plt.show()

def calculate_rc_parameters(df):
    """Calcula parâmetros do circuito RC"""
    
    # Encontra o ponto onde a tensão do capacitor é 63.2% da tensão inicial
    vc_initial = df['Tensao_Capacitor_V'].iloc[0]
    vc_target = vc_initial * 0.368  # 63.2% de queda
    
    # Encontra o tempo correspondente
    tau_idx = np.argmin(np.abs(df['Tensao_Capacitor_V'] - vc_target))
    tau_time = df['Tempo_ms'].iloc[tau_idx] / 1000.0  # em segundos
    
    print(f"\n=== Análise do Circuito RC ===")
    print(f"Tensão inicial do capacitor: {vc_initial:.3f} V")
    print(f"Tensão final do capacitor: {df['Tensao_Capacitor_V'].iloc[-1]:.3f} V")
    print(f"Tempo de constante (τ): {tau_time:.3f} s")
    print(f"Tensão do resistor máxima: {df['Tensao_Resistor_V'].max():.3f} V")
    print(f"Tensão do resistor mínima: {df['Tensao_Resistor_V'].min():.3f} V")
    
    return tau_time

def main():
    """Função principal"""
    print("=== Análise do Circuito RC ===")
    
    # Encontra o arquivo de dados mais recente
    data_file = find_latest_data_file()
    
    if data_file is None:
        print("Nenhum arquivo de dados encontrado!")
        print("Execute primeiro o serial_data_collector.py para coletar dados.")
        return
    
    # Carrega os dados
    df = load_data(data_file)
    
    if df is None:
        return
    
    # Cria os gráficos
    print("\nCriando gráficos individuais...")
    create_individual_plots(df)
    
    print("\nCriando gráfico de comparação...")
    create_comparison_plot(df)
    
    print("\nCriando análise completa...")
    create_all_plots_subplot(df)
    
    # Calcula parâmetros do circuito
    tau = calculate_rc_parameters(df)
    
    print(f"\nGráficos salvos na pasta ../results/")
    print("Análise concluída!")

if __name__ == "__main__":
    main()
