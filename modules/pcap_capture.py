from core.detector import DDoSDetector
try:
    from scapy.all import sniff, IP
except ImportError:
    IP = None

def run_pcap_capture(detector: DDoSDetector, interface: str):
    if IP is None:
        print("ERRO: 'scapy' não instalado. Modo 'pcap' desativado."); return
    print(f"Iniciando captura de pacotes na interface: {interface}")
    def packet_callback(packet):
        if IP in packet:
            detector.process_request(packet[IP].src)
    try:
        sniff(iface=interface, prn=packet_callback, store=0)
    except (PermissionError, OSError) as e:
        print(f"\nERRO: Permissão negada ou interface '{interface}' não encontrada. Detalhes: {e}")
        