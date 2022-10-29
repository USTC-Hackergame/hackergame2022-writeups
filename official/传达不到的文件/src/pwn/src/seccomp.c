#include <linux/seccomp.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/prctl.h>
#include <sys/syscall.h>
#include <unistd.h>

int install_seccomp() {
  int notify_fd;
  static unsigned char filter[] = {32,0,0,0,4,0,0,0,21,0,0,13,62,0,0,192,32,0,0,0,0,0,0,0,53,0,11,0,0,0,0,64,21,0,10,0,62,0,0,0,21,0,9,0,200,0,0,0,21,0,8,0,234,0,0,0,21,0,6,0,2,0,0,0,21,0,6,0,1,1,0,0,21,0,5,0,181,1,0,0,21,0,4,0,178,1,0,0,21,0,3,0,134,0,0,0,21,0,2,0,48,1,0,0,6,0,0,0,0,0,255,127,6,0,0,0,0,0,192,127,6,0,0,0,0,0,0,0};
  struct prog {
    unsigned short len;
    unsigned char *filter;
  } rule = {
    .len = sizeof(filter) >> 3,
    .filter = filter
  };
  if(prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) < 0) { perror("prctl(PR_SET_NO_NEW_PRIVS)"); exit(2); }
  if((notify_fd = syscall(SYS_seccomp,SECCOMP_SET_MODE_FILTER,SECCOMP_FILTER_FLAG_NEW_LISTENER,&rule)) < 0) { perror("seccomp(SECCOMP_SET_MODE_FILTER)"); exit(2); }
  return notify_fd;
}
