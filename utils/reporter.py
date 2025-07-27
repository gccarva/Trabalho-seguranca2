import json
import time
import os

def generate_and_save_reports(report_obj: dict, base_path: str, report_format: str):
    """
    Gera e salva relatórios em JSON e/ou HTML.
    """
    print("\nGerando relatórios finais de atividade...")
    
    reports_generated = {}
    report_format_lower = report_format.lower()

    if report_format_lower in ['json', 'both']:
        reports_generated['json'] = json.dumps(report_obj, indent=4)
    if report_format_lower in ['html', 'both']:
        reports_generated['html'] = _generate_html_report(report_obj)

    for format_ext, content in reports_generated.items():
        file_path = f"{base_path}.{format_ext}"
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"SUCESSO: Relatório '{format_ext.upper()}' salvo em: {os.path.abspath(file_path)}")
        except Exception as e:
            print(f"ERRO: Falha ao salvar o relatório '{format_ext.upper()}': {e}")


def _generate_html_report(report_obj: dict) -> str:
    """Gera uma string de relatório HTML a partir do objeto de relatório."""
    html = f"""
    <!DOCTYPE html><html lang="pt-br"><head><meta charset="UTF-8"><title>Relatório de Detecção de DDoS</title>
    <style>body{{font-family:Arial,sans-serif;margin:20px;background-color:#f4f4f9}}h1,h2{{color:#333}}.container{{background-color:#fff;padding:20px;border-radius:8px;box-shadow:0 0 10px rgba(0,0,0,.1)}}table{{width:100%;border-collapse:collapse;margin-top:20px}}th,td{{padding:12px;border:1px solid #ddd;text-align:left}}th{{background-color:#4CAF50;color:#fff}}tr:nth-child(even){{background-color:#f2f2f2}}.alert{{color:#D8000C;font-weight:700}}</style>
    </head><body><div class="container"><h1>Relatório de Detecção de DDoS</h1>
    <p><strong>Gerado em:</strong> {report_obj['generation_time']}</p><h2>Configuração Utilizada</h2>
    <ul><li><strong>Janela de Tempo:</strong> {report_obj['config']['TIME_WINDOW_SECONDS']} segundos</li>
    <li><strong>Limite de Requisições:</strong> {report_obj['config']['MAX_REQUESTS_PER_IP']}</li>
    <li><strong>Bloqueio via iptables:</strong> {'Ativado' if report_obj['config']['ENABLE_IPTABLES_BLOCK'] else 'Desativado'}</li></ul>
    <h2>Resumo</h2><p><strong>Total de IPs rastreados:</strong> {report_obj['total_ips_tracked']}</p>
    <p><strong>IPs que acionaram alertas:</strong> {len(report_obj['alerted_ips'])}</p>
    <h2>Top IPs Mais Ativos</h2><table><tr><th>Endereço IP</th><th>Contagem de Requisições</th><th>Status</th></tr>
    """
    for ip, count in report_obj['top_active_ips'].items():
        status = '<span class="alert">ALERTA</span>' if ip in report_obj['alerted_ips'] else 'Normal'
        html += f"<tr><td>{ip}</td><td>{count}</td><td>{status}</td></tr>"
    html += "</table></div></body></html>"
    return html