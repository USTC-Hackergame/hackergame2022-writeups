# check if arch is X86_64
A = arch
A == ARCH_X86_64 ? next : dead
A = sys_number
A >= 0x40000000 ? dead : next
A == kill ? dead : next
A == tkill ? dead : next
A == tgkill ? dead : next
A == open ? notify : next
A == openat ? dead : next
A == 437 ? dead : next
A == 434 ? dead : next
A == uselib ? dead : next
A == open_by_handle_at ? dead : next
ok:
return ALLOW
notify:
# return ALLOW
return USER_NOTIF
# return TRACE
dead:
return KILL


## trace listen OPEN, 如果 open 不以 /proc 开头的文件，就不让。
## ban 掉 openat openat2 ....