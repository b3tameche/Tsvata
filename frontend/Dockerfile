FROM node:18-alpine as build

WORKDIR /client

COPY package.json /client/package.json
COPY package-lock.json /client/package-lock.json

RUN npm ci --silent

COPY . /client/

EXPOSE 80

CMD ["npm", "run", "dev"]