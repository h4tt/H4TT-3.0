FROM alpine

# docker args
ARG SERVER_FILES=directories
ARG VULN_USER=evilcorp-user
ARG HTTP_PORT=3000
ARG SSH_PORT=22

# set ENV args
ENV VULN_USER=${VULN_USER}
ENV HTTP_PORT=${HTTP_PORT}

# install packages
RUN apk add --no-cache nodejs npm sudo shadow openssh openrc bash

# setup users
# change passwords (www-data and root meant to be unbreakable)
# use MD5 for vulnerable user
RUN echo "root:mordremoththejungledragon" | chpasswd -c SHA256
RUN useradd -s /bin/rbash --create-home ${VULN_USER}
RUN echo "${VULN_USER}:1nokungfu" | chpasswd -c MD5
RUN useradd -M www-data
RUN echo "www-data:atotallyunbreakablesha256password" | chpasswd -c SHA256

# set up directories
# node server directories
COPY app/ /var/www
RUN chown -R root:www-data /var/www
RUN chmod -R 770 /var/www

# vulnerable user directories
# remove vuln users ability do modify or delete his home directory
COPY ${SERVER_FILES}/home/home-files/* /home/${VULN_USER}/
RUN chown root:root /home/${VULN_USER}

# /etc directories
COPY ${SERVER_FILES}/etc/* /etc/
RUN cp /etc/shadow /etc/shadow.bak
RUN chmod +r /etc/shadow.bak
RUN echo "${VULN_USER} ALL=(ALL) /usr/bin/hexdump" >> /etc/sudoers

# /tmp and /root directories
COPY ${SERVER_FILES}/tmp/* /tmp/
RUN chmod 755 /tmp
COPY ${SERVER_FILES}/root/* /root/

# remove vulnerable users ability to run certain commands (append to list to lock down more)
RUN chown root:www-data /usr/bin/node /usr/bin/npx /usr/bin/npm
RUN chmod 770 /usr/bin/node /usr/bin/npx /usr/bin/npm

# set up restricted bash directory
RUN cp /bin/bash /bin/rbash
RUN mkdir /usr/rbash-programs
WORKDIR /usr/rbash-programs
RUN mkdir echo vi
RUN ln -s /usr/bin/vi vi/vi
RUN ln -s /bin/echo echo/echo

# expose ports
EXPOSE ${HTTP_PORT}/tcp
EXPOSE ${SSH_PORT}/tcp

# run services
WORKDIR /var/www/
RUN npm install --only=prod
ENTRYPOINT ./init.sh $HTTP_PORT $VULN_USER
