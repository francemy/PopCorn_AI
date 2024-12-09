# Etapa 1: Construção do Next.js
FROM node:current-alpine AS builder

WORKDIR /app

# Copiar apenas arquivos essenciais para instalar dependências
COPY package.json package-lock.json ./

# Instalar todas as dependências para o build
RUN npm install

# Copiar o restante dos arquivos para o build
COPY . .

# Gerar o build da aplicação
RUN npm run build

# Etapa 2: Servidor Node.js para produção
FROM node:current-alpine

WORKDIR /app

# Copiar os arquivos necessários do build
COPY --from=builder /app/package.json /app/package-lock.json /app/
COPY --from=builder /app/.next /app/.next
COPY --from=builder /app/public /app/public
# Instalar apenas dependências de produção
# RUN npm ci --omit=dev

# Definir variáveis de ambiente
# ENV NODE_ENV production
# ENV NEXT_PUBLIC_API_URL http://backend:8000/api/
# ENV NEXT_PUBLIC_APP_URL http://frontend:3000/

# Expor a porta padrão do Next.js
EXPOSE 3000

# Comando para iniciar o servidor Next.js
CMD ["npm", "start"]
