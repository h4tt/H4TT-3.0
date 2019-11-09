FROM alpine

COPY talk_to_me_ssh/run-challenge.sh /app/

RUN apk add openssh-server docker bash busybox-suid && \
    mkdir /var/run/sshd && \
    rm /etc/motd && \
    chown 1000:1000 /app/run-challenge.sh && \
    adduser -s "/app/run-challenge.sh" -D -S eviluser -G wheel && \
    echo "eviluser:12345" | chpasswd && \
    ssh-keygen -f /etc/ssh/ssh_host_rsa_key -N '' -t rsa && \
    ssh-keygen -f /etc/ssh/ssh_host_dsa_key -N '' -t dsa

CMD ["/usr/sbin/sshd", "-D"]