FROM ubuntu
WORKDIR /challenge
USER root

# Add tools
RUN apt-get update && \
	apt-get install -y strace objdump cowsay && \
	wget https://raw.githubusercontent.com/neandrake/cowsay/master/cows/parrot.cow -P /usr/share/cows && \
	echo "root:G-9vn&bK)4Q;ECek" | chpasswd

# Setup challenge
ADD talk2 /challenge/talk2
RUN useradd -s /bin/bash eviluser2 && \
	chown root:root /challenge && \
	chmod 1777 /challenge && \
	chown root:root /challenge/talk2 && \
	chmod 6755 /challenge/talk2 && \
	echo "flag{g0nna_n33d_4_p1ung3r}" > /challenge/flag && \
	chown root:root /challenge/flag && \
	chmod 600 /challenge/flag
