# Detector de Ataques DDoS Baseado em Python

Este projeto é uma ferramenta de segurança de rede, escrita em Python, projetada para detectar ataques de Negação de Serviço Distribuída (DDoS) através da análise de tráfego em tempo real. Ele combina detecção baseada em limites de taxa (rate-limiting) com um modelo de Machine Learning (Isolation Forest) para identificar padrões de tráfego anômalos.

## Funcionalidades Principais

- **Detecção Híbrida:** Utiliza uma abordagem de duas camadas para precisão:
  1.  **Limite de Taxa:** Alerta quando um IP excede um número configurável de requisições em uma janela de tempo.
  2.  **Machine Learning:** Emprega um modelo `IsolationForest` para identificar anomalias sutis que não violam regras fixas.
- **Múltiplos Modos de Operação:**
  - `log`: Monitora arquivos de log de servidores web (ex: Nginx, Apache) em tempo real.
  - `pcap`: Captura e analisa pacotes de rede ao vivo de uma interface de rede.
  - `simulate`: Simula tráfego em memória para testar a lógica de detecção.
  - `generate-log`: Cria um arquivo de log com tráfego realista para testes offline.
- **Resposta Automatizada:** Pode ser configurado para bloquear automaticamente IPs suspeitos usando `iptables` em sistemas Linux.
- **Relatórios Detalhados:** Gera relatórios em formato JSON e/ou HTML ao final da execução, resumindo a atividade e os alertas gerados.

## Estrutura do Projeto

O código é organizado de forma modular para facilitar a manutenção e a extensão:

```
.
├── main.py           # Ponto de entrada da aplicação
├── config.py         # Arquivo de configuração central
├── core/
│   └── detector.py   # Lógica principal de detecção (rate-limit e ML)
├── modules/
│   ├── log_monitor.py  # Módulo para análise de logs
│   ├── pcap_capture.py # Módulo para captura de pacotes
│   └── simulator.py    # Módulo para simulação e geração de logs
└── utils/
    ├── firewall.py   # Utilitário para interação com iptables
    └── reporter.py   # Utilitário para geração de relatórios
```

## Requisitos

- Python 3.7+
- Bibliotecas:
  ```bash
  pip install scapy scikit-learn numpy
  ```

## Como Usar

### 1. Configuração

Antes de executar, revise e ajuste os parâmetros no arquivo `config.py` de acordo com suas necessidades (limites, caminhos de arquivo, interface de rede, etc.).

### 2. Execução

Execute o script a partir do diretório raiz do projeto.

**Gerar um Arquivo de Log para Testes:**
Cria um arquivo `simulated_access.log` para ser usado com o modo `log`.

```bash
python main.py generate-log
```

**Analisar um Arquivo de Log:**
Monitore um arquivo de log (lembre-se de ajustar `LOG_FILE_PATH` em `config.py`).

```bash
python main.py log
```

**Capturar Pacotes de Rede:**
Monitore o tráfego de uma interface de rede em tempo real.

```bash
sudo python main.py pcap
```

**Simular Tráfego em Memória:**
A maneira mais rápida de ver o detector em ação sem dependências externas.

```bash
python main.py simulate
```

Ao encerrar qualquer modo de monitoramento (com `Ctrl+C`), relatórios em JSON e/ou HTML serão gerados no diretório do projeto.
