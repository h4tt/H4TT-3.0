FROM alpine:3.10.3

COPY ./ /app

WORKDIR /app

RUN apk add nodejs npm && \
    npm install

EXPOSE 1337/tcp

CMD [ "node", "challenge-server.js" ]