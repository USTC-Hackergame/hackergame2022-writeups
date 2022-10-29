.PHONY: all
all: bin/rootfs.cpio

bin/chall: src/pwn.c
	gcc -o $@ $<

bin/rootfs.cpio: bin/chall bin/rootfs_orig.cpio
	./scripts/build_rootfs.sh

.PHONY: clean
clean:
	rm -rf bin/rootfs.cpio bin/chall