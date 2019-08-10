#!/bin/bash

zipname=TOP-SECRET.zip

echo "Rebuilding the encrypted zip file..."
rm app/public/${zipname}
zip -e -j --password "$(cat zip-file/password.txt)" ${zipname} zip-file/flag.txt zip-file/top-secret.md
mv ${zipname} app/public/
