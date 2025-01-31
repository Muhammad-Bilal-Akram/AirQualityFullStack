FROM node:16-slim

WORKDIR /app
COPY package*.json ./

RUN npm install
COPY . .
COPY .env ./

RUN npm run build
EXPOSE 3000
RUN npm install -g serve

CMD ["serve", "-s", "build", "-l", "3000"]
