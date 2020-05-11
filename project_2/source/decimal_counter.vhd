----------------------------------------------------------------------------------
-- Company: SUSTech
-- Engineer: Scrooge
-- 
-- Create Date: 2017/03/30 14:11:06
-- Design Name: 
-- Module Name: decimal_counter - Behavioral
-- Project Name: 
-- Target Devices: 
-- Tool Versions: 
-- Description: 
-- 
-- Dependencies: 
-- 
-- Revision:
-- Revision 0.01 - File Created
-- Additional Comments:
-- 
----------------------------------------------------------------------------------


library IEEE;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity decimal_counter is
    Port ( CLK : in STD_LOGIC;
           RESET : in STD_LOGIC;
           D1 : out STD_LOGIC_VECTOR (3 downto 0);
           D10 : out STD_LOGIC_VECTOR (3 downto 0);
           D100 : out STD_LOGIC_VECTOR (3 downto 0));
end decimal_counter;

architecture concurrent_arch of decimal_counter is
signal d1_reg, d10_reg, d100_reg: std_logic_vector(3 downto 0);
signal d1_next, d10_next, d100_next: std_logic_vector(3 downto 0);
begin
process(CLK,RESET)is
begin
if RESET='1'then
d1_reg <= "0000";
d10_reg <= "0000";
d100_reg <= "0000";
elsif CLK'event and CLK='1'then
d1_reg <= d1_next;
d10_reg <= d10_next;
d100_reg <= d100_next;
end if;
end process;
d1_next <= "0000" when d1_reg = 9 else d1_reg+1;
d10_next <= "0000" when (d1_reg = 9 and d10_reg=9)
    else
    d10_reg+1 when d1_reg=9
        else
        d10_reg;
d100_next <= "0000" when (d1_reg = 9 and d10_reg=9 and d100_reg=9)
    else
    d100_reg+1 when(d1_reg = 9 and d10_reg=9)
        else
        d100_reg;
d1      <= d1_reg;
d10     <= d10_reg;
d100    <= d100_reg;
end architecture concurrent_arch;
