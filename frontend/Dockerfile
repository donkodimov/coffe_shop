FROM node:14.15.1-alpine3.11

WORKDIR /app

COPY ./ /app/

RUN npm install -g @ionic/cli
RUN apk --no-cache add g++ gcc libgcc libstdc++ linux-headers make python
RUN npm install

EXPOSE 8100
CMD ["ionic", "serve", "--host=0.0.0.0"]