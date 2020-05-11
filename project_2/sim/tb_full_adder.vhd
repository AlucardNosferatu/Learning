----------------------------------------------------------------------------------
-- Company: SUSTech
-- Engineer: Scrooge
-- 
-- Create Date: 2017/03/30 12:00:41
-- Design Name: 
-- Module Name: tb_full_adder - Behavioral
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

entity full_adder_tbw is
--  Port ( );
end full_adder_tbw;
architecture behavior of full_adder_tbw is
component full_adder
port(
    A :in std_logic;
    B :in std_logic;
    Cin :in std_logic;
    Cout :out std_logic;
    Sum :out std_logic
    );
end component;
signal A    :std_logic :='0';--:=是变量赋值，信号赋值要用<=
signal B    :std_logic :='0';
signal Cin  :std_logic :='0';
signal Cout :std_logic;
signal Sum  :std_logic;
constant A_period   :time :=20ns;
constant B_period   :time :=40ns;
constant Cin_period :time :=40ns;
begin
uut:full_adder port map(
    A       => A,
    B       => B,
    Cin     => Cin,
    Cout    => Cout,
    Sum     => Sum 
    );    
A_process:process
begin
    A <='1';
    wait for A_period/2;
    A <='0';
    wait for A_period/2;
end process;
B_process:process
begin
    B <='0';
    wait for B_period/2;
    B <='1';
    wait for B_period/2;
end process;
Cin_process:process
begin
    Cin <='0';
    wait for Cin_period/4;
    Cin <='1';
    wait for Cin_period/4;
    Cin <='0';
    wait for Cin_period/2;
end process;
end;
