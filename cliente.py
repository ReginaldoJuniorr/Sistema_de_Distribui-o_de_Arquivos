import socket
import json

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((HOST, PORT))
    except ConnectionRefusedError:
        print("Erro: O servidor não está rodando.")
        exit()
        
    # 1. Envia a intenção (Simulando o prompt do RAG)
    mensagem = input("Digite seu pedido para o sistema: ")
    s.sendall(mensagem.encode('utf-8'))
    
    # 2. Recebe o cabeçalho (exatos 1024 bytes)
    header_bytes = s.recv(1024)
    if not header_bytes:
        print("Conexão encerrada pelo servidor.")
        exit()
        
    # Limpa os espaços que usamos para preencher (strip) e transforma de volta em Dicionário
    header_str = header_bytes.decode('utf-8').strip()
    header = json.loads(header_str)
    
    # 3. Analisa a resposta do servidor
    if header.get("status") == "erro":
        print(f"\n[!] Resposta do Servidor: {header.get('mensagem')}")
    else:
        filename = header.get("filename")
        filesize = header.get("filesize")
        
        print(f"\n[+] Arquivo encontrado: {filename} ({filesize} bytes)")
        
        # Adiciona um prefixo para não sobrescrever o arquivo do servidor (se rodar na mesma pasta)
        nome_salvar = "recebido_pelo_cliente_" + filename
        bytes_recebidos = 0
        
        # 4. Recebe o conteúdo do arquivo em blocos (Download)
        print("Baixando arquivo...")
        with open(nome_salvar, 'wb') as f:
            while bytes_recebidos < filesize:
                # Pede 4096 bytes, ou apenas o que falta para completar o arquivo
                bytes_faltantes = filesize - bytes_recebidos
                chunk_size = min(4096, bytes_faltantes)
                
                chunk = s.recv(chunk_size)
                if not chunk:
                    break
                f.write(chunk)
                bytes_recebidos += len(chunk)
                
        print(f"\n[OK] Download concluído! Arquivo salvo como: {nome_salvar}")