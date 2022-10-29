;--------------------------------------------------------
; File Created by SDCC : free open source ANSI-C Compiler
; Version 3.8.0 #10562 (Linux)
;--------------------------------------------------------
	.module firmware
	.optsdcc -mmcs51 --model-small
	
;--------------------------------------------------------
; Public variables in this module
;--------------------------------------------------------
	.globl _uint8_to_str_PARM_2
	.globl _tokenizer_init_PARM_2
	.globl _i2c_read_PARM_3
	.globl _i2c_read_PARM_2
	.globl _i2c_write_PARM_3
	.globl _i2c_write_PARM_2
	.globl _main
	.globl _port_to_int8
	.globl _str_to_uint8
	.globl _uint8_to_str
	.globl _tokenizer_next
	.globl _tokenizer_init
	.globl _serial_read_char
	.globl _i2c_status_to_error
	.globl _i2c_read
	.globl _i2c_write
	.globl _serial_print
	.globl _rand
	.globl _POWERSAVE
	.globl _POWEROFF
	.globl _I2C_READ_WRITE
	.globl _I2C_ADDRESS
	.globl _I2C_BUFFER_SIZE
	.globl _I2C_BUFFER_XRAM_HIGH
	.globl _I2C_BUFFER_XRAM_LOW
	.globl _I2C_STATUS
	.globl _SERIAL_IN_READY
	.globl _SERIAL_IN_DATA
	.globl _SERIAL_OUT_READY
	.globl _SERIAL_OUT_DATA
	.globl _table
	.globl _speedtb
	.globl _init_rand
;--------------------------------------------------------
; special function registers
;--------------------------------------------------------
	.area RSEG    (ABS,DATA)
	.org 0x0000
_SERIAL_OUT_DATA	=	0x00f2
_SERIAL_OUT_READY	=	0x00f3
_SERIAL_IN_DATA	=	0x00fa
_SERIAL_IN_READY	=	0x00fb
_I2C_STATUS	=	0x00e1
_I2C_BUFFER_XRAM_LOW	=	0x00e2
_I2C_BUFFER_XRAM_HIGH	=	0x00e3
_I2C_BUFFER_SIZE	=	0x00e4
_I2C_ADDRESS	=	0x00e6
_I2C_READ_WRITE	=	0x00e7
_POWEROFF	=	0x00ff
_POWERSAVE	=	0x00fe
;--------------------------------------------------------
; special function bits
;--------------------------------------------------------
	.area RSEG    (ABS,DATA)
	.org 0x0000
;--------------------------------------------------------
; overlayable register banks
;--------------------------------------------------------
	.area REG_BANK_0	(REL,OVR,DATA)
	.ds 8
;--------------------------------------------------------
; internal ram data
;--------------------------------------------------------
	.area DSEG    (DATA)
_init_rand::
	.ds 1
_speedtb::
	.ds 8
_table::
	.ds 20
_main_t_131075_50:
	.ds 5
_main_num_327687_70:
	.ds 4
;--------------------------------------------------------
; overlayable items in internal ram 
;--------------------------------------------------------
	.area	OSEG    (OVR,DATA)
	.area	OSEG    (OVR,DATA)
_i2c_write_PARM_2:
	.ds 1
_i2c_write_PARM_3:
	.ds 2
	.area	OSEG    (OVR,DATA)
_i2c_read_PARM_2:
	.ds 1
_i2c_read_PARM_3:
	.ds 2
	.area	OSEG    (OVR,DATA)
	.area	OSEG    (OVR,DATA)
_tokenizer_init_PARM_2:
	.ds 3
	.area	OSEG    (OVR,DATA)
_tokenizer_next_t_65536_24:
	.ds 3
_tokenizer_next_token_start_65537_29:
	.ds 3
	.area	OSEG    (OVR,DATA)
_uint8_to_str_PARM_2:
	.ds 1
_uint8_to_str_sloc0_1_0:
	.ds 2
	.area	OSEG    (OVR,DATA)
;--------------------------------------------------------
; Stack segment in internal ram 
;--------------------------------------------------------
	.area	SSEG
__start__stack:
	.ds	1

;--------------------------------------------------------
; indirectly addressable internal ram data
;--------------------------------------------------------
	.area ISEG    (DATA)
;--------------------------------------------------------
; absolute internal ram data
;--------------------------------------------------------
	.area IABS    (ABS,DATA)
	.area IABS    (ABS,DATA)
;--------------------------------------------------------
; bit data
;--------------------------------------------------------
	.area BSEG    (BIT)
;--------------------------------------------------------
; paged external ram data
;--------------------------------------------------------
	.area PSEG    (PAG,XDATA)
;--------------------------------------------------------
; external ram data
;--------------------------------------------------------
	.area XSEG    (XDATA)
_main_cmd_65537_43:
	.ds 384
_main_i2c_buf_65537_43:
	.ds 128
_main_i2c_buf2_65537_43:
	.ds 128
;--------------------------------------------------------
; absolute external ram data
;--------------------------------------------------------
	.area XABS    (ABS,XDATA)
;--------------------------------------------------------
; external initialized ram data
;--------------------------------------------------------
	.area XISEG   (XDATA)
	.area HOME    (CODE)
	.area GSINIT0 (CODE)
	.area GSINIT1 (CODE)
	.area GSINIT2 (CODE)
	.area GSINIT3 (CODE)
	.area GSINIT4 (CODE)
	.area GSINIT5 (CODE)
	.area GSINIT  (CODE)
	.area GSFINAL (CODE)
	.area CSEG    (CODE)
;--------------------------------------------------------
; interrupt vector 
;--------------------------------------------------------
	.area HOME    (CODE)
__interrupt_vect:
	ljmp	__sdcc_gsinit_startup
;--------------------------------------------------------
; global & static initialisations
;--------------------------------------------------------
	.area HOME    (CODE)
	.area GSINIT  (CODE)
	.area GSFINAL (CODE)
	.area GSINIT  (CODE)
	.globl __sdcc_gsinit_startup
	.globl __sdcc_program_startup
	.globl __start__stack
	.globl __mcs51_genXINIT
	.globl __mcs51_genXRAMCLEAR
	.globl __mcs51_genRAMCLEAR
