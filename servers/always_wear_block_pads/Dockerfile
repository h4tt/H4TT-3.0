FROM alpine:3.10.3

COPY ./ /app

WORKDIR /app

RUN apk add nodejs npm && \
    npm install

CMD [ "node", "challenge-server.js" ]