#!/usr/bin/env python3
"""
Script principal para análise do circuito RC
Menu interativo para coleta de dados e geração de gráficos
"""

import os
import sys
from serial_data_collector import collect_data, find_arduino_port
from rc_analysis import main as analysis_main, find_latest_data_file

def show_menu():
    """Exibe o menu principal"""
    print("\n" + "="*50)
    print("    ANÁLISE DO CIRCUITO RC - MENU PRINCIPAL")
    print("="*50)
    print("1. Coletar dados do Arduino")
    print("2. Analisar dados existentes")
    print("3. Coletar e analisar (completo)")
    print("4. Listar arquivos de dados")
    print("5. Sair")
    print("="*50)

def collect_data_menu():
    """Menu para coleta de dados"""
    print("\n--- COLETA DE DADOS ---")
    
    # Tenta encontrar a porta automaticamente
    port = find_arduino_port()
    
    if port is None:
        print("Arduino não detectado automaticamente.")
        port = input("Digite a porta do Arduino (ex: COM3, /dev/ttyUSB0): ")
        if not port:
            print("Porta não especificada. Cancelando...")
            return
    
    try:
        duration = int(input("Duração da coleta em segundos (padrão: 60): ") or "60")
    except ValueError:
        duration = 60
        print("Valor inválido. Usando 60 segundos.")
    
    print(f"\nIniciando coleta de dados...")
    print(f"Porta: {port}")
    print(f"Duração: {duration} segundos")
    print("Pressione Ctrl+C para parar antes do tempo")
    
    try:
        output_file, data = collect_data(port, duration)
        if data:
            print(f"\n✅ Coleta concluída com sucesso!")
            print(f"📁 Dados salvos em: {output_file}")
            print(f"📊 Total de pontos: {len(data)}")
            
            # Pergunta se quer analisar imediatamente
            analyze = input("\nDeseja analisar os dados agora? (s/n): ").lower()
            if analyze in ['s', 'sim', 'y', 'yes']:
                analysis_main()
        else:
            print("❌ Falha na coleta de dados.")
    except KeyboardInterrupt:
        print("\n⚠️ Coleta interrompida pelo usuário.")
    except Exception as e:
        print(f"❌ Erro durante a coleta: {e}")

def analyze_data_menu():
    """Menu para análise de dados"""
    print("\n--- ANÁLISE DE DADOS ---")
    
    data_file = find_latest_data_file()
    if data_file is None:
        print("❌ Nenhum arquivo de dados encontrado!")
        print("Execute primeiro a opção 1 para coletar dados.")
        return
    
    print(f"📁 Arquivo encontrado: {data_file}")
    analyze = input("Deseja analisar este arquivo? (s/n): ").lower()
    
    if analyze in ['s', 'sim', 'y', 'yes']:
        try:
            analysis_main()
            print("\n✅ Análise concluída!")
        except Exception as e:
            print(f"❌ Erro durante a análise: {e}")
    else:
        print("Análise cancelada.")

def list_data_files():
    """Lista arquivos de dados disponíveis"""
    print("\n--- ARQUIVOS DE DADOS ---")
    
    import glob
    data_files = glob.glob("../data/rc_data_*.csv")
    
    if not data_files:
        print("❌ Nenhum arquivo de dados encontrado na pasta ../data/")
        return
    
    print(f"📁 Encontrados {len(data_files)} arquivo(s):")
    for i, file in enumerate(data_files, 1):
        file_size = os.path.getsize(file)
        file_time = os.path.getmtime(file)
        from datetime import datetime
        time_str = datetime.fromtimestamp(file_time).strftime("%Y-%m-%d %H:%M:%S")
        print(f"  {i}. {os.path.basename(file)} ({file_size} bytes) - {time_str}")

def main():
    """Função principal com menu interativo"""
    
    # Cria diretórios necessários
    os.makedirs("../data", exist_ok=True)
    os.makedirs("../results", exist_ok=True)
    
    while True:
        show_menu()
        
        try:
            choice = input("Escolha uma opção (1-5): ").strip()
            
            if choice == "1":
                collect_data_menu()
            elif choice == "2":
                analyze_data_menu()
            elif choice == "3":
                print("\n--- COLETA E ANÁLISE COMPLETA ---")
                collect_data_menu()
                # Se chegou aqui, a coleta foi bem-sucedida
                print("\nIniciando análise automática...")
                analysis_main()
            elif choice == "4":
                list_data_files()
            elif choice == "5":
                print("\n👋 Encerrando programa. Até logo!")
                break
            else:
                print("❌ Opção inválida. Escolha entre 1-5.")
        
        except KeyboardInterrupt:
            print("\n\n👋 Programa interrompido pelo usuário. Até logo!")
            break
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
        
        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()
