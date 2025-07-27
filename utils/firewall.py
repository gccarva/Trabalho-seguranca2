import subprocess

def block_ip(ip_address: str):
    """
    Bloqueia um endereço IP usando iptables. Requer privilégios de root.
    """
    print(f"AVISO: Tentando bloquear o IP {ip_address} via iptables...")
    try:
        command = ['sudo', 'iptables', '-I', 'INPUT', '1', '-s', ip_address, '-j', 'DROP']
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"SUCESSO: IP {ip_address} bloqueado no firewall.")
    except FileNotFoundError:
        print("ERRO: O comando 'iptables' não foi encontrado.")
    except subprocess.CalledProcessError as e:
        print(f"ERRO: Falha ao executar o comando iptables para bloquear {ip_address}.")
        print(f"  -> Erro: {e.stderr}")
    except Exception as e:
        print(f"ERRO: Ocorreu um erro inesperado ao tentar bloquear o IP: {e}")