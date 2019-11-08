FROM ubuntu

WORKDIR /challenge
USER root

# Add tools people may use
RUN apt-get update && \
	apt-get install --no-install-recommends -y strace vi vim nano && \
	echo "root:G-9vn&bK)4Q;ECek" | chpasswd

# Setup challenge
COPY talk /challenge/talk
RUN useradd -s /bin/bash eviluser && \
	chown root:root /challenge && \
	chmod 1777 /challenge && \
	chown root:root /challenge/talk && \
	chmod 6755 /challenge/talk && \
	echo "Hello there! I have a secret... I bet you'll never guess what it is." > /challenge/words.txt && \
	chown eviluser:eviluser /challenge/words.txt && \
	chmod 644 /challenge/words.txt && \
	echo "flag{h1c0ry_d1c0ry_d0c}" > /challenge/flag && \
	chown root:root /challenge/flag && \
	chmod 600 /challenge/flag
