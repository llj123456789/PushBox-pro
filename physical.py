#滑动摩擦系数
u=0.006
#中立
g=9.8
import math


def friction_force(m):#滑动摩檫力
    return m * g * u
def friction_force_a():#滑动摩擦力给的加速度
    return -g * u
def setV(obj1,obj2):#碰撞后的速度#默认弹性碰撞
    Vy1 = obj1.v*math.sin(obj1.angle)
    Vx1 = obj1.v*math.cos(obj1.angle)
    Vy2 = obj2.v*math.sin(obj2.angle)
    Vx2 = obj2.v*math.cos(obj2.angle)
    m1=obj1.m
    m2=obj2.m
    vy1=(Vy1*(m1-m2)+2*m2*Vy2)/(m1+m2)
    vy2=(Vy2*(m2-m1)+2*m1*Vy1)/(m1+m2)
    vx1=(Vx1*(m1-m2)+2*m2*Vx2)/(m1+m2)
    vx2=(Vx2*(m2-m1)+2*m1*Vx1)/(m1+m2)
    #print(vy1,vx1,vy1,vx2)
    obj1.v=math.sqrt(vx1**2+vy1**2)
    obj2.v=math.sqrt(vx2**2+vy2**2)
    if(vx1==0):
        if(vy1>0):
            obj1.angle=math.pi/2
        else:
            obj1.angle=-math.pi/2
    else:
        obj1.angle=math.atan(vy1/vx1)
        if(vx1<0):
            obj1.angle=obj1.angle+math.pi
    if(vx2==0):
        if(vy2>0):
            obj2.angle=math.pi/2
        else:
            obj2.angle=-math.pi/2
    else:
        obj2.angle=math.atan(vy2/vx2)
        if(vx2<0):
            obj2.angle=obj2.angle+math.pi
    obj1.stdAngle()
    obj2.stdAngle()
    
    