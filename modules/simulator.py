import random
import time
import datetime
from core.detector import DDoSDetector

def run_simulation(detector: DDoSDetector):
    """Simula tráfego em memória para testar a detecção em tempo real."""
    print("Iniciando simulação em memória... Pressione Ctrl+C para parar.")
    normal_ips = [f"10.0.0.{i}" for i in range(1, 21)]
    malicious_ip = "192.168.1.100"
    while True:
        if detector.ml_enabled and not detector.model_trained:
            detector.process_request(random.choice(normal_ips))
            print(f"\rColetando dados para treino: {len(detector.training_data)}/{detector.config['ML_TRAINING_SAMPLES']}", end="")
        else:
            for _ in range(random.randint(5, 15)):
                detector.process_request(random.choice(normal_ips))
            if random.random() < 0.2:
                print("\n**Simulando pico de ataque!**")
                for _ in range(detector.config['MAX_REQUESTS_PER_IP'] + 50):
                    detector.process_request(malicious_ip)
                print("**Pico de ataque simulado concluído.**")
        time.sleep(0.1)

def generate_log_file(output_path: str, duration_seconds: int, max_requests_per_ip: int):
    """Gera um arquivo de log com tráfego normal e picos de ataque."""
    print(f"Gerando arquivo de log simulado em '{output_path}' por {duration_seconds} segundos...")
    
    normal_ips = [f"10.0.0.{i}" for i in range(1, 21)]
    malicious_ip = "192.168.1."
    start_time = time.time()
    
    try:
        with open(output_path, 'w') as f:
            while time.time() - start_time < duration_seconds:
                for _ in range(random.randint(20, 50)):
                    ip = random.choice(normal_ips)
                    timestamp = datetime.datetime.now().strftime('%d/%b/%Y:%H:%M:%S %z')
                    log_line = f'{ip} - - [{timestamp}] "GET /index.html HTTP/1.1" 200 1234 "-" "Simulated-User-Agent"\n'
                    f.write(log_line)
                
                if random.random() < 0.5:
                    print(f"  -> Gerando pico de ataque do IP {malicious_ip}...")
                    for _ in range(max_requests_per_ip + 50):
                        timestamp = datetime.datetime.now().strftime('%d/%b/%Y:%H:%M:%S %z')
                        log_line = f'{malicious_ip+str(random.randint(10,200))} - - [{timestamp}] "GET /login.php HTTP/1.1" 401 500 "-" "Attack-Tool"\n'
                        f.write(log_line)
                time.sleep(1)
        print(f"\nSUCESSO: Arquivo de log '{output_path}' gerado com sucesso.")
    except IOError as e:
        print(f"ERRO: Não foi possível escrever no arquivo '{output_path}'. Erro: {e}")
    