# Variáveis para os caminhos e comandos
VENV_NAME = venv
PYTHON = python3
PIP = $(VENV_NAME)/bin/pip
ACTIVATE = $(VENV_NAME)/bin/activate
WIN_PYTHON = python
WIN_PIP = $(VENV_NAME)\Scripts\pip.exe
WIN_ACTIVATE = $(VENV_NAME)\Scripts\activate.bat

# Verificar se o sistema é Windows ou Linux
ifeq ($(OS),Windows_NT)
    PYTHON := $(WIN_PYTHON)
    PIP := $(WIN_PIP)
    ACTIVATE := $(WIN_ACTIVATE)
else
    PYTHON := python3
    PIP := $(VENV_NAME)/bin/pip
    ACTIVATE := $(VENV_NAME)/bin/activate
endif

# Alvo para configurar o ambiente virtual
init:
	@if [ ! -d "$(VENV_NAME)" ]; then \
        $(PYTHON) -m venv $(VENV_NAME); \
        $(PIP) install --upgrade pip; \
        $(PIP) install -r requirements.txt; \
    else \
        echo "Ambiente virtual já existe"; \
    fi

# Alvo para ativar o ambiente virtual
activate:
	@echo "Para ativar o ambiente virtual, execute:"
	@if [ "$(OS)" == "Windows_NT" ]; then \
        echo "  .\\$(ACTIVATE)"; \
    else \
        echo "  source $(ACTIVATE)"; \
    fi

# Alvo para rodar o servidor Django
run:
	@echo "Iniciando o servidor Django..."
	@if [ "$(OS)" == "Windows_NT" ]; then \
		$(VENV_NAME)\\Scripts\\python manage.py runserver; \
	else \
		$(VENV_NAME)/bin/python manage.py runserver; \
	fi

# Alvo para rodar as migrações do banco de dados
migrate:
	@echo "Rodando migrações..."
	@if [ "$(OS)" == "Windows_NT" ]; then \
		$(VENV_NAME)\\Scripts\\python manage.py migrate; \
	else \
		$(VENV_NAME)/bin/python manage.py migrate; \
	fi

# Alvo para rodar os testes
test:
	@echo "Rodando os testes..."
	@if [ "$(OS)" == "Windows_NT" ]; then \
		$(VENV_NAME)\\Scripts\\python -m pytest; \
	else \
		$(VENV_NAME)/bin/python -m pytest; \
	fi

# Alvo para criar superusuário (admin)
createsuperuser:
	@echo "Criando superusuário..."
	@if [ "$(OS)" == "Windows_NT" ]; then \
		$(VENV_NAME)\\Scripts\\python manage.py createsuperuser; \
	else \
		$(VENV_NAME)/bin/python manage.py createsuperuser; \
	fi

# Alvo para instalar dependências a partir do requirements.txt
install:
	@pip install --no-cache-dir -r requirements.txt

# Alvo para limpar arquivos temporários e caches (opcional)
clean:
	@if [ -d "$(VENV_NAME)" ]; then \
		rm -rf $(VENV_NAME); \
		echo "Ambiente virtual removido"; \
	else \
		echo "Ambiente virtual não encontrado"; \
	fi

# Alvo para rodar o projeto (com todas as etapas anteriores)
setup: 
    init install migrate

# Alvo para criar o ambiente virtual (alternativo)
venv:
    python -m venv $(VENV_NAME)

upgrade-pip:
    python -m pip install --upgrade pip setuptools wheel

migrate-manage:
    python manage.py migrate
seed:
    python manage.py seed

create-db:
	python manage.py makemigrations api
    python manage.py makemigrations
    python manage.py migrate