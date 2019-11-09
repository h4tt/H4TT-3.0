FROM alpine:3.10.3

WORKDIR /home/restricted

COPY app.c .
COPY flag.txt .

RUN apk add socat && \
    apk add --virtual build-dependencies gcc libc-dev && \
    gcc app.c -o getflag && \
    chmod +x getflag && \
    rm app.c && \
    chown root:root getflag && \
    chmod 4777 getflag && \
    chmod 600 flag.txt && \
    apk del build-dependencies

CMD ["socat", "TCP4-LISTEN:9000,fork", "EXEC:./getflag"]
