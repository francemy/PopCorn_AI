# Base de imagem
FROM python:3.12.7-alpine3.20

# Definir o diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
# Instalar dependências do sistema usando apk (Alpine Package Manager)
RUN apk add --no-cache \
    gcc \
    g++ \
    musl-dev \
    libpq-dev \
    postgresql-dev \
    linux-headers \
    build-base \
    py3-numpy \
    py3-scipy

# Atualizar o pip
RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install --upgrade pip

# Copiar e instalar as dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py makemigrations api
RUN python manage.py migrate
RUN python manage.py seed

# Copiar o código da aplicação
COPY . .

# Expor a porta padrão do Django (8000)
EXPOSE 8000

# Comando para iniciar o servidor de desenvolvimento do Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# para subir em produção
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "seu_projeto.wsgi:application"]
