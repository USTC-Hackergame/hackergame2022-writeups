`timescale 1ns / 1ps
// memory mapped SPI mode SD card driver
//
//  3.3V          ----+++              wp
//                    |||         +---- =-----
//                    RRR         =8
//  MISO(SD_DAT[0]) --|||---------=7
//                    |||  GND ---=6
//  SCLK(SD_CLK)    --||+---------=5
//                    ||   VCC ---=4
//                    ||   GND ---=3
//  MOSI(SD_CMD)    --|+----------=2
//  CS(SD_DAT[3])   --+-----------=1
//                                  +=9
//                                    +-------
//
// *addresses have already x4
// read/write 0x0000 to 0x01fc: 128*32 block cache
// read/write 0x1000: get/set <address> for R/W, auto 512 aligned (may lost changes)
// write 0x1004: do a read at <address> (may lost changes)
// write 0x1008: do a write to <address>
// read 0x2000: negative card detect
// read 0x2004: write protected
// read 0x2010: ready, used for polling
// read 0x2014: dirty?

// TODO: ready/rd for cache!
module sdcard
    (
        input clk,
        //input clk_slow,
        input rst,

        input sd_dat0,
        input sd_ncd,
        output sd_dat1,
        output sd_dat2,
        output sd_dat3,
        output sd_cmd,
        output sd_sck,
        // SD_DAT[2] and SD_DAT[1] high, SD_RESET low
        
        // memory interface
        input [15:0]a,
        input [31:0]d,
        input we,
        output [31:0]spo,

        output reg irq = 0
    );

	reg [31:0]regspo;
	wire [31:0]data = {d[7:0], d[15:8], d[23:16], d[31:24]};
	//wire [31:0]data = d;
	assign spo = regspo;
	//assign spo = {regspo[7:0], regspo[15:8], regspo[23:16], regspo[31:24]};

    // slow clock
    reg [5:0]clkcounter = 0;
    always @ (posedge clk) begin
        if (rst) clkcounter <= 6'b0;
        else clkcounter <= clkcounter + 1;
    end
    wire clk_pulse_slow = (clkcounter[5:0] == 6'b0);

    assign sd_dat1 = 1;
    assign sd_dat2 = 1;
    //assign sd_reset = 0;

    reg [31:0]sd_address = 32'hffffffff; // init as an invalid address
    reg [31:0]block[127:0];
    reg dirty = 0;

    reg sd_rd = 0;
    wire [7:0]sd_dout;
    wire sd_readnext;
    reg sd_wr = 0;
    reg [7:0]sd_din = 0;
    wire sd_writenext;
    wire sd_ready;
    wire [4:0]sd_status;
    sd_controller sd_controller_inst
    (
        .clk(clk),
        .clk_pulse_slow(clk_pulse_slow),
        .reset(rst),

        .cs(sd_dat3),
        .mosi(sd_cmd),
        .miso(sd_dat0),
        .sclk(sd_sck),

        .address(sd_address),

        .rd(sd_rd),
        .dout(sd_dout),
        .byte_available(sd_readnext),
        .wr(sd_wr),
        .din(sd_din),
        .ready_for_next_byte(sd_writenext),

        .ready(sd_ready),

        .status(sd_status)
    );

    // manual slow clock posedge detection
    reg sd_ready_old = 0;
    reg sd_readnext_old = 0;
    reg sd_writenext_old = 0;
    always @ (posedge clk) begin
        sd_ready_old <= sd_ready;
        sd_readnext_old <= sd_readnext;
        sd_writenext_old <= sd_writenext;
    end
    wire sd_ready_posedge = !sd_ready_old & sd_ready;
    wire sd_readnext_posedge = !sd_readnext_old & sd_readnext;
    wire sd_writenext_posedge = !sd_writenext_old & sd_writenext;

    wire sd_ready_real = sd_ready & !sd_rd & !sd_wr;

    reg reading = 0;
    reg writing = 0;
    reg [9:0]counter = 0;
    //wire [31:0]cache = block[counter[8:2]];
    reg [7:0]cache1;
    reg [7:0]cache2;
    reg [7:0]cache3;
    always @ (posedge clk) begin
        if (rst) begin
            sd_address <= 32'hffffffff;
            dirty <= 0;
            reading <= 0;
            writing <= 0;
            sd_rd <= 0;
            sd_wr <= 0;
        end
        else begin
            if (sd_ready_real) begin
                if (we) begin
                    case (a[15:0])
						// pay attention to endian here
                        16'h1000: sd_address <= data;
                        16'h1004: sd_rd <= data[0];
                        16'h1008: sd_wr <= data[0];
                        default: ;
                    endcase
                end
                // send/receive data has finished
                reading <= 0;
                writing <= 0;
            end
            else begin
                // sdcard has received signal and not IDLE
                // so we can stop rd/wr signals
                // and prepare to send/receive data
                if (sd_rd & !sd_ready) begin
                    sd_rd <= 0;
                    reading <= 1; counter <= 0;
                end
                else if (sd_wr & !sd_ready) begin
                    sd_wr <= 0;
                    writing <= 1; counter <= 0;
                    dirty <= 0;
                end
            end

            if (reading & sd_readnext_posedge) begin
                case (counter[1:0])
                    2'b00: cache1 <= sd_dout;
                    2'b01: cache2 <= sd_dout;
                    2'b10: cache3 <= sd_dout;
                    2'b11: block[counter[8:2]] <= {cache1, cache2, cache3, sd_dout};
                endcase
                counter <= counter + 1;
            end
            else if (writing & sd_writenext_posedge) begin
                case (counter[1:0])
                    2'b00: sd_din <= blockcounterspo[31:24];
                    2'b01: sd_din <= blockcounterspo[23:16];
                    2'b10: sd_din <= blockcounterspo[15:8];
                    2'b11: sd_din <= blockcounterspo[7:0];
                endcase
                counter <= counter + 1;
            end
            else if (we) begin
                if (a[15:12] == 0) begin
					block[a[8:2]] <= d; // pay attention to endian here
                    dirty <= 1;
                end
            end
        end
    end

    // handle non-relevant control address reading
	// TODO: fix this
	reg [31:0]blockaspo;
	reg [31:0]blockcounterspo;
	always @ (*) begin
		if (a[15:12] == 0) blockaspo <= block[a[8:2]];
		blockcounterspo <= block[counter[8:2]];
	end
    always @ (*) begin
        regspo = 0;
        if (a[15:12] == 0) regspo = blockaspo;
        else case (a[15:0])
            16'h1000: regspo = {sd_address[7:0], sd_address[15:8], sd_address[23:16], sd_address[31:24]};
            16'h2000: regspo = {7'b0, sd_ncd, 24'b0};
            16'h2010: regspo = {7'b0, sd_ready_real, 24'b0};
            16'h2014: regspo = {7'b0, dirty, 24'b0};
            default: ;
        endcase
    end

    // interrupt when ready
    //assign irq = sd_ready_posedge;

endmodule

