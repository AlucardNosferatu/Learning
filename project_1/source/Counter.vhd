----------------------------------------------------------------------------------
-- Company: SUSTech
-- Engineer: Scrooge
-- 
-- Create Date: 2017/03/27 14:19:41
-- Design Name: 
-- Module Name: Counter - Behavioral
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
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;
-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity Counter is
    port ( clock : in STD_LOGIC;
           reset : in STD_LOGIC;
           direction : in STD_LOGIC;
           count_out : out STD_LOGIC_VECTOR (3 downto 0));
end Counter;

architecture Behavioral of Counter is--下方初始化电路存在的信号和变量
signal count_in, count_in_next: std_logic_vector(3 downto 0); --定义信号count_in和count_in_next，数据类型为逻辑矢量
signal delay, delay_next: std_logic_vector(24 downto 0);
begin
process(reset,clock)--重置时钟,输入信号reset和clock，下一个begin到end为止顺序执行
begin
if reset='1' then
delay <=(others=>'0');--dalay各位赋值为0
count_in <=(others=>'0');
elsif clock='1' and clock'event then--时钟信号发生改变且时钟信号为1的时候（上升沿）
delay <=delay_next;
count_in <=count_in_next;
end if;
end process;
delay_next <=delay+1;--在这里完成计数功能
count_in_next <=count_in+1 when delay=0 and direction='1'else
                count_in-1 when delay=0 and direction='0'else
                count_in;--论缩进和封号对长语句的意义
count_out<=count_in;
end Behavioral;
