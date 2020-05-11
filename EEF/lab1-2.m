clear;

clc;

 

figure(1)

k=9e9;

Q1=5e-9;

Q2=-5e-9;

xm=5;

ym=5;

x=linspace(-xm,xm,80);

y=linspace(-ym,ym,80);

[X,Y]=meshgrid(x,y);

R1=sqrt((X+2).^2+Y.^2);

V1=k*Q1./R1;

R2=sqrt((X-2).^2+Y.^2);

V2=k*Q2./R2;

V=V1+V2;

mesh(X,Y,V);

hold on;

title({'真空中两个等量异号电荷场的电位分布图';'作者：林昊波 学号：11210112'},'fontsize',20);

xlabel('X轴(单位:m)','fontsize',20);

ylabel('Y轴(单位:m)','fontsize',20);

 

figure(2)

Vmin=-200;

Vmax=200;

Veq=linspace(Vmin,Vmax,1000);

contour(X,Y,V,Veq);

grid on

hold on

plot(-2,0,'o','MarkerSize',5)

plot(2,0,'o','MarkerSize',5)

title({'真空中两个等量异号电荷场的等电位线';'作者：林昊波 学号：11210112'},'fontsize',20);

xlabel('X轴(单位:m)','fontsize',20);

ylabel('Y轴(单位:m)','fontsize',20);

 

figure(3)

[Ex,Ey]=gradient(-V);

del_theta=1;

theta=(0:del_theta:360).*pi/180;

xs=0.004*cos(theta);

ys=0.004*sin(theta);

streamline(X,Y,Ex,Ey,xs-2,ys)

hold on

streamline(X,Y,-Ex,-Ey,xs+2,ys)

grid on

hold on

contour(X,Y,V,Veq);

plot(-2,0,'o','MarkerSize',5)

plot(2,0,'o','MarkerSize',5)

title({'真空中两个等量异号电荷场的等电位线和电力线（用光滑连续曲线表示）';'作者：林昊波 学号：11210112'},'fontsize',20);

xlabel('X轴(单位:m)','fontsize',12);

ylabel('Y轴(单位:m)','fontsize',12);

 

figure(4)

E=sqrt(Ex.^2+Ey.^2);

Ex=Ex./E;

Ey=Ey./E;

quiver(X,Y,Ex,Ey);

hold on;

contour(X,Y,V,Veq);

title({'真空中两个等量异号电荷场的等电位线和电力线（用归一化箭头表示）';'作者：林昊波 学号：11210112'},'fontsize',20);

xlabel('X轴(单位:m)','fontsize',12);

ylabel('Y轴(单位:m)','fontsize',12);
