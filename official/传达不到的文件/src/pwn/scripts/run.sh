#!/bin/sh

cwd=$(cd $(dirname "$0"); pwd)

cat $cwd/../flag2 > /dev/shm/flag2

qemu-system-x86_64 \
    -m 256M \
    -kernel $cwd/../bin/bzImage \
    -initrd $cwd/../bin/rootfs.cpio \
    -monitor /dev/null \
    -append "root=/dev/ram console=ttyS0 oops=panic quiet panic=1 kaslr" \
    -cpu kvm64,+smep,+smap\
    -drive file=/dev/shm/flag2,format=raw,index=0,media=disk \
    -nographic \
    -no-reboot \
    $@
