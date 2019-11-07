# This image builds other containers inside of the DinD container for later SSH spawning

FROM alpine:3.10.3

RUN apk add docker

RUN echo "#!/bin/ash" >> /run.sh && \
    echo "until docker ps; do sleep 2; done; docker build -f /app/Dockerfile /app" >> /run.sh && \
    chmod +x /run.sh

CMD [ "/run.sh" ]