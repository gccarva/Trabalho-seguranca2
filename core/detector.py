import time
from collections import deque

try:
    import numpy as np
    from sklearn.ensemble import IsolationForest
except ImportError:
    np = None
    IsolationForest = None
    
from utils.firewall import block_ip

class DDoSDetector:
    def __init__(self, config: dict):
        self.config = config
        self.ip_requests = {}
        self.alerted_ips = set()
        
        self.ml_enabled = config['ML_ENABLED'] and IsolationForest is not None
        self.model = None
        self.model_trained = False
        self.training_data = []
        if self.ml_enabled:
            print("INFO: Detecção por Machine Learning está HABILITADA.")
            self.model = IsolationForest(contamination=self.config['ML_CONTAMINATION'], random_state=42)
        else:
            print("INFO: Detecção por Machine Learning está DESABILITADA.")

    def process_request(self, ip_address: str):
        current_time = time.time()
        timestamps = self.ip_requests.setdefault(ip_address, deque())
        timestamps.append(current_time)
        
        while timestamps and current_time - timestamps[0] > self.config['TIME_WINDOW_SECONDS']:
            timestamps.popleft()

        num_requests = len(timestamps)

        if num_requests > self.config['MAX_REQUESTS_PER_IP']:
            if ip_address not in self.alerted_ips:
                self._trigger_alert(ip_address, num_requests, "Limite de Taxa Excedido")
        elif ip_address in self.alerted_ips and num_requests < self.config['MAX_REQUESTS_PER_IP'] / 2:
             print(f"INFO: O tráfego do IP {ip_address} voltou a um nível normal.")
             self.alerted_ips.remove(ip_address)

        if self.ml_enabled:
            self._process_ml(ip_address, num_requests)

    def _process_ml(self, ip_address: str, num_requests: int):
        feature_vector = [num_requests]
        if not self.model_trained:
            self.training_data.append(feature_vector)
            if len(self.training_data) >= self.config['ML_TRAINING_SAMPLES']:
                self._train_model()
        else:
            prediction = self.model.predict(np.array(feature_vector).reshape(1, -1))
            if prediction[0] == 1 and ip_address not in self.alerted_ips:
                self._trigger_alert(ip_address, num_requests, "Anomalia Detectada por ML")

    def _train_model(self):
        print("\nINFO: Coletadas amostras suficientes. Treinando o modelo de ML...")
        self.model.fit(np.array(self.training_data))
        self.model_trained = True
        self.training_data = []
        print("INFO: Modelo de ML treinado e ativo.\n")

    def _trigger_alert(self, ip_address: str, request_count: int, reason: str):
        print(f"\n🚨 ALERTA: IP {ip_address} | Requisições: {request_count} | Gatilho: {reason} 🚨")
        self.alerted_ips.add(ip_address)
        if self.config['ENABLE_IPTABLES_BLOCK']:
            block_ip(ip_address)

    def get_report_data(self) -> dict:
        """Prepara os dados para o relatório final."""
        report_data = {ip: len(ts) for ip, ts in self.ip_requests.items() if ts}
        sorted_report = sorted(report_data.items(), key=lambda item: item[1], reverse=True)
        
        return {
            'generation_time': time.ctime(),
            'config': self.config,
            'total_ips_tracked': len(self.ip_requests),
            'alerted_ips': list(self.alerted_ips),
            'top_active_ips': dict(sorted_report[:20])
        }