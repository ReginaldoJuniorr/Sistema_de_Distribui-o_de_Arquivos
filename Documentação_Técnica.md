# **Documentação Técnica: Sistema de Distribuição de Arquivos e Diagnóstico**

## Visão Geral do Sistema
O sistema consiste em uma arquitetura Cliente-Servidor desenvolvida em Python sobre o protocolo TCP/IP (camada de transporte). A aplicação simula o comportamento de uma interface de recuperação de dados (Retrieval-Augmented Generation / RAG), onde o cliente solicita relatórios em linguagem natural e o servidor responde dinamicamente gerando e transferindo arquivos com dados de diagnósticos e métricas do sistema hospedeiro.

## Arquitetura da Comunicação e Protocolo
Para a transferência confiável de arquivos via Sockets TCP, foi implementado um Protocolo de Cabeçalho de Tamanho Fixo (Fixed-Length Header Protocol).

Funcionamento do Protocolo:

Solicitação: O cliente envia uma mensagem em formato de texto simples contendo a intenção.
Cabeçalho (Header): O servidor responde primeiramente enviando uma estrutura em formato JSON codificada em UTF-8, obrigatoriamente preenchida (padded) com espaços em branco até atingir o tamanho exato de 1024 bytes.

Vantagem: Evita o problema do framing no TCP, garantindo que o cliente leia primeiro os metadados antes de iniciar a leitura dos dados brutos do arquivo.

Mapeamento do JSON no Cabeçalho:

status: "sucesso" ou "erro".
filename: Nome original do arquivo gerado.
filesize: Tamanho total do arquivo em bytes.
mensagem: Presente apenas em casos de erro.
Carga Útil (Payload / Transmissão de Arquivo): O servidor transmite o conteúdo do arquivo em blocos binários de 4096 bytes (4 KB). O cliente lê continuamente o fluxo de dados até atingir a quantidade exata informada em filesize.

## Documentação do Código: Servidor (servidor.py)
O servidor atua como o nó central de escuta (listener), responsável por processar requisições, gerar diagnósticos em tempo real e servir os arquivos.

Módulos Utilizados
socket: Gerenciamento da interface de rede (família AF_INET, tipo SOCK_STREAM).

json: Serialização de metadados para envio.

os: Leitura de tamanho de arquivos e manipulação do sistema de arquivos.

platform: Coleta de informações sobre o hardware e SO da máquina servidor.

datetime: Registro de timestamps nos relatórios.

Funções e Componentes
gerar_relatorio()
Descrição: Função interna responsável por simular o processo de "geração/recuperação de contexto" do RAG. Ela coleta métricas do sistema operacional do servidor e escreve um arquivo de texto localmente.

Retorno: str — Nome do arquivo .txt gerado no disco com carimbo de data e hora.

Fluxo Principal do Socket (with socket.socket(...))
s.bind((HOST, PORT)): Vincula o socket ao endereço IP local e à porta configurada (65432).

s.listen(): Coloca o socket em modo de escuta para aguardar conexões de entrada.

s.accept(): Bloqueia a execução até que um cliente se conecte, retornando o objeto de conexão (conn) e o endereço do cliente (addr).

conn.recv(1024): Lê a mensagem enviada pelo cliente.

conn.sendall(...): Garante o envio completo dos bytes de cabeçalho e dos blocos do arquivo através do buffer do sistema operacional.

## Documentação do Código: Cliente (cliente.py)
O cliente atua como a interface do usuário, enviando solicitações e reconstruindo o arquivo recebido via rede no armazenamento local.

Módulos Utilizados
socket: Abertura do canal de comunicação TCP.

json: Desserialização do cabeçalho de resposta.

Fluxo de Execução
Estabelecimento de Conexão (s.connect((HOST, PORT))): Inicia a negociação (three-way handshake) com o servidor.

Envio da Requisição (s.sendall(...)): Coleta a entrada do usuário (input) e a converte para bytes via UTF-8.

Leitura e Tratamento do Cabeçalho:

Executa s.recv(1024) para ler rigorosamente o bloco inicial de 1024 bytes.

Aplica .strip() no texto recebido para remover os espaços de preenchimento e realiza o parse via json.loads().

Reconstrução do Arquivo (Download em Chunks):

Cria um novo arquivo local usando o modo de escrita binária ('wb').

Mantém um acumulador bytes_recebidos.

Em um laço while, solicita ao socket a quantidade exata restante (min(4096, bytes_faltantes)), garantindo que não leia mais dados do que o tamanho delimitado pelo cabeçalho.

Escreve os bytes recebidos continuamente no arquivo local.

## Exemplo de Execução e Saída no Terminal
**Terminal do Servidor**

```python
Servidor RAG aguardando conexões em 127.0.0.1:65432...

[+] Nova conexão de ('127.0.0.1', 54321)
Comando recebido do cliente: 'relatorio'
Processando relatório...
Arquivo relatorio_20260817_164900.txt enviado com sucesso!
```

**Terminal do Cliente**

```python
Digite seu pedido para o sistema: relatorio

[+] Arquivo encontrado: relatorio_20260817_164900.txt (285 bytes)
Baixando arquivo...

[OK] Download concluído! Arquivo salvo como: recebido_pelo_cliente_relatorio_20260817_164900.txt
```
