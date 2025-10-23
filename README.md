# Circuito RC - Análise de Dados

Este projeto implementa a coleta e análise de dados de um circuito RC (Resistor-Capacitor) usando Arduino e Python. O sistema coleta dados do monitor serial do Arduino e gera gráficos de carga e descarga do circuito RC.

## 📁 Estrutura do Projeto

```
Pond2_M04/
├── arduino_code/
│   └── rc_circuit.ino          # Código Arduino para coleta de dados
├── python_analysis/
│   ├── main.py                 # Script principal com menu interativo
│   ├── serial_data_collector.py # Coleta dados do monitor serial
│   ├── rc_analysis.py          # Análise e geração de gráficos
│   └── requirements.txt        # Dependências Python
├── data/                       # Dados coletados (gerado automaticamente)
├── results/                    # Gráficos gerados (gerado automaticamente)
└── README.md                   # Este arquivo
```

## 🚀 Como Usar

### 1. Preparação do Ambiente

1. **Instale o Python 3.x** (se ainda não tiver)
2. **Instale as dependências Python:**
   ```bash
   cd python_analysis
   pip install -r requirements.txt
   ```

### 2. Configuração do Arduino

1. **Carregue o código** `arduino_code/rc_circuit.ino` no seu Arduino
2. **Conecte o circuito RC** conforme o esquema
3. **Abra o Monitor Serial** (9600 baud) para verificar se está funcionando

### 3. Coleta e Análise de Dados

**Opção A - Menu Interativo (Recomendado):**
```bash
cd python_analysis
python main.py
```

**Opção B - Coleta Manual:**
```bash
cd python_analysis
python serial_data_collector.py
```

**Opção C - Análise de Dados Existentes:**
```bash
cd python_analysis
python rc_analysis.py
```

## 📊 Gráficos Gerados

O sistema gera os seguintes gráficos:

1. **Carga no Capacitor (C)** - Tensão no capacitor ao longo do tempo
2. **Descarga no Resistor (R)** - Tensão no resistor ao longo do tempo  
3. **Comparação** - Ambos os gráficos sobrepostos + soma das tensões
4. **Análise Completa** - Todos os gráficos em uma única figura

## 🔧 Requisitos Técnicos

### Hardware
- Arduino (Uno, Nano, etc.)
- Resistor
- Capacitor
- Fios de conexão

### Software
- Arduino IDE
- Python 3.x
- Bibliotecas Python:
  - `pyserial` - Comunicação serial
  - `matplotlib` - Geração de gráficos
  - `pandas` - Manipulação de dados
  - `numpy` - Cálculos numéricos

## 📈 Exemplo de Saída

O sistema coleta dados no formato:
```
1234ms | VR: 1.23| VC: 3.77
```

E gera gráficos similares aos mostrados na imagem de referência, com:
- Eixo X: Tempo (segundos)
- Eixo Y: Tensão (Volts)
- Linhas coloridas para cada componente
- Análise estatística dos dados

## 🐛 Solução de Problemas

### Arduino não detectado
- Verifique se o driver USB está instalado
- Teste diferentes portas COM
- Verifique se o Arduino está conectado corretamente

### Erro de permissão na porta serial
- Feche o Monitor Serial do Arduino IDE
- No Windows: execute como administrador
- No Linux: adicione seu usuário ao grupo dialout

### Dados não aparecem
- Verifique se o baud rate está correto (9600)
- Confirme se o circuito está montado corretamente
- Teste com o Monitor Serial do Arduino IDE primeiro

## 📝 Notas

- Os dados são salvos automaticamente em formato CSV
- Os gráficos são salvos em alta resolução (300 DPI)
- O sistema detecta automaticamente a porta do Arduino
- É possível interromper a coleta com Ctrl+C

## 🤝 Contribuição

Este projeto foi desenvolvido para análise de circuitos RC em laboratório. Sinta-se à vontade para sugerir melhorias ou reportar problemas!
