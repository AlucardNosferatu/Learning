----------------------------------------------------------------------------------
-- Company: SUSTech
-- Engineer: Scrooge
-- 
-- Create Date: 2017/03/27 15:21:00
-- Design Name: 
-- Module Name: tb_counter - Behavioral
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
use IEEE.STD_LOGIC_UNSIGNED.ALL;
use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity counter_tbw is
--  Port ( );
end counter_tbw;

architecture behavior of counter_tbw is
--component declaration for the Unit Under Test (UUT)
component counter
port(
    clock :in std_logic;
    reset :in std_logic;
    direction :in std_logic;
    count_out :out std_logic_vector(3 downto 0)
    );
end component;
--Inputs
signal clock :std_logic :='0';--:=是变量赋值，信号赋值要用<=
signal reset :std_logic :='0';
signal direction :std_logic :='0';
--Outputs
signal count_out :std_logic_vector(3 downto 0);
--clock period definitions
constant clock_period :time :=40ns;
begin
--Instantiate the Unit Under Test (UUT)
uut:counter port map(
    clock => clock,
    reset => reset,
    direction => direction,
    count_out => count_out
    );
--clock process definitions
clock_process:process
begin
    clock <='0';
    wait for clock_period/2;
    clock <='1';
    wait for clock_period/2;
end process;
--reset process definitions
reset_process:process
begin
    reset <='1';
    for i in 1 to 2 loop
    wait until clock='1';
    end loop;
    reset <='0';
    wait;
end process;
--stimulus process
stim_proc:process
begin
    direction <='1';
    wait for 1400ns;
    direction <='0';
    wait for 800ns;
    direction <='1';
    wait;
end process;
end;
