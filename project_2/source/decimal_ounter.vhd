----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 2017/04/03 00:11:54
-- Design Name: 
-- Module Name: decimal_ounter - if_arch
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
use IEEE.STD_LOGIC_1164.ALL;
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

architecture if_arch of decimal_counter is
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
process(d1_reg,d10_reg,d100_reg)
begin
d10_next <= d10_reg;
d100_next <= d100_reg;
if d1_reg /= 9 then
    d1_next <= d1_reg+1;
else
    d1_next <= "0000";
    if d10_reg/=9 then
        d10_next <= d10_reg+1; 
    else
        d10_next <= "0000";
        if d100_reg/=9 then
            d100_next <= d100_reg+1;
        else
            d100_next <= "0000";
        end if;
    end if;
end if;
end process;
d1      <= d1_reg;
d10     <= d10_reg;
d100    <= d100_reg;
end if_arch;