# Definições de variáveis
PROJECT_NAME := popcornia
BRANCH := $(shell git symbolic-ref --short HEAD)
BRANCH_NAME := $(BRANCH)

# Exibe o sistema operacional detectado
print-os:
	@echo "Sistema operacional detectado: $(OS)"

# Comandos específicos para cada sistema operacional
ifeq ($(OS),Windows_NT)
    IS_WINDOWS := true
    RM = del /F /Q
    MKDIR = mkdir
    RMDIR = rmdir /S /Q
    TOUCH = type nul >
    SHELL := powershell.exe
    CLEAR_CMD = @powershell -Command "Clear-Host"
    SLEEP := @timeout /t
    STOP_CMD := docker ps -q | ForEach-Object { docker stop $_ }
    REMOVE_CMD = docker ps -a -q | ForEach-Object { docker rm $_ }
    VOLUME_PRUNE = docker volume prune -f
else
    IS_WINDOWS := false
    RM = rm -f
    MKDIR = mkdir -p
    RMDIR = rm -rf
    TOUCH = touch
    CLEAR_CMD = @clear # No Linux, usar clear
    SLEEP := @sleep
    STOP_CMD := docker ps -a -q | xargs docker stop
    REMOVE_CMD = docker ps -a -q | xargs docker rm -v
    VOLUME_PRUNE = docker volume prune -f
endif

# Docker commands
docker-compose:
	@echo "Subindo os serviços definidos no docker-compose.yml..."
	docker-compose up -d
	@echo "Serviços iniciados com sucesso!"

docker-compose-down:
	@echo "Encerrando os serviços definidos no docker-compose.yml..."
	docker-compose down
	@echo "Serviços encerrados."

docker-clean-all:
	@echo "Parando e removendo todos os contêineres e volumes..."
	@$(STOP_CMD)
	@$(REMOVE_CMD)
	@$(VOLUME_PRUNE)
	@echo "Contêineres e volumes removidos com sucesso!"

docker-build:
	@echo "Construindo as imagens Docker..."
	docker-compose build
	@echo "Imagens construídas com sucesso!"

docker-stop:
	@echo "Parando o contêiner Docker $(PROJECT_NAME)..."
	docker stop $(PROJECT_NAME)
	docker rm $(PROJECT_NAME)

docker-logs:
	@echo "Exibindo os logs do contêiner Docker..."
	docker logs $(PROJECT_NAME)

# Gerenciamento de arquivos e diretórios
mdir:
	@echo "Criando o diretório $(TARGET_DIR)..."
	$(MKDIR) $(TARGET_DIR)
	@echo "Diretório $(TARGET_DIR) criado com sucesso!"

limpar:
	@echo "Limpando o terminal... $(CLEAR_CMD)"
	$(CLEAR_CMD)

# Git commands
status:
	@echo "Verificando status do repositório..."
	git status

add:
	@echo "Adicionando todas as alterações ao stage..."
	git add .

commit:
	@if [ -z "$(message)" ]; then \
		echo "Realizando commit com a mensagem padrão: $(MESSAGE)..."; \
		git commit -m "$(MESSAGE)"; \
	else \
		echo "Realizando commit com a mensagem personalizada: $(message)..."; \
		git commit -m "$(message)"; \
	fi

push:
	@echo "Enviando alterações para a branch $(BRANCH)..."
	git push origin $(BRANCH)

CHECK-GIT-DIFF:
	@echo "Verificando alterações..."
	ifeq ($(OS),Windows_NT)
		git diff --quiet || (echo "Alterações detectadas." && exit 1)
	else
		git diff --quiet || (echo "Alterações detectadas." && exit 1)
	endif

# Criar nova branch
new-branch:
	@echo "Criando a nova branch: $(BRANCH_NAME)..."
	git checkout -b $(BRANCH_NAME)

# Excluir uma branch local
delete-branch:
	@echo "Excluindo a branch local: $(BRANCH_NAME)..."
	git branch -d $(BRANCH_NAME)

# Listar todas as branches locais
branches:
	@echo "Listando todas as branches locais..."
	git branch

# Verificar logs do Git
log:
	@echo "Exibindo logs do Git..."
	git log --oneline --graph --decorate --all

# Comandos informativos e de ajuda
help:
	@echo "Comandos disponíveis no Makefile:"
	@echo ""
	@echo " - make docker-build: Construir as imagens Docker."
	@echo " - make docker-compose-up: Subir os serviços definidos no docker-compose."
	@echo " - make docker-compose-down: Parar os serviços definidos no docker-compose."
	@echo " - make docker-clean-all: Parar e remover todos os contêineres e volumes Docker."
	@echo ""
	@echo "Git:"
	@echo " - make commit: Realizar um commit com uma mensagem."
	@echo " - make push: Enviar alterações para o repositório remoto."
	@echo " - make pull: Atualizar o repositório local com alterações remotas."
	@echo " - make status: Verificar o status do repositório Git."
	@echo " - make branches: Listar as branches locais."
	@echo ""
	@echo "Gerenciamento de Arquivos e Diretórios:"
	@echo " - make mdir: Criar o diretório $(TARGET_DIR)."
	@echo " - make limpar: Limpar o terminal."

# Testar se o Docker está em execução corretamente no sistema
docker-health-check:
	@echo "Verificando se o Docker está em execução no sistema..."
	@if $(IS_WINDOWS); then \
		docker info >/dev/null || (echo "Docker não está em execução!" && exit 1); \
	else \
		docker info >/dev/null || (echo "Docker não está em execução!" && exit 1); \
	fi
	@echo "Docker está em execução corretamente!"

# Meta-alvo padrão
.DEFAULT_GOAL := help
