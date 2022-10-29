#!/bin/bash
cat /root/flag1 > /dev/shm/flag1
chown judger:judger /dev/shm/flag1
chmod 700 /dev/shm/flag1

cat /root/flag2 > /dev/shm/flag2
chown judger:judger /dev/shm/flag2
chmod 700 /dev/shm/flag2

cp -r /judger /dev/shm/judger
chown -R judger:judger /dev/shm/judger
chmod 777 /dev/shm/judger/temp

cd /dev/shm/judger
gosu judger /bin/bash -c "exec -a \"Wow! You are reading cmdline of proc! But no flag here, try something else! ^_^\" /usr/local/bin/python ./checker.py" 
