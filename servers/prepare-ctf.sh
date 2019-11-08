#!/bin/bash

git clone https://github.com/CTFd/CTFd ctfd

cd ..
python3 clean.py
cd servers

mkdir ctfd/plugins
cd ctfd/plugins

git clone https://github.com/alokmenghrajani/ctfd-event-countdown.git
git clone https://github.com/alokmenghrajani/ctfd-timed-releases-plugin.git

git clone https://github.com/stormctf/CTFd-Theme-StormCTF.git
mv CTFd-Theme-StormCTF/stormctf ../CTFd/themes/
mv CTFd-Theme-StormCTF/plugins/challenges/assets/view.html ../CTFd/plugins/challenges/assets/view.html
mv CTFd-Theme-StormCTF/plugins/challenges/assets/view.js ../CTFd/plugins/challenges/assets/view.js
rm -rf CTFd-Theme-StormCTF

cd ../../

docker build -t ctfd-import ctfd
docker run \
    -v "$(pwd)/.data/CTFd/logs:/var/log/CTFd" \
    -v "$(pwd)/.data/CTFd/uploads:/var/uploads" \
    -v "$(pwd)/ctfd/:/opt/CTFd:ro" \
    -v "$(pwd)/../CTFd-import:/import" \
    -w /opt/CTFd/ \
    --entrypoint /bin/sh \
    ctfd-import \
    import.py /import/ctfd-import.zip