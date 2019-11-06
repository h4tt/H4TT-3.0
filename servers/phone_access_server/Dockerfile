FROM alpine:3.10.3

COPY ./ /app

WORKDIR /app

RUN apk add nodejs npm python gcc make libc-dev g++ && \
    npm install

CMD [ "node", "challenge-server.js" ]