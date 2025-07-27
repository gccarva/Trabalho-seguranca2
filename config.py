CONFIG = {
    # --- Configurações de Detecção ---
    'TIME_WINDOW_SECONDS': 10,
    'MAX_REQUESTS_PER_IP': 100,

    # --- Configurações de Modo ---
    'LOG_FILE_PATH': 'simulated_access.log',
    'PCAP_INTERFACE': 'Ethernet',
    'SIMULATED_LOG_PATH': 'simulated_access.log',

    # --- Configuração de Ação de Bloqueio ---
    'ENABLE_IPTABLES_BLOCK': False,

    # --- Configurações de Relatório ---
    'REPORT_FORMAT': 'both',  # 'json', 'html', ou 'both'
    'REPORT_FILE_PATH': 'ddos_report',

    # --- Configurações de Machine Learning ---
    'ML_ENABLED': True,
    'ML_TRAINING_SAMPLES': 200,
    'ML_CONTAMINATION': 0.1,
}