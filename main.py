import argparse
import os
import sys

# Adiciona o diretório raiz ao path para permitir importações absolutas
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import CONFIG
from core.detector import DDoSDetector
from modules.log_monitor import run_log_monitoring
from modules.pcap_capture import run_pcap_capture
from modules.simulator import run_simulation, generate_log_file 
from utils.reporter import generate_and_save_reports

def main():
    parser = argparse.ArgumentParser(
        description="Ferramenta de Detecção de DDoS Modular.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('mode', 
        choices=['log', 'pcap', 'simulate', 'generate-log'], 
        help="""Modo de operação:
  log            - Monitora um arquivo de log de acesso em tempo real.
  pcap           - Captura pacotes de rede ao vivo (requer sudo).
  simulate       - Simula tráfego em memória para testar a detecção.
  generate-log   - Cria um arquivo de log simulado para testes offline."""
    )
    args = parser.parse_args()

    if args.mode == 'generate-log':
        try:
            duration = int(input("Por quantos segundos você deseja gerar o log? (ex: 30): "))
        except ValueError:
            print("Entrada inválida. Usando 30 segundos como padrão.")
            duration = 30
        
        generate_log_file(
            output_path=CONFIG['SIMULATED_LOG_PATH'],
            duration_seconds=duration,
            max_requests_per_ip=CONFIG['MAX_REQUESTS_PER_IP']
        )
        sys.exit(0)

    if CONFIG['ENABLE_IPTABLES_BLOCK'] and os.geteuid() != 0:
        print("ERRO: Bloqueio de IP ativado, mas o script não é root. Execute com 'sudo'.")
        sys.exit(1)

    detector = DDoSDetector(config=CONFIG)
    
    print("="*60)
    print("      INICIANDO O DETECTOR DE DDOS (VERSÃO MODULAR)      ")
    print(f"Modo Selecionado: {args.mode.upper()}")
    print("Pressione Ctrl+C para parar e gerar um relatório.")
    print("="*60)

    try:
        if args.mode == 'log':
            run_log_monitoring(detector, CONFIG['LOG_FILE_PATH'])
        elif args.mode == 'pcap':
            run_pcap_capture(detector, CONFIG['PCAP_INTERFACE'])
        elif args.mode == 'simulate':
            run_simulation(detector)
    except KeyboardInterrupt:
        print("\n\nExecução interrompida pelo usuário.")
    except Exception as e:
        print(f"\nOcorreu um erro fatal: {e}")
    finally:
        if args.mode != 'generate-log':
            report_data = detector.get_report_data()
            generate_and_save_reports(
                report_obj=report_data,
                base_path=CONFIG['REPORT_FILE_PATH'],
                report_format=CONFIG['REPORT_FORMAT']
            )
            print("\nDetector encerrado.")

if __name__ == "__main__":
    main()