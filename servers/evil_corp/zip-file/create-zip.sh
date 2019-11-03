zipname=TOP-SECRET.zip
password=$(cat ./password.txt)
zip -e -j --password "${password}" ../app/public/${zipname} ./flag.txt ./top-secret.md
