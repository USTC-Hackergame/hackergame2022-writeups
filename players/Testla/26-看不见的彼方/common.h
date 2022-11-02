#ifndef COMMON_H
#define COMMON_H

#include <sys/types.h>
#include <sys/msg.h>

#include "error_functions.h"

#define SERVER_KEY 0xb29632b1

typedef struct msg_t {
    long mtype;  // Always 1
    char content[64];
} msg_t;

#endif  // COMMON_H
