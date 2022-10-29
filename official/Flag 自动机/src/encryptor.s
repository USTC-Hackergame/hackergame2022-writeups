	.file	"encryptor.cpp"
	.text
	.section	.text$_Z8__ROL1__hi,"x"
	.linkonce discard
	.globl	__Z8__ROL1__hi
	.def	__Z8__ROL1__hi;	.scl	2;	.type	32;	.endef
__Z8__ROL1__hi:
	pushl	%ebp
	movl	%esp, %ebp
	subl	$40, %esp
	movl	8(%ebp), %eax
	movb	%al, -12(%ebp)
	movzbl	-12(%ebp), %eax
	movl	12(%ebp), %edx
	movl	%edx, 4(%esp)
	movl	%eax, (%esp)
	call	__Z7__ROL__IhET_S0_i
	leave
	ret
	.section	.text$_Z8__ROR1__hi,"x"
	.linkonce discard
	.globl	__Z8__ROR1__hi
	.def	__Z8__ROR1__hi;	.scl	2;	.type	32;	.endef
__Z8__ROR1__hi:
	pushl	%ebp
	movl	%esp, %ebp
	subl	$40, %esp
	movl	8(%ebp), %eax
	movb	%al, -12(%ebp)
	movl	12(%ebp), %eax
	negl	%eax
	movl	%eax, %edx
	movzbl	-12(%ebp), %eax
	movl	%edx, 4(%esp)
	movl	%eax, (%esp)
	call	__Z7__ROL__IhET_S0_i
	leave
	ret
	.section	.text$_Z6printfPKcz,"x"
	.linkonce discard
	.globl	__Z6printfPKcz
	.def	__Z6printfPKcz;	.scl	2;	.type	32;	.endef
__Z6printfPKcz:
	pushl	%ebp
	movl	%esp, %ebp
	pushl	%ebx
	subl	$36, %esp
	leal	12(%ebp), %eax
	movl	%eax, -16(%ebp)
	movl	-16(%ebp), %ebx
	movl	$1, (%esp)
	movl	__imp____acrt_iob_func, %eax
	call	*%eax
	movl	%eax, %edx
	movl	%ebx, 8(%esp)
	movl	8(%ebp), %eax
	movl	%eax, 4(%esp)
	movl	%edx, (%esp)
	call	___mingw_vfprintf
	movl	%eax, -12(%ebp)
	movl	-12(%ebp), %eax
	addl	$36, %esp
	popl	%ebx
	popl	%ebp
	ret
	.globl	_key
	.data
	.align 4
_key:
	.ascii "Kanbe_Kotori\0"
	.globl	_box
	.bss
	.align 32
_box:
	.space 43
	.globl	_encrypted
	.data
	.align 32
_encrypted:
	.byte	25
	.byte	27
	.byte	-24
	.byte	-19
	.byte	-126
	.byte	-49
	.byte	51
	.byte	-79
	.byte	-39
	.byte	16
	.byte	16
	.byte	-9
	.byte	-13
	.byte	43
	.byte	62
	.byte	32
	.byte	2
	.byte	-35
	.byte	46
	.byte	-71
	.byte	-113
	.byte	57
	.byte	21
	.byte	-74
	.byte	-8
	.byte	88
	.byte	12
	.byte	-50
	.byte	104
	.byte	14
	.byte	-109
	.byte	-33
	.byte	46
	.byte	-54
	.byte	67
	.byte	-113
	.byte	-100
	.byte	-24
	.byte	-86
	.byte	126
	.byte	-46
	.byte	67
	.byte	-63
	.globl	_output
	.bss
	.align 32
_output:
	.space 43
	.text
	.globl	__Z6getnumi
	.def	__Z6getnumi;	.scl	2;	.type	32;	.endef
__Z6getnumi:
	pushl	%ebp
	movl	%esp, %ebp
	cmpl	$0, 8(%ebp)
	jne	L8
	movl	$25, %eax
	jmp	L9
L8:
	cmpl	$1, 8(%ebp)
	jne	L10
	movl	$17, %eax
	jmp	L9
L10:
	cmpl	$2, 8(%ebp)
	jne	L11
	movl	$69, %eax
	jmp	L9
L11:
	cmpl	$3, 8(%ebp)
	jne	L12
	movl	$20, %eax
	jmp	L9
L12:
	movl	$0, %eax
L9:
	popl	%ebp
	ret
	.section .rdata,"dr"
LC0:
	.ascii "%d \0"
