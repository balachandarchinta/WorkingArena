FROM node:18-slim

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npx tsc

EXPOSE 8080

CMD ["node", "proxy.js"]
