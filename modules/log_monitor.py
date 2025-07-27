import re
import time
from core.detector import DDoSDetector

def run_log_monitoring(detector: DDoSDetector, log_file: str):
    print(f"Iniciando monitoramento do arquivo de log: {log_file}")
    ip_regex = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    try:
        with open(log_file, 'r') as f:
            #f.seek(0, 2)
            while True:
                line = f.readline()
                if not line:
                    #print("acabou")
                    time.sleep(0.1); continue
                match = ip_regex.match(line)
                if match:
                    detector.process_request(match.group(0))
    except FileNotFoundError:
        print(f"ERRO: O arquivo de log '{log_file}' não foi encontrado.")
    except Exception as e:
        print(f"ERRO: Ocorreu um erro ao monitorar o log: {e}")