LC1:
	.ascii "\12\0"
	.text
	.globl	__Z7initBoxv
	.def	__Z7initBoxv;	.scl	2;	.type	32;	.endef
__Z7initBoxv:
	pushl	%ebp
	movl	%esp, %ebp
	pushl	%edi
	pushl	%esi
	pushl	%ebx
	subl	$44, %esp
	movl	$0, -28(%ebp)
L17:
	cmpl	$12, -28(%ebp)
	jg	L14
	movl	$0, -36(%ebp)
L16:
	movl	-36(%ebp), %eax
	cmpl	$3, %eax
	jg	L15
	movl	-36(%ebp), %edx
	movl	%edx, %eax
	sall	$2, %eax
	addl	%edx, %eax
	jz      .initBox1
	jnz		.initBox1
	.byte	0xEA
.initBox1:
	addl	%eax, %eax
	addl	%eax, %edx
	movl	%edx, %eax
	sarl	$31, %eax
	shrl	$30, %eax
	addl	%eax, %edx
	andl	$3, %edx
	subl	%eax, %edx
	movl	%edx, %eax
	movl	%eax, (%esp)
	call	__Z6getnumi
	movzbl	%al, %eax
	andl	$7, %eax
	movl	%eax, %edi
	movl	-28(%ebp), %edx
	movl	%edx, %eax
	addl	%eax, %eax
	addl	%edx, %eax
	pushl 	%eax
	pushl	%edx
    jmp 	label_1
label_2:
    movl 	(%esp), %eax
    addl 	$8, %esp
    jmp 	*%eax
label_1:
    call 	label_2
    popl 	%eax
	sall	$2, %eax
	addl	%eax, %edx
	movl	-36(%ebp), %eax
	leal	(%edx,%eax), %ecx
	movl	$1321528399, %edx
	movl	%ecx, %eax
	imull	%edx
	sarl	$2, %edx
	movl	%ecx, %eax
	sarl	$31, %eax
	subl	%eax, %edx
	movl	%edx, %eax
	addl	%eax, %eax
	addl	%edx, %eax
	sall	$2, %eax
	addl	%edx, %eax
	subl	%eax, %ecx
	movl	%ecx, %edx
	movzbl	_key(%edx), %eax
	movzbl	%al, %esi
	movl	-28(%ebp), %eax
	leal	0(,%eax,4), %edx
	movl	-36(%ebp), %eax
	leal	(%edx,%eax), %ecx
	movl	$799063683, %edx
	movl	%ecx, %eax
	imull	%edx
	sarl	$3, %edx
	movl	%ecx, %eax
	sarl	$31, %eax
	movl	%edx, %ebx
	subl	%eax, %ebx
	imull	$43, %ebx, %eax
	movl	%ecx, %ebx
	subl	%eax, %ebx
	movl	%edi, 4(%esp)
	movl	%esi, (%esp)
	call	__Z8__ROL1__hi
	movb	%al, _box(%ebx)
	movl	-28(%ebp), %eax
	leal	0(,%eax,4), %edx
	movl	-36(%ebp), %eax
	leal	(%edx,%eax), %ecx
	movl	$1321528399, %edx
	movl	%ecx, %eax
	imull	%edx
	sarl	$2, %edx
	movl	%ecx, %eax
	sarl	$31, %eax
	subl	%eax, %edx
	movl	%edx, %eax
	addl	%eax, %eax
	addl	%edx, %eax
	sall	$2, %eax
	addl	%edx, %eax
	subl	%eax, %ecx
	movl	%ecx, %edx
	movzbl	_key(%edx), %ebx
	movl	-36(%ebp), %eax
	cltd
	shrl	$30, %edx
	addl	%edx, %eax
	andl	$3, %eax
	subl	%edx, %eax
	movl	%eax, (%esp)
	call	__Z6getnumi
	addl	%ebx, %eax
	movzbl	%al, %ebx
	movl	-28(%ebp), %eax
	leal	0(,%eax,4), %edx
	movl	-36(%ebp), %eax
	leal	(%edx,%eax), %ecx
	movl	$799063683, %edx
	movl	%ecx, %eax
	imull	%edx
	sarl	$3, %edx
	movl	%ecx, %eax
	sarl	$31, %eax
	subl	%eax, %edx
	movl	%edx, %eax
	imull	$43, %eax, %eax
	subl	%eax, %ecx
	movl	%ecx, %eax
	movzbl	_box(%eax), %edx
	movl	%edx, %ecx
	movl	%ebx, %edx
	xorl	%ecx, %edx
	movb	%dl, _box(%eax)
	movl	-28(%ebp), %edx
	movl	%edx, %eax
	sall	$2, %eax
	addl	%edx, %eax
	addl	%eax, %eax
	addl	%eax, %edx
	movl	%edx, %eax
	sarl	$31, %eax
	shrl	$30, %eax
	addl	%eax, %edx
	andl	$3, %edx
	subl	%eax, %edx
	movl	%edx, %eax
	movl	%eax, (%esp)
	call	__Z6getnumi
	movzbl	%al, %eax
	andl	$7, %eax
	movl	%eax, %ebx
	movl	-28(%ebp), %edx
	movl	%edx, %eax
	addl	%eax, %eax
	addl	%edx, %eax
	sall	$2, %eax
	addl	%eax, %edx
	movl	-36(%ebp), %eax
	leal	(%edx,%eax), %ecx
	movl	$1321528399, %edx
	movl	%ecx, %eax
	imull	%edx
	sarl	$2, %edx
	movl	%ecx, %eax
	sarl	$31, %eax
	subl	%eax, %edx
	movl	%edx, %eax
	addl	%eax, %eax
	addl	%edx, %eax
	sall	$2, %eax
	addl	%edx, %eax
	subl	%eax, %ecx
	movl	%ecx, %edx
	movzbl	_key(%edx), %eax
	movzbl	%al, %eax
	movl	%ebx, 4(%esp)
	movl	%eax, (%esp)
	call	__Z8__ROR1__hi
	movzbl	%al, %ebx
	movl	-28(%ebp), %eax
	leal	0(,%eax,4), %edx
	movl	-36(%ebp), %eax
	leal	(%edx,%eax), %ecx
	movl	$799063683, %edx
	movl	%ecx, %eax
	imull	%edx
	sarl	$3, %edx
	movl	%ecx, %eax
	sarl	$31, %eax
	subl	%eax, %edx
	movl	%edx, %eax
	imull	$43, %eax, %eax
	subl	%eax, %ecx
	movl	%ecx, %eax
	movzbl	_box(%eax), %edx
	movl	%edx, %ecx
	movl	%ebx, %edx
	xorl	%ecx, %edx
	movb	%dl, _box(%eax)
	movl	-36(%ebp), %eax
	addl	$1, %eax
	movl	%eax, -36(%ebp)
	jmp	L16
