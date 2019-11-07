# This image builds other containers inside of the DinD container for later SSH spawning

FROM alpine:3.10.3

RUN apk add docker bash;

RUN echo "#!/bin/bash" >> /run.sh && \
    echo "env; cat /run.sh; until docker ps; do sleep 2; done; docker build -f /app/Dockerfile -t \"\${IMAGE_NAME}\" /app" >> /run.sh && \
    chmod +x /run.sh

ENTRYPOINT [ "/run.sh" ]