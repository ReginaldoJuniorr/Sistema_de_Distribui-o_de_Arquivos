import socket
import json
import os
import platform
import psutil
from datetime import datetime

# =================================================================
# ATENÇÃO: Coloque aqui o IP da máquina onde o SERVIDOR está rodando
# Exemplo: '192.168.1.15' (Não use 127.0.0.1 se for testar em PCs diferentes)
# =================================================================
HOST = '127.0.0.1' 
PORT = 65432

def gerar_telemetria():
    """Coleta dados de hardware DESTA máquina para enviar ao Servidor."""
    nome_maquina = platform.node()
    nome_arquivo = f"telemetria_{nome_maquina}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disco = psutil.disk_usage("/").percent
    
    status = "ESTÁVEL"
    if cpu >= 90 or ram >= 90 or disco >= 90:
        status = "CRÍTICO - Risco de travamento"
        
    conteudo = f"""=== RELATORIO DE TELEMETRIA ===
Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
Maquina Monitorada: {nome_maquina}
SO: {platform.system()} {platform.release()}

--- LEITURA DE HARDWARE ---
CPU: {cpu}%
RAM: {ram}%
Disco: {disco}%

Status Geral: {status}
==============================="""
    
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    return nome_arquivo, nome_maquina

print("Coletando informações de hardware...")
arquivo_path, nome_maquina = gerar_telemetria()
tamanho_arquivo = os.path.getsize(arquivo_path)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        print(f"Conectando à Central de Monitoramento ({HOST}:{PORT})...")
        s.connect((HOST, PORT))
    except ConnectionRefusedError:
        print("[ERRO] Central de Monitoramento offline ou IP incorreto.")
        exit()
        
    # INOVAÇÃO DO GRUPO: Criamos um protocolo onde o agente avisa 
    # quem ele é e o que está enviando via JSON
    header = json.dumps({
        "status": "sucesso",
        "maquina": nome_maquina,
        "filename": arquivo_path,
        "filesize": tamanho_arquivo
    })
    
    # Envia cabeçalho formatado
    header_padded = header.ljust(1024).encode('utf-8')
    s.sendall(header_padded)
    
    # Envia o arquivo com os dados
    print("Enviando relatório de telemetria...")
    with open(arquivo_path, 'rb') as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            s.sendall(chunk)
            
    print("[OK] Dados enviados com sucesso!")