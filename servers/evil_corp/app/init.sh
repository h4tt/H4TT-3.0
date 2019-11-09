#!/bin/sh

HTTP_PORT=$1
VULN_USER=$2

echo "Running with args: [${1}, ${2}]"

# start ssh service
rc-update add sshd
rc-status
touch /run/openrc/softlevel
/etc/init.d/sshd start

# zip file
zipname=TOP-SECRET.zip
password=$(cat ./zip-file/password.txt)
zip -e -j --password "${password}" ./public/${zipname} ./zip-file/flag.txt ./zip-file/top-secret.md
rm -rf ./zip-file

# run http service
su www-data -c "npm run start ${HTTP_PORT} ${VULN_USER}"
