#!/bin/sh

HTTP_PORT=$1
VULN_USER=$2

echo "Running with args: [${1}, ${2}]"

rc-update add sshd
rc-status
touch /run/openrc/softlevel
/etc/init.d/sshd start
su www-data -c "npm run start ${HTTP_PORT} ${VULN_USER}"
