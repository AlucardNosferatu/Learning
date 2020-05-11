clear all

a=2;%电流环半径

I=500;%环电流大小

C=I/(4*pi);%归并常数

N=50;%电流环分段数

ym=5;%场域范围

zm=5;%场域范围

y=linspace(-ym,ym,20);%y轴20等分

z=linspace(-zm,zm,20);%z轴20等分

theta0=linspace(0,2*pi,N+1);%环的圆周角分段

theta1=theta0(1:N);%起点

x1=a*cos(theta1);%环分段矢量起始坐标

y1=a*sin(theta1);%环分段矢量起始坐标

theta2=theta0(2:N+1);%终点

x2=a*cos(theta2);%环分段矢量终止坐标

y2=a*sin(theta2);%环分段矢量终止坐标

zc1=1;%环分段矢量中点坐标分量

zc2=-1;

xc=(x2+x1)./2;%环分段矢量中点坐标分量

yc=(y2+y1)./2;%环分段矢量中点坐标分量

dlz=0;%环分段长度dl分量

dlx=x2-x1;%环分段长度dl分量

dly=y2-y1;%环分段长度dl分量

NGx=20;%网格线数

NGy=20;%网格线数

Hy1=zeros(20);

Hz1=zeros(20);

Hy2=zeros(20);

Hz2=zeros(20);

Hy=zeros(20);

Hz=zeros(20);

for i=1:NGy

for j=1:NGx

rx=0-xc;

ry=y(j)-yc;

rz1=z(i)-zc1;

rz2=z(i)-zc2;

 

r31=sqrt(rx.^2+ry.^2+rz1.^2).^3;

r32=sqrt(rx.^2+ry.^2+rz2.^2).^3;

dlXr_y1=dlz.*rx-dlx.*rz1;

dlXr_y2=dlz.*rx-dlx.*rz2;

dlXr_z=dlx.*ry-dly.*rx;

Hy1(i,j)=sum(C.*dlXr_y1./r31);

Hz1(i,j)=sum(C.*dlXr_z./r31);

Hy2(i,j)=sum(C.*dlXr_y2./r32);

Hz2(i,j)=sum(C.*dlXr_z./r32);

Hy(i,j)=Hy1(i,j)+Hy2(i,j);

Hz(i,j)=Hz1(i,j)+Hz2(i,j);

H1=(Hy1.^2+Hz1.^2).^0.5;

H2=(Hy2.^2+Hz2.^2).^0.5;

end

end

quiver(y,z,Hy1,Hz1);

hold on

quiver(y,z,Hy2,Hz2);

hold on

axis([-5,5,-5,5]);

plot(2,1,'ro',-2,1,'bo'),

plot(2,-1,'ro',-2,-1,'bo'),

xlabel('y'),

ylabel('z'),

hold on;                               

title('两个等流同径导电环磁场的矢量分布图  11210112 林昊波','fontsize',15);%绘出标题                                      

mesh(y,z,H1+H2);

axis([-5,5,-5,5,0,700])

xlabel('y'),

ylabel('z'),

zlabel('H');

hold on;                               

title('两个等流同径导电环磁场的强度分布图  11210112 林昊波','fontsize',15);%绘出标题                                      

theta=[0 20 40 60 80 100 120 140 160 180].*pi/180;

ys1=2*cos(theta);

zs1=2*sin(theta);

ys2=2*cos(-theta);

zs2=2*sin(-theta);

streamline(y,z,Hy,Hz,ys1,zs1);

streamline(y,z,-Hy,-Hz,ys1,zs1);

streamline(y,z,Hy,Hz,ys2,zs2);

streamline(y,z,-Hy,-Hz,ys2,zs2);

xlabel('y'),

ylabel('z');

hold on;                               

title('两个等流同径导电环磁场的等势分布图  11210112 林昊波','fontsize',15);%绘出标题                                      
