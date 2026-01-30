FROM node:20-alpine

WORKDIR /app

# Instalar dependencias
COPY package*.json ./
RUN npm install

# Copiar resto del código
COPY . .

EXPOSE 3000

# Modo desarrollo por defecto (Next.js dev server)
CMD ["npm", "run", "dev", "--", "-H", "0.0.0.0"]

