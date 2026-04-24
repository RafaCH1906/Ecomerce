FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --omit=dev

COPY src ./src
COPY swagger.yaml ./swagger.yaml

EXPOSE 3003

CMD ["npm", "start"]
