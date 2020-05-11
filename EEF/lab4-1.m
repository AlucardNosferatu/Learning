clear all
m=0.02;%质量
q=1.6e-2;%电荷
dt=0.00005;%时间间隔
t=0:dt:3;%时间跨度

for j=1:8%针对八个粒子
vx(j,:)=linspace(0,0,length(t));%速度
vy(j,:)=vx(j,:);
vz(j,:)=vx(j,:);
vx(j,1)=0.1*sin(j*pi/4);%初速
vy(j,1)=0.1*cos(j*pi/4);
vz(j,1)=10;

rx(j,:)=linspace(0,0,length(t));%位置坐标
ry(j,:)=rx(j,:);
rz(j,:)=rx(j,:);

Fx(j,:)=linspace(0,0,length(t));%受力分量
Fy(j,:)=Fx(j,:);
Fz(j,:)=Fx(j,:);

ax(j,:)=linspace(0,0,length(t));%加速分量
ay(j,:)=ax(j,:);
az(j,:)=ax(j,:);
end

Ex=0;%电场分量
Ey=0;
Ez=0;
Bx=0;%磁场分量
By=0;
Bz=8;

for j=1:8%八个粒子
for i=1:(length(t)-1)%每个时刻
Fx(j,i)=q*Ex+q*(vy(j,i)*Bz-vz(j,i)*By);%库仑力加洛伦兹力
Fy(j,i)=q*Ey+q*(vz(j,i)*Bx-vx(j,i)*Bz);
Fz(j,i)=q*Ez+q*(vx(j,i)*By-vy(j,i)*Bx);
ax(j,i)=Fx(j,i)/m;
ay(j,i)=Fy(j,i)/m;
az(j,i)=Fz(j,i)/m;
vx(j,i+1)=vx(j,i)+ax(j,i)*dt;
vy(j,i+1)=vy(j,i)+ay(j,i)*dt;
vz(j,i+1)=vz(j,i)+az(j,i)*dt;
rx(j,i+1)=rx(j,i)+vx(j,i)*dt;
ry(j,i+1)=ry(j,i)+vy(j,i)*dt;
rz(j,i+1)=rz(j,i)+vz(j,i)*dt;
end
end
figure
for j=1:8%一次画出一个粒子的轨迹
plot3(rx(j,:),ry(j,:),rz(j,:));
hold on%然后叠加
end
grid;
title('8个带电粒子在磁场中的磁聚焦现象');
xlabel('X轴','fontsize',12);
ylabel('Y轴','fontsize',12);
zlabel('Z轴','fontsize',12);
