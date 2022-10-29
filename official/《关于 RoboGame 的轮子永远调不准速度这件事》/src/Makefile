all: pwmctrl firmware

firmware:chip/firmware/firmware.c
	cd chip/firmware && sdcc firmware.c
	packihx chip/firmware/firmware.ihx > chip/firmware/firmware.hex
	srec_cat chip/firmware/firmware.hex -intel -Output -Binary > firmware

pwmctrl: *.h pwmctrl.cc flag
	g++ pwmctrl.cc emu8051/emu8051.cc -o pwmctrl