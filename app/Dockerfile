FROM python:3.12-slim

WORKDIR /app

# Instala apenas as dependências necessárias (Requisito 2)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação (app.py)
COPY app.py .

# Expõe a porta 5000 exigida no enunciado
EXPOSE 5000

# Comando para iniciar o servidor Flask
CMD ["python", "app.py"]
