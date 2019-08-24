# --- Docker Setup ---

FROM alpine:latest

ARG SERVER_FILES=directories
ARG VULN_USER=evilcorp-user
ARG HTTP_PORT=3000
ARG SSH_PORT=22

EXPOSE ${HTTP_PORT}/tcp
EXPOSE ${SSH_PORT}/tcp


# --- System Setup ---

# Set environment variables
ENV VULN_USER=${VULN_USER}
ENV HTTP_PORT=${HTTP_PORT}

# Install packages
RUN apk add --no-cache nodejs \
    npm \
    sudo \
    shadow \
    openssh \
    openrc \
    bash


# --- User Setup ---

# System Users
# meant to be unbreakable
RUN echo "root:mordremoththejungledragon" | chpasswd -c SHA256; \
    useradd -M www-data; \
    echo "www-data:atotallyunbreakablesha256password" | chpasswd -c SHA256

# Vulnerable user
# uses MD5 instead of SHA256 etc... to make cracking a little quicker
RUN useradd -s /bin/rbash --create-home ${VULN_USER}; \
    echo "${VULN_USER}:1nokungfu" | chpasswd -c MD5


# --- Directory Setup ---

# Webapp directories
# copy them over and ensure only www-data and root can access
COPY app/ /var/www
RUN chown -R root:www-data /var/www; \
    chmod -R 770 /var/www

# /etc directories
# Ensure vuln user can run hexdump as sudo and /etc/shadow.bak is readable by all users
COPY ${SERVER_FILES}/etc/* /etc/
RUN cp /etc/shadow /etc/shadow.bak; \
    chmod +r /etc/shadow.bak; \
    echo "${VULN_USER} ALL=(ALL) /usr/bin/hexdump" >> /etc/sudoers

# Vulnerable user home directory
# Change the home directory to root such that vulnerable user cannot modify or change anything
COPY ${SERVER_FILES}/home/home-files/* /home/${VULN_USER}/
RUN chown root:root /home/${VULN_USER}


# /tmp and /root directories
# Ensure /tmp can be read by not edited by the vuln user
COPY ${SERVER_FILES}/tmp/* /tmp/
COPY ${SERVER_FILES}/root/* /root/
RUN chmod 755 /tmp


# --- Bash Setup ---

# Remove vulnerable users ability to run or modify certain binaries
RUN chown root:www-data /usr/bin/node \
                        /usr/bin/npx \
                        /usr/bin/npm
RUN chmod 770 /usr/bin/node \
              /usr/bin/npx \
              /usr/bin/npm

# Setup vulnerable users restricted bash
RUN cp /bin/bash /bin/rbash; \
    mkdir /usr/rbash-programs; \
    cd /usr/rbash-programs; \
    mkdir echo vi; \
    ln -s /usr/bin/vi vi/vi; \
    ln -s /bin/echo echo/echo


# --- Run Services ---

WORKDIR /var/www/
RUN npm install --only=prod
ENTRYPOINT ./init.sh $HTTP_PORT $VULN_USER
