`timescale 1ns/1ps
`default_nettype none

module reset_generator #(
    parameter integer RESET_CYCLES = 16
) (
    input  logic clk,
    output logic reset
);
    localparam integer COUNTER_WIDTH =
        (RESET_CYCLES < 2) ? 1 : $clog2(RESET_CYCLES + 1);

    logic [COUNTER_WIDTH-1:0] counter = '0;

    always_ff @(posedge clk) begin
        if (counter < RESET_CYCLES)
            counter <= counter + 1'b1;
    end

    assign reset = (counter < RESET_CYCLES);
endmodule

`default_nettype wire