;	firmware.c:23: int8_t init_rand=7;
	mov	_init_rand,#0x07
;	firmware.c:24: int8_t speedtb[8]={0x11,0x45,0x14,0x19,0x81,0x24,0x00,0x19};
	mov	_speedtb,#0x11
	mov	(_speedtb + 0x0001),#0x45
	mov	(_speedtb + 0x0002),#0x14
	mov	(_speedtb + 0x0003),#0x19
	mov	(_speedtb + 0x0004),#0x81
	mov	(_speedtb + 0x0005),#0x24
	mov	(_speedtb + 0x0006),#0x00
	mov	(_speedtb + 0x0007),#0x19
;	firmware.c:137: uint8_t table[20]="0123456789ABCDEF";
	mov	_table,#0x30
	mov	(_table + 0x0001),#0x31
	mov	(_table + 0x0002),#0x32
	mov	(_table + 0x0003),#0x33
	mov	(_table + 0x0004),#0x34
	mov	(_table + 0x0005),#0x35
	mov	(_table + 0x0006),#0x36
	mov	(_table + 0x0007),#0x37
	mov	(_table + 0x0008),#0x38
	mov	(_table + 0x0009),#0x39
	mov	(_table + 0x000a),#0x41
	mov	(_table + 0x000b),#0x42
	mov	(_table + 0x000c),#0x43
	mov	(_table + 0x000d),#0x44
	mov	(_table + 0x000e),#0x45
	mov	(_table + 0x000f),#0x46
	mov	(_table + 0x0010),#0x00
	mov	(_table + 0x0011),#0x00
	mov	(_table + 0x0012),#0x00
	mov	(_table + 0x0013),#0x00
	.area GSFINAL (CODE)
	ljmp	__sdcc_program_startup
;--------------------------------------------------------
; Home
;--------------------------------------------------------
	.area HOME    (CODE)
	.area HOME    (CODE)
__sdcc_program_startup:
	ljmp	_main
;	return from main will return to caller
;--------------------------------------------------------
; code
;--------------------------------------------------------
	.area CSEG    (CODE)
;------------------------------------------------------------
;Allocation info for local variables in function 'rand'
;------------------------------------------------------------
;	firmware.c:25: int8_t rand(){
;	-----------------------------------------
;	 function rand
;	-----------------------------------------
_rand:
	ar7 = 0x07
	ar6 = 0x06
	ar5 = 0x05
	ar4 = 0x04
	ar3 = 0x03
	ar2 = 0x02
	ar1 = 0x01
	ar0 = 0x00
;	firmware.c:26: init_rand+=1;
	inc	_init_rand
;	firmware.c:27: init_rand&=7;
	anl	_init_rand,#0x07
;	firmware.c:28: return speedtb[init_rand];
	mov	a,_init_rand
	add	a,#_speedtb
	mov	r1,a
	mov	dpl,@r1
;	firmware.c:29: }
	ret
