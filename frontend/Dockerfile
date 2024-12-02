FROM node:22.9.0-alpine

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos de configuração
COPY package.json package-lock.json ./

# Instalar as dependências do projeto
RUN npm install

# Copiar o restante dos arquivos do projeto para o contêiner
COPY . .

# Gerar o build de produção do Next.js
RUN npm run build

# Instalar o servidor HTTP para Next.js
RUN npm install -g serve

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos necessários do estágio de build
COPY --from=builder /app/package.json /app/package-lock.json ./
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public

# Expor a porta padrão do Next.js
EXPOSE 3000

# Comando para iniciar a aplicação
CMD ["npx", "next", "dev"]