# **Fake RAG - Sistema de Transmissão de Arquivos via Sockets TCP**

Uma aplicação Cliente-Servidor em Python desenvolvida com a biblioteca nativa socket, projetada para simular uma interface de recuperação de dados (Retrieval-Augmented Generation - RAG). O sistema interpreta comandos em linguagem natural e entrega relatórios e diagnósticos do sistema dinamicamente através da rede.

Projeto desenvolvido para a disciplina de Ferramentas de Gerenciamento de Redes.

## 📌 Funcionalidades
Comunicação TCP/IP: Conexão confiável entre cliente e servidor utilizando a biblioteca nativa socket.

Geração Dinâmica de Relatórios: O servidor coleta métricas em tempo real da máquina hospedeira (SO, processador, data/hora) para compor a resposta.

Protocolo de Cabeçalho de Tamanho Fixo: Envio de metadados em JSON preenchidos (padded) para ter exatos 1024 bytes, eliminando problemas de framing no TCP.

Download em Chunks: Transferência de arquivos em blocos de 4 KB (4096 bytes), garantindo integridade e eficiência de memória.

## 🛠️ Tecnologias Utilizadas
Linguagem: Python 3.12

Módulos nativos: socket, json, os, platform, datetime

## 📂 Arquitetura do Projeto

├── servidor.py    # Aplicação do servidor (listening & geração de arquivos)

├── cliente.py     # Aplicação do cliente (interface & download)

├── .gitignore     # Filtro para não versionar arquivos temporários

└── README.md      # Documentação do projeto

## 🔄 Como Funciona o Protocolo

```text
+-----------+                                         +------------+
|  Cliente  |                                         |  Servidor  |
+-----------+                                         +------------+
      |                                                     |
      | ------ 1. Envia comando: "relatório" -------------> |
      |                                                     | (Gera relatório .txt)
      | <----- 2. Envia Header JSON (Exatos 1024 Bytes) --- | (Status, Nome e Tamanho)
      |                                                     |
      | <----- 3. Envia Arquivo em Chunks (4 KB) ---------- |
      |                                                     |
      v                                                     v
[Salva o arquivo]                                  [Aguarda nova conexão]
```
## 🚀 Como Executar

Por utilizar a camada de transporte com Sockets TCP locais, a aplicação precisa ser executada em um ambiente com suporte a terminal local (VS Code, PowerShell, Terminal Linux ou GitHub Codespaces).

Pré-requisitos

Python 3.8 ou superior instalado.

Passo a Passo
Clone o repositório:

Bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
Inicie o Servidor (Terminal 1):

Bash
python servidor.py
O servidor ficará aguardando conexões na porta 65432.

Inicie o Cliente (Terminal 2):

Bash
python cliente.py
Interaja com o sistema:
No terminal do cliente, digite a palavra relatório para receber o arquivo do sistema ou envie qualquer outro texto para testar a resposta de erro.

## 📝 Licença

Este projeto foi desenvolvido para fins educacionais. Sinta-se à vontade para utilizar e modificar!