;------------------------------------------------------------
;Allocation info for local variables in function 'serial_print'
;------------------------------------------------------------
;s                         Allocated to registers 
;------------------------------------------------------------
;	firmware.c:31: void serial_print(const char *s) {
;	-----------------------------------------
;	 function serial_print
;	-----------------------------------------
_serial_print:
	mov	r5,dpl
	mov	r6,dph
	mov	r7,b
;	firmware.c:32: while (*s) {
00104$:
	mov	dpl,r5
	mov	dph,r6
	mov	b,r7
	lcall	__gptrget
	jz	00107$
;	firmware.c:33: while (!SERIAL_OUT_READY);
00101$:
	mov	a,_SERIAL_OUT_READY
	jz	00101$
;	firmware.c:34: SERIAL_OUT_DATA = *s++;
	mov	dpl,r5
	mov	dph,r6
	mov	b,r7
	lcall	__gptrget
	mov	_SERIAL_OUT_DATA,a
	inc	dptr
	mov	r5,dpl
	mov	r6,dph
	sjmp	00104$
00107$:
;	firmware.c:36: }
	ret
;------------------------------------------------------------
;Allocation info for local variables in function 'i2c_write'
;------------------------------------------------------------
;req_len                   Allocated with name '_i2c_write_PARM_2'
;buf                       Allocated with name '_i2c_write_PARM_3'
;port                      Allocated to registers r7 
;status                    Allocated to registers r7 
;------------------------------------------------------------
;	firmware.c:38: int8_t i2c_write(int8_t port, uint8_t req_len, __xdata uint8_t *buf) {
;	-----------------------------------------
;	 function i2c_write
;	-----------------------------------------
_i2c_write:
	mov	r7,dpl
;	firmware.c:39: while (I2C_STATUS == 1) {
00101$:
	mov	a,#0x01
	cjne	a,_I2C_STATUS,00103$
;	firmware.c:40: POWERSAVE = 1;  // Enter power save mode for a few milliseconds.
	mov	_POWERSAVE,#0x01
	sjmp	00101$
00103$:
;	firmware.c:43: I2C_BUFFER_XRAM_LOW = (uint8_t)(uint16_t)buf;
	mov	_I2C_BUFFER_XRAM_LOW,_i2c_write_PARM_3
;	firmware.c:44: I2C_BUFFER_XRAM_HIGH = (uint8_t)((uint16_t)buf >> 8);
	mov	r6,(_i2c_write_PARM_3 + 1)
	mov	_I2C_BUFFER_XRAM_HIGH,r6
;	firmware.c:45: I2C_BUFFER_SIZE = req_len;
	mov	_I2C_BUFFER_SIZE,_i2c_write_PARM_2
;	firmware.c:46: I2C_ADDRESS = port;
	mov	_I2C_ADDRESS,r7
;	firmware.c:48: I2C_READ_WRITE = 0;  // Start write.
	mov	_I2C_READ_WRITE,#0x00
;	firmware.c:51: while ((status = I2C_STATUS) == 1) {
00104$:
	mov	r7,_I2C_STATUS
	mov	a,#0x01
	cjne	a,_I2C_STATUS,00106$
;	firmware.c:52: POWERSAVE = 1;  // Enter power save mode for a few milliseconds.
	mov	_POWERSAVE,#0x01
	sjmp	00104$
00106$:
;	firmware.c:55: return status;
	mov	dpl,r7
;	firmware.c:56: }
	ret
;------------------------------------------------------------
;Allocation info for local variables in function 'i2c_read'
;------------------------------------------------------------
;req_len                   Allocated with name '_i2c_read_PARM_2'
;buf                       Allocated with name '_i2c_read_PARM_3'
;port                      Allocated to registers r7 
;status                    Allocated to registers r7 
;------------------------------------------------------------
;	firmware.c:58: int8_t i2c_read(int8_t port, uint8_t req_len, __xdata uint8_t *buf) {
;	-----------------------------------------
;	 function i2c_read
;	-----------------------------------------
_i2c_read:
	mov	r7,dpl
;	firmware.c:59: while (I2C_STATUS == 1) {
00101$:
	mov	a,#0x01
	cjne	a,_I2C_STATUS,00103$
;	firmware.c:60: POWERSAVE = 1;  // Enter power save mode for a few milliseconds.
	mov	_POWERSAVE,#0x01
	sjmp	00101$
00103$:
;	firmware.c:63: I2C_BUFFER_XRAM_LOW = (uint8_t)(uint16_t)buf;
	mov	_I2C_BUFFER_XRAM_LOW,_i2c_read_PARM_3
;	firmware.c:64: I2C_BUFFER_XRAM_HIGH = (uint8_t)((uint16_t)buf >> 8);
	mov	r6,(_i2c_read_PARM_3 + 1)
	mov	_I2C_BUFFER_XRAM_HIGH,r6
;	firmware.c:65: I2C_BUFFER_SIZE = req_len;
	mov	_I2C_BUFFER_SIZE,_i2c_read_PARM_2
;	firmware.c:66: I2C_ADDRESS = port;
	mov	_I2C_ADDRESS,r7
;	firmware.c:68: I2C_READ_WRITE = 1;  // Start read.
	mov	_I2C_READ_WRITE,#0x01
;	firmware.c:71: while ((status = I2C_STATUS) == 1) {
00104$:
	mov	r7,_I2C_STATUS
	mov	a,#0x01
	cjne	a,_I2C_STATUS,00106$
;	firmware.c:72: POWERSAVE = 1;  // Enter power save mode for a few milliseconds.
	mov	_POWERSAVE,#0x01
	sjmp	00104$
00106$:
;	firmware.c:75: return status;
	mov	dpl,r7
;	firmware.c:76: }
	ret
;------------------------------------------------------------
;Allocation info for local variables in function 'i2c_status_to_error'
;------------------------------------------------------------
;err                       Allocated to registers r7 
;------------------------------------------------------------
;	firmware.c:78: const char *i2c_status_to_error(int8_t err) {
;	-----------------------------------------
;	 function i2c_status_to_error
;	-----------------------------------------
_i2c_status_to_error:
	mov	r7,dpl
;	firmware.c:79: switch (err) {
	cjne	r7,#0x00,00124$
	sjmp	00101$
00124$:
	cjne	r7,#0x01,00125$
	sjmp	00102$
00125$:
	cjne	r7,#0x02,00126$
	sjmp	00103$
00126$:
;	firmware.c:80: case 0: return "i2c status: transaction completed / ready\n";
	cjne	r7,#0x03,00105$
	sjmp	00104$
00101$:
	mov	dptr,#___str_0
	mov	b,#0x80
;	firmware.c:81: case 1: return "i2c status: busy\n";
	ret
00102$:
	mov	dptr,#___str_1
	mov	b,#0x80
;	firmware.c:82: case 2: return "i2c status: error - device not found\n";
	ret
00103$:
	mov	dptr,#___str_2
	mov	b,#0x80
;	firmware.c:83: case 3: return "i2c status: error - device misbehaved\n";
	ret
00104$:
	mov	dptr,#___str_3
	mov	b,#0x80
;	firmware.c:84: }
	ret
00105$:
;	firmware.c:86: return "i2c status: unknown error\n";
	mov	dptr,#___str_4
	mov	b,#0x80
;	firmware.c:87: }
	ret
;------------------------------------------------------------
;Allocation info for local variables in function 'serial_read_char'
;------------------------------------------------------------
;	firmware.c:90: char serial_read_char(void) {
;	-----------------------------------------
;	 function serial_read_char
;	-----------------------------------------
_serial_read_char:
;	firmware.c:91: while (1) {
00104$:
;	firmware.c:92: if (SERIAL_IN_READY) {
	mov	a,_SERIAL_IN_READY
	jz	00102$
;	firmware.c:93: return (char)SERIAL_IN_DATA;
	mov	dpl,_SERIAL_IN_DATA
	ret
00102$:
;	firmware.c:96: POWERSAVE = 1;
	mov	_POWERSAVE,#0x01
;	firmware.c:98: }
	sjmp	00104$
;------------------------------------------------------------
;Allocation info for local variables in function 'tokenizer_init'
;------------------------------------------------------------
;str                       Allocated with name '_tokenizer_init_PARM_2'
;t                         Allocated to registers r5 r6 r7 
;------------------------------------------------------------
;	firmware.c:105: void tokenizer_init(struct tokenizer_st *t, char *str) {
;	-----------------------------------------
;	 function tokenizer_init
;	-----------------------------------------
_tokenizer_init:
;	firmware.c:106: t->ptr = str;
	mov	r5,dpl
	mov	r6,dph
	mov	r7,b
	mov	a,_tokenizer_init_PARM_2
	lcall	__gptrput
	inc	dptr
	mov	a,(_tokenizer_init_PARM_2 + 1)
	lcall	__gptrput
	inc	dptr
	mov	a,(_tokenizer_init_PARM_2 + 2)
	lcall	__gptrput
;	firmware.c:107: t->replaced = 0x7fff;
	mov	a,#0x03
	add	a,r5
	mov	r5,a
	clr	a
	addc	a,r6
	mov	r6,a
	mov	dpl,r5
	mov	dph,r6
	mov	b,r7
	mov	a,#0xff
	lcall	__gptrput
	inc	dptr
	mov	a,#0x7f
;	firmware.c:108: }
	ljmp	__gptrput
;------------------------------------------------------------
;Allocation info for local variables in function 'tokenizer_next'
;------------------------------------------------------------
;t                         Allocated with name '_tokenizer_next_t_65536_24'
;token_start               Allocated with name '_tokenizer_next_token_start_65537_29'
;ch                        Allocated to registers r7 
;------------------------------------------------------------
;	firmware.c:110: char *tokenizer_next(struct tokenizer_st *t) {
;	-----------------------------------------
;	 function tokenizer_next
;	-----------------------------------------
_tokenizer_next:
	mov	_tokenizer_next_t_65536_24,dpl
	mov	(_tokenizer_next_t_65536_24 + 1),dph
	mov	(_tokenizer_next_t_65536_24 + 2),b
;	firmware.c:111: if (t->replaced != 0x7fff) {
	mov	a,#0x03
	add	a,_tokenizer_next_t_65536_24
	mov	r2,a
	clr	a
	addc	a,(_tokenizer_next_t_65536_24 + 1)
	mov	r3,a
	mov	r4,(_tokenizer_next_t_65536_24 + 2)
	mov	dpl,r2
	mov	dph,r3
	mov	b,r4
	lcall	__gptrget
	mov	r0,a
	inc	dptr
	lcall	__gptrget
	mov	r1,a
	cjne	r0,#0xff,00144$
	cjne	r1,#0x7f,00144$
	sjmp	00103$
00144$:
;	firmware.c:112: *t->ptr = (char)t->replaced;
	mov	dpl,_tokenizer_next_t_65536_24
	mov	dph,(_tokenizer_next_t_65536_24 + 1)
	mov	b,(_tokenizer_next_t_65536_24 + 2)
	lcall	__gptrget
	mov	r5,a
	inc	dptr
	lcall	__gptrget
	mov	r6,a
	inc	dptr
	lcall	__gptrget
	mov	r7,a
	mov	dpl,r5
	mov	dph,r6
	mov	b,r7
	mov	a,r0
	lcall	__gptrput
;	firmware.c:115: while (*t->ptr == ' ') {
00103$:
	mov	dpl,_tokenizer_next_t_65536_24
	mov	dph,(_tokenizer_next_t_65536_24 + 1)
	mov	b,(_tokenizer_next_t_65536_24 + 2)
	lcall	__gptrget
	mov	r5,a
	inc	dptr
	lcall	__gptrget
	mov	r6,a
	inc	dptr
	lcall	__gptrget
	mov	r7,a
	mov	dpl,r5
	mov	dph,r6
	mov	b,r7
	lcall	__gptrget
	mov	r5,a
	cjne	r5,#0x20,00105$
;	firmware.c:116: t->ptr++;
	mov	dpl,_tokenizer_next_t_65536_24
	mov	dph,(_tokenizer_next_t_65536_24 + 1)
	mov	b,(_tokenizer_next_t_65536_24 + 2)
	lcall	__gptrget
	mov	r5,a
	inc	dptr
	lcall	__gptrget
	mov	r6,a
	inc	dptr
	lcall	__gptrget
	mov	r7,a
	inc	r5
	cjne	r5,#0x00,00147$
	inc	r6
00147$:
	mov	dpl,_tokenizer_next_t_65536_24
	mov	dph,(_tokenizer_next_t_65536_24 + 1)
	mov	b,(_tokenizer_next_t_65536_24 + 2)
	mov	a,r5
	lcall	__gptrput
	inc	dptr
	mov	a,r6
	lcall	__gptrput
	inc	dptr
	mov	a,r7
	lcall	__gptrput
	sjmp	00103$
00105$:
;	firmware.c:119: if (*t->ptr == '\0') {
	mov	dpl,_tokenizer_next_t_65536_24
	mov	dph,(_tokenizer_next_t_65536_24 + 1)
	mov	b,(_tokenizer_next_t_65536_24 + 2)
	lcall	__gptrget
	mov	r5,a
	inc	dptr
	lcall	__gptrget
	mov	r6,a
	inc	dptr
	lcall	__gptrget
	mov	r7,a
	mov	dpl,r5
	mov	dph,r6
	mov	b,r7
	lcall	__gptrget
;	firmware.c:120: return NULL;
	jnz	00107$
	mov	dptr,#0x0000
	mov	b,a
	ret
00107$:
;	firmware.c:123: char *token_start = t->ptr;
	mov	dpl,_tokenizer_next_t_65536_24
	mov	dph,(_tokenizer_next_t_65536_24 + 1)
	mov	b,(_tokenizer_next_t_65536_24 + 2)
	lcall	__gptrget
	mov	_tokenizer_next_token_start_65537_29,a
	inc	dptr
	lcall	__gptrget
	mov	(_tokenizer_next_token_start_65537_29 + 1),a
	inc	dptr
	lcall	__gptrget
	mov	(_tokenizer_next_token_start_65537_29 + 2),a
00113$:
;	firmware.c:125: char ch = *t->ptr;
	mov	dpl,_tokenizer_next_t_65536_24
	mov	dph,(_tokenizer_next_t_65536_24 + 1)
	mov	b,(_tokenizer_next_t_65536_24 + 2)
	lcall	__gptrget
	mov	r0,a
	inc	dptr
	lcall	__gptrget
	mov	r1,a
	inc	dptr
	lcall	__gptrget
	mov	r7,a
	mov	dpl,r0
	mov	dph,r1
	mov	b,r7
	lcall	__gptrget
	mov	r7,a
;	firmware.c:126: if (ch != ' ' && ch != '\0') {
	cjne	r7,#0x20,00149$
	sjmp	00109$
00149$:
	mov	a,r7
	jz	00109$
;	firmware.c:127: t->ptr++;
	mov	dpl,_tokenizer_next_t_65536_24
	mov	dph,(_tokenizer_next_t_65536_24 + 1)
	mov	b,(_tokenizer_next_t_65536_24 + 2)
	lcall	__gptrget
	mov	r5,a
	inc	dptr
	lcall	__gptrget
	mov	r6,a
	inc	dptr
	lcall	__gptrget
	mov	r7,a
	inc	r5
	cjne	r5,#0x00,00151$
	inc	r6
00151$:
	mov	dpl,_tokenizer_next_t_65536_24
	mov	dph,(_tokenizer_next_t_65536_24 + 1)
	mov	b,(_tokenizer_next_t_65536_24 + 2)
	mov	a,r5
	lcall	__gptrput
	inc	dptr
	mov	a,r6
	lcall	__gptrput
	inc	dptr
	mov	a,r7
	lcall	__gptrput
;	firmware.c:128: continue;
	sjmp	00113$
00109$:
;	firmware.c:131: t->replaced = *t->ptr;
	mov	dpl,_tokenizer_next_t_65536_24
	mov	dph,(_tokenizer_next_t_65536_24 + 1)
	mov	b,(_tokenizer_next_t_65536_24 + 2)
	lcall	__gptrget
	mov	r5,a
	inc	dptr
	lcall	__gptrget
	mov	r6,a
	inc	dptr
	lcall	__gptrget
	mov	r7,a
	mov	dpl,r5
	mov	dph,r6
	mov	b,r7
	lcall	__gptrget
	mov	r5,a
	mov	r7,#0x00
	mov	dpl,r2
	mov	dph,r3
	mov	b,r4
	mov	a,r5
	lcall	__gptrput
	inc	dptr
	mov	a,r7
	lcall	__gptrput
;	firmware.c:132: *t->ptr = '\0';
	mov	dpl,_tokenizer_next_t_65536_24
	mov	dph,(_tokenizer_next_t_65536_24 + 1)
	mov	b,(_tokenizer_next_t_65536_24 + 2)
	lcall	__gptrget
	mov	r5,a
	inc	dptr
	lcall	__gptrget
	mov	r6,a
	inc	dptr
	lcall	__gptrget
	mov	r7,a
	mov	dpl,r5
	mov	dph,r6
	mov	b,r7
	clr	a
	lcall	__gptrput
;	firmware.c:133: return token_start;
	mov	dpl,_tokenizer_next_token_start_65537_29
	mov	dph,(_tokenizer_next_token_start_65537_29 + 1)
	mov	b,(_tokenizer_next_token_start_65537_29 + 2)
;	firmware.c:135: }
	ret
;------------------------------------------------------------
;Allocation info for local variables in function 'uint8_to_str'
;------------------------------------------------------------
;v                         Allocated with name '_uint8_to_str_PARM_2'
;buf                       Allocated to registers r5 r6 r7 
;sloc0                     Allocated with name '_uint8_to_str_sloc0_1_0'
;------------------------------------------------------------
;	firmware.c:138: void uint8_to_str(char *buf, uint8_t v) {
;	-----------------------------------------
;	 function uint8_to_str
;	-----------------------------------------
_uint8_to_str:
	mov	r5,dpl
	mov	r6,dph
	mov	r7,b
;	firmware.c:139: *buf++=table[(v&0xf0)>>4];
	mov	_uint8_to_str_sloc0_1_0,_uint8_to_str_PARM_2
	mov	(_uint8_to_str_sloc0_1_0 + 1),#0x00
	mov	a,#0xf0
	anl	a,_uint8_to_str_sloc0_1_0
	mov	r2,a
	clr	a
	xch	a,r2
	swap	a
	anl	a,#0x0f
	xrl	a,r2
	xch	a,r2
	anl	a,#0x0f
	xch	a,r2
	xrl	a,r2
	xch	a,r2
	jnb	acc.3,00103$
	orl	a,#0xf0
00103$:
	mov	a,r2
	add	a,#_table
	mov	r1,a
	mov	ar4,@r1
	mov	dpl,r5
	mov	dph,r6
	mov	b,r7
	mov	a,r4
	lcall	__gptrput
	inc	r5
	cjne	r5,#0x00,00104$
	inc	r6
00104$:
;	firmware.c:140: *buf++=table[v&0x0f];
	mov	a,#0x0f
	anl	a,_uint8_to_str_sloc0_1_0
	add	a,#_table
	mov	r1,a
	mov	ar4,@r1
	mov	dpl,r5
	mov	dph,r6
	mov	b,r7
	mov	a,r4
	lcall	__gptrput
	inc	r5
	cjne	r5,#0x00,00105$
	inc	r6
00105$:
;	firmware.c:141: *buf=0;
	mov	dpl,r5
	mov	dph,r6
	mov	b,r7
	clr	a
;	firmware.c:142: }
	ljmp	__gptrput
;------------------------------------------------------------
;Allocation info for local variables in function 'str_to_uint8'
;------------------------------------------------------------
;s                         Allocated to registers 
;v                         Allocated to registers r4 
;digit                     Allocated to registers r3 
;------------------------------------------------------------
;	firmware.c:144: uint8_t str_to_uint8(const char *s) {
;	-----------------------------------------
;	 function str_to_uint8
;	-----------------------------------------
_str_to_uint8:
	mov	r5,dpl
	mov	r6,dph
	mov	r7,b
;	firmware.c:145: uint8_t v = 0;
	mov	r4,#0x00
;	firmware.c:146: while (*s) {
00101$:
	mov	dpl,r5
	mov	dph,r6
	mov	b,r7
	lcall	__gptrget
	mov	r3,a
	jz	00103$
;	firmware.c:147: uint8_t digit = *s++ - '0';
	inc	r5
	cjne	r5,#0x00,00116$
	inc	r6
00116$:
	mov	a,r3
	add	a,#0xd0
	mov	r3,a
;	firmware.c:148: v = v * 10 + digit;
	mov	ar2,r4
	mov	a,r2
	mov	b,#0x0a
	mul	ab
	mov	r2,a
	add	a,r3
	mov	r4,a
	sjmp	00101$
00103$:
;	firmware.c:150: return v;
	mov	dpl,r4
;	firmware.c:151: }
	ret
;------------------------------------------------------------
;Allocation info for local variables in function 'port_to_int8'
;------------------------------------------------------------
;port                      Allocated to registers r5 r6 r7 
;------------------------------------------------------------
;	firmware.c:153: int8_t port_to_int8(char *port) {
;	-----------------------------------------
;	 function port_to_int8
;	-----------------------------------------
_port_to_int8:
	mov	r5,dpl
	mov	r6,dph
	mov	r7,b
;	firmware.c:154: if (port[1]!=0&&port[1]!=' ') {
	mov	a,#0x01
	add	a,r5
	mov	r2,a
	clr	a
	addc	a,r6
	mov	r3,a
	mov	ar4,r7
	mov	dpl,r2
	mov	dph,r3
	mov	b,r4
	lcall	__gptrget
	mov	r4,a
	jz	00102$
	cjne	r4,#0x20,00115$
	sjmp	00102$
00115$:
;	firmware.c:156: return -1;
	mov	dpl,#0xff
	ret
00102$:
;	firmware.c:158: return (int8_t)str_to_uint8(port);
	mov	dpl,r5
	mov	dph,r6
	mov	b,r7
;	firmware.c:159: }
	ljmp	_str_to_uint8
;------------------------------------------------------------
;Allocation info for local variables in function 'main'
;------------------------------------------------------------
;i                         Allocated to registers r6 r7 
;ch                        Allocated to registers r3 
;t                         Allocated with name '_main_t_131075_50'
;p                         Allocated to registers r3 r5 r6 
;write                     Allocated to registers r4 
;port                      Allocated to registers r7 
;req_len                   Allocated to registers r6 
;i                         Allocated to registers r5 
;ret                       Allocated to registers r5 
;ret                       Allocated to registers r7 
;i                         Allocated to registers r7 
;num                       Allocated with name '_main_num_327687_70'
;cmd                       Allocated with name '_main_cmd_65537_43'
;i2c_buf                   Allocated with name '_main_i2c_buf_65537_43'
;i2c_buf2                  Allocated with name '_main_i2c_buf2_65537_43'
;------------------------------------------------------------
;	firmware.c:163: int main(void) {
;	-----------------------------------------
;	 function main
;	-----------------------------------------
_main:
;	firmware.c:164: serial_print("INIT OK\n");
	mov	dptr,#___str_5
	mov	b,#0x80
	lcall	_serial_print
;	firmware.c:169: while (true) {
00137$:
;	firmware.c:170: serial_print("> ");
	mov	dptr,#___str_6
	mov	b,#0x80
	lcall	_serial_print
;	firmware.c:173: for (i = 0; i < CMD_BUF_SZ; i++) {
	mov	r6,#0x00
	mov	r7,#0x00
	mov	r4,#0x00
	mov	r5,#0x00
00139$:
;	firmware.c:174: char ch = serial_read_char();
	push	ar7
	push	ar6
	push	ar5
	push	ar4
	lcall	_serial_read_char
	mov	r3,dpl
	pop	ar4
	pop	ar5
	pop	ar6
	pop	ar7
;	firmware.c:175: if (ch == '\n') {
	cjne	r3,#0x0a,00102$
;	firmware.c:176: cmd[i] = '\0';
	mov	a,r6
	add	a,#_main_cmd_65537_43
	mov	dpl,a
	mov	a,r7
	addc	a,#(_main_cmd_65537_43 >> 8)
	mov	dph,a
	clr	a
	movx	@dptr,a
;	firmware.c:177: break;
	sjmp	00103$
00102$:
;	firmware.c:179: cmd[i] = ch;
	mov	a,r4
	add	a,#_main_cmd_65537_43
	mov	dpl,a
	mov	a,r5
	addc	a,#(_main_cmd_65537_43 >> 8)
	mov	dph,a
	mov	a,r3
	movx	@dptr,a
;	firmware.c:173: for (i = 0; i < CMD_BUF_SZ; i++) {
	inc	r4
	cjne	r4,#0x00,00253$
	inc	r5
00253$:
	mov	ar6,r4
	mov	ar7,r5
	clr	c
	mov	a,r4
	subb	a,#0x80
	mov	a,r5
	xrl	a,#0x80
	subb	a,#0x81
	jc	00139$
00103$:
;	firmware.c:182: if (i == CMD_BUF_SZ) {
	cjne	r6,#0x80,00105$
	cjne	r7,#0x01,00105$
;	firmware.c:183: serial_print("-err: command too long, rejected\n");
	mov	dptr,#___str_7
	mov	b,#0x80
	lcall	_serial_print
;	firmware.c:184: continue;
	sjmp	00137$
00105$:
;	firmware.c:188: tokenizer_init(&t, cmd);
	mov	_tokenizer_init_PARM_2,#_main_cmd_65537_43
	mov	(_tokenizer_init_PARM_2 + 1),#(_main_cmd_65537_43 >> 8)
	mov	(_tokenizer_init_PARM_2 + 2),#0x00
	mov	dptr,#_main_t_131075_50
	mov	b,#0x40
	lcall	_tokenizer_init
;	firmware.c:190: char *p = tokenizer_next(&t);
	mov	dptr,#_main_t_131075_50
	mov	b,#0x40
	lcall	_tokenizer_next
	mov	r5,dpl
	mov	r6,dph
	mov	r7,b
;	firmware.c:191: if (p == NULL) {
	mov	a,r5
	orl	a,r6
	jnz	00107$
;	firmware.c:192: serial_print("-err: command format incorrect\n");
	mov	dptr,#___str_8
	mov	b,#0x80
	lcall	_serial_print
;	firmware.c:193: continue;
	ljmp	00137$
00107$:
;	firmware.c:197: if (*p == 'r') {
	mov	dpl,r5
	mov	dph,r6
	mov	b,r7
	lcall	__gptrget
	mov	r4,a
	cjne	r4,#0x72,00112$
;	firmware.c:198: write = false;
	mov	r4,#0x00
	sjmp	00113$
00112$:
;	firmware.c:199: } else if (*p == 'w') {
	mov	dpl,r5
	mov	dph,r6
	mov	b,r7
	lcall	__gptrget
	mov	r5,a
	cjne	r5,#0x77,00109$
;	firmware.c:200: write = true;
	mov	r4,#0x01
	sjmp	00113$
00109$:
;	firmware.c:202: serial_print("-err: unknown command\n");
	mov	dptr,#___str_9
	mov	b,#0x80
	lcall	_serial_print
;	firmware.c:203: continue;
	ljmp	00137$
00113$:
;	firmware.c:206: p = tokenizer_next(&t);
	mov	dptr,#_main_t_131075_50
	mov	b,#0x40
	push	ar4
	lcall	_tokenizer_next
	mov	r5,dpl
	mov	r6,dph
	mov	r7,b
	pop	ar4
;	firmware.c:207: if (p == NULL) {
	mov	a,r5
	orl	a,r6
	jnz	00115$
;	firmware.c:208: serial_print("-err: command format incorrect\n");
	mov	dptr,#___str_8
	mov	b,#0x80
	lcall	_serial_print
;	firmware.c:209: continue;
	ljmp	00137$
00115$:
;	firmware.c:212: int8_t port = port_to_int8(p);
	mov	dpl,r5
	mov	dph,r6
	mov	b,r7
	push	ar4
	lcall	_port_to_int8
	mov	r7,dpl
	pop	ar4
;	firmware.c:213: if (port == -1) {
	cjne	r7,#0xff,00117$
;	firmware.c:214: serial_print("-err: port invalid or not allowed\n");
	mov	dptr,#___str_10
	mov	b,#0x80
	lcall	_serial_print
;	firmware.c:215: continue;
	ljmp	00137$
00117$:
;	firmware.c:218: p = tokenizer_next(&t);
	mov	dptr,#_main_t_131075_50
	mov	b,#0x40
	push	ar7
	push	ar4
	lcall	_tokenizer_next
	mov	r3,dpl
	mov	r5,dph
	mov	r6,b
	pop	ar4
	pop	ar7
;	firmware.c:219: if (p == NULL) {
	mov	a,r3
	orl	a,r5
	jnz	00119$
;	firmware.c:220: serial_print("-err: command format incorrect\n");
	mov	dptr,#___str_8
	mov	b,#0x80
	lcall	_serial_print
;	firmware.c:221: continue;
	ljmp	00137$
00119$:
;	firmware.c:224: uint8_t req_len = str_to_uint8(p);
	mov	dpl,r3
	mov	dph,r5
	mov	b,r6
	push	ar7
	push	ar4
	lcall	_str_to_uint8
	mov	r6,dpl
	pop	ar4
	pop	ar7
;	firmware.c:225: if (req_len == 0 || req_len > I2C_BUF_SZ) {
	mov	a,r6
	jz	00120$
	mov	a,r6
	add	a,#0xff - 0x80
	jnc	00121$
00120$:
;	firmware.c:226: serial_print("-err: I2C request length incorrect\n");
	mov	dptr,#___str_11
	mov	b,#0x80
	lcall	_serial_print
;	firmware.c:227: continue;
	ljmp	00137$
00121$:
;	firmware.c:230: if (write) {
	mov	a,r4
	jnz	00268$
	ljmp	00134$
00268$:
;	firmware.c:231: for (uint8_t i = 0; i < req_len; i++) {
	mov	r5,#0x00
00142$:
	clr	c
	mov	a,r5
	subb	a,r6
	jnc	00125$
;	firmware.c:232: p = tokenizer_next(&t);
	mov	dptr,#_main_t_131075_50
	mov	b,#0x40
	push	ar7
	push	ar6
	push	ar5
	lcall	_tokenizer_next
	mov	r2,dpl
	mov	r3,dph
	mov	r4,b
	pop	ar5
	pop	ar6
	pop	ar7
;	firmware.c:233: if (p == NULL) {
	mov	a,r2
	orl	a,r3
	jz	00125$
;	firmware.c:237: i2c_buf[i] = str_to_uint8(p);
	mov	a,r5
	add	a,#_main_i2c_buf_65537_43
	mov	r0,a
	clr	a
	addc	a,#(_main_i2c_buf_65537_43 >> 8)
	mov	r1,a
	mov	dpl,r2
	mov	dph,r3
	mov	b,r4
	push	ar7
	push	ar6
	push	ar5
	push	ar1
	push	ar0
	lcall	_str_to_uint8
	mov	r4,dpl
	pop	ar0
	pop	ar1
	pop	ar5
	mov	dpl,r0
	mov	dph,r1
	mov	a,r4
	movx	@dptr,a
;	firmware.c:238: i2c_buf2[i] = rand();
	mov	a,r5
	add	a,#_main_i2c_buf2_65537_43
	mov	r3,a
	clr	a
	addc	a,#(_main_i2c_buf2_65537_43 >> 8)
	mov	r4,a
	push	ar5
	push	ar4
	push	ar3
	lcall	_rand
	mov	r2,dpl
	pop	ar3
	pop	ar4
	pop	ar5
	pop	ar6
	pop	ar7
	mov	dpl,r3
	mov	dph,r4
	mov	a,r2
	movx	@dptr,a
;	firmware.c:231: for (uint8_t i = 0; i < req_len; i++) {
	inc	r5
	sjmp	00142$
00125$:
;	firmware.c:241: int8_t ret = i2c_write(port, req_len, i2c_buf);
	mov	_i2c_write_PARM_2,r6
	mov	_i2c_write_PARM_3,#_main_i2c_buf_65537_43
	mov	(_i2c_write_PARM_3 + 1),#(_main_i2c_buf_65537_43 >> 8)
	mov	dpl,r7
	push	ar7
	push	ar6
	lcall	_i2c_write
	mov	r5,dpl
	pop	ar6
	pop	ar7
;	firmware.c:242: i2c_write((port+1)%10,req_len,i2c_buf2);
	mov	a,r7
	mov	r3,a
	rlc	a
	subb	a,acc
	mov	r4,a
	mov	dpl,r3
	mov	dph,r4
	inc	dptr
	mov	__modsint_PARM_2,#0x0a
	mov	(__modsint_PARM_2 + 1),#0x00
	push	ar6
	push	ar5
	push	ar4
	push	ar3
	lcall	__modsint
	mov	r1,dpl
	pop	ar3
	pop	ar4
	pop	ar5
	pop	ar6
	mov	dpl,r1
	mov	_i2c_write_PARM_2,r6
	mov	_i2c_write_PARM_3,#_main_i2c_buf2_65537_43
	mov	(_i2c_write_PARM_3 + 1),#(_main_i2c_buf2_65537_43 >> 8)
	push	ar6
	push	ar5
	push	ar4
	push	ar3
	lcall	_i2c_write
	pop	ar3
	pop	ar4
;	firmware.c:243: i2c_write((port+9)%10,req_len,i2c_buf2);
	mov	a,#0x09
	add	a,r3
	mov	dpl,a
	clr	a
	addc	a,r4
	mov	dph,a
	mov	__modsint_PARM_2,#0x0a
	mov	(__modsint_PARM_2 + 1),#0x00
	lcall	__modsint
	mov	r3,dpl
	pop	ar5
	pop	ar6
	mov	_i2c_write_PARM_3,#_main_i2c_buf2_65537_43
	mov	(_i2c_write_PARM_3 + 1),#(_main_i2c_buf2_65537_43 >> 8)
	mov	_i2c_write_PARM_2,r6
	mov	dpl,r3
	push	ar5
	lcall	_i2c_write
	pop	ar5
;	firmware.c:244: serial_print(i2c_status_to_error(ret));
	mov	dpl,r5
	lcall	_i2c_status_to_error
	lcall	_serial_print
	ljmp	00137$
00134$:
;	firmware.c:246: int8_t ret = i2c_read(port, req_len, i2c_buf);
	mov	_i2c_read_PARM_3,#_main_i2c_buf_65537_43
	mov	(_i2c_read_PARM_3 + 1),#(_main_i2c_buf_65537_43 >> 8)
	mov	_i2c_read_PARM_2,r6
	mov	dpl,r7
	push	ar6
	lcall	_i2c_read
	mov	r7,dpl
	pop	ar6
;	firmware.c:247: serial_print(i2c_status_to_error(ret));
	mov	dpl,r7
	push	ar7
	push	ar6
	lcall	_i2c_status_to_error
	lcall	_serial_print
	pop	ar6
	pop	ar7
;	firmware.c:248: if(ret!=2)
	cjne	r7,#0x02,00271$
	ljmp	00132$
00271$:
;	firmware.c:249: for (uint8_t i = 0; i < req_len; i++) {
	mov	r7,#0x00
00145$:
	clr	c
	mov	a,r7
	subb	a,r6
	jc	00272$
	ljmp	00132$
00272$:
;	firmware.c:251: uint8_to_str(num, i2c_buf[i]);
	mov	a,r7
	add	a,#_main_i2c_buf_65537_43
	mov	dpl,a
	clr	a
	addc	a,#(_main_i2c_buf_65537_43 >> 8)
	mov	dph,a
	movx	a,@dptr
	mov	_uint8_to_str_PARM_2,a
	mov	dptr,#_main_num_327687_70
	mov	b,#0x40
	push	ar7
	push	ar6
	lcall	_uint8_to_str
;	firmware.c:252: serial_print(num);
	mov	dptr,#_main_num_327687_70
	mov	b,#0x40
	lcall	_serial_print
	pop	ar6
	pop	ar7
;	firmware.c:254: if ((i + 1) % 16 == 0 && i +1 != req_len) {
	mov	ar4,r7
	mov	r5,#0x00
	mov	dpl,r4
	mov	dph,r5
	inc	dptr
	mov	__modsint_PARM_2,#0x10
;	1-genFromRTrack replaced	mov	(__modsint_PARM_2 + 1),#0x00
	mov	(__modsint_PARM_2 + 1),r5
	push	ar7
	push	ar6
	push	ar5
	push	ar4
	lcall	__modsint
	mov	a,dpl
	mov	b,dph
	pop	ar4
	pop	ar5
	pop	ar6
	pop	ar7
	orl	a,b
	jnz	00127$
	inc	r4
	cjne	r4,#0x00,00274$
	inc	r5
00274$:
	mov	ar2,r6
	mov	r3,#0x00
	mov	a,r4
	cjne	a,ar2,00275$
	mov	a,r5
	cjne	a,ar3,00275$
	sjmp	00127$
00275$:
;	firmware.c:255: serial_print("\n");
	mov	dptr,#___str_12
	mov	b,#0x80
	push	ar7
	push	ar6
	lcall	_serial_print
	pop	ar6
	pop	ar7
	sjmp	00146$
00127$:
;	firmware.c:257: serial_print(" ");
	mov	dptr,#___str_13
	mov	b,#0x80
	push	ar7
	push	ar6
	lcall	_serial_print
	pop	ar6
	pop	ar7
00146$:
;	firmware.c:249: for (uint8_t i = 0; i < req_len; i++) {
	inc	r7
	ljmp	00145$
00132$:
;	firmware.c:261: serial_print("\n-end\n");
	mov	dptr,#___str_14
	mov	b,#0x80
	lcall	_serial_print
;	firmware.c:266: }
	ljmp	00137$
	.area CSEG    (CODE)
	.area CONST   (CODE)
___str_0:
	.ascii "i2c status: transaction completed / ready"
	.db 0x0a
	.db 0x00
___str_1:
	.ascii "i2c status: busy"
	.db 0x0a
	.db 0x00
___str_2:
	.ascii "i2c status: error - device not found"
	.db 0x0a
	.db 0x00
___str_3:
	.ascii "i2c status: error - device misbehaved"
	.db 0x0a
	.db 0x00
___str_4:
	.ascii "i2c status: unknown error"
	.db 0x0a
	.db 0x00
___str_5:
	.ascii "INIT OK"
	.db 0x0a
	.db 0x00
___str_6:
	.ascii "> "
	.db 0x00
___str_7:
	.ascii "-err: command too long, rejected"
	.db 0x0a
	.db 0x00
___str_8:
	.ascii "-err: command format incorrect"
	.db 0x0a
	.db 0x00
___str_9:
	.ascii "-err: unknown command"
	.db 0x0a
	.db 0x00
___str_10:
	.ascii "-err: port invalid or not allowed"
	.db 0x0a
	.db 0x00
___str_11:
	.ascii "-err: I2C request length incorrect"
	.db 0x0a
	.db 0x00
___str_12:
	.db 0x0a
	.db 0x00
___str_13:
	.ascii " "
	.db 0x00
___str_14:
	.db 0x0a
	.ascii "-end"
	.db 0x0a
	.db 0x00
	.area XINIT   (CODE)
	.area CABS    (ABS,CODE)
