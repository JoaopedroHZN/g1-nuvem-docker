# Sistema de Mensagens Distribuído

Trabalho desenvolvido para a disciplina de Computação em Nuvem. O projeto consiste num sistema distribuído onde 3 containers (app1, app2 e app3) trocam mensagens entre si via rede bridge personalizada e persistem os dados num volume partilhado.

## Estrutura do Projeto
- `app/app.py`: Serviço REST em Python (Flask) com os endpoints `/send` e `/messages`.
- `docker-compose.yml`: Orquestração de 3 instâncias, mapeamento de portas (5001, 5002, 5003), rede e volume.
- `test.sh`: Script para automatizar a validação do sistema.

## Como Executar

1. Construa e inicie os containers em background:
   ```bash
   docker compose up -d --build
