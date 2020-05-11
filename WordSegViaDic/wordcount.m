function []=wordcount()
%思路：中文词频统计涉及到对“词语”的判断，需要导入词典或编写判断规则，很复杂。
%最简单的办法是直接统计英文词频，并由空格直接划分词语。然后再翻译即可得到中文词频。

%从官方网站上下载的pdf，转成reportfulltext.txt，存到workspace进行操作 全文共25003个字符。

clc;
clear;
report=fileread('reportfulltext.txt'); %读入全文
report=regexprep(report,'\W',' '); %不是字符的，都转换为空格。主要是去除标点符号
report=lower(report); %变成小写
words=regexp(report,' ','split')'; %根据空格分隔为单词cell

%至此每个单词都拿出来了

rank = tabulate(words); %rank是三列向量，包括名称，出现次数和百分比
ans=sortrows(rank,-2); %只根据第二列进行排序 -2表示降序

xlswrite('results',ans);%输出为excel文件
end
