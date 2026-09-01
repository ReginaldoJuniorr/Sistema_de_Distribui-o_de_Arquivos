# Documentação Técnica: Central de Telemetria e Monitoramento de Redes

## Visão Geral do Sistema

O sistema consiste em uma arquitetura Cliente-Servidor desenvolvida em Python sobre o protocolo TCP/IP (camada de transporte). A aplicação adota o modelo de Agente Ativo (Push Architecture), onde o cliente (cliente_agente.py) executa o diagnóstico de recursos de hardware em tempo real (CPU, RAM e Disco) e envia proativamente os relatórios para a Central de Monitoramento (servidor_central.py), que grava os dados centralizadamente para auditoria e controle de rede.

## Arquitetura da Comunicação e Protocolo

Para garantir a integridade no envio dos relatórios via Sockets TCP, foi mantido o Protocolo de Cabeçalho de Tamanho Fixo (Fixed-Length Header Protocol).

## Funcionamento do Protocolo:

1. Coleta e Empacotamento Local: O Agente gera o arquivo de telemetria contendo o diagnóstico de hardware e calcula os metadados (tamanho do arquivo, nome da máquina e nome do arquivo).

2. Cabeçalho (Header): O Agente inicia a transmissão enviando uma estrutura JSON codificada em UTF-8, preenchida (padded) com espaços em branco até atingir o tamanho exato de 1024 bytes.

   - Vantagem: Elimina o problema de framing no TCP, permitindo que a Central saiba exatamente de qual máquina veio a requisição e qual o tamanho exato do payload a ser lido antes de abrir o buffer do arquivo.

3. Mapeamento do JSON no Cabeçalho:

   - status: "sucesso".
     
   - maquina: Nome de identificação do host gerador da telemetria (platform.node()).
     
   - filename: Nome original do arquivo .txt gerado no cliente.
     
   - filesize: Tamanho total do arquivo em bytes.

4. Carga Útil (Payload / Transmissão de Arquivo): O Agente transmite o arquivo de telemetria em blocos binários de 4096 bytes (4 KB). A Central lê iterativamente o fluxo até completar a quantidade exata informada em filesize e o grava em disco com o prefixo recebido_.

# Documentação do Código: Central de Monitoramento (servidor_central.py)

A Central atua como o nó receptor (listener), configurado para escutar requisições de qualquer interface de rede e armazenar os dados enviados pelos agentes.

## Módulos Utilizados

- socket: Gerenciamento da interface de rede (família AF_INET, tipo SOCK_STREAM).
  
- json: Desserialização do cabeçalho de metadados.
  
## Componentes e Fluxo do Socket

- HOST = '0.0.0.0': Escuta em todas as placas de rede ativas na máquina Servidor, permitindo conexões vindas de computadores externos na mesma rede local.
  
- s.bind((HOST, PORT)): Vincula o socket à porta configurada (65432).
  
- s.listen(): Coloca o socket em modo de escuta contínua.
  
- s.accept(): Bloqueia a execução aguardando o envio de dados de um Agente.
  
- conn.recv(1024): Captura rigorosamente os 1024 bytes iniciais do cabeçalho de metadados.
  
- conn.recv(chunk_size): Lê a carga útil (arquivo) em blocos de até 4 KB até totalizar o filesize, escrevendo diretamente em um novo arquivo com a nomenclatura recebido_<nome_do_arquivo>.

# Documentação do Código: Agente de Telemetria (cliente_agente.py)

O Agente atua na ponta monitorada, realizando a leitura de hardware, gerando os relatórios de saúde do sistema e enviando-os para a Central via Socket.

Módulos Utilizados

- socket: Abertura do canal de comunicação TCP com a Central.
  
- json: Serialização do cabeçalho de metadados.
  
- os: Leitura do tamanho do arquivo gerado (os.path.getsize).
  
- platform: Coleta do nome da máquina e sistema operacional.
  
- psutil: Módulo externo para leitura direta dos sensores de uso de CPU, Memória RAM e Disco.
  
- datetime: Carimbo de data e hora para versionamento do relatório.
  
# Funções e Componentes

## gerar_telemetria()

- Descrição: Lê as porcentagens de uso de CPU (psutil.cpu_percent), RAM (psutil.virtual_memory().percent) e Disco (psutil.disk_usage). Aplica uma lógica de decisão: caso qualquer recurso ultrapasse 90%, define o status geral como CRÍTICO, caso contrário, ESTÁVEL. Salva esses dados em um arquivo .txt local.

- Retorno: tuple — (arquivo_path, nome_maquina).

## Fluxo de Execução

1. Geração de Dados: Invoca gerar_telemetria() e calcula o tamanho final do relatório (os.path.getsize).

2. Estabelecimento de Conexão (s.connect((HOST, PORT))): Conecta-se à Central de Monitoramento.
  
4. Envio do Cabeçalho Padded: Converte o dicionário com os metadados em JSON, preenche com espaços (.ljust(1024)) e transmite via s.sendall().
  
5. Transmissão em Chunks: Abre o arquivo de telemetria em modo leitura binária ('rb'), lê blocos de 4 KB e transmite sequencialmente pelo socket até o encerramento do arquivo.

## Exemplo de Execução e Saída no Terminal

### Terminal do Servidor Central (servidor_central.py)


```
==================================================
 INOVAÇÃO DO GRUPO: Central de Monitoramento Ativa
 Aguardando relatórios de telemetria de outras máquinas...
==================================================

[+] Conexão recebida da máquina: 192.168.1.15
    -> Recebendo relatório de: NOTEBOOK-SERGIO
    -> Tamanho do arquivo: 342 bytes
[OK] Relatório da máquina 'NOTEBOOK-SERGIO' salvo como 'recebido_telemetria_NOTEBOOK-SERGIO_20260901_170000.txt'

```

### Terminal do Cliente Agente (cliente_agente.py)


```
Coletando informações de hardware...
Conectando à Central de Monitoramento (192.168.1.10:65432)...
Enviando relatório de telemetria...
[OK] Dados enviados com sucesso!
```
