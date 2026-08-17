import socket
import json
import os
import platform
from datetime import datetime

# Configurações de rede
HOST = '127.0.0.1'  # Localhost
PORT = 65432        # Porta para a conexão

def gerar_relatorio():
    """Gera um arquivo de texto com dados reais do sistema para simular a resposta do RAG"""
    nome_arquivo = f"relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    conteudo = f"""=== RELATORIO DO SISTEMA ===
Data da solicitacao: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
Sistema Operacional: {platform.system()} {platform.release()}
Nome da Maquina: {platform.node()}
Processador: {platform.processor()}

Status: Operacao normal. Nenhum erro critico detectado na rede.
============================"""
    
    # Cria o arquivo no disco
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    return nome_arquivo

# Criação do Socket TCP (SOCK_STREAM)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Servidor RAG aguardando conexões em {HOST}:{PORT}...")
    
    while True:
        conn, addr = s.accept()
        with conn:
            print(f"\n[+] Nova conexão de {addr}")
            # Recebe a intenção do cliente (até 1024 bytes)
            data = conn.recv(1024).decode('utf-8').strip()
            print(f"Comando recebido do cliente: '{data}'")
            
            # Lógica do "Fake RAG"
            if "relatorio" in data.lower() or "relatório" in data.lower():
                print("Processando relatório...")
                
                # 1. Gera o arquivo dinamicamente
                arquivo_path = gerar_relatorio()
                tamanho_arquivo = os.path.getsize(arquivo_path)
                
                # 2. Cria o cabeçalho (Header) com metadados em JSON
                header = json.dumps({
                    "status": "sucesso",
                    "filename": arquivo_path,
                    "filesize": tamanho_arquivo
                })
                
                # Preenche o JSON com espaços vazios até ter exatos 1024 bytes
                # Isso garante que o cliente não confunda o cabeçalho com o conteúdo do arquivo
                header_padded = header.ljust(1024).encode('utf-8')
                conn.sendall(header_padded)
                
                # 3. Envia o arquivo em blocos (Chunks)
                with open(arquivo_path, 'rb') as f:
                    while True:
                        chunk = f.read(4096) # Lê 4KB por vez
                        if not chunk:
                            break
                        conn.sendall(chunk)
                print(f"Arquivo {arquivo_path} enviado com sucesso!")
                
            else:
                # Caso o pedido não seja reconhecido
                print("Comando não reconhecido.")
                header = json.dumps({
                    "status": "erro",
                    "mensagem": "Comando nao reconhecido pelo RAG. Tente pedir um 'relatorio'."
                })
                conn.sendall(header.ljust(1024).encode('utf-8'))