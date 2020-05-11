----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 2017/04/03 22:32:26
-- Design Name: 
-- Module Name: tb_decimal_counter - behavior
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

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity decimal_counter_tbw is
--  Port ( );
end decimal_counter_tbw;

architecture behavior of decimal_counter_tbw is
component decimal_counter
port(
    CLK     :in     std_logic;
    RESET   :in     std_logic;
    D1      :out    std_logic_vector(3 downto 0);
    D10     :out    std_logic_vector(3 downto 0);
    D100    :out    std_logic_vector(3 downto 0)
    );
end component;
signal CLK      :   std_logic := '0';
signal RESET    :   std_logic := '0';
--Outputs
signal D1           :   std_logic_vector(3 downto 0);
signal D10          :   std_logic_vector(3 downto 0);
signal D100         :   std_logic_vector(3 downto 0);
constant CLK_period :   time := 5ns;
begin
uut: decimal_counter port map(
CLK => CLK,
RESET => RESET, 
D1      => D1,
D10     => D10,
D100    => D100
);
CLK_process:process
begin
CLK<='0';
wait for CLK_period/2;
CLK<='1';
wait for CLK_period/2;
end process;
RESET_process:process
begin
RESET<='1';
wait for CLK_period/2;
RESET<='0';
wait;
end process;
end behavior;
