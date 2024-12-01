# Variáveis para os caminhos e comandos
VENV_NAME = venv
PYTHON = python3
PIP = $(VENV_NAME)/bin/pip
ACTIVATE = $(VENV_NAME)/bin/activate
WIN_PYTHON = python
WIN_PIP = $(VENV_NAME)\Scripts\pip.exe
WIN_ACTIVATE = $(VENV_NAME)\Scripts\activate.bat

# Detectando o sistema operacional
OS := $(shell uname -s)

# Verificar se o sistema é Windows ou Linux
ifeq ($(OS),Windows_NT)
    PYTHON := $(WIN_PYTHON)
    PIP := $(WIN_PIP)
    ACTIVATE := $(WIN_ACTIVATE)
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
	@source $(ACTIVATE) && python manage.py runserver

# Alvo para rodar as migrações do banco de dados
migrate:
	@source $(ACTIVATE) && python manage.py migrate

# Alvo para rodar os testes
test:
	@source $(ACTIVATE) && pytest

# Alvo para criar superusuário (admin)
createsuperuser:
	@source $(ACTIVATE) && python manage.py createsuperuser

# Alvo para instalar dependências a partir do requirements.txt
install:
	@$(PIP) install -r requirements.txt

# Alvo para limpar arquivos temporários e caches (opcional)
clean:
	@rm -rf $(VENV_NAME)
	@echo "Ambiente virtual removido"

# Alvo para rodar o projeto (com todas as etapas anteriores)
setup: init install migrate

