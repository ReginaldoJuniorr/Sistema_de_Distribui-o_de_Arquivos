# 🛡️ Central de Telemetria e Monitoramento de Redes via Sockets TCP

Uma aplicação Cliente-Servidor em Python projetada para monitoramento ativo de saúde e métricas de hardware em rede. O sistema utiliza um agente local que realiza leituras de **CPU, Memória RAM e Disco**, classifica o status da máquina e envia o relatório em tempo real para uma Central de Monitoramento.

Projeto desenvolvido para a disciplina de **Ferramentas de Gerenciamento de Redes**.

## 📌 Funcionalidades
* **Arquitetura Agente-Central (Push):** O agente remoto coleta as métricas e reporta ativamente para a Central de Monitoramento.

* **Leitura de Telemetria de Hardware:** Coleta contínua de uso de CPU, RAM e espaço em disco utilizando a biblioteca `psutil`, gerando alertas automáticos de status (`ESTÁVEL` ou `CRÍTICO`).
  
* **Escuta Multi-Interface (0.0.0.0):** A Central aceita relatórios de qualquer computador conectado à mesma rede local.
  
* **Protocolo de Cabeçalho de Tamanho Fixo:** Envio inicial de metadados em JSON preenchidos (*padded*) com exatos 1024 bytes para identificação do remetente e tamanho do payload.
  
* **Envio de Dados em Chunks:** Transmissão segura do arquivo de telemetria dividida em blocos de 4 KB (4096 bytes).

## 🛠️ Tecnologias Utilizadas
* **Linguagem:** Python 3.12
* **Módulo externo:** `psutil`
* **Módulos nativos:** `socket`, `json`, `os`, `platform`, `datetime`

## 📂 Arquitetura do Projeto
```text
├── servidor_central.py  # Central que recebe e armazena relatórios de rede
├── cliente_agente.py    # Agente remoto que lê o hardware e envia a telemetria
├── .gitignore           # Filtro para não versionar relatórios temporários
└── README.md            # Documentação do projeto
```

## 🔄 Como Funciona o Protocolo
``` text

+------------------+                                 +--------------------+
|  Cliente Agente  |                                 |  Servidor Central  |
+------------------+                                 +--------------------+
         |                                                     |
         | (1. Coleta métricas: CPU/RAM/Disco)                 |
         | (2. Gera relatório telemetria.txt)                  |
         |                                                     |
         | ------ 1. Conecta e envia Header JSON (1024 B) ---> |
         |                                                     | (Lê metadados/máquina)
         | ------ 2. Envia Relatório em Chunks (4 KB) -------> |
         |                                                     |
         v                                                     v
 [Conclusão de Envio]                                [Salva recebido_*.txt]
```
## 🚀 Como Executar
Por utilizar a camada de transporte com Sockets TCP locais, a aplicação precisa ser executada em um ambiente com suporte a terminal local (VS Code, PowerShell, Terminal Linux ou GitHub Codespaces).

Pré-requisitos

- Python 3.8 ou superior instalado.
- Biblioteca de monitoramento psutil instalada
  > ``` pip install psutil ``` 

*Passo a Passo*

Clone o repositório:

 ```
git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
cd seu-repositorio
```

Inicie a Central de Monitoramento (Terminal 1):

```
python servidor_central.py
```
A Central ficará aguardando conexões na porta 65432.


Configure o Agente (Opcional):
Se for testar entre máquinas diferentes na mesma rede, abra o arquivo cliente_agente.py e substitua a variável HOST = '127.0.0.1' pelo IP da máquina Servidor.

Inicie o Agente de Telemetria (Terminal 2):

```
Bash
python cliente_agente.py
```
O agente fará a leitura do sistema, enviará o arquivo e a Central salvará com o prefixo recebido_


## 📝 Licença
Este projeto foi desenvolvido para fins educacionais. Sinta-se à vontade para utilizar e modificar!
