#! /bin/bash

cwd=$(cd $(dirname "$0"); pwd) 

if [ -d "/tmp/hg2022/core" ]; then
    rm -rf /tmp/hg2022/core
fi
mkdir -p /tmp/hg2022/core

if file $cwd/../bin/rootfs_orig.cpio | grep "zip"; then
    cp $cwd/../bin/rootfs_orig.cpio /tmp/hg2022/core/core.cpio.gz
    gunzip /tmp/hg2022/core/core.cpio.gz
else
    cp $cwd/../bin/rootfs_orig.cpio /tmp/hg2022/core/core.cpio
fi

cp $cwd/../bin/chall /tmp/hg2022/core/ 

# cp /home/v1me/exp/exp /tmp/hg2022/core/exp
# cp /home/v1me/exp/exp1 /tmp/hg2022/core/exp1

pushd /tmp/hg2022/core/ 
cpio -idm < ./core.cpio
rm ./core.cpio

cat << EOF > ./etc/init.d/rcS
#! /bin/sh

mkdir -p /tmp
mount -t proc none /proc
mount -t sysfs none /sys
mount -t debugfs none /sys/kernel/debug
mount -t devtmpfs devtmpfs /dev
mount -t tmpfs none /tmp
mdev -s

echo 1 > /proc/sys/kernel/kptr_restrict
echo 1 > /proc/sys/kernel/dmesg_restrict
chmod 400 /proc/kallsyms

mkdir -p /chall_env
chown 1337:1337 /chall_env
cp /bin/busybox /chall_env/busybox

chown 1337:1337 /chall
chmod 4555 /chall

cat /dev/sda > /flag
chown 1337:1337 /flag
chmod 0400 /flag

poweroff -d 120 -f &
setsid /bin/cttyhack setuidgid 1337 /chall /chall_env

umount /proc
umount /tmp


poweroff -d 0  -f
EOF


find . -print0 | cpio --null -ov --format=newc | gzip -9 -n > $cwd/../bin/rootfs.cpio
popd

rm -rf /tmp/hg2022