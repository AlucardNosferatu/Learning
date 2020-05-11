function a=nn(input1,input2,input3,link1,link2,link3,b1,b2,b3)
% input只针对输入层每一个（一共三个）神经元，为一维矢量
% link有两端，两端可能组合3*3，用二维矩阵表示
b(1,:)=b1;
b(2,:)=b2;
b(3,:)=b3;
input(1,:)=input1;
input(2,:)=input2;
input(3,:)=input3;
link(1,:,:)=link1;
link(2,:,:)=link2;
link(3,:,:)=link3;

for i=1:3
    if i==1;
        for j=1:3
            a(1,j)=neuron(input(j,:),link(i,j,:),b(i,j));
            % input(j,:)	输入层每个神经元各自的输入（每个神经元三个不相同的输入，每个神经元的输入各不相同，一共九个输入）
            % link(i,j,:)   i=1时为link(1,j,k)，为输入到输入层神经元的连接权重，i为层数，j为同一层各个神经元的编号，向量长度为3
            % b(i,j)        i=1时为b(1,j)，为输入层各个神经元的偏置
        end
    else
        for j=1:3
            a(i,j)=neuron(a(i-1,:),link(i,j,:),b(i,j));
        end
    end
end

p=softmax(a,link,b);
% 采用softmax layer作为输出层

% 以下是softmax函数的内容
% function p=softmax(a,link,bias)
% for i=1:3
%     z(i)=dot(a(2,:),link(3,i,:))+bias(3,i);
% end
% output=exp(z);
% ot=0;
% for i=1:3
%     ot=ot+output(i);
%     if i==3
%         p(i)=output(i)/ot;
%         p(i-1)=output(i-1)/ot;
%         p(i-2)=output(i-2)/ot;
%     end
% end


% 以下是neuron函数的内容
% function output=neuron(input,link,bias)
% z=input.*link+bias;
% output=1./(1.+exp(-z));
% 该神经元采用sigmoid函数作为激励函数
