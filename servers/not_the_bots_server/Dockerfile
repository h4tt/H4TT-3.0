FROM alpine:3.10.3

COPY ./ /app

WORKDIR /app

RUN apk add nodejs npm && \
    npm install

EXPOSE 3000/tcp

CMD [ "node", "index.js" ]