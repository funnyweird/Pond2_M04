#!/usr/bin/env python3
"""
Script para capturar dados do monitor serial do Arduino
e salvar em arquivo CSV para análise posterior.
"""

import serial
import csv
import time
import re
from datetime import datetime
import os

def find_arduino_port():
    """Encontra automaticamente a porta do Arduino"""
    import serial.tools.list_ports
    
    for port in serial.tools.list_ports.comports():
        if 'Arduino' in port.description or 'USB' in port.description:
            return port.device
    
    # Se não encontrar, lista todas as portas disponíveis
    print("Portas disponíveis:")
    for port in serial.tools.list_ports.comports():
        print(f"  {port.device} - {port.description}")
    
    return None

def parse_serial_data(line):
    """Extrai tempo, tensão do resistor e tensão do capacitor da linha do serial"""
    try:
        # Padrão: "1234ms | VR: 1.23| VC: 3.77"
        pattern = r'(\d+)ms \| VR: ([\d.]+)\| VC: ([\d.]+)'
        match = re.match(pattern, line.strip())
        
        if match:
            time_ms = int(match.group(1))
            vr = float(match.group(2))
            vc = float(match.group(3))
            return time_ms, vr, vc
    except Exception as e:
        print(f"Erro ao processar linha: {line.strip()} - {e}")
    
    return None, None, None

def collect_data(port, duration_seconds=60, output_file=None):
    """
    Coleta dados do Arduino por um tempo determinado
    
    Args:
        port: Porta serial do Arduino
        duration_seconds: Duração da coleta em segundos
        output_file: Arquivo de saída (opcional)
    """
    
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"../data/rc_data_{timestamp}.csv"
    
    # Cria diretório se não existir
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    try:
        # Conecta ao Arduino
        ser = serial.Serial(port, 9600, timeout=1)
        print(f"Conectado ao Arduino na porta {port}")
        print(f"Coletando dados por {duration_seconds} segundos...")
        print("Pressione Ctrl+C para parar antes do tempo")
        
        # Aguarda um pouco para o Arduino inicializar
        time.sleep(2)
        
        # Limpa buffer
        ser.flushInput()
        
        data_points = []
        start_time = time.time()
        
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Tempo_ms', 'Tensao_Resistor_V', 'Tensao_Capacitor_V'])
            
            while time.time() - start_time < duration_seconds:
                try:
                    if ser.in_waiting > 0:
                        line = ser.readline().decode('utf-8').strip()
                        
                        if line:
                            time_ms, vr, vc = parse_serial_data(line)
                            
                            if time_ms is not None:
                                data_points.append([time_ms, vr, vc])
                                writer.writerow([time_ms, vr, vc])
                                print(f"Tempo: {time_ms}ms | VR: {vr:.3f}V | VC: {vc:.3f}V")
                
                except KeyboardInterrupt:
                    print("\nColeta interrompida pelo usuário")
                    break
                except Exception as e:
                    print(f"Erro na leitura: {e}")
                    continue
        
        ser.close()
        print(f"\nColeta finalizada! {len(data_points)} pontos coletados")
        print(f"Dados salvos em: {output_file}")
        
        return output_file, data_points
        
    except serial.SerialException as e:
        print(f"Erro de conexão serial: {e}")
        return None, None

def main():
    """Função principal"""
    print("=== Coletor de Dados do Circuito RC ===")
    
    # Tenta encontrar a porta automaticamente
    port = find_arduino_port()
    
    if port is None:
        port = input("Digite a porta do Arduino (ex: COM3, /dev/ttyUSB0): ")
    
    if not port:
        print("Porta não especificada. Encerrando...")
        return
    
    try:
        duration = int(input("Duração da coleta em segundos (padrão: 60): ") or "60")
    except ValueError:
        duration = 60
    
    output_file, data = collect_data(port, duration)
    
    if data:
        print(f"\nEstatísticas dos dados coletados:")
        print(f"  Total de pontos: {len(data)}")
        if data:
            times = [point[0] for point in data]
            print(f"  Tempo mínimo: {min(times)}ms")
            print(f"  Tempo máximo: {max(times)}ms")
            print(f"  Duração real: {(max(times) - min(times))/1000:.1f}s")

if __name__ == "__main__":
    main()
