clear;%清除内存

clc;%清理屏幕

 

figure(1)%图片一

k=9e9;%真空介电系数

Q=1e-9;%电荷量

xm=0.05;%横向分布区域

ym=0.05;%纵向分布区域

x=linspace(-xm,xm,100);%80等分区域得横坐标

y=linspace(-ym,ym,100);%80等分区域得纵坐标

[X,Y]=meshgrid(x,y);%得到空间格子

R1=sqrt((X+0.01).^2+Y.^2);%与点电荷1的距离

V1=k*Q./R1;%点电荷1的电位分布

R2=sqrt((X-0.01).^2+Y.^2);%与点电荷2的距离

V2=k*Q./R2;%点电荷2的电位分布

V=V1+V2;%总的电位分布

mesh(X,Y,V);

hold on;

title({'真空中两个等量同号点电荷电场的电位分布图';' 作者：林昊波 学号：11210112'},'fontsize',20);

xlabel('X轴(单位:m)','fontsize',20);

ylabel('Y轴(单位:m)','fontsize',20);

 

figure(2)

Vmin=0;

Vmax=10000;

Veq=linspace(Vmin,Vmax,500);

contour(X,Y,V,Veq);

grid on

hold on

plot(0,0,'o','MarkerSize',12)

title({'真空中两个等量同号点电荷电场的等电位线';' 作者：林昊波 学号：11210112'},'fontsize',20);

xlabel('X轴(单位:m)','fontsize',20);

ylabel('Y轴(单位:m)','fontsize',20);

 

figure(3)

[Ex,Ey]=gradient(-V);

del_theta=20;

theta=(20:del_theta:340).*pi/180;

theta2=(200:del_theta:520).*pi/180;

xs=0.004*cos(theta);

ys=0.004*sin(theta);

xs2=0.004*cos(theta2);

ys2=0.004*sin(theta2);

streamline(X,Y,Ex,Ey,xs-0.01,ys)

hold on

streamline(X,Y,Ex,Ey,xs2+0.01,ys2)

grid on

hold on

contour(X,Y,V,Veq);

plot(0,0,'o','MarkerSize',12)

title({'真空中两个等量同号点电荷电场的等电位线和电力线（用光滑连续曲线表示）';' 作者：林昊波 学号：11210112'},'fontsize',20);

xlabel('X轴(单位:m)','fontsize',12);

ylabel('Y轴(单位:m)','fontsize',12);

 

figure(4)

E=sqrt(Ex.^2+Ey.^2);

Ex=Ex./E;

Ey=Ey./E;

quiver(X,Y,Ex,Ey);

hold on;

contour(X,Y,V,Veq);

title({'真空中两个等量同号点电荷电场的等电位线和电力线（用归一化箭头表示）';' 作者：林昊波 学号：11210112'},'fontsize',20);

xlabel('X轴(单位:m)','fontsize',12);

ylabel('Y轴(单位:m)','fontsize',12);
