#!/bin/bash

echo "Levantando os containers..."
docker compose up -d

echo "Aguardando 3 segundos para os serviços iniciarem..."
sleep 3

echo "Enviando mensagem para o app1 (Porta 5001)..."
curl -X POST -H "Content-Type: application/json" -d '{"message":"hello"}' http://localhost:5001/send
echo -e "\n"

echo "Verificando as mensagens armazenadas através do app2 (Porta 5002)..."
curl http://localhost:5002/messages
echo -e "\n"

echo "Testes concluidos. Verifique os logs no volume partilhado com:"
echo "docker compose exec app1 ls -l /data"
