clear;

clc;

 

figure(1)

k=9e9;

Q=8e-9;

xm=5;

ym=5;

x=linspace(-xm,xm,100);

y=linspace(-ym,ym,100);

[X,Y]=meshgrid(x,y);

R1=sqrt((X+sqrt(3)).^2+(Y+1).^2);

V1=k*Q./R1;

R2=sqrt((X-sqrt(3)).^2+(Y+1).^2);

V2=k*Q./R2;

R3=sqrt(X.^2+(Y-2).^2);

V3=k*Q./R3;

V=V1+V2+V3;

mesh(X,Y,V);

hold on;

title({'真空中单个点电荷电场的电位分布图';'作者：林昊波 学号：11210112'},'fontsize',20);

xlabel('X轴(单位:m)','fontsize',20);

ylabel('Y轴(单位:m)','fontsize',20);

 

figure(2)

Vmin=0;

Vmax=2000;

Veq=linspace(Vmin,Vmax,1000);

contour(X,Y,V,Veq);

grid on

hold on

plot(0,2,'o','MarkerSize',12)

plot(-sqrt(3),-1,'o','MarkerSize',12)

plot(sqrt(3),-1,'o','MarkerSize',12)

title({'真空中单个点电荷电场的等电位线';'作者：林昊波 学号：11210112'},'fontsize',20);

xlabel('X轴(单位:m)','fontsize',20);

ylabel('Y轴(单位:m)','fontsize',20);

 

figure(3)

[Ex,Ey]=gradient(-V);

del_theta=10;

theta=(0:del_theta:360).*pi/180;

xs=0.004*cos(theta);

ys=0.004*sin(theta);

streamline(X,Y,Ex,Ey,xs,ys+2)

hold on

streamline(X,Y,Ex,Ey,xs+sqrt(3),ys-1)

hold on

streamline(X,Y,Ex,Ey,xs-sqrt(3),ys-1)

grid on

hold on

contour(X,Y,V,Veq);

plot(0,2,'o','MarkerSize',12)

plot(-sqrt(3),-1,'o','MarkerSize',12)

plot(sqrt(3),-1,'o','MarkerSize',12)

title({'真空中单个点电荷电场的等电位线和电力线（用光滑连续曲线表示）';'作者：林昊波 学号：11210112'},'fontsize',12);

xlabel('X轴(单位:m)','fontsize',12);

ylabel('Y轴(单位:m)','fontsize',12);

 

figure(4)

E=sqrt(Ex.^2+Ey.^2);

Ex=Ex./E;

Ey=Ey./E;

quiver(X,Y,Ex,Ey);

hold on;

contour(X,Y,V,Veq);

title({'真空中单个点电荷电场的等电位线和电力线（用归一化箭头表示）';'作者：林昊波 学号：11210112'},'fontsize',12);

xlabel('X轴(单位:m)','fontsize',12);

ylabel('Y轴(单位:m)','fontsize',12);
