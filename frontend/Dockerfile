FROM node:21.7.1-alpine
WORKDIR /app

COPY package.json package.json
COPY package-lock.json package-lock.json

RUN npm install -g npm@10.8.2 && npm install --legacy-peer-deps

COPY . .
RUN npm run build
RUN npm install --global http-server

CMD ["npx", "-y", "http-server", "-p", "9000", "/app/build"]