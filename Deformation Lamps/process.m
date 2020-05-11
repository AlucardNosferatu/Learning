clear;
clc;
d=imread('sample-2.gif');
dur=length(imfinfo('sample-2.gif'));
for i=1:dur
    mix(:,:,1,i)=d(:,:,1,i)-d(:,:,1,6);
end
imwrite(mix,'dout.gif','gif');
