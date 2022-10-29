.PHONY: all
all: bin/rootfs.cpio

# chall: main.c seccomp.c link.lds
# 	gcc -nostartfiles main.c seccomp.c -T link.lds -o $@

bin/chall: src/main.c src/seccomp.c
	gcc -nostartfiles $^ -o $@

bin/rootfs.cpio: bin/chall bin/rootfs_orig.cpio
	./scripts/build_rootfs.sh

src/seccomp.S: src/seccomp.asm
	echo ".intel_syntax noprefix\n.global install_seccomp" > $@
	seccomp-tools asm $< -f assembly >> $@
	echo ".att_syntax prefix\n" >> $@ 
	sed -i '/push   _filter_end - _filter >> 3/c\  lea    rdx, [rip + _filter_end]\n  lea    rsi, [rip + _filter]\n  sub    rdx, rsi\n  shr    rdx, 3\n  push   rdx' $@ 

src/seccomp.c: src/seccomp.asm
	seccomp-tools asm $< -f c_source > $@
	sed -i "/static void install_seccomp()/c\int install_seccomp() {\n  int notify_fd;" $@
	sed -i "/if(prctl(PR_SET_SECCOMP/c\  if((notify_fd = syscall(SYS_seccomp,SECCOMP_SET_MODE_FILTER,SECCOMP_FILTER_FLAG_NEW_LISTENER,&rule)) < 0) { perror(\"seccomp(SECCOMP_SET_MODE_FILTER)\"); exit(2); }\n  return notify_fd;" $@
	sed -i '/#include <sys\/prctl.h>/a #include <sys\/syscall.h>\n#include <unistd.h>' $@

.PHONY: clean
clean:
	rm -f bin/chall src/seccomp.S src/seccomp.c bin/rootfs.cpio