L15:
	addl	$1, -28(%ebp)
	jmp	L17
L14:
	movl	$0, -32(%ebp)
L19:
	cmpl	$42, -32(%ebp)
	jg	L18
	movl	-32(%ebp), %eax
	addl	$_box, %eax
	movzbl	(%eax), %eax
	movzbl	%al, %eax
	movl	%eax, 4(%esp)
	movl	$LC0, (%esp)
	call	__Z6printfPKcz
	addl	$1, -32(%ebp)
	jmp	L19
L18:
	movl	$LC1, (%esp)
	call	__Z6printfPKcz
	nop
	addl	$44, %esp
	popl	%ebx
	popl	%esi
	popl	%edi
	popl	%ebp
	ret
	.globl	__Z7decryptv
	.def	__Z7decryptv;	.scl	2;	.type	32;	.endef
__Z7decryptv:
	pushl	%ebp
	movl	%esp, %ebp
	pushl	%esi
	pushl	%ebx
	subl	$48, %esp
	movl	$0, -12(%ebp)
L22:
	cmpl	$42, -12(%ebp)
	jg	L23
	movl	-12(%ebp), %eax
	addl	$_encrypted, %eax
	movzbl	(%eax), %ebx
	movl	-12(%ebp), %eax
	addl	$_box, %eax
	movzbl	(%eax), %eax
	movzbl	%al, %esi
	movl	-12(%ebp), %edx
	movl	%edx, %eax
	sall	$2, %eax
	addl	%edx, %eax
	addl	%eax, %eax
	leal	(%eax,%edx), %ecx
	movl	$1321528399, %edx
	movl	%ecx, %eax
	imull	%edx
	sarl	$2, %edx
	movl	%ecx, %eax
	sarl	$31, %eax
	subl	%eax, %edx
	movl	%edx, %eax
	addl	%eax, %eax
	addl	%edx, %eax
	sall	$2, %eax
	addl	%edx, %eax
	subl	%eax, %ecx
	movl	%ecx, %edx
	movzbl	_key(%edx), %eax
	movzbl	%al, %eax
	addl	%esi, %eax
	movb	%al, -25(%ebp)
	movl	-12(%ebp), %edx
	movl	%edx, %eax
	addl	%eax, %eax
	addl	%edx, %eax
	sall	$2, %eax
	addl	%eax, %edx
	movl	%edx, %eax
	sarl	$31, %eax
	shrl	$30, %eax
	addl	%eax, %edx
	andl	$3, %edx
	subl	%eax, %edx
	movl	%edx, %eax
	movl	%eax, (%esp)
	call	__Z6getnumi
	movl	%eax, %edx
	movzbl	-25(%ebp), %eax
	imull	%edx, %eax
	subl	%eax, %ebx
	movl	%ebx, %eax
	movl	%eax, %edx
	movl	-12(%ebp), %eax
	addl	$_box, %eax
	movzbl	(%eax), %eax
	xorl	%edx, %eax
	movl	%eax, %edx
	movl	-12(%ebp), %eax
	addl	$_encrypted, %eax
	movb	%dl, (%eax)
	addl	$1, -12(%ebp)
	jmp	L22
