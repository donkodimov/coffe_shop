FROM node:14.19.0-alpine3.15

WORKDIR /app

# COPY package*.json /app/

COPY ./ /app/

RUN npm install -g @ionic/cli
RUN npm install



EXPOSE 8100
CMD ["ionic", "serve"]