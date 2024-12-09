# Base de imagem
FROM python:3.12.7-alpine3.20

# Definir o diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apk add --no-cache \
    gcc \
    g++ \
    musl-dev \
    libpq-dev \
    postgresql-dev \
    linux-headers \
    build-base \
    py3-numpy \
    py3-scipy \
    && apk del build-base  # Remover build-base após instalação para reduzir a imagem

# Atualizar o pip
RUN python -m pip install --upgrade pip setuptools wheel

# Copiar apenas o arquivo requirements.txt primeiro
COPY requirements.txt .

# Instalar as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código da aplicação
COPY . .
RUN mkdir -p /app/logs
RUN chmod -R 777 /app/logs

# Coletar arquivos estáticos do Django
# Não é recomendado rodar isso no Dockerfile diretamente, mas mantendo aqui como parte do processo inicial
# Você pode rodar isso manualmente após o build ou como parte de um script de inicialização.
RUN python manage.py collectstatic --noinput

# Expor a porta padrão do Django (8000)
EXPOSE 8000

# Rodar a aplicação com Gunicorn em produção
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi:application"]
