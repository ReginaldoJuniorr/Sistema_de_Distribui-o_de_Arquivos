import socket
import json

HOST = '0.0.0.0'  # Escuta conexões de qualquer máquina na rede
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    
    print("==================================================")
    print(" INOVAÇÃO DO GRUPO: Central de Monitoramento Ativa")
    print(" Aguardando relatórios de telemetria de outras máquinas...")
    print("==================================================\n")
    
    while True:
        conn, addr = s.accept()
        with conn:
            print(f"[+] Conexão recebida da máquina: {addr[0]}")
            
            # 1. Recebe o cabeçalho JSON (1024 bytes) com os metadados do Agente
            header_bytes = conn.recv(1024)
            if not header_bytes:
                continue
                
            header = json.loads(header_bytes.decode('utf-8').strip())
            
            filename = header.get("filename")
            filesize = header.get("filesize")
            maquina = header.get("maquina")
            
            print(f"    -> Recebendo relatório de: {maquina}")
            print(f"    -> Tamanho do arquivo: {filesize} bytes")
            
            nome_salvar = f"recebido_{filename}"
            bytes_recebidos = 0
            
            # 2. Recebe o conteúdo do arquivo (Telemetria)
            with open(nome_salvar, 'wb') as f:
                while bytes_recebidos < filesize:
                    bytes_faltantes = filesize - bytes_recebidos
                    chunk_size = min(4096, bytes_faltantes)
                    
                    chunk = conn.recv(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    bytes_recebidos += len(chunk)
                    
            print(f"[OK] Relatório da máquina '{maquina}' salvo como '{nome_salvar}'\n")