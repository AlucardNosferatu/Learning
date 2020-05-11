----------------------------------------------------------------------------------
-- Company: SUSTech
-- Engineer: Scrooge
-- 
-- Create Date: 2017/03/30 13:18:17
-- Design Name: 
-- Module Name: sig_var_tbw - Behavioral
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

entity sig_var_tbw is
--  Port ( );
end sig_var_tbw;
architecture behavior of sig_var_tbw is
component sig_var
port(
    X       :in     std_logic;
    Y       :in     std_logic;
    Z       :in     std_logic;
    Res1    :out    std_logic;
    Res2    :out    std_logic
    );
end component;
signal X    :std_logic :='0';--:=是变量赋值，信号赋值要用<=
signal Y    :std_logic :='0';
signal Z    :std_logic :='0';
signal Res1 :std_logic;
signal Res2 :std_logic;
constant X_period   :time :=80ns;
constant Y_period   :time :=40ns;
constant Z_period   :time :=20ns;
begin
uut:sig_var port map(
    X       => X,
    Y       => Y,
    Z       => Z,
    Res1    => Res1,
    Res2    => Res2 
    );    
X_process:process
    begin
        X <='0';
        wait for X_period/2;
        X <='1';
        wait for X_period/2;
    end process;
Y_process:process
    begin
        Y <='0';
        wait for Y_period/2;
        Y <='1';
        wait for Y_period/2;
    end process;
Z_process:process
    begin
        Z <='0';
        wait for Z_period/2;
        Z <='1';
        wait for Z_period/2;
    end process;
end;