L23:
	nop
	addl	$48, %esp
	popl	%ebx
	popl	%esi
	popl	%ebp
	ret
	.section .rdata,"dr"
	.align 4
LC2:
	.ascii "Hint: You don't need to reverse the decryption logic itself.\0"
LC3:
	.ascii "%s\0"
	.text
	.globl	__Z7getflagP6HWND__l
	.def	__Z7getflagP6HWND__l;	.scl	2;	.type	32;	.endef
__Z7getflagP6HWND__l:
	pushl	%ebp
	movl	%esp, %ebp
	subl	$40, %esp
	call	__Z7initBoxv
	call	__Z7decryptv
	movl	$_encrypted, 4(%esp)
	movl	$LC3, (%esp)
	call	__Z6printfPKcz
	movl	$43, (%esp)
	call	_malloc
	movl	%eax, -16(%ebp)
	movl	$43, 8(%esp)
	movl	$_encrypted, 4(%esp)
	movl	-16(%ebp), %eax
	movl	%eax, (%esp)
	call	_strncpy
	movl	-16(%ebp), %eax
	leave
	ret
	.section	.text$_Z7__ROL__IhET_S0_i,"x"
	.linkonce discard
	.globl	__Z7__ROL__IhET_S0_i
	.def	__Z7__ROL__IhET_S0_i;	.scl	2;	.type	32;	.endef
__Z7__ROL__IhET_S0_i:
	pushl	%ebp
	movl	%esp, %ebp
	subl	$20, %esp
	movl	8(%ebp), %eax
	movb	%al, -20(%ebp)
	movl	$8, -4(%ebp)
	cmpl	$0, 12(%ebp)
	jle	L27
	andl	$7, 12(%ebp)
	movzbl	-20(%ebp), %edx
	movl	12(%ebp), %eax
	movl	$8, %ecx
	subl	%eax, %ecx
	movl	%ecx, %eax
	movl	%eax, %ecx
	sarl	%cl, %edx
	movl	%edx, %eax
	movb	%al, -5(%ebp)
	movzbl	-20(%ebp), %edx
	movl	12(%ebp), %eax
	movl	%eax, %ecx
	sall	%cl, %edx
	movl	%edx, %eax
	movb	%al, -20(%ebp)
	movzbl	-5(%ebp), %eax
	orb	%al, -20(%ebp)
	jmp	L28
L27:
	movl	12(%ebp), %eax
	negl	%eax
	andl	$7, %eax
	movl	%eax, 12(%ebp)
	movzbl	-20(%ebp), %edx
	movl	12(%ebp), %eax
	movl	$8, %ecx
	subl	%eax, %ecx
	movl	%ecx, %eax
	movl	%eax, %ecx
	sall	%cl, %edx
	movl	%edx, %eax
	movb	%al, -6(%ebp)
	movzbl	-20(%ebp), %edx
	movl	12(%ebp), %eax
	movl	%eax, %ecx
	sarl	%cl, %edx
	movl	%edx, %eax
	movb	%al, -20(%ebp)
	movzbl	-6(%ebp), %eax
	orb	%al, -20(%ebp)
L28:
	movzbl	-20(%ebp), %eax
	leave
	ret
	.ident	"GCC: (x86_64-win32-sjlj-rev0, Built by MinGW-W64 project) 8.1.0"
	.def	___mingw_vfprintf;	.scl	2;	.type	32;	.endef
	.def	_puts;	.scl	2;	.type	32;	.endef
	.def	_malloc;	.scl	2;	.type	32;	.endef
	.def	_strncpy;	.scl	2;	.type	32;	.endef
