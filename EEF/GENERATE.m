%单一微元划分情形的图形生成函数

function [Vdivide,E,Ex,Ey]=GENERATE(divide,nofigure)%参数divide为线电荷划分段数

%初始化物理参数

k=9e9;%为1/(4*π*ε0)的约化系数

Rho=1e-9;%线电荷密度

ldivide=2/divide;%划分后微元对应线电荷长度

Qdivide=ldivide*Rho;%划分后微元的电荷量

%初始化空间坐标

xm=2;%空间X轴方向范围从-2到2

ym=2;%空间Y轴方向范围从-2到2

x=linspace(-xm,xm,200);%空间X轴方向范围200等分成有限个点（有限元处理）

y=linspace(-ym,ym,200);%空间Y轴方向范围200等分成有限个点（有限元处理）

[X,Y]=meshgrid(x,y);%将分别记录有限个点坐标的两个一维向量x和y转化为矩阵X和Y

%绘制电位分布图

figure%将以下内容绘制到第一幅图（电位分布）上

R=sqrt((X+1).^2+Y.^2);%求出场点与源点的距离（第一个源点位于最左端）

Vdivide=k*Qdivide./R;%从最左端第一个电荷微元开始计算其在场点的电位

for i=1:divide%一共有divide个电荷微元，因此循环叠加电位divide次

R=sqrt((X+1-(i*ldivide)).^2+Y.^2);%计算新的电荷微元到场点的距离

Vdivide=Vdivide+k*Qdivide./R;%算出新的微源给出的电位并累加到电位总值上

end%累加完divide次后所有微元在该点的电位都得到累加，循环结束

mesh(X,Y,Vdivide);%根据坐标和对应电位的矩阵作图

hold on%接着在同一图里绘制下述内容

title(sprintf('%d等分线电荷在空间中的电位分布\n作者：林昊波 学号：11210112', divide),'fontsize',20);%图片的标题和副标题以及对应字体尺寸

xlabel('X轴(单位:m)','fontsize',20);%X轴

ylabel('Y轴(单位:m)','fontsize',20);%Y轴

if nofigure==1

    close all;

end

%求出等势线的参考值

Vmin=0;%最低电势参考值

Vmax=100;%最高电势参考值

Veq=linspace(Vmin,Vmax,60);%将上述区间60等分取60个数值作为电势参考值

%绘制等势线图

figure%将以下内容绘制到第二幅图（等势线图）上

xm=2;%空间X轴方向范围从-2到2

ym=0.5;%空间Y轴方向范围从-0.5到0.5

x=linspace(-xm,xm,200);%空间X轴方向范围200等分成有限个点（有限元处理）

y=linspace(-ym,ym,200);%空间Y轴方向范围200等分成有限个点（有限元处理）

[X,Y]=meshgrid(x,y);%将分别记录有限个点坐标的两个一维向量x和y转化为矩阵X和Y

contour(X,Y,Vdivide,Veq);%根据参考电势值Veq、场点坐标及场点电位作等势线图

grid on%给等势线图添加网格

hold on%接着在同一图里绘制下述内容

title(sprintf('%d等分线电荷在空间中的等势线图\n作者：林昊波 学号：11210112', divide),'fontsize',20);%图片的标题和副标题以及对应字体尺寸

xlabel('X轴(单位:m)','fontsize',20);%X轴

ylabel('Y轴(单位:m)','fontsize',20);%Y轴

if nofigure==1

    close all;

end

%绘制电力线图

figure%将以下内容绘制到第三幅图（电力线图）上

xm=2;%空间X轴方向范围从-2到2

ym=2;%空间Y轴方向范围从-2到2

x=linspace(-xm,xm,200);%空间X轴方向范围200等分成有限个点（有限元处理）

y=linspace(-ym,ym,200);%空间Y轴方向范围200等分成有限个点（有限元处理）

[X,Y]=meshgrid(x,y);%将分别记录有限个点坐标的两个一维向量x和y转化为矩阵X和Y

[Ex,Ey]=gradient(-Vdivide);%利用公式E=-▽V求出E的x方向和y方向分量

del_theta=20;%设定设定流线图的径向疏密程度（越大越稀疏）

theta=(0:del_theta:360).*pi/180;%把疏密程度转化为角度值

xs=0.005*cos(theta)-1;%设定绘制流线图的起点（线电荷最左端开始）横坐标

ys=0.005*sin(theta);%设定绘制流线图的起点（线电荷最左端开始）纵坐标

hold on%接着在同一图里绘制下述内容

for i=1:(divide-1)%一共进行divide次循环（电力线）生成

    xs=xs+ldivide;%移动到下一段电荷微元

    streamline(X,Y,Ex,Ey,xs,ys)%生成该段电荷微元的电力线

    hold on%接着在同一图里绘制下述内容

end%当divide段电荷微元全部生成（电力线）完毕后结束循环

grid on%给等势线图添加网格

hold on%接着在同一图里绘制下述内容

title(sprintf('%d等分线电荷在空间中的电力线图\n作者：林昊波 学号：11210112', divide),'fontsize',20);%图片的标题和副标题以及对应字体尺寸

xlabel('X轴(单位:m)','fontsize',20);%X轴

ylabel('Y轴(单位:m)','fontsize',20);%Y轴

if nofigure==1

    close all;

end

%绘制电力线图（归一化箭头）

figure%将以下内容绘制到第四幅图（电力线图（归一化箭头））上

E=sqrt(Ex.^2+Ey.^2);%根据电场Ex和Ey分量求出模值E

Ex=Ex./E;%分别将电场矢量横（纵）坐标归一化

Ey=Ey./E;%分别将电场矢量（横）纵坐标归一化

quiver(X,Y,Ex,Ey);%根据归一化电场矢量绘制箭头图（电力线）

hold on;%接着在同一图里绘制下述内容

contour(X,Y,Vdivide,Veq);%根据参考电势值Veq、场点坐标及场点电位作等势线图

title(sprintf('%d等分线电荷在空间中的电力线图（归一化箭头）\n作者：林昊波 学号：11210112', divide),'fontsize',20);%图片的标题和副标题以及对应字体尺寸

xlabel('X轴(单位:m)','fontsize',20);%X轴

ylabel('Y轴(单位:m)','fontsize',20);%Y轴

if nofigure==1

    close all;

end
