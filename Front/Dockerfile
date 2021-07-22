FROM node:10 as builder

WORKDIR /usr/src/app/Front

COPY package.json ./

RUN npm install

COPY ./ ./

RUN npm install

RUN npm run build

FROM nginx:latest
EXPOSE 80
COPY --from=builder /usr/src/app/Front/build /usr/share/nginx/html