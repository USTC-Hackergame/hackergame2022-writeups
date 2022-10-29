                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ANSI-C Compiler
                                      3 ; Version 3.8.0 #10562 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module firmware
                                      6 	.optsdcc -mmcs51 --model-small
                                      7 	
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _uint8_to_str_PARM_2
                                     12 	.globl _tokenizer_init_PARM_2
                                     13 	.globl _i2c_read_PARM_3
                                     14 	.globl _i2c_read_PARM_2
                                     15 	.globl _i2c_write_PARM_3
                                     16 	.globl _i2c_write_PARM_2
                                     17 	.globl _main
                                     18 	.globl _port_to_int8
                                     19 	.globl _str_to_uint8
                                     20 	.globl _uint8_to_str
                                     21 	.globl _tokenizer_next
                                     22 	.globl _tokenizer_init
                                     23 	.globl _serial_read_char
                                     24 	.globl _i2c_status_to_error
                                     25 	.globl _i2c_read
                                     26 	.globl _i2c_write
                                     27 	.globl _serial_print
                                     28 	.globl _rand
                                     29 	.globl _POWERSAVE
                                     30 	.globl _POWEROFF
                                     31 	.globl _I2C_READ_WRITE
                                     32 	.globl _I2C_ADDRESS
                                     33 	.globl _I2C_BUFFER_SIZE
                                     34 	.globl _I2C_BUFFER_XRAM_HIGH
                                     35 	.globl _I2C_BUFFER_XRAM_LOW
                                     36 	.globl _I2C_STATUS
                                     37 	.globl _SERIAL_IN_READY
                                     38 	.globl _SERIAL_IN_DATA
                                     39 	.globl _SERIAL_OUT_READY
                                     40 	.globl _SERIAL_OUT_DATA
                                     41 	.globl _table
                                     42 	.globl _speedtb
                                     43 	.globl _init_rand
                                     44 ;--------------------------------------------------------
                                     45 ; special function registers
                                     46 ;--------------------------------------------------------
                                     47 	.area RSEG    (ABS,DATA)
      000000                         48 	.org 0x0000
                           0000F2    49 _SERIAL_OUT_DATA	=	0x00f2
                           0000F3    50 _SERIAL_OUT_READY	=	0x00f3
                           0000FA    51 _SERIAL_IN_DATA	=	0x00fa
                           0000FB    52 _SERIAL_IN_READY	=	0x00fb
                           0000E1    53 _I2C_STATUS	=	0x00e1
                           0000E2    54 _I2C_BUFFER_XRAM_LOW	=	0x00e2
                           0000E3    55 _I2C_BUFFER_XRAM_HIGH	=	0x00e3
                           0000E4    56 _I2C_BUFFER_SIZE	=	0x00e4
                           0000E6    57 _I2C_ADDRESS	=	0x00e6
                           0000E7    58 _I2C_READ_WRITE	=	0x00e7
                           0000FF    59 _POWEROFF	=	0x00ff
                           0000FE    60 _POWERSAVE	=	0x00fe
                                     61 ;--------------------------------------------------------
                                     62 ; special function bits
                                     63 ;--------------------------------------------------------
                                     64 	.area RSEG    (ABS,DATA)
      000000                         65 	.org 0x0000
                                     66 ;--------------------------------------------------------
                                     67 ; overlayable register banks
                                     68 ;--------------------------------------------------------
                                     69 	.area REG_BANK_0	(REL,OVR,DATA)
      000000                         70 	.ds 8
                                     71 ;--------------------------------------------------------
                                     72 ; internal ram data
                                     73 ;--------------------------------------------------------
                                     74 	.area DSEG    (DATA)
      000008                         75 _init_rand::
      000008                         76 	.ds 1
      000009                         77 _speedtb::
      000009                         78 	.ds 8
      000011                         79 _table::
      000011                         80 	.ds 20
      000025                         81 _main_t_131075_50:
      000025                         82 	.ds 5
      00002A                         83 _main_num_327687_70:
      00002A                         84 	.ds 4
                                     85 ;--------------------------------------------------------
                                     86 ; overlayable items in internal ram 
                                     87 ;--------------------------------------------------------
                                     88 	.area	OSEG    (OVR,DATA)
                                     89 	.area	OSEG    (OVR,DATA)
      00002E                         90 _i2c_write_PARM_2:
      00002E                         91 	.ds 1
      00002F                         92 _i2c_write_PARM_3:
      00002F                         93 	.ds 2
                                     94 	.area	OSEG    (OVR,DATA)
      00002E                         95 _i2c_read_PARM_2:
      00002E                         96 	.ds 1
      00002F                         97 _i2c_read_PARM_3:
      00002F                         98 	.ds 2
                                     99 	.area	OSEG    (OVR,DATA)
                                    100 	.area	OSEG    (OVR,DATA)
      00002E                        101 _tokenizer_init_PARM_2:
      00002E                        102 	.ds 3
                                    103 	.area	OSEG    (OVR,DATA)
      00002E                        104 _tokenizer_next_t_65536_24:
      00002E                        105 	.ds 3
      000031                        106 _tokenizer_next_token_start_65537_29:
      000031                        107 	.ds 3
                                    108 	.area	OSEG    (OVR,DATA)
      00002E                        109 _uint8_to_str_PARM_2:
      00002E                        110 	.ds 1
      00002F                        111 _uint8_to_str_sloc0_1_0:
      00002F                        112 	.ds 2
                                    113 	.area	OSEG    (OVR,DATA)
                                    114 ;--------------------------------------------------------
                                    115 ; Stack segment in internal ram 
                                    116 ;--------------------------------------------------------
                                    117 	.area	SSEG
      000034                        118 __start__stack:
      000034                        119 	.ds	1
                                    120 
                                    121 ;--------------------------------------------------------
                                    122 ; indirectly addressable internal ram data
                                    123 ;--------------------------------------------------------
                                    124 	.area ISEG    (DATA)
                                    125 ;--------------------------------------------------------
                                    126 ; absolute internal ram data
                                    127 ;--------------------------------------------------------
                                    128 	.area IABS    (ABS,DATA)
                                    129 	.area IABS    (ABS,DATA)
                                    130 ;--------------------------------------------------------
                                    131 ; bit data
                                    132 ;--------------------------------------------------------
                                    133 	.area BSEG    (BIT)
                                    134 ;--------------------------------------------------------
                                    135 ; paged external ram data
                                    136 ;--------------------------------------------------------
                                    137 	.area PSEG    (PAG,XDATA)
                                    138 ;--------------------------------------------------------
                                    139 ; external ram data
                                    140 ;--------------------------------------------------------
                                    141 	.area XSEG    (XDATA)
      000001                        142 _main_cmd_65537_43:
      000001                        143 	.ds 384
      000181                        144 _main_i2c_buf_65537_43:
      000181                        145 	.ds 128
      000201                        146 _main_i2c_buf2_65537_43:
      000201                        147 	.ds 128
                                    148 ;--------------------------------------------------------
                                    149 ; absolute external ram data
                                    150 ;--------------------------------------------------------
                                    151 	.area XABS    (ABS,XDATA)
                                    152 ;--------------------------------------------------------
                                    153 ; external initialized ram data
                                    154 ;--------------------------------------------------------
                                    155 	.area XISEG   (XDATA)
                                    156 	.area HOME    (CODE)
                                    157 	.area GSINIT0 (CODE)
                                    158 	.area GSINIT1 (CODE)
                                    159 	.area GSINIT2 (CODE)
                                    160 	.area GSINIT3 (CODE)
                                    161 	.area GSINIT4 (CODE)
                                    162 	.area GSINIT5 (CODE)
                                    163 	.area GSINIT  (CODE)
                                    164 	.area GSFINAL (CODE)
                                    165 	.area CSEG    (CODE)
                                    166 ;--------------------------------------------------------
                                    167 ; interrupt vector 
                                    168 ;--------------------------------------------------------
                                    169 	.area HOME    (CODE)
      000000                        170 __interrupt_vect:
      000000 02 00 06         [24]  171 	ljmp	__sdcc_gsinit_startup
                                    172 ;--------------------------------------------------------
                                    173 ; global & static initialisations
                                    174 ;--------------------------------------------------------
                                    175 	.area HOME    (CODE)
                                    176 	.area GSINIT  (CODE)
                                    177 	.area GSFINAL (CODE)
                                    178 	.area GSINIT  (CODE)
                                    179 	.globl __sdcc_gsinit_startup
                                    180 	.globl __sdcc_program_startup
                                    181 	.globl __start__stack
                                    182 	.globl __mcs51_genXINIT
                                    183 	.globl __mcs51_genXRAMCLEAR
                                    184 	.globl __mcs51_genRAMCLEAR
                                    185 ;	firmware.c:23: int8_t init_rand=7;
      00005F 75 08 07         [24]  186 	mov	_init_rand,#0x07
                                    187 ;	firmware.c:24: int8_t speedtb[8]={0x11,0x45,0x14,0x19,0x81,0x24,0x00,0x19};
      000062 75 09 11         [24]  188 	mov	_speedtb,#0x11
      000065 75 0A 45         [24]  189 	mov	(_speedtb + 0x0001),#0x45
      000068 75 0B 14         [24]  190 	mov	(_speedtb + 0x0002),#0x14
      00006B 75 0C 19         [24]  191 	mov	(_speedtb + 0x0003),#0x19
      00006E 75 0D 81         [24]  192 	mov	(_speedtb + 0x0004),#0x81
      000071 75 0E 24         [24]  193 	mov	(_speedtb + 0x0005),#0x24
      000074 75 0F 00         [24]  194 	mov	(_speedtb + 0x0006),#0x00
      000077 75 10 19         [24]  195 	mov	(_speedtb + 0x0007),#0x19
                                    196 ;	firmware.c:137: uint8_t table[20]="0123456789ABCDEF";
      00007A 75 11 30         [24]  197 	mov	_table,#0x30
      00007D 75 12 31         [24]  198 	mov	(_table + 0x0001),#0x31
      000080 75 13 32         [24]  199 	mov	(_table + 0x0002),#0x32
      000083 75 14 33         [24]  200 	mov	(_table + 0x0003),#0x33
      000086 75 15 34         [24]  201 	mov	(_table + 0x0004),#0x34
      000089 75 16 35         [24]  202 	mov	(_table + 0x0005),#0x35
      00008C 75 17 36         [24]  203 	mov	(_table + 0x0006),#0x36
      00008F 75 18 37         [24]  204 	mov	(_table + 0x0007),#0x37
      000092 75 19 38         [24]  205 	mov	(_table + 0x0008),#0x38
      000095 75 1A 39         [24]  206 	mov	(_table + 0x0009),#0x39
      000098 75 1B 41         [24]  207 	mov	(_table + 0x000a),#0x41
      00009B 75 1C 42         [24]  208 	mov	(_table + 0x000b),#0x42
      00009E 75 1D 43         [24]  209 	mov	(_table + 0x000c),#0x43
      0000A1 75 1E 44         [24]  210 	mov	(_table + 0x000d),#0x44
      0000A4 75 1F 45         [24]  211 	mov	(_table + 0x000e),#0x45
      0000A7 75 20 46         [24]  212 	mov	(_table + 0x000f),#0x46
      0000AA 75 21 00         [24]  213 	mov	(_table + 0x0010),#0x00
      0000AD 75 22 00         [24]  214 	mov	(_table + 0x0011),#0x00
      0000B0 75 23 00         [24]  215 	mov	(_table + 0x0012),#0x00
      0000B3 75 24 00         [24]  216 	mov	(_table + 0x0013),#0x00
                                    217 	.area GSFINAL (CODE)
      0000B6 02 00 03         [24]  218 	ljmp	__sdcc_program_startup
                                    219 ;--------------------------------------------------------
                                    220 ; Home
                                    221 ;--------------------------------------------------------
                                    222 	.area HOME    (CODE)
                                    223 	.area HOME    (CODE)
      000003                        224 __sdcc_program_startup:
      000003 02 04 0B         [24]  225 	ljmp	_main
                                    226 ;	return from main will return to caller
                                    227 ;--------------------------------------------------------
                                    228 ; code
                                    229 ;--------------------------------------------------------
                                    230 	.area CSEG    (CODE)
                                    231 ;------------------------------------------------------------
                                    232 ;Allocation info for local variables in function 'rand'
                                    233 ;------------------------------------------------------------
                                    234 ;	firmware.c:25: int8_t rand(){
                                    235 ;	-----------------------------------------
                                    236 ;	 function rand
                                    237 ;	-----------------------------------------
      0000B9                        238 _rand:
                           000007   239 	ar7 = 0x07
                           000006   240 	ar6 = 0x06
                           000005   241 	ar5 = 0x05
                           000004   242 	ar4 = 0x04
                           000003   243 	ar3 = 0x03
                           000002   244 	ar2 = 0x02
                           000001   245 	ar1 = 0x01
                           000000   246 	ar0 = 0x00
                                    247 ;	firmware.c:26: init_rand+=1;
      0000B9 05 08            [12]  248 	inc	_init_rand
                                    249 ;	firmware.c:27: init_rand&=7;
      0000BB 53 08 07         [24]  250 	anl	_init_rand,#0x07
                                    251 ;	firmware.c:28: return speedtb[init_rand];
      0000BE E5 08            [12]  252 	mov	a,_init_rand
      0000C0 24 09            [12]  253 	add	a,#_speedtb
      0000C2 F9               [12]  254 	mov	r1,a
      0000C3 87 82            [24]  255 	mov	dpl,@r1
                                    256 ;	firmware.c:29: }
      0000C5 22               [24]  257 	ret
                                    258 ;------------------------------------------------------------
                                    259 ;Allocation info for local variables in function 'serial_print'
                                    260 ;------------------------------------------------------------
                                    261 ;s                         Allocated to registers 
                                    262 ;------------------------------------------------------------
                                    263 ;	firmware.c:31: void serial_print(const char *s) {
                                    264 ;	-----------------------------------------
                                    265 ;	 function serial_print
                                    266 ;	-----------------------------------------
      0000C6                        267 _serial_print:
      0000C6 AD 82            [24]  268 	mov	r5,dpl
      0000C8 AE 83            [24]  269 	mov	r6,dph
      0000CA AF F0            [24]  270 	mov	r7,b
                                    271 ;	firmware.c:32: while (*s) {
      0000CC                        272 00104$:
      0000CC 8D 82            [24]  273 	mov	dpl,r5
      0000CE 8E 83            [24]  274 	mov	dph,r6
      0000D0 8F F0            [24]  275 	mov	b,r7
      0000D2 12 07 A2         [24]  276 	lcall	__gptrget
      0000D5 60 16            [24]  277 	jz	00107$
                                    278 ;	firmware.c:33: while (!SERIAL_OUT_READY);
      0000D7                        279 00101$:
      0000D7 E5 F3            [12]  280 	mov	a,_SERIAL_OUT_READY
      0000D9 60 FC            [24]  281 	jz	00101$
                                    282 ;	firmware.c:34: SERIAL_OUT_DATA = *s++;
      0000DB 8D 82            [24]  283 	mov	dpl,r5
      0000DD 8E 83            [24]  284 	mov	dph,r6
      0000DF 8F F0            [24]  285 	mov	b,r7
      0000E1 12 07 A2         [24]  286 	lcall	__gptrget
      0000E4 F5 F2            [12]  287 	mov	_SERIAL_OUT_DATA,a
      0000E6 A3               [24]  288 	inc	dptr
      0000E7 AD 82            [24]  289 	mov	r5,dpl
      0000E9 AE 83            [24]  290 	mov	r6,dph
      0000EB 80 DF            [24]  291 	sjmp	00104$
      0000ED                        292 00107$:
                                    293 ;	firmware.c:36: }
      0000ED 22               [24]  294 	ret
                                    295 ;------------------------------------------------------------
                                    296 ;Allocation info for local variables in function 'i2c_write'
                                    297 ;------------------------------------------------------------
                                    298 ;req_len                   Allocated with name '_i2c_write_PARM_2'
                                    299 ;buf                       Allocated with name '_i2c_write_PARM_3'
                                    300 ;port                      Allocated to registers r7 
                                    301 ;status                    Allocated to registers r7 
                                    302 ;------------------------------------------------------------
                                    303 ;	firmware.c:38: int8_t i2c_write(int8_t port, uint8_t req_len, __xdata uint8_t *buf) {
                                    304 ;	-----------------------------------------
                                    305 ;	 function i2c_write
                                    306 ;	-----------------------------------------
      0000EE                        307 _i2c_write:
      0000EE AF 82            [24]  308 	mov	r7,dpl
                                    309 ;	firmware.c:39: while (I2C_STATUS == 1) {
      0000F0                        310 00101$:
      0000F0 74 01            [12]  311 	mov	a,#0x01
      0000F2 B5 E1 05         [24]  312 	cjne	a,_I2C_STATUS,00103$
                                    313 ;	firmware.c:40: POWERSAVE = 1;  // Enter power save mode for a few milliseconds.
      0000F5 75 FE 01         [24]  314 	mov	_POWERSAVE,#0x01
      0000F8 80 F6            [24]  315 	sjmp	00101$
      0000FA                        316 00103$:
                                    317 ;	firmware.c:43: I2C_BUFFER_XRAM_LOW = (uint8_t)(uint16_t)buf;
      0000FA 85 2F E2         [24]  318 	mov	_I2C_BUFFER_XRAM_LOW,_i2c_write_PARM_3
                                    319 ;	firmware.c:44: I2C_BUFFER_XRAM_HIGH = (uint8_t)((uint16_t)buf >> 8);
      0000FD AE 30            [24]  320 	mov	r6,(_i2c_write_PARM_3 + 1)
      0000FF 8E E3            [24]  321 	mov	_I2C_BUFFER_XRAM_HIGH,r6
                                    322 ;	firmware.c:45: I2C_BUFFER_SIZE = req_len;
      000101 85 2E E4         [24]  323 	mov	_I2C_BUFFER_SIZE,_i2c_write_PARM_2
                                    324 ;	firmware.c:46: I2C_ADDRESS = port;
      000104 8F E6            [24]  325 	mov	_I2C_ADDRESS,r7
                                    326 ;	firmware.c:48: I2C_READ_WRITE = 0;  // Start write.
      000106 75 E7 00         [24]  327 	mov	_I2C_READ_WRITE,#0x00
                                    328 ;	firmware.c:51: while ((status = I2C_STATUS) == 1) {
      000109                        329 00104$:
      000109 AF E1            [24]  330 	mov	r7,_I2C_STATUS
      00010B 74 01            [12]  331 	mov	a,#0x01
      00010D B5 E1 05         [24]  332 	cjne	a,_I2C_STATUS,00106$
                                    333 ;	firmware.c:52: POWERSAVE = 1;  // Enter power save mode for a few milliseconds.
      000110 75 FE 01         [24]  334 	mov	_POWERSAVE,#0x01
      000113 80 F4            [24]  335 	sjmp	00104$
      000115                        336 00106$:
                                    337 ;	firmware.c:55: return status;
      000115 8F 82            [24]  338 	mov	dpl,r7
                                    339 ;	firmware.c:56: }
      000117 22               [24]  340 	ret
                                    341 ;------------------------------------------------------------
                                    342 ;Allocation info for local variables in function 'i2c_read'
                                    343 ;------------------------------------------------------------
                                    344 ;req_len                   Allocated with name '_i2c_read_PARM_2'
                                    345 ;buf                       Allocated with name '_i2c_read_PARM_3'
                                    346 ;port                      Allocated to registers r7 
                                    347 ;status                    Allocated to registers r7 
                                    348 ;------------------------------------------------------------
                                    349 ;	firmware.c:58: int8_t i2c_read(int8_t port, uint8_t req_len, __xdata uint8_t *buf) {
                                    350 ;	-----------------------------------------
                                    351 ;	 function i2c_read
                                    352 ;	-----------------------------------------
      000118                        353 _i2c_read:
      000118 AF 82            [24]  354 	mov	r7,dpl
                                    355 ;	firmware.c:59: while (I2C_STATUS == 1) {
      00011A                        356 00101$:
      00011A 74 01            [12]  357 	mov	a,#0x01
      00011C B5 E1 05         [24]  358 	cjne	a,_I2C_STATUS,00103$
                                    359 ;	firmware.c:60: POWERSAVE = 1;  // Enter power save mode for a few milliseconds.
      00011F 75 FE 01         [24]  360 	mov	_POWERSAVE,#0x01
      000122 80 F6            [24]  361 	sjmp	00101$
      000124                        362 00103$:
                                    363 ;	firmware.c:63: I2C_BUFFER_XRAM_LOW = (uint8_t)(uint16_t)buf;
      000124 85 2F E2         [24]  364 	mov	_I2C_BUFFER_XRAM_LOW,_i2c_read_PARM_3
                                    365 ;	firmware.c:64: I2C_BUFFER_XRAM_HIGH = (uint8_t)((uint16_t)buf >> 8);
      000127 AE 30            [24]  366 	mov	r6,(_i2c_read_PARM_3 + 1)
      000129 8E E3            [24]  367 	mov	_I2C_BUFFER_XRAM_HIGH,r6
                                    368 ;	firmware.c:65: I2C_BUFFER_SIZE = req_len;
      00012B 85 2E E4         [24]  369 	mov	_I2C_BUFFER_SIZE,_i2c_read_PARM_2
                                    370 ;	firmware.c:66: I2C_ADDRESS = port;
      00012E 8F E6            [24]  371 	mov	_I2C_ADDRESS,r7
                                    372 ;	firmware.c:68: I2C_READ_WRITE = 1;  // Start read.
      000130 75 E7 01         [24]  373 	mov	_I2C_READ_WRITE,#0x01
                                    374 ;	firmware.c:71: while ((status = I2C_STATUS) == 1) {
      000133                        375 00104$:
      000133 AF E1            [24]  376 	mov	r7,_I2C_STATUS
      000135 74 01            [12]  377 	mov	a,#0x01
      000137 B5 E1 05         [24]  378 	cjne	a,_I2C_STATUS,00106$
                                    379 ;	firmware.c:72: POWERSAVE = 1;  // Enter power save mode for a few milliseconds.
      00013A 75 FE 01         [24]  380 	mov	_POWERSAVE,#0x01
      00013D 80 F4            [24]  381 	sjmp	00104$
      00013F                        382 00106$:
                                    383 ;	firmware.c:75: return status;
      00013F 8F 82            [24]  384 	mov	dpl,r7
                                    385 ;	firmware.c:76: }
      000141 22               [24]  386 	ret
                                    387 ;------------------------------------------------------------
                                    388 ;Allocation info for local variables in function 'i2c_status_to_error'
                                    389 ;------------------------------------------------------------
                                    390 ;err                       Allocated to registers r7 
                                    391 ;------------------------------------------------------------
                                    392 ;	firmware.c:78: const char *i2c_status_to_error(int8_t err) {
                                    393 ;	-----------------------------------------
                                    394 ;	 function i2c_status_to_error
                                    395 ;	-----------------------------------------
      000142                        396 _i2c_status_to_error:
      000142 AF 82            [24]  397 	mov	r7,dpl
                                    398 ;	firmware.c:79: switch (err) {
      000144 BF 00 02         [24]  399 	cjne	r7,#0x00,00124$
      000147 80 0F            [24]  400 	sjmp	00101$
      000149                        401 00124$:
      000149 BF 01 02         [24]  402 	cjne	r7,#0x01,00125$
      00014C 80 11            [24]  403 	sjmp	00102$
      00014E                        404 00125$:
      00014E BF 02 02         [24]  405 	cjne	r7,#0x02,00126$
      000151 80 13            [24]  406 	sjmp	00103$
      000153                        407 00126$:
                                    408 ;	firmware.c:80: case 0: return "i2c status: transaction completed / ready\n";
      000153 BF 03 1E         [24]  409 	cjne	r7,#0x03,00105$
      000156 80 15            [24]  410 	sjmp	00104$
      000158                        411 00101$:
      000158 90 07 F8         [24]  412 	mov	dptr,#___str_0
      00015B 75 F0 80         [24]  413 	mov	b,#0x80
                                    414 ;	firmware.c:81: case 1: return "i2c status: busy\n";
      00015E 22               [24]  415 	ret
      00015F                        416 00102$:
      00015F 90 08 23         [24]  417 	mov	dptr,#___str_1
      000162 75 F0 80         [24]  418 	mov	b,#0x80
                                    419 ;	firmware.c:82: case 2: return "i2c status: error - device not found\n";
      000165 22               [24]  420 	ret
      000166                        421 00103$:
      000166 90 08 35         [24]  422 	mov	dptr,#___str_2
      000169 75 F0 80         [24]  423 	mov	b,#0x80
                                    424 ;	firmware.c:83: case 3: return "i2c status: error - device misbehaved\n";
      00016C 22               [24]  425 	ret
      00016D                        426 00104$:
      00016D 90 08 5B         [24]  427 	mov	dptr,#___str_3
      000170 75 F0 80         [24]  428 	mov	b,#0x80
                                    429 ;	firmware.c:84: }
      000173 22               [24]  430 	ret
      000174                        431 00105$:
                                    432 ;	firmware.c:86: return "i2c status: unknown error\n";
      000174 90 08 82         [24]  433 	mov	dptr,#___str_4
      000177 75 F0 80         [24]  434 	mov	b,#0x80
                                    435 ;	firmware.c:87: }
      00017A 22               [24]  436 	ret
                                    437 ;------------------------------------------------------------
                                    438 ;Allocation info for local variables in function 'serial_read_char'
                                    439 ;------------------------------------------------------------
                                    440 ;	firmware.c:90: char serial_read_char(void) {
                                    441 ;	-----------------------------------------
                                    442 ;	 function serial_read_char
                                    443 ;	-----------------------------------------
      00017B                        444 _serial_read_char:
                                    445 ;	firmware.c:91: while (1) {
      00017B                        446 00104$:
                                    447 ;	firmware.c:92: if (SERIAL_IN_READY) {
      00017B E5 FB            [12]  448 	mov	a,_SERIAL_IN_READY
      00017D 60 04            [24]  449 	jz	00102$
                                    450 ;	firmware.c:93: return (char)SERIAL_IN_DATA;
      00017F 85 FA 82         [24]  451 	mov	dpl,_SERIAL_IN_DATA
      000182 22               [24]  452 	ret
      000183                        453 00102$:
                                    454 ;	firmware.c:96: POWERSAVE = 1;
      000183 75 FE 01         [24]  455 	mov	_POWERSAVE,#0x01
                                    456 ;	firmware.c:98: }
      000186 80 F3            [24]  457 	sjmp	00104$
                                    458 ;------------------------------------------------------------
                                    459 ;Allocation info for local variables in function 'tokenizer_init'
                                    460 ;------------------------------------------------------------
                                    461 ;str                       Allocated with name '_tokenizer_init_PARM_2'
                                    462 ;t                         Allocated to registers r5 r6 r7 
                                    463 ;------------------------------------------------------------
                                    464 ;	firmware.c:105: void tokenizer_init(struct tokenizer_st *t, char *str) {
                                    465 ;	-----------------------------------------
                                    466 ;	 function tokenizer_init
                                    467 ;	-----------------------------------------
      000188                        468 _tokenizer_init:
                                    469 ;	firmware.c:106: t->ptr = str;
      000188 AD 82            [24]  470 	mov	r5,dpl
      00018A AE 83            [24]  471 	mov	r6,dph
      00018C AF F0            [24]  472 	mov	r7,b
      00018E E5 2E            [12]  473 	mov	a,_tokenizer_init_PARM_2
      000190 12 07 3A         [24]  474 	lcall	__gptrput
      000193 A3               [24]  475 	inc	dptr
      000194 E5 2F            [12]  476 	mov	a,(_tokenizer_init_PARM_2 + 1)
      000196 12 07 3A         [24]  477 	lcall	__gptrput
      000199 A3               [24]  478 	inc	dptr
      00019A E5 30            [12]  479 	mov	a,(_tokenizer_init_PARM_2 + 2)
      00019C 12 07 3A         [24]  480 	lcall	__gptrput
                                    481 ;	firmware.c:107: t->replaced = 0x7fff;
      00019F 74 03            [12]  482 	mov	a,#0x03
      0001A1 2D               [12]  483 	add	a,r5
      0001A2 FD               [12]  484 	mov	r5,a
      0001A3 E4               [12]  485 	clr	a
      0001A4 3E               [12]  486 	addc	a,r6
      0001A5 FE               [12]  487 	mov	r6,a
      0001A6 8D 82            [24]  488 	mov	dpl,r5
      0001A8 8E 83            [24]  489 	mov	dph,r6
      0001AA 8F F0            [24]  490 	mov	b,r7
      0001AC 74 FF            [12]  491 	mov	a,#0xff
      0001AE 12 07 3A         [24]  492 	lcall	__gptrput
      0001B1 A3               [24]  493 	inc	dptr
      0001B2 74 7F            [12]  494 	mov	a,#0x7f
                                    495 ;	firmware.c:108: }
      0001B4 02 07 3A         [24]  496 	ljmp	__gptrput
                                    497 ;------------------------------------------------------------
                                    498 ;Allocation info for local variables in function 'tokenizer_next'
                                    499 ;------------------------------------------------------------
                                    500 ;t                         Allocated with name '_tokenizer_next_t_65536_24'
                                    501 ;token_start               Allocated with name '_tokenizer_next_token_start_65537_29'
                                    502 ;ch                        Allocated to registers r7 
                                    503 ;------------------------------------------------------------
                                    504 ;	firmware.c:110: char *tokenizer_next(struct tokenizer_st *t) {
                                    505 ;	-----------------------------------------
                                    506 ;	 function tokenizer_next
                                    507 ;	-----------------------------------------
      0001B7                        508 _tokenizer_next:
      0001B7 85 82 2E         [24]  509 	mov	_tokenizer_next_t_65536_24,dpl
      0001BA 85 83 2F         [24]  510 	mov	(_tokenizer_next_t_65536_24 + 1),dph
      0001BD 85 F0 30         [24]  511 	mov	(_tokenizer_next_t_65536_24 + 2),b
                                    512 ;	firmware.c:111: if (t->replaced != 0x7fff) {
      0001C0 74 03            [12]  513 	mov	a,#0x03
      0001C2 25 2E            [12]  514 	add	a,_tokenizer_next_t_65536_24
      0001C4 FA               [12]  515 	mov	r2,a
      0001C5 E4               [12]  516 	clr	a
      0001C6 35 2F            [12]  517 	addc	a,(_tokenizer_next_t_65536_24 + 1)
      0001C8 FB               [12]  518 	mov	r3,a
      0001C9 AC 30            [24]  519 	mov	r4,(_tokenizer_next_t_65536_24 + 2)
      0001CB 8A 82            [24]  520 	mov	dpl,r2
      0001CD 8B 83            [24]  521 	mov	dph,r3
      0001CF 8C F0            [24]  522 	mov	b,r4
      0001D1 12 07 A2         [24]  523 	lcall	__gptrget
      0001D4 F8               [12]  524 	mov	r0,a
      0001D5 A3               [24]  525 	inc	dptr
      0001D6 12 07 A2         [24]  526 	lcall	__gptrget
      0001D9 F9               [12]  527 	mov	r1,a
      0001DA B8 FF 05         [24]  528 	cjne	r0,#0xff,00144$
      0001DD B9 7F 02         [24]  529 	cjne	r1,#0x7f,00144$
      0001E0 80 21            [24]  530 	sjmp	00103$
      0001E2                        531 00144$:
                                    532 ;	firmware.c:112: *t->ptr = (char)t->replaced;
      0001E2 85 2E 82         [24]  533 	mov	dpl,_tokenizer_next_t_65536_24
      0001E5 85 2F 83         [24]  534 	mov	dph,(_tokenizer_next_t_65536_24 + 1)
      0001E8 85 30 F0         [24]  535 	mov	b,(_tokenizer_next_t_65536_24 + 2)
      0001EB 12 07 A2         [24]  536 	lcall	__gptrget
      0001EE FD               [12]  537 	mov	r5,a
      0001EF A3               [24]  538 	inc	dptr
      0001F0 12 07 A2         [24]  539 	lcall	__gptrget
      0001F3 FE               [12]  540 	mov	r6,a
      0001F4 A3               [24]  541 	inc	dptr
      0001F5 12 07 A2         [24]  542 	lcall	__gptrget
      0001F8 FF               [12]  543 	mov	r7,a
      0001F9 8D 82            [24]  544 	mov	dpl,r5
      0001FB 8E 83            [24]  545 	mov	dph,r6
      0001FD 8F F0            [24]  546 	mov	b,r7
      0001FF E8               [12]  547 	mov	a,r0
      000200 12 07 3A         [24]  548 	lcall	__gptrput
                                    549 ;	firmware.c:115: while (*t->ptr == ' ') {
      000203                        550 00103$:
      000203 85 2E 82         [24]  551 	mov	dpl,_tokenizer_next_t_65536_24
      000206 85 2F 83         [24]  552 	mov	dph,(_tokenizer_next_t_65536_24 + 1)
      000209 85 30 F0         [24]  553 	mov	b,(_tokenizer_next_t_65536_24 + 2)
      00020C 12 07 A2         [24]  554 	lcall	__gptrget
      00020F FD               [12]  555 	mov	r5,a
      000210 A3               [24]  556 	inc	dptr
      000211 12 07 A2         [24]  557 	lcall	__gptrget
      000214 FE               [12]  558 	mov	r6,a
      000215 A3               [24]  559 	inc	dptr
      000216 12 07 A2         [24]  560 	lcall	__gptrget
      000219 FF               [12]  561 	mov	r7,a
      00021A 8D 82            [24]  562 	mov	dpl,r5
      00021C 8E 83            [24]  563 	mov	dph,r6
      00021E 8F F0            [24]  564 	mov	b,r7
      000220 12 07 A2         [24]  565 	lcall	__gptrget
      000223 FD               [12]  566 	mov	r5,a
      000224 BD 20 35         [24]  567 	cjne	r5,#0x20,00105$
                                    568 ;	firmware.c:116: t->ptr++;
      000227 85 2E 82         [24]  569 	mov	dpl,_tokenizer_next_t_65536_24
      00022A 85 2F 83         [24]  570 	mov	dph,(_tokenizer_next_t_65536_24 + 1)
      00022D 85 30 F0         [24]  571 	mov	b,(_tokenizer_next_t_65536_24 + 2)
      000230 12 07 A2         [24]  572 	lcall	__gptrget
      000233 FD               [12]  573 	mov	r5,a
      000234 A3               [24]  574 	inc	dptr
      000235 12 07 A2         [24]  575 	lcall	__gptrget
      000238 FE               [12]  576 	mov	r6,a
      000239 A3               [24]  577 	inc	dptr
      00023A 12 07 A2         [24]  578 	lcall	__gptrget
      00023D FF               [12]  579 	mov	r7,a
      00023E 0D               [12]  580 	inc	r5
      00023F BD 00 01         [24]  581 	cjne	r5,#0x00,00147$
      000242 0E               [12]  582 	inc	r6
      000243                        583 00147$:
      000243 85 2E 82         [24]  584 	mov	dpl,_tokenizer_next_t_65536_24
      000246 85 2F 83         [24]  585 	mov	dph,(_tokenizer_next_t_65536_24 + 1)
      000249 85 30 F0         [24]  586 	mov	b,(_tokenizer_next_t_65536_24 + 2)
      00024C ED               [12]  587 	mov	a,r5
      00024D 12 07 3A         [24]  588 	lcall	__gptrput
      000250 A3               [24]  589 	inc	dptr
      000251 EE               [12]  590 	mov	a,r6
      000252 12 07 3A         [24]  591 	lcall	__gptrput
      000255 A3               [24]  592 	inc	dptr
      000256 EF               [12]  593 	mov	a,r7
      000257 12 07 3A         [24]  594 	lcall	__gptrput
      00025A 80 A7            [24]  595 	sjmp	00103$
      00025C                        596 00105$:
                                    597 ;	firmware.c:119: if (*t->ptr == '\0') {
      00025C 85 2E 82         [24]  598 	mov	dpl,_tokenizer_next_t_65536_24
      00025F 85 2F 83         [24]  599 	mov	dph,(_tokenizer_next_t_65536_24 + 1)
      000262 85 30 F0         [24]  600 	mov	b,(_tokenizer_next_t_65536_24 + 2)
      000265 12 07 A2         [24]  601 	lcall	__gptrget
      000268 FD               [12]  602 	mov	r5,a
      000269 A3               [24]  603 	inc	dptr
      00026A 12 07 A2         [24]  604 	lcall	__gptrget
      00026D FE               [12]  605 	mov	r6,a
      00026E A3               [24]  606 	inc	dptr
      00026F 12 07 A2         [24]  607 	lcall	__gptrget
      000272 FF               [12]  608 	mov	r7,a
      000273 8D 82            [24]  609 	mov	dpl,r5
      000275 8E 83            [24]  610 	mov	dph,r6
      000277 8F F0            [24]  611 	mov	b,r7
      000279 12 07 A2         [24]  612 	lcall	__gptrget
                                    613 ;	firmware.c:120: return NULL;
      00027C 70 06            [24]  614 	jnz	00107$
      00027E 90 00 00         [24]  615 	mov	dptr,#0x0000
      000281 F5 F0            [12]  616 	mov	b,a
      000283 22               [24]  617 	ret
      000284                        618 00107$:
                                    619 ;	firmware.c:123: char *token_start = t->ptr;
      000284 85 2E 82         [24]  620 	mov	dpl,_tokenizer_next_t_65536_24
      000287 85 2F 83         [24]  621 	mov	dph,(_tokenizer_next_t_65536_24 + 1)
      00028A 85 30 F0         [24]  622 	mov	b,(_tokenizer_next_t_65536_24 + 2)
      00028D 12 07 A2         [24]  623 	lcall	__gptrget
      000290 F5 31            [12]  624 	mov	_tokenizer_next_token_start_65537_29,a
      000292 A3               [24]  625 	inc	dptr
      000293 12 07 A2         [24]  626 	lcall	__gptrget
      000296 F5 32            [12]  627 	mov	(_tokenizer_next_token_start_65537_29 + 1),a
      000298 A3               [24]  628 	inc	dptr
      000299 12 07 A2         [24]  629 	lcall	__gptrget
      00029C F5 33            [12]  630 	mov	(_tokenizer_next_token_start_65537_29 + 2),a
      00029E                        631 00113$:
                                    632 ;	firmware.c:125: char ch = *t->ptr;
      00029E 85 2E 82         [24]  633 	mov	dpl,_tokenizer_next_t_65536_24
      0002A1 85 2F 83         [24]  634 	mov	dph,(_tokenizer_next_t_65536_24 + 1)
      0002A4 85 30 F0         [24]  635 	mov	b,(_tokenizer_next_t_65536_24 + 2)
      0002A7 12 07 A2         [24]  636 	lcall	__gptrget
      0002AA F8               [12]  637 	mov	r0,a
      0002AB A3               [24]  638 	inc	dptr
      0002AC 12 07 A2         [24]  639 	lcall	__gptrget
      0002AF F9               [12]  640 	mov	r1,a
      0002B0 A3               [24]  641 	inc	dptr
      0002B1 12 07 A2         [24]  642 	lcall	__gptrget
      0002B4 FF               [12]  643 	mov	r7,a
      0002B5 88 82            [24]  644 	mov	dpl,r0
      0002B7 89 83            [24]  645 	mov	dph,r1
      0002B9 8F F0            [24]  646 	mov	b,r7
      0002BB 12 07 A2         [24]  647 	lcall	__gptrget
      0002BE FF               [12]  648 	mov	r7,a
                                    649 ;	firmware.c:126: if (ch != ' ' && ch != '\0') {
      0002BF BF 20 02         [24]  650 	cjne	r7,#0x20,00149$
      0002C2 80 38            [24]  651 	sjmp	00109$
      0002C4                        652 00149$:
      0002C4 EF               [12]  653 	mov	a,r7
      0002C5 60 35            [24]  654 	jz	00109$
                                    655 ;	firmware.c:127: t->ptr++;
      0002C7 85 2E 82         [24]  656 	mov	dpl,_tokenizer_next_t_65536_24
      0002CA 85 2F 83         [24]  657 	mov	dph,(_tokenizer_next_t_65536_24 + 1)
      0002CD 85 30 F0         [24]  658 	mov	b,(_tokenizer_next_t_65536_24 + 2)
      0002D0 12 07 A2         [24]  659 	lcall	__gptrget
      0002D3 FD               [12]  660 	mov	r5,a
      0002D4 A3               [24]  661 	inc	dptr
      0002D5 12 07 A2         [24]  662 	lcall	__gptrget
      0002D8 FE               [12]  663 	mov	r6,a
      0002D9 A3               [24]  664 	inc	dptr
      0002DA 12 07 A2         [24]  665 	lcall	__gptrget
      0002DD FF               [12]  666 	mov	r7,a
      0002DE 0D               [12]  667 	inc	r5
      0002DF BD 00 01         [24]  668 	cjne	r5,#0x00,00151$
      0002E2 0E               [12]  669 	inc	r6
      0002E3                        670 00151$:
      0002E3 85 2E 82         [24]  671 	mov	dpl,_tokenizer_next_t_65536_24
      0002E6 85 2F 83         [24]  672 	mov	dph,(_tokenizer_next_t_65536_24 + 1)
      0002E9 85 30 F0         [24]  673 	mov	b,(_tokenizer_next_t_65536_24 + 2)
      0002EC ED               [12]  674 	mov	a,r5
      0002ED 12 07 3A         [24]  675 	lcall	__gptrput
      0002F0 A3               [24]  676 	inc	dptr
      0002F1 EE               [12]  677 	mov	a,r6
      0002F2 12 07 3A         [24]  678 	lcall	__gptrput
      0002F5 A3               [24]  679 	inc	dptr
      0002F6 EF               [12]  680 	mov	a,r7
      0002F7 12 07 3A         [24]  681 	lcall	__gptrput
                                    682 ;	firmware.c:128: continue;
      0002FA 80 A2            [24]  683 	sjmp	00113$
      0002FC                        684 00109$:
                                    685 ;	firmware.c:131: t->replaced = *t->ptr;
      0002FC 85 2E 82         [24]  686 	mov	dpl,_tokenizer_next_t_65536_24
      0002FF 85 2F 83         [24]  687 	mov	dph,(_tokenizer_next_t_65536_24 + 1)
      000302 85 30 F0         [24]  688 	mov	b,(_tokenizer_next_t_65536_24 + 2)
      000305 12 07 A2         [24]  689 	lcall	__gptrget
      000308 FD               [12]  690 	mov	r5,a
      000309 A3               [24]  691 	inc	dptr
      00030A 12 07 A2         [24]  692 	lcall	__gptrget
      00030D FE               [12]  693 	mov	r6,a
      00030E A3               [24]  694 	inc	dptr
      00030F 12 07 A2         [24]  695 	lcall	__gptrget
      000312 FF               [12]  696 	mov	r7,a
      000313 8D 82            [24]  697 	mov	dpl,r5
      000315 8E 83            [24]  698 	mov	dph,r6
      000317 8F F0            [24]  699 	mov	b,r7
      000319 12 07 A2         [24]  700 	lcall	__gptrget
      00031C FD               [12]  701 	mov	r5,a
      00031D 7F 00            [12]  702 	mov	r7,#0x00
      00031F 8A 82            [24]  703 	mov	dpl,r2
      000321 8B 83            [24]  704 	mov	dph,r3
      000323 8C F0            [24]  705 	mov	b,r4
      000325 ED               [12]  706 	mov	a,r5
      000326 12 07 3A         [24]  707 	lcall	__gptrput
      000329 A3               [24]  708 	inc	dptr
      00032A EF               [12]  709 	mov	a,r7
      00032B 12 07 3A         [24]  710 	lcall	__gptrput
                                    711 ;	firmware.c:132: *t->ptr = '\0';
      00032E 85 2E 82         [24]  712 	mov	dpl,_tokenizer_next_t_65536_24
      000331 85 2F 83         [24]  713 	mov	dph,(_tokenizer_next_t_65536_24 + 1)
      000334 85 30 F0         [24]  714 	mov	b,(_tokenizer_next_t_65536_24 + 2)
      000337 12 07 A2         [24]  715 	lcall	__gptrget
      00033A FD               [12]  716 	mov	r5,a
      00033B A3               [24]  717 	inc	dptr
      00033C 12 07 A2         [24]  718 	lcall	__gptrget
      00033F FE               [12]  719 	mov	r6,a
      000340 A3               [24]  720 	inc	dptr
      000341 12 07 A2         [24]  721 	lcall	__gptrget
      000344 FF               [12]  722 	mov	r7,a
      000345 8D 82            [24]  723 	mov	dpl,r5
      000347 8E 83            [24]  724 	mov	dph,r6
      000349 8F F0            [24]  725 	mov	b,r7
      00034B E4               [12]  726 	clr	a
      00034C 12 07 3A         [24]  727 	lcall	__gptrput
                                    728 ;	firmware.c:133: return token_start;
      00034F 85 31 82         [24]  729 	mov	dpl,_tokenizer_next_token_start_65537_29
      000352 85 32 83         [24]  730 	mov	dph,(_tokenizer_next_token_start_65537_29 + 1)
      000355 85 33 F0         [24]  731 	mov	b,(_tokenizer_next_token_start_65537_29 + 2)
                                    732 ;	firmware.c:135: }
      000358 22               [24]  733 	ret
                                    734 ;------------------------------------------------------------
                                    735 ;Allocation info for local variables in function 'uint8_to_str'
                                    736 ;------------------------------------------------------------
                                    737 ;v                         Allocated with name '_uint8_to_str_PARM_2'
                                    738 ;buf                       Allocated to registers r5 r6 r7 
                                    739 ;sloc0                     Allocated with name '_uint8_to_str_sloc0_1_0'
                                    740 ;------------------------------------------------------------
                                    741 ;	firmware.c:138: void uint8_to_str(char *buf, uint8_t v) {
                                    742 ;	-----------------------------------------
                                    743 ;	 function uint8_to_str
                                    744 ;	-----------------------------------------
      000359                        745 _uint8_to_str:
      000359 AD 82            [24]  746 	mov	r5,dpl
      00035B AE 83            [24]  747 	mov	r6,dph
      00035D AF F0            [24]  748 	mov	r7,b
                                    749 ;	firmware.c:139: *buf++=table[(v&0xf0)>>4];
      00035F 85 2E 2F         [24]  750 	mov	_uint8_to_str_sloc0_1_0,_uint8_to_str_PARM_2
      000362 75 30 00         [24]  751 	mov	(_uint8_to_str_sloc0_1_0 + 1),#0x00
      000365 74 F0            [12]  752 	mov	a,#0xf0
      000367 55 2F            [12]  753 	anl	a,_uint8_to_str_sloc0_1_0
      000369 FA               [12]  754 	mov	r2,a
      00036A E4               [12]  755 	clr	a
      00036B CA               [12]  756 	xch	a,r2
      00036C C4               [12]  757 	swap	a
      00036D 54 0F            [12]  758 	anl	a,#0x0f
      00036F 6A               [12]  759 	xrl	a,r2
      000370 CA               [12]  760 	xch	a,r2
      000371 54 0F            [12]  761 	anl	a,#0x0f
      000373 CA               [12]  762 	xch	a,r2
      000374 6A               [12]  763 	xrl	a,r2
      000375 CA               [12]  764 	xch	a,r2
      000376 30 E3 02         [24]  765 	jnb	acc.3,00103$
      000379 44 F0            [12]  766 	orl	a,#0xf0
      00037B                        767 00103$:
      00037B EA               [12]  768 	mov	a,r2
      00037C 24 11            [12]  769 	add	a,#_table
      00037E F9               [12]  770 	mov	r1,a
      00037F 87 04            [24]  771 	mov	ar4,@r1
      000381 8D 82            [24]  772 	mov	dpl,r5
      000383 8E 83            [24]  773 	mov	dph,r6
      000385 8F F0            [24]  774 	mov	b,r7
      000387 EC               [12]  775 	mov	a,r4
      000388 12 07 3A         [24]  776 	lcall	__gptrput
      00038B 0D               [12]  777 	inc	r5
      00038C BD 00 01         [24]  778 	cjne	r5,#0x00,00104$
      00038F 0E               [12]  779 	inc	r6
      000390                        780 00104$:
                                    781 ;	firmware.c:140: *buf++=table[v&0x0f];
      000390 74 0F            [12]  782 	mov	a,#0x0f
      000392 55 2F            [12]  783 	anl	a,_uint8_to_str_sloc0_1_0
      000394 24 11            [12]  784 	add	a,#_table
      000396 F9               [12]  785 	mov	r1,a
      000397 87 04            [24]  786 	mov	ar4,@r1
      000399 8D 82            [24]  787 	mov	dpl,r5
      00039B 8E 83            [24]  788 	mov	dph,r6
      00039D 8F F0            [24]  789 	mov	b,r7
      00039F EC               [12]  790 	mov	a,r4
      0003A0 12 07 3A         [24]  791 	lcall	__gptrput
      0003A3 0D               [12]  792 	inc	r5
      0003A4 BD 00 01         [24]  793 	cjne	r5,#0x00,00105$
      0003A7 0E               [12]  794 	inc	r6
      0003A8                        795 00105$:
                                    796 ;	firmware.c:141: *buf=0;
      0003A8 8D 82            [24]  797 	mov	dpl,r5
      0003AA 8E 83            [24]  798 	mov	dph,r6
      0003AC 8F F0            [24]  799 	mov	b,r7
      0003AE E4               [12]  800 	clr	a
                                    801 ;	firmware.c:142: }
      0003AF 02 07 3A         [24]  802 	ljmp	__gptrput
                                    803 ;------------------------------------------------------------
                                    804 ;Allocation info for local variables in function 'str_to_uint8'
                                    805 ;------------------------------------------------------------
                                    806 ;s                         Allocated to registers 
                                    807 ;v                         Allocated to registers r4 
                                    808 ;digit                     Allocated to registers r3 
                                    809 ;------------------------------------------------------------
                                    810 ;	firmware.c:144: uint8_t str_to_uint8(const char *s) {
                                    811 ;	-----------------------------------------
                                    812 ;	 function str_to_uint8
                                    813 ;	-----------------------------------------
      0003B2                        814 _str_to_uint8:
      0003B2 AD 82            [24]  815 	mov	r5,dpl
      0003B4 AE 83            [24]  816 	mov	r6,dph
      0003B6 AF F0            [24]  817 	mov	r7,b
                                    818 ;	firmware.c:145: uint8_t v = 0;
      0003B8 7C 00            [12]  819 	mov	r4,#0x00
                                    820 ;	firmware.c:146: while (*s) {
      0003BA                        821 00101$:
      0003BA 8D 82            [24]  822 	mov	dpl,r5
      0003BC 8E 83            [24]  823 	mov	dph,r6
      0003BE 8F F0            [24]  824 	mov	b,r7
      0003C0 12 07 A2         [24]  825 	lcall	__gptrget
      0003C3 FB               [12]  826 	mov	r3,a
      0003C4 60 15            [24]  827 	jz	00103$
                                    828 ;	firmware.c:147: uint8_t digit = *s++ - '0';
      0003C6 0D               [12]  829 	inc	r5
      0003C7 BD 00 01         [24]  830 	cjne	r5,#0x00,00116$
      0003CA 0E               [12]  831 	inc	r6
      0003CB                        832 00116$:
      0003CB EB               [12]  833 	mov	a,r3
      0003CC 24 D0            [12]  834 	add	a,#0xd0
      0003CE FB               [12]  835 	mov	r3,a
                                    836 ;	firmware.c:148: v = v * 10 + digit;
      0003CF 8C 02            [24]  837 	mov	ar2,r4
      0003D1 EA               [12]  838 	mov	a,r2
      0003D2 75 F0 0A         [24]  839 	mov	b,#0x0a
      0003D5 A4               [48]  840 	mul	ab
      0003D6 FA               [12]  841 	mov	r2,a
      0003D7 2B               [12]  842 	add	a,r3
      0003D8 FC               [12]  843 	mov	r4,a
      0003D9 80 DF            [24]  844 	sjmp	00101$
      0003DB                        845 00103$:
                                    846 ;	firmware.c:150: return v;
      0003DB 8C 82            [24]  847 	mov	dpl,r4
                                    848 ;	firmware.c:151: }
      0003DD 22               [24]  849 	ret
                                    850 ;------------------------------------------------------------
                                    851 ;Allocation info for local variables in function 'port_to_int8'
                                    852 ;------------------------------------------------------------
                                    853 ;port                      Allocated to registers r5 r6 r7 
                                    854 ;------------------------------------------------------------
                                    855 ;	firmware.c:153: int8_t port_to_int8(char *port) {
                                    856 ;	-----------------------------------------
                                    857 ;	 function port_to_int8
                                    858 ;	-----------------------------------------
      0003DE                        859 _port_to_int8:
      0003DE AD 82            [24]  860 	mov	r5,dpl
      0003E0 AE 83            [24]  861 	mov	r6,dph
      0003E2 AF F0            [24]  862 	mov	r7,b
                                    863 ;	firmware.c:154: if (port[1]!=0&&port[1]!=' ') {
      0003E4 74 01            [12]  864 	mov	a,#0x01
      0003E6 2D               [12]  865 	add	a,r5
      0003E7 FA               [12]  866 	mov	r2,a
      0003E8 E4               [12]  867 	clr	a
      0003E9 3E               [12]  868 	addc	a,r6
      0003EA FB               [12]  869 	mov	r3,a
      0003EB 8F 04            [24]  870 	mov	ar4,r7
      0003ED 8A 82            [24]  871 	mov	dpl,r2
      0003EF 8B 83            [24]  872 	mov	dph,r3
      0003F1 8C F0            [24]  873 	mov	b,r4
      0003F3 12 07 A2         [24]  874 	lcall	__gptrget
      0003F6 FC               [12]  875 	mov	r4,a
      0003F7 60 09            [24]  876 	jz	00102$
      0003F9 BC 20 02         [24]  877 	cjne	r4,#0x20,00115$
      0003FC 80 04            [24]  878 	sjmp	00102$
      0003FE                        879 00115$:
                                    880 ;	firmware.c:156: return -1;
      0003FE 75 82 FF         [24]  881 	mov	dpl,#0xff
      000401 22               [24]  882 	ret
      000402                        883 00102$:
                                    884 ;	firmware.c:158: return (int8_t)str_to_uint8(port);
      000402 8D 82            [24]  885 	mov	dpl,r5
      000404 8E 83            [24]  886 	mov	dph,r6
      000406 8F F0            [24]  887 	mov	b,r7
                                    888 ;	firmware.c:159: }
      000408 02 03 B2         [24]  889 	ljmp	_str_to_uint8
                                    890 ;------------------------------------------------------------
                                    891 ;Allocation info for local variables in function 'main'
                                    892 ;------------------------------------------------------------
                                    893 ;i                         Allocated to registers r6 r7 
                                    894 ;ch                        Allocated to registers r3 
                                    895 ;t                         Allocated with name '_main_t_131075_50'
                                    896 ;p                         Allocated to registers r3 r5 r6 
                                    897 ;write                     Allocated to registers r4 
                                    898 ;port                      Allocated to registers r7 
                                    899 ;req_len                   Allocated to registers r6 
                                    900 ;i                         Allocated to registers r5 
                                    901 ;ret                       Allocated to registers r5 
                                    902 ;ret                       Allocated to registers r7 
                                    903 ;i                         Allocated to registers r7 
                                    904 ;num                       Allocated with name '_main_num_327687_70'
                                    905 ;cmd                       Allocated with name '_main_cmd_65537_43'
                                    906 ;i2c_buf                   Allocated with name '_main_i2c_buf_65537_43'
                                    907 ;i2c_buf2                  Allocated with name '_main_i2c_buf2_65537_43'
                                    908 ;------------------------------------------------------------
                                    909 ;	firmware.c:163: int main(void) {
                                    910 ;	-----------------------------------------
                                    911 ;	 function main
                                    912 ;	-----------------------------------------
      00040B                        913 _main:
                                    914 ;	firmware.c:164: serial_print("INIT OK\n");
      00040B 90 08 9D         [24]  915 	mov	dptr,#___str_5
      00040E 75 F0 80         [24]  916 	mov	b,#0x80
      000411 12 00 C6         [24]  917 	lcall	_serial_print
                                    918 ;	firmware.c:169: while (true) {
      000414                        919 00137$:
                                    920 ;	firmware.c:170: serial_print("> ");
      000414 90 08 A6         [24]  921 	mov	dptr,#___str_6
      000417 75 F0 80         [24]  922 	mov	b,#0x80
      00041A 12 00 C6         [24]  923 	lcall	_serial_print
                                    924 ;	firmware.c:173: for (i = 0; i < CMD_BUF_SZ; i++) {
      00041D 7E 00            [12]  925 	mov	r6,#0x00
      00041F 7F 00            [12]  926 	mov	r7,#0x00
      000421 7C 00            [12]  927 	mov	r4,#0x00
      000423 7D 00            [12]  928 	mov	r5,#0x00
      000425                        929 00139$:
                                    930 ;	firmware.c:174: char ch = serial_read_char();
      000425 C0 07            [24]  931 	push	ar7
      000427 C0 06            [24]  932 	push	ar6
      000429 C0 05            [24]  933 	push	ar5
      00042B C0 04            [24]  934 	push	ar4
      00042D 12 01 7B         [24]  935 	lcall	_serial_read_char
      000430 AB 82            [24]  936 	mov	r3,dpl
      000432 D0 04            [24]  937 	pop	ar4
      000434 D0 05            [24]  938 	pop	ar5
      000436 D0 06            [24]  939 	pop	ar6
      000438 D0 07            [24]  940 	pop	ar7
                                    941 ;	firmware.c:175: if (ch == '\n') {
      00043A BB 0A 0E         [24]  942 	cjne	r3,#0x0a,00102$
                                    943 ;	firmware.c:176: cmd[i] = '\0';
      00043D EE               [12]  944 	mov	a,r6
      00043E 24 01            [12]  945 	add	a,#_main_cmd_65537_43
      000440 F5 82            [12]  946 	mov	dpl,a
      000442 EF               [12]  947 	mov	a,r7
      000443 34 00            [12]  948 	addc	a,#(_main_cmd_65537_43 >> 8)
      000445 F5 83            [12]  949 	mov	dph,a
      000447 E4               [12]  950 	clr	a
      000448 F0               [24]  951 	movx	@dptr,a
                                    952 ;	firmware.c:177: break;
      000449 80 20            [24]  953 	sjmp	00103$
      00044B                        954 00102$:
                                    955 ;	firmware.c:179: cmd[i] = ch;
      00044B EC               [12]  956 	mov	a,r4
      00044C 24 01            [12]  957 	add	a,#_main_cmd_65537_43
      00044E F5 82            [12]  958 	mov	dpl,a
      000450 ED               [12]  959 	mov	a,r5
      000451 34 00            [12]  960 	addc	a,#(_main_cmd_65537_43 >> 8)
      000453 F5 83            [12]  961 	mov	dph,a
      000455 EB               [12]  962 	mov	a,r3
      000456 F0               [24]  963 	movx	@dptr,a
                                    964 ;	firmware.c:173: for (i = 0; i < CMD_BUF_SZ; i++) {
      000457 0C               [12]  965 	inc	r4
      000458 BC 00 01         [24]  966 	cjne	r4,#0x00,00253$
      00045B 0D               [12]  967 	inc	r5
      00045C                        968 00253$:
      00045C 8C 06            [24]  969 	mov	ar6,r4
      00045E 8D 07            [24]  970 	mov	ar7,r5
      000460 C3               [12]  971 	clr	c
      000461 EC               [12]  972 	mov	a,r4
      000462 94 80            [12]  973 	subb	a,#0x80
      000464 ED               [12]  974 	mov	a,r5
      000465 64 80            [12]  975 	xrl	a,#0x80
      000467 94 81            [12]  976 	subb	a,#0x81
      000469 40 BA            [24]  977 	jc	00139$
      00046B                        978 00103$:
                                    979 ;	firmware.c:182: if (i == CMD_BUF_SZ) {
      00046B BE 80 0E         [24]  980 	cjne	r6,#0x80,00105$
      00046E BF 01 0B         [24]  981 	cjne	r7,#0x01,00105$
                                    982 ;	firmware.c:183: serial_print("-err: command too long, rejected\n");
      000471 90 08 A9         [24]  983 	mov	dptr,#___str_7
      000474 75 F0 80         [24]  984 	mov	b,#0x80
      000477 12 00 C6         [24]  985 	lcall	_serial_print
                                    986 ;	firmware.c:184: continue;
      00047A 80 98            [24]  987 	sjmp	00137$
      00047C                        988 00105$:
                                    989 ;	firmware.c:188: tokenizer_init(&t, cmd);
      00047C 75 2E 01         [24]  990 	mov	_tokenizer_init_PARM_2,#_main_cmd_65537_43
      00047F 75 2F 00         [24]  991 	mov	(_tokenizer_init_PARM_2 + 1),#(_main_cmd_65537_43 >> 8)
      000482 75 30 00         [24]  992 	mov	(_tokenizer_init_PARM_2 + 2),#0x00
      000485 90 00 25         [24]  993 	mov	dptr,#_main_t_131075_50
      000488 75 F0 40         [24]  994 	mov	b,#0x40
      00048B 12 01 88         [24]  995 	lcall	_tokenizer_init
                                    996 ;	firmware.c:190: char *p = tokenizer_next(&t);
      00048E 90 00 25         [24]  997 	mov	dptr,#_main_t_131075_50
      000491 75 F0 40         [24]  998 	mov	b,#0x40
      000494 12 01 B7         [24]  999 	lcall	_tokenizer_next
      000497 AD 82            [24] 1000 	mov	r5,dpl
      000499 AE 83            [24] 1001 	mov	r6,dph
      00049B AF F0            [24] 1002 	mov	r7,b
                                   1003 ;	firmware.c:191: if (p == NULL) {
      00049D ED               [12] 1004 	mov	a,r5
      00049E 4E               [12] 1005 	orl	a,r6
      00049F 70 0C            [24] 1006 	jnz	00107$
                                   1007 ;	firmware.c:192: serial_print("-err: command format incorrect\n");
      0004A1 90 08 CB         [24] 1008 	mov	dptr,#___str_8
      0004A4 75 F0 80         [24] 1009 	mov	b,#0x80
      0004A7 12 00 C6         [24] 1010 	lcall	_serial_print
                                   1011 ;	firmware.c:193: continue;
      0004AA 02 04 14         [24] 1012 	ljmp	00137$
      0004AD                       1013 00107$:
                                   1014 ;	firmware.c:197: if (*p == 'r') {
      0004AD 8D 82            [24] 1015 	mov	dpl,r5
      0004AF 8E 83            [24] 1016 	mov	dph,r6
      0004B1 8F F0            [24] 1017 	mov	b,r7
      0004B3 12 07 A2         [24] 1018 	lcall	__gptrget
      0004B6 FC               [12] 1019 	mov	r4,a
      0004B7 BC 72 04         [24] 1020 	cjne	r4,#0x72,00112$
                                   1021 ;	firmware.c:198: write = false;
      0004BA 7C 00            [12] 1022 	mov	r4,#0x00
      0004BC 80 1D            [24] 1023 	sjmp	00113$
      0004BE                       1024 00112$:
                                   1025 ;	firmware.c:199: } else if (*p == 'w') {
      0004BE 8D 82            [24] 1026 	mov	dpl,r5
      0004C0 8E 83            [24] 1027 	mov	dph,r6
      0004C2 8F F0            [24] 1028 	mov	b,r7
      0004C4 12 07 A2         [24] 1029 	lcall	__gptrget
      0004C7 FD               [12] 1030 	mov	r5,a
      0004C8 BD 77 04         [24] 1031 	cjne	r5,#0x77,00109$
                                   1032 ;	firmware.c:200: write = true;
      0004CB 7C 01            [12] 1033 	mov	r4,#0x01
      0004CD 80 0C            [24] 1034 	sjmp	00113$
      0004CF                       1035 00109$:
                                   1036 ;	firmware.c:202: serial_print("-err: unknown command\n");
      0004CF 90 08 EB         [24] 1037 	mov	dptr,#___str_9
      0004D2 75 F0 80         [24] 1038 	mov	b,#0x80
      0004D5 12 00 C6         [24] 1039 	lcall	_serial_print
                                   1040 ;	firmware.c:203: continue;
      0004D8 02 04 14         [24] 1041 	ljmp	00137$
      0004DB                       1042 00113$:
                                   1043 ;	firmware.c:206: p = tokenizer_next(&t);
      0004DB 90 00 25         [24] 1044 	mov	dptr,#_main_t_131075_50
      0004DE 75 F0 40         [24] 1045 	mov	b,#0x40
      0004E1 C0 04            [24] 1046 	push	ar4
      0004E3 12 01 B7         [24] 1047 	lcall	_tokenizer_next
      0004E6 AD 82            [24] 1048 	mov	r5,dpl
      0004E8 AE 83            [24] 1049 	mov	r6,dph
      0004EA AF F0            [24] 1050 	mov	r7,b
      0004EC D0 04            [24] 1051 	pop	ar4
                                   1052 ;	firmware.c:207: if (p == NULL) {
      0004EE ED               [12] 1053 	mov	a,r5
      0004EF 4E               [12] 1054 	orl	a,r6
      0004F0 70 0C            [24] 1055 	jnz	00115$
                                   1056 ;	firmware.c:208: serial_print("-err: command format incorrect\n");
      0004F2 90 08 CB         [24] 1057 	mov	dptr,#___str_8
      0004F5 75 F0 80         [24] 1058 	mov	b,#0x80
      0004F8 12 00 C6         [24] 1059 	lcall	_serial_print
                                   1060 ;	firmware.c:209: continue;
      0004FB 02 04 14         [24] 1061 	ljmp	00137$
      0004FE                       1062 00115$:
                                   1063 ;	firmware.c:212: int8_t port = port_to_int8(p);
      0004FE 8D 82            [24] 1064 	mov	dpl,r5
      000500 8E 83            [24] 1065 	mov	dph,r6
      000502 8F F0            [24] 1066 	mov	b,r7
      000504 C0 04            [24] 1067 	push	ar4
      000506 12 03 DE         [24] 1068 	lcall	_port_to_int8
      000509 AF 82            [24] 1069 	mov	r7,dpl
      00050B D0 04            [24] 1070 	pop	ar4
                                   1071 ;	firmware.c:213: if (port == -1) {
      00050D BF FF 0C         [24] 1072 	cjne	r7,#0xff,00117$
                                   1073 ;	firmware.c:214: serial_print("-err: port invalid or not allowed\n");
      000510 90 09 02         [24] 1074 	mov	dptr,#___str_10
      000513 75 F0 80         [24] 1075 	mov	b,#0x80
      000516 12 00 C6         [24] 1076 	lcall	_serial_print
                                   1077 ;	firmware.c:215: continue;
      000519 02 04 14         [24] 1078 	ljmp	00137$
      00051C                       1079 00117$:
                                   1080 ;	firmware.c:218: p = tokenizer_next(&t);
      00051C 90 00 25         [24] 1081 	mov	dptr,#_main_t_131075_50
      00051F 75 F0 40         [24] 1082 	mov	b,#0x40
      000522 C0 07            [24] 1083 	push	ar7
      000524 C0 04            [24] 1084 	push	ar4
      000526 12 01 B7         [24] 1085 	lcall	_tokenizer_next
      000529 AB 82            [24] 1086 	mov	r3,dpl
      00052B AD 83            [24] 1087 	mov	r5,dph
      00052D AE F0            [24] 1088 	mov	r6,b
      00052F D0 04            [24] 1089 	pop	ar4
      000531 D0 07            [24] 1090 	pop	ar7
                                   1091 ;	firmware.c:219: if (p == NULL) {
      000533 EB               [12] 1092 	mov	a,r3
      000534 4D               [12] 1093 	orl	a,r5
      000535 70 0C            [24] 1094 	jnz	00119$
                                   1095 ;	firmware.c:220: serial_print("-err: command format incorrect\n");
      000537 90 08 CB         [24] 1096 	mov	dptr,#___str_8
      00053A 75 F0 80         [24] 1097 	mov	b,#0x80
      00053D 12 00 C6         [24] 1098 	lcall	_serial_print
                                   1099 ;	firmware.c:221: continue;
      000540 02 04 14         [24] 1100 	ljmp	00137$
      000543                       1101 00119$:
                                   1102 ;	firmware.c:224: uint8_t req_len = str_to_uint8(p);
      000543 8B 82            [24] 1103 	mov	dpl,r3
      000545 8D 83            [24] 1104 	mov	dph,r5
      000547 8E F0            [24] 1105 	mov	b,r6
      000549 C0 07            [24] 1106 	push	ar7
      00054B C0 04            [24] 1107 	push	ar4
      00054D 12 03 B2         [24] 1108 	lcall	_str_to_uint8
      000550 AE 82            [24] 1109 	mov	r6,dpl
      000552 D0 04            [24] 1110 	pop	ar4
      000554 D0 07            [24] 1111 	pop	ar7
                                   1112 ;	firmware.c:225: if (req_len == 0 || req_len > I2C_BUF_SZ) {
      000556 EE               [12] 1113 	mov	a,r6
      000557 60 05            [24] 1114 	jz	00120$
      000559 EE               [12] 1115 	mov	a,r6
      00055A 24 7F            [12] 1116 	add	a,#0xff - 0x80
      00055C 50 0C            [24] 1117 	jnc	00121$
      00055E                       1118 00120$:
                                   1119 ;	firmware.c:226: serial_print("-err: I2C request length incorrect\n");
      00055E 90 09 25         [24] 1120 	mov	dptr,#___str_11
      000561 75 F0 80         [24] 1121 	mov	b,#0x80
      000564 12 00 C6         [24] 1122 	lcall	_serial_print
                                   1123 ;	firmware.c:227: continue;
      000567 02 04 14         [24] 1124 	ljmp	00137$
      00056A                       1125 00121$:
                                   1126 ;	firmware.c:230: if (write) {
      00056A EC               [12] 1127 	mov	a,r4
      00056B 70 03            [24] 1128 	jnz	00268$
      00056D 02 06 6F         [24] 1129 	ljmp	00134$
      000570                       1130 00268$:
                                   1131 ;	firmware.c:231: for (uint8_t i = 0; i < req_len; i++) {
      000570 7D 00            [12] 1132 	mov	r5,#0x00
      000572                       1133 00142$:
      000572 C3               [12] 1134 	clr	c
      000573 ED               [12] 1135 	mov	a,r5
      000574 9E               [12] 1136 	subb	a,r6
      000575 50 6E            [24] 1137 	jnc	00125$
                                   1138 ;	firmware.c:232: p = tokenizer_next(&t);
      000577 90 00 25         [24] 1139 	mov	dptr,#_main_t_131075_50
      00057A 75 F0 40         [24] 1140 	mov	b,#0x40
      00057D C0 07            [24] 1141 	push	ar7
      00057F C0 06            [24] 1142 	push	ar6
      000581 C0 05            [24] 1143 	push	ar5
      000583 12 01 B7         [24] 1144 	lcall	_tokenizer_next
      000586 AA 82            [24] 1145 	mov	r2,dpl
      000588 AB 83            [24] 1146 	mov	r3,dph
      00058A AC F0            [24] 1147 	mov	r4,b
      00058C D0 05            [24] 1148 	pop	ar5
      00058E D0 06            [24] 1149 	pop	ar6
      000590 D0 07            [24] 1150 	pop	ar7
                                   1151 ;	firmware.c:233: if (p == NULL) {
      000592 EA               [12] 1152 	mov	a,r2
      000593 4B               [12] 1153 	orl	a,r3
      000594 60 4F            [24] 1154 	jz	00125$
                                   1155 ;	firmware.c:237: i2c_buf[i] = str_to_uint8(p);
      000596 ED               [12] 1156 	mov	a,r5
      000597 24 81            [12] 1157 	add	a,#_main_i2c_buf_65537_43
      000599 F8               [12] 1158 	mov	r0,a
      00059A E4               [12] 1159 	clr	a
      00059B 34 01            [12] 1160 	addc	a,#(_main_i2c_buf_65537_43 >> 8)
      00059D F9               [12] 1161 	mov	r1,a
      00059E 8A 82            [24] 1162 	mov	dpl,r2
      0005A0 8B 83            [24] 1163 	mov	dph,r3
      0005A2 8C F0            [24] 1164 	mov	b,r4
      0005A4 C0 07            [24] 1165 	push	ar7
      0005A6 C0 06            [24] 1166 	push	ar6
      0005A8 C0 05            [24] 1167 	push	ar5
      0005AA C0 01            [24] 1168 	push	ar1
      0005AC C0 00            [24] 1169 	push	ar0
      0005AE 12 03 B2         [24] 1170 	lcall	_str_to_uint8
      0005B1 AC 82            [24] 1171 	mov	r4,dpl
      0005B3 D0 00            [24] 1172 	pop	ar0
      0005B5 D0 01            [24] 1173 	pop	ar1
      0005B7 D0 05            [24] 1174 	pop	ar5
      0005B9 88 82            [24] 1175 	mov	dpl,r0
      0005BB 89 83            [24] 1176 	mov	dph,r1
      0005BD EC               [12] 1177 	mov	a,r4
      0005BE F0               [24] 1178 	movx	@dptr,a
                                   1179 ;	firmware.c:238: i2c_buf2[i] = rand();
      0005BF ED               [12] 1180 	mov	a,r5
      0005C0 24 01            [12] 1181 	add	a,#_main_i2c_buf2_65537_43
      0005C2 FB               [12] 1182 	mov	r3,a
      0005C3 E4               [12] 1183 	clr	a
      0005C4 34 02            [12] 1184 	addc	a,#(_main_i2c_buf2_65537_43 >> 8)
      0005C6 FC               [12] 1185 	mov	r4,a
      0005C7 C0 05            [24] 1186 	push	ar5
      0005C9 C0 04            [24] 1187 	push	ar4
      0005CB C0 03            [24] 1188 	push	ar3
      0005CD 12 00 B9         [24] 1189 	lcall	_rand
      0005D0 AA 82            [24] 1190 	mov	r2,dpl
      0005D2 D0 03            [24] 1191 	pop	ar3
      0005D4 D0 04            [24] 1192 	pop	ar4
      0005D6 D0 05            [24] 1193 	pop	ar5
      0005D8 D0 06            [24] 1194 	pop	ar6
      0005DA D0 07            [24] 1195 	pop	ar7
      0005DC 8B 82            [24] 1196 	mov	dpl,r3
      0005DE 8C 83            [24] 1197 	mov	dph,r4
      0005E0 EA               [12] 1198 	mov	a,r2
      0005E1 F0               [24] 1199 	movx	@dptr,a
                                   1200 ;	firmware.c:231: for (uint8_t i = 0; i < req_len; i++) {
      0005E2 0D               [12] 1201 	inc	r5
      0005E3 80 8D            [24] 1202 	sjmp	00142$
      0005E5                       1203 00125$:
                                   1204 ;	firmware.c:241: int8_t ret = i2c_write(port, req_len, i2c_buf);
      0005E5 8E 2E            [24] 1205 	mov	_i2c_write_PARM_2,r6
      0005E7 75 2F 81         [24] 1206 	mov	_i2c_write_PARM_3,#_main_i2c_buf_65537_43
      0005EA 75 30 01         [24] 1207 	mov	(_i2c_write_PARM_3 + 1),#(_main_i2c_buf_65537_43 >> 8)
      0005ED 8F 82            [24] 1208 	mov	dpl,r7
      0005EF C0 07            [24] 1209 	push	ar7
      0005F1 C0 06            [24] 1210 	push	ar6
      0005F3 12 00 EE         [24] 1211 	lcall	_i2c_write
      0005F6 AD 82            [24] 1212 	mov	r5,dpl
      0005F8 D0 06            [24] 1213 	pop	ar6
      0005FA D0 07            [24] 1214 	pop	ar7
                                   1215 ;	firmware.c:242: i2c_write((port+1)%10,req_len,i2c_buf2);
      0005FC EF               [12] 1216 	mov	a,r7
      0005FD FB               [12] 1217 	mov	r3,a
      0005FE 33               [12] 1218 	rlc	a
      0005FF 95 E0            [12] 1219 	subb	a,acc
      000601 FC               [12] 1220 	mov	r4,a
      000602 8B 82            [24] 1221 	mov	dpl,r3
      000604 8C 83            [24] 1222 	mov	dph,r4
      000606 A3               [24] 1223 	inc	dptr
      000607 75 2E 0A         [24] 1224 	mov	__modsint_PARM_2,#0x0a
      00060A 75 2F 00         [24] 1225 	mov	(__modsint_PARM_2 + 1),#0x00
      00060D C0 06            [24] 1226 	push	ar6
      00060F C0 05            [24] 1227 	push	ar5
      000611 C0 04            [24] 1228 	push	ar4
      000613 C0 03            [24] 1229 	push	ar3
      000615 12 07 BE         [24] 1230 	lcall	__modsint
      000618 A9 82            [24] 1231 	mov	r1,dpl
      00061A D0 03            [24] 1232 	pop	ar3
      00061C D0 04            [24] 1233 	pop	ar4
      00061E D0 05            [24] 1234 	pop	ar5
      000620 D0 06            [24] 1235 	pop	ar6
      000622 89 82            [24] 1236 	mov	dpl,r1
      000624 8E 2E            [24] 1237 	mov	_i2c_write_PARM_2,r6
      000626 75 2F 01         [24] 1238 	mov	_i2c_write_PARM_3,#_main_i2c_buf2_65537_43
      000629 75 30 02         [24] 1239 	mov	(_i2c_write_PARM_3 + 1),#(_main_i2c_buf2_65537_43 >> 8)
      00062C C0 06            [24] 1240 	push	ar6
      00062E C0 05            [24] 1241 	push	ar5
      000630 C0 04            [24] 1242 	push	ar4
      000632 C0 03            [24] 1243 	push	ar3
      000634 12 00 EE         [24] 1244 	lcall	_i2c_write
      000637 D0 03            [24] 1245 	pop	ar3
      000639 D0 04            [24] 1246 	pop	ar4
                                   1247 ;	firmware.c:243: i2c_write((port+9)%10,req_len,i2c_buf2);
      00063B 74 09            [12] 1248 	mov	a,#0x09
      00063D 2B               [12] 1249 	add	a,r3
      00063E F5 82            [12] 1250 	mov	dpl,a
      000640 E4               [12] 1251 	clr	a
      000641 3C               [12] 1252 	addc	a,r4
      000642 F5 83            [12] 1253 	mov	dph,a
      000644 75 2E 0A         [24] 1254 	mov	__modsint_PARM_2,#0x0a
      000647 75 2F 00         [24] 1255 	mov	(__modsint_PARM_2 + 1),#0x00
      00064A 12 07 BE         [24] 1256 	lcall	__modsint
      00064D AB 82            [24] 1257 	mov	r3,dpl
      00064F D0 05            [24] 1258 	pop	ar5
      000651 D0 06            [24] 1259 	pop	ar6
      000653 75 2F 01         [24] 1260 	mov	_i2c_write_PARM_3,#_main_i2c_buf2_65537_43
      000656 75 30 02         [24] 1261 	mov	(_i2c_write_PARM_3 + 1),#(_main_i2c_buf2_65537_43 >> 8)
      000659 8E 2E            [24] 1262 	mov	_i2c_write_PARM_2,r6
      00065B 8B 82            [24] 1263 	mov	dpl,r3
      00065D C0 05            [24] 1264 	push	ar5
      00065F 12 00 EE         [24] 1265 	lcall	_i2c_write
      000662 D0 05            [24] 1266 	pop	ar5
                                   1267 ;	firmware.c:244: serial_print(i2c_status_to_error(ret));
      000664 8D 82            [24] 1268 	mov	dpl,r5
      000666 12 01 42         [24] 1269 	lcall	_i2c_status_to_error
      000669 12 00 C6         [24] 1270 	lcall	_serial_print
      00066C 02 04 14         [24] 1271 	ljmp	00137$
      00066F                       1272 00134$:
                                   1273 ;	firmware.c:246: int8_t ret = i2c_read(port, req_len, i2c_buf);
      00066F 75 2F 81         [24] 1274 	mov	_i2c_read_PARM_3,#_main_i2c_buf_65537_43
      000672 75 30 01         [24] 1275 	mov	(_i2c_read_PARM_3 + 1),#(_main_i2c_buf_65537_43 >> 8)
      000675 8E 2E            [24] 1276 	mov	_i2c_read_PARM_2,r6
      000677 8F 82            [24] 1277 	mov	dpl,r7
      000679 C0 06            [24] 1278 	push	ar6
      00067B 12 01 18         [24] 1279 	lcall	_i2c_read
      00067E AF 82            [24] 1280 	mov	r7,dpl
      000680 D0 06            [24] 1281 	pop	ar6
                                   1282 ;	firmware.c:247: serial_print(i2c_status_to_error(ret));
      000682 8F 82            [24] 1283 	mov	dpl,r7
      000684 C0 07            [24] 1284 	push	ar7
      000686 C0 06            [24] 1285 	push	ar6
      000688 12 01 42         [24] 1286 	lcall	_i2c_status_to_error
      00068B 12 00 C6         [24] 1287 	lcall	_serial_print
      00068E D0 06            [24] 1288 	pop	ar6
      000690 D0 07            [24] 1289 	pop	ar7
                                   1290 ;	firmware.c:248: if(ret!=2)
      000692 BF 02 03         [24] 1291 	cjne	r7,#0x02,00271$
      000695 02 07 2E         [24] 1292 	ljmp	00132$
      000698                       1293 00271$:
                                   1294 ;	firmware.c:249: for (uint8_t i = 0; i < req_len; i++) {
      000698 7F 00            [12] 1295 	mov	r7,#0x00
      00069A                       1296 00145$:
      00069A C3               [12] 1297 	clr	c
      00069B EF               [12] 1298 	mov	a,r7
      00069C 9E               [12] 1299 	subb	a,r6
      00069D 40 03            [24] 1300 	jc	00272$
      00069F 02 07 2E         [24] 1301 	ljmp	00132$
      0006A2                       1302 00272$:
                                   1303 ;	firmware.c:251: uint8_to_str(num, i2c_buf[i]);
      0006A2 EF               [12] 1304 	mov	a,r7
      0006A3 24 81            [12] 1305 	add	a,#_main_i2c_buf_65537_43
      0006A5 F5 82            [12] 1306 	mov	dpl,a
      0006A7 E4               [12] 1307 	clr	a
      0006A8 34 01            [12] 1308 	addc	a,#(_main_i2c_buf_65537_43 >> 8)
      0006AA F5 83            [12] 1309 	mov	dph,a
      0006AC E0               [24] 1310 	movx	a,@dptr
      0006AD F5 2E            [12] 1311 	mov	_uint8_to_str_PARM_2,a
      0006AF 90 00 2A         [24] 1312 	mov	dptr,#_main_num_327687_70
      0006B2 75 F0 40         [24] 1313 	mov	b,#0x40
      0006B5 C0 07            [24] 1314 	push	ar7
      0006B7 C0 06            [24] 1315 	push	ar6
      0006B9 12 03 59         [24] 1316 	lcall	_uint8_to_str
                                   1317 ;	firmware.c:252: serial_print(num);
      0006BC 90 00 2A         [24] 1318 	mov	dptr,#_main_num_327687_70
      0006BF 75 F0 40         [24] 1319 	mov	b,#0x40
      0006C2 12 00 C6         [24] 1320 	lcall	_serial_print
      0006C5 D0 06            [24] 1321 	pop	ar6
      0006C7 D0 07            [24] 1322 	pop	ar7
                                   1323 ;	firmware.c:254: if ((i + 1) % 16 == 0 && i +1 != req_len) {
      0006C9 8F 04            [24] 1324 	mov	ar4,r7
      0006CB 7D 00            [12] 1325 	mov	r5,#0x00
      0006CD 8C 82            [24] 1326 	mov	dpl,r4
      0006CF 8D 83            [24] 1327 	mov	dph,r5
      0006D1 A3               [24] 1328 	inc	dptr
      0006D2 75 2E 10         [24] 1329 	mov	__modsint_PARM_2,#0x10
                                   1330 ;	1-genFromRTrack replaced	mov	(__modsint_PARM_2 + 1),#0x00
      0006D5 8D 2F            [24] 1331 	mov	(__modsint_PARM_2 + 1),r5
      0006D7 C0 07            [24] 1332 	push	ar7
      0006D9 C0 06            [24] 1333 	push	ar6
      0006DB C0 05            [24] 1334 	push	ar5
      0006DD C0 04            [24] 1335 	push	ar4
      0006DF 12 07 BE         [24] 1336 	lcall	__modsint
      0006E2 E5 82            [12] 1337 	mov	a,dpl
      0006E4 85 83 F0         [24] 1338 	mov	b,dph
      0006E7 D0 04            [24] 1339 	pop	ar4
      0006E9 D0 05            [24] 1340 	pop	ar5
      0006EB D0 06            [24] 1341 	pop	ar6
      0006ED D0 07            [24] 1342 	pop	ar7
      0006EF 45 F0            [12] 1343 	orl	a,b
      0006F1 70 26            [24] 1344 	jnz	00127$
      0006F3 0C               [12] 1345 	inc	r4
      0006F4 BC 00 01         [24] 1346 	cjne	r4,#0x00,00274$
      0006F7 0D               [12] 1347 	inc	r5
      0006F8                       1348 00274$:
      0006F8 8E 02            [24] 1349 	mov	ar2,r6
      0006FA 7B 00            [12] 1350 	mov	r3,#0x00
      0006FC EC               [12] 1351 	mov	a,r4
      0006FD B5 02 06         [24] 1352 	cjne	a,ar2,00275$
      000700 ED               [12] 1353 	mov	a,r5
      000701 B5 03 02         [24] 1354 	cjne	a,ar3,00275$
      000704 80 13            [24] 1355 	sjmp	00127$
      000706                       1356 00275$:
                                   1357 ;	firmware.c:255: serial_print("\n");
      000706 90 09 49         [24] 1358 	mov	dptr,#___str_12
      000709 75 F0 80         [24] 1359 	mov	b,#0x80
      00070C C0 07            [24] 1360 	push	ar7
      00070E C0 06            [24] 1361 	push	ar6
      000710 12 00 C6         [24] 1362 	lcall	_serial_print
      000713 D0 06            [24] 1363 	pop	ar6
      000715 D0 07            [24] 1364 	pop	ar7
      000717 80 11            [24] 1365 	sjmp	00146$
      000719                       1366 00127$:
                                   1367 ;	firmware.c:257: serial_print(" ");
      000719 90 09 4B         [24] 1368 	mov	dptr,#___str_13
      00071C 75 F0 80         [24] 1369 	mov	b,#0x80
      00071F C0 07            [24] 1370 	push	ar7
      000721 C0 06            [24] 1371 	push	ar6
      000723 12 00 C6         [24] 1372 	lcall	_serial_print
      000726 D0 06            [24] 1373 	pop	ar6
      000728 D0 07            [24] 1374 	pop	ar7
      00072A                       1375 00146$:
                                   1376 ;	firmware.c:249: for (uint8_t i = 0; i < req_len; i++) {
      00072A 0F               [12] 1377 	inc	r7
      00072B 02 06 9A         [24] 1378 	ljmp	00145$
      00072E                       1379 00132$:
                                   1380 ;	firmware.c:261: serial_print("\n-end\n");
      00072E 90 09 4D         [24] 1381 	mov	dptr,#___str_14
      000731 75 F0 80         [24] 1382 	mov	b,#0x80
      000734 12 00 C6         [24] 1383 	lcall	_serial_print
                                   1384 ;	firmware.c:266: }
      000737 02 04 14         [24] 1385 	ljmp	00137$
                                   1386 	.area CSEG    (CODE)
                                   1387 	.area CONST   (CODE)
      0007F8                       1388 ___str_0:
      0007F8 69 32 63 20 73 74 61  1389 	.ascii "i2c status: transaction completed / ready"
             74 75 73 3A 20 74 72
             61 6E 73 61 63 74 69
             6F 6E 20 63 6F 6D 70
             6C 65 74 65 64 20 2F
             20 72 65 61 64 79
      000821 0A                    1390 	.db 0x0a
      000822 00                    1391 	.db 0x00
      000823                       1392 ___str_1:
      000823 69 32 63 20 73 74 61  1393 	.ascii "i2c status: busy"
             74 75 73 3A 20 62 75
             73 79
      000833 0A                    1394 	.db 0x0a
      000834 00                    1395 	.db 0x00
      000835                       1396 ___str_2:
      000835 69 32 63 20 73 74 61  1397 	.ascii "i2c status: error - device not found"
             74 75 73 3A 20 65 72
             72 6F 72 20 2D 20 64
             65 76 69 63 65 20 6E
             6F 74 20 66 6F 75 6E
             64
      000859 0A                    1398 	.db 0x0a
      00085A 00                    1399 	.db 0x00
      00085B                       1400 ___str_3:
      00085B 69 32 63 20 73 74 61  1401 	.ascii "i2c status: error - device misbehaved"
             74 75 73 3A 20 65 72
             72 6F 72 20 2D 20 64
             65 76 69 63 65 20 6D
             69 73 62 65 68 61 76
             65 64
      000880 0A                    1402 	.db 0x0a
      000881 00                    1403 	.db 0x00
      000882                       1404 ___str_4:
      000882 69 32 63 20 73 74 61  1405 	.ascii "i2c status: unknown error"
             74 75 73 3A 20 75 6E
             6B 6E 6F 77 6E 20 65
             72 72 6F 72
      00089B 0A                    1406 	.db 0x0a
      00089C 00                    1407 	.db 0x00
      00089D                       1408 ___str_5:
      00089D 49 4E 49 54 20 4F 4B  1409 	.ascii "INIT OK"
      0008A4 0A                    1410 	.db 0x0a
      0008A5 00                    1411 	.db 0x00
      0008A6                       1412 ___str_6:
      0008A6 3E 20                 1413 	.ascii "> "
      0008A8 00                    1414 	.db 0x00
      0008A9                       1415 ___str_7:
      0008A9 2D 65 72 72 3A 20 63  1416 	.ascii "-err: command too long, rejected"
             6F 6D 6D 61 6E 64 20
             74 6F 6F 20 6C 6F 6E
             67 2C 20 72 65 6A 65
             63 74 65 64
      0008C9 0A                    1417 	.db 0x0a
      0008CA 00                    1418 	.db 0x00
      0008CB                       1419 ___str_8:
      0008CB 2D 65 72 72 3A 20 63  1420 	.ascii "-err: command format incorrect"
             6F 6D 6D 61 6E 64 20
             66 6F 72 6D 61 74 20
             69 6E 63 6F 72 72 65
             63 74
      0008E9 0A                    1421 	.db 0x0a
      0008EA 00                    1422 	.db 0x00
      0008EB                       1423 ___str_9:
      0008EB 2D 65 72 72 3A 20 75  1424 	.ascii "-err: unknown command"
             6E 6B 6E 6F 77 6E 20
             63 6F 6D 6D 61 6E 64
      000900 0A                    1425 	.db 0x0a
      000901 00                    1426 	.db 0x00
      000902                       1427 ___str_10:
      000902 2D 65 72 72 3A 20 70  1428 	.ascii "-err: port invalid or not allowed"
             6F 72 74 20 69 6E 76
             61 6C 69 64 20 6F 72
             20 6E 6F 74 20 61 6C
             6C 6F 77 65 64
      000923 0A                    1429 	.db 0x0a
      000924 00                    1430 	.db 0x00
      000925                       1431 ___str_11:
      000925 2D 65 72 72 3A 20 49  1432 	.ascii "-err: I2C request length incorrect"
             32 43 20 72 65 71 75
             65 73 74 20 6C 65 6E
             67 74 68 20 69 6E 63
             6F 72 72 65 63 74
      000947 0A                    1433 	.db 0x0a
      000948 00                    1434 	.db 0x00
      000949                       1435 ___str_12:
      000949 0A                    1436 	.db 0x0a
      00094A 00                    1437 	.db 0x00
      00094B                       1438 ___str_13:
      00094B 20                    1439 	.ascii " "
      00094C 00                    1440 	.db 0x00
      00094D                       1441 ___str_14:
      00094D 0A                    1442 	.db 0x0a
      00094E 2D 65 6E 64           1443 	.ascii "-end"
      000952 0A                    1444 	.db 0x0a
      000953 00                    1445 	.db 0x00
                                   1446 	.area XINIT   (CODE)
                                   1447 	.area CABS    (ABS,CODE)
