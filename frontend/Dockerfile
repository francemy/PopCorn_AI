FROM node:22.9.0-alpine

# Defina o diretório de trabalho
WORKDIR /app

# Copie apenas o package.json e o pnpm-lock.yaml para instalar dependências
COPY package.json pnpm-lock.yaml ./

# Instale o pnpm globalmente
RUN npm install -g pnpm

# Instale as dependências do projeto
RUN pnpm install --frozen-lockfile

# Copie o restante do código do projeto, exceto o que está no .dockerignore
COPY . .
# Adicione a dependência vue-tsc como devDependency
RUN pnpm add vue-tsc --save-dev

# Execute o comando de build
RUN pnpm run build

# Exponha a porta do servidor
EXPOSE 8080

# Comando para rodar o servidor
CMD ["pnpm", "run", "dev"]