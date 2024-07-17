#Python大作业
#推箱子游戏
#2024年5月
#联系方式qq:2041584846
#游戏素材部分来源于网络和老师提供
import pygame
from physical import *
pi=math.pi

class Music:#音乐类
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.load("./music/back/girl_not_sad.mp3")
        pygame.mixer.music.set_volume(0.2)
    def playBackMusic(self):
        pygame.mixer.music.play()
    def setAudio(self,file):
        self.sound=pygame.mixer.Sound(file)
    def playAudio(self):
        self.sound.play()
    def stopAudio(self):
        self.sound.stop()

class Object:
    def __init__(self,ImageFile,type,label='',num=0,isMoveable=False,isVisible=True):#初始化对象，图片文件，对象类型，对象标签，对象编号
        self.image=pygame.image.load(ImageFile).convert_alpha()#单一图片加载
        self.image=pygame.transform.scale(self.image,(50,50))#图片SIZE可更改，此游戏位于方便统一设置成50*50
        self.rect=self.image.get_rect()
        self.visible=isVisible#是否可见
        self.num=num#对象编号，便于后续存储操作
        self.label=label#对象标签，便于后续操作
        self.isMoveable=isMoveable#是否可移动
        self.nowCanMove=isMoveable
        self.canBeDestroy=True
        self.type=type#对象类型
        self.imgleft=list()#存储图片列表
        self.imgright=list()
        self.imgup=list()
        self.imgdown=list()
        self.frameLEFT=0#帧数//用于控制图片加载
        self.frameRIGHT=0
        self.frameUP=0
        self.frameDOWN=0
        self.angle=0#角度//用于控制图片加载,和行进方向有关##O---------------------->x为极轴angle
        self.rect.x=0
        self.rect.y=0
        self.toward=0#移动方向 0 1 2 3 代表上下左右
        self.v=0#物体移动速度
        self.m=1#物体质量kg
        self.isPushed=False#是否被推动
        self.collisionList=list()#碰撞列表
        self.runtime=0#运行时间
        self.isEdge=False#是否在边缘
        self.isMoving=False#是否在移动
        self.transparent=False#是否透明#相对于墙
    def setDestroy(self,canBeDestroy):
        self.canBeDestroy=canBeDestroy
    def setPos(self,x,y):
        self.rect.x=x
        self.rect.y=y
    def getPos(self):
        return self.rect.x,self.rect.y
    def draw(self,screen):#绘制对象在屏幕上
        screen.blit(self.image,self.rect)
    def setvisible(self,visible):#设置是否可见
        self.visible=visible
    def isVisible(self):#返回是否可见
        return self.visible
    def setMoveable(self,moveable):
        self.isMoveable=moveable
    def isMoveable(self):
        return self.isMoveable
    def appendImgleft(self,img):
        self.imgleft.append(img)
        self.imgLenLeft=len(self.imgleft)
    def appendImgright(self,img):
        self.imgright.append(img)
        self.imgLenRight=len(self.imgright)
    def appendImgup(self,img):
        self.imgup.append(img)
        self.imgLenUp=len(self.imgup)
    def appendImgdown(self,img):
        self.imgdown.append(img)
        self.imgLenDown=len(self.imgdown)
    def setFrameUp(self):
        if(self.frameUP+1<self.imgLenUp):
            self.frameUP+=1
        else:
            self.frameUP=0
    def setFrameDown(self):
        if(self.frameDOWN+1<self.imgLenDown):
            self.frameDOWN+=1
        else:
            self.frameDOWN=0
    def setFrameLeft(self):
        if(self.frameLEFT+1<self.imgLenLeft):
            self.frameLEFT+=1
        else:
            self.frameLEFT=0
    def setFrameRight(self):
        if(self.frameRIGHT+1<self.imgLenRight):
            self.frameRIGHT+=1
        else:
            self.frameRIGHT=0 
    def stdAngle(self):
        if(self.angle>2*pi):
            self.angle=self.angle-2*pi
        if(self.angle<0):
            self.angle=2*pi+self.angle
    def isCollision(self,rect):#碰撞检测
        return self.rect.colliderect(rect)

class objectStore:#存储游戏对象
    def __init__(self,infoFile):
        self.background=list()
        self.road=list()
        self.wall=list()
        self.target=list()
        self.man=list()
        self.box=list()
        self.clear()
        f=open(infoFile)
        a=f.read().split("\n")
        for i in range(len(a)):
            type=("{}".format(a[i].split(':')[0]))
            num=int("{}".format(a[i].split(':')[1]))
            for j in range(num):
                if(type=='man'):
                    self.append(Object("./image/man/2.png","man",'M',j,True,True))
                if(type=='box'):
                    self.append(Object("./image/box/box0.gif","box","B{}".format(j),j,True,True))
    def append(self,object=Object):#添加对象到游戏对象列表
        if(object.type=="background"):
            self.background.append(object)
            object.num=len(self.background)-1#设置对象编号,and start from 0
            self.numOfBack=len(self.background)#记录背景对象数量,防止用len()函数多次调用
        elif(object.type=="road"):
            self.road.append(object)
            object.num=len(self.road)-1
            self.numOfRoad=len(self.road)
        elif(object.type=="wall"):
            self.wall.append(object)
            object.num=len(self.wall)-1
            self.numOfWall=len(self.wall)
        elif(object.type=="target"):
            self.target.append(object)
            object.num=len(self.target)-1
            self.numOfTarget=len(self.target)
        elif(object.type=="man"):
            self.man.append(object)
            self.numOfMan=len(self.man)
        elif(object.type=="box"):
            self.box.append(object)      
            self.numOfBox=len(self.box)  
    def pop(self,type):#删除对象
        if(type=="background"):
            self.background.pop()
        elif(type=="road"):
            self.road.pop()
        elif(type=="wall"):
            self.wall.pop()
        elif(type=="target"):
            self.target.pop()
    def clear(self):#清空对象列表
        self.background.clear()
        self.road.clear()
        self.wall.clear()
        self.target.clear()
        self.man.clear()
        self.box.clear()
    def put(self,object=Object,screen=None):#放置对象
        screen.blit(object.image,object.rect)

def distance(obj1=Object,obj2=Object):#计算两个对象之间的距离
    return math.sqrt((obj1.rect.x-obj2.rect.x)**2+(obj1.rect.y-obj2.rect.y)**2)
class Goal:#目标类
    def __init__(self,objS=objectStore):
        self.score=0   
        self.goal=objS.numOfTarget
    def judge(self,objS=objectStore):#判断是否胜利
        self.score=0
        for i in range(objS.numOfBox):
            for j in range(objS.numOfTarget):
                if(distance(objS.box[i],objS.target[j])<10):
                    self.score+=1
                    break
        if(self.score==self.goal):
            return True
        else:
            return False
    def getScore(self,objS=objectStore):
        self.score=0
        for i in range(objS.numOfBox):
            for j in range(objS.numOfTarget):
                if(distance(objS.box[i],objS.target[j])<10):
                    self.score+=1
                    break
        return self.score
        
#地图类：存储地图信息
#采用外部地图读取，便于地图绘制，当然也给出了地图设置函数，可内部设置地图
#由于游戏操作对象较少，并且地图信息不会改变，所以不需要存储地图对象，地图对象固定
#地图对象由地图文件加载，地图文件中的每个字符代表一个对象
#可自行设置地图文件，但是地图文件中的字符必须与游戏对象对应，否则无法加载，当然字符可更改,以获取初始position
#地图类中存储地图文件路径，便于后续操作
#地图元素与元素之间必须用|分隔，否则无法加载
class Map:
    def __init__(self):
        pass
    def load_map(self,mapFile):#加载地图文件，后续也可以再次更换地图
        try:
            self.path=mapFile#存储地图文件路径，便于后续再次操作
            f=open(mapFile)#文件读取操作
        except FileNotFoundError:
            print("Error: cannot open map file!!!",mapFile)#读取失败
            raise FileNotFoundError
        except Exception as e:
            print("Error: ",e)
            raise Exception
        else:
            self.map=f.read().split("\n")#得到列表，but every element is a string,代表每一行
            for i in range (len(self.map)):#change string to list
                self.map[i]=self.map[i].split('|')#split by '|'#a[x][y] is string，不建议修改
            f.close()#关闭文件`
            
    def set_map(self,r,c):#设置地图，可用于地图编辑器
        for i in range(r):
            for j in range (c):
                self.map[i][j]=input("Please input the map element:")
        #‘#’代表外墙，‘ ’代表路，‘*’代表目标，‘B’代表箱子，‘M’代表人物，‘@’代表内墙，初始位置
        #仅代表地图元素，不代表对象，对象由地图元素生成，并且以'|'分割,通过|a|之前的label(a)来确定对象位置，和对象是谁，a是每个元素独有的标号，不可重复
        #地图元素与元素之间必须用|分隔，否则无法加载，或者加载错误
    '''
    ps:
    目前游戏内定#'#'代表外墙，' '代表路，'*'代表目标,'B'代表箱子,'M'代表人物,'@'代表内墙，初始位置
    请在地图文件中按照规则设置地图，否则加载出错
    '''
    #drawMap一次绘制，因为地图元素不会改变，所以不需要重复绘制
    def drawMapFirst(self,objS=objectStore,screen=None):#指定物体存储库和屏幕，绘制地图，不包括人物和箱子(which is Moveable)
        self.r=len(self.map)#行数
        self.c=len(self.map[0])#列数
        for i in range(self.r):#i is row also is x
            for j in range(self.c):#j is column also is y
                #检查label
                if(self.map[i][j]==' '):#路
                    objS.append(Object("./image/road/road0.gif","road",' ',0,False,True))
                    objS.road[objS.numOfRoad-1].setPos(j*50,i*50)
                    objS.road[objS.numOfRoad-1].draw(screen)
                if(self.map[i][j]=='#'):#外墙
                    objS.append(Object("./image/back/back0.gif","background",'#',0,False,True))
                    objS.background[objS.numOfBack-1].setPos(j*50,i*50)
                    objS.background[objS.numOfBack-1].draw(screen)
                if(self.map[i][j]=='*'):#目标
                    objS.append(Object("./image/pos/pos0.gif","target",'*',0,False,True))
                    objS.target[objS.numOfTarget-1].setPos(j*50,i*50)
                    objS.target[objS.numOfTarget-1].draw(screen)
                if(self.map[i][j]=='@'):#wall
                    objS.append(Object("./image/wall/wall0.gif","wall","@",0,False,True))
                    objS.wall[objS.numOfWall-1].setPos(j*50,i*50)
                    objS.wall[objS.numOfWall-1].draw(screen)
                    objS.wall[objS.numOfWall-1].m=99999999999999999999999999
                for k in range(objS.numOfMan):
                    if(objS.man[k].label==self.map[i][j]):
                        objS.man[k].setPos(j*50,i*50)
                        objS.append(Object("./image/road/road0.gif","road",' ',0,False,True))
                        objS.road[objS.numOfRoad-1].setPos(j*50,i*50)
                        screen.blit(objS.man[0].image,objS.man[k].rect)#默认初始化人物在路上，并且以road0为背景
                        continue    
                for k in range(objS.numOfBox):
                    if(objS.box[k].label==self.map[i][j]):
                        objS.box[k].setPos(j*50,i*50)
                        objS.append(Object("./image/road/road0.gif","road",' ',0,False,True))
                        objS.road[objS.numOfRoad-1].setPos(j*50,i*50)
                        screen.blit(objS.box[0].image,objS.box[k].rect)#默认初始化箱子在路上，并且以road0为背景
                        continue  
    def drawMap(self,objS=objectStore,screen=None):#指定物体存储库和屏幕，绘制地图，不包括人物和箱子(which is Moveable)
        self.r=len(self.map)#行数
        self.c=len(self.map[0])#列数
        for i in range(objS.numOfBack):
            if(objS.background[i].isVisible()):
                objS.background[i].draw(screen)
        for i in range(objS.numOfWall):
            if(objS.wall[i].isVisible()):
                objS.wall[i].draw(screen)
        for i in range(objS.numOfRoad):
            if(objS.road[i].isVisible()):
                objS.road[i].draw(screen)
        for i in range(objS.numOfTarget):
            if(objS.target[i].isVisible()):
                objS.target[i].draw(screen)
        
                
class operation:#操作类
    def __init__(self):
        pass


def move(event,man,box,objS,map,screen):#移动函数,主控操作
#global man,objS,screen,box
    if event.type==pygame.KEYDOWN:
        man.v==5
        #print(man.angle)
        if event.key==pygame.K_j:#控制旋转方向
            man.angle-=pi/8
            man.stdAngle()
            if(man.rect.x>800-50):
                man.rect.x=800-50
            if(man.rect.x<0):
                man.rect.x=0
            if(man.rect.y>600-50):
                man.rect.y=600-50
            if(man.rect.y<0):
                man.rect.y=0 
            map.drawMap(objS,screen)
            if(man.angle>=pi/4 and man.angle<=3*pi/4):
                screen.blit(man.imgdown[man.frameDOWN],man.rect)
                man.setFrameDown()
            elif(man.angle>3*pi/4 and man.angle<=5*pi/4):
                screen.blit(man.imgleft[man.frameLEFT],man.rect)
                man.setFrameLeft()
            elif(man.angle>5*pi/4 and man.angle<=7*pi/4):
                screen.blit(man.imgup[man.frameUP],man.rect)
                man.setFrameUp()
            else:
                screen.blit(man.imgright[man.frameRIGHT],man.rect)
                man.setFrameRight()
            
        elif event.key==pygame.K_l:#控制旋转方向
            man.angle+=pi/8
            man.stdAngle()
            if(man.rect.x>800-50):
                man.rect.x=800-50
            if(man.rect.x<0):
                man.rect.x=0
            if(man.rect.y>600-50):
                man.rect.y=600-50
            if(man.rect.y<0):
                man.rect.y=0 
            map.drawMap(objS,screen)
            if(man.angle>=pi/4 and man.angle<=3*pi/4):
                man.setFrameDown()
                screen.blit(man.imgdown[man.frameDOWN],man.rect)
                
            elif(man.angle>3*pi/4 and man.angle<=5*pi/4):
                man.setFrameLeft()
                screen.blit(man.imgleft[man.frameLEFT],man.rect)
                
            elif(man.angle>5*pi/4 and man.angle<=7*pi/4):
                man.setFrameUp()
                screen.blit(man.imgup[man.frameUP],man.rect)
                
            else:
                man.setFrameRight()
                screen.blit(man.imgright[man.frameRIGHT],man.rect)
                
            
        elif event.key==pygame.K_i :#控制前进
            if(man.nowCanMove):
                man.stdAngle()
                movx=man.v*math.cos(man.angle)
                movy=man.v*math.sin(man.angle)
                #print(movx,movy)
                man.rect.x+=movx
                man.rect.y+=movy
                if(man.rect.x>800-50):
                    man.rect.x=800-50
                if(man.rect.x<0):
                    man.rect.x=0
                if(man.rect.y>600-50):
                    man.rect.y=600-50
                if(man.rect.y<0):
                    man.rect.y=0 
                map.drawMap(objS,screen)
                if(man.angle>=pi/4 and man.angle<=3*pi/4):
                    man.setFrameDown()
                    screen.blit(man.imgdown[man.frameDOWN],man.rect)
                    
                elif(man.angle>3*pi/4 and man.angle<=5*pi/4):
                    man.setFrameLeft()
                    screen.blit(man.imgleft[man.frameLEFT],man.rect)
                    
                elif(man.angle>5*pi/4 and man.angle<=7*pi/4):
                    man.setFrameUp()
                    screen.blit(man.imgup[man.frameUP],man.rect)
                    
                else:
                    man.setFrameRight()
                    screen.blit(man.imgright[man.frameRIGHT],man.rect)
            
                    
                
        elif event.key==pygame.K_k:#后退
            man.v=-man.v
            man.stdAngle()
            movx=man.v*math.cos(man.angle)
            movy=man.v*math.sin(man.angle)
            man.rect.x+=movx
            man.rect.y+=movy
            if(man.rect.x>800-50):
                man.rect.x=800-50
            if(man.rect.x<0):
                man.rect.x=0
            if(man.rect.y>600-50):
                man.rect.y=600-50
            if(man.rect.y<0):
                man.rect.y=0 
            map.drawMap(objS,screen)
            if(man.angle>=pi/4 and man.angle<=3*pi/4):
                screen.blit(man.imgdown[man.frameDOWN],man.rect)
                man.setFrameDown()
            elif(man.angle>3*pi/4 and man.angle<=5*pi/4):
                screen.blit(man.imgleft[man.frameLEFT],man.rect)
                man.setFrameLeft()
            elif(man.angle>5*pi/4 and man.angle<=7*pi/4):
                screen.blit(man.imgup[man.frameUP],man.rect)
                man.setFrameUp()
            else:
                screen.blit(man.imgright[man.frameRIGHT],man.rect)
                man.setFrameRight()
            man.v=-man.v
            
        elif event.key==pygame.K_LEFT or event.key==pygame.K_a:#移动
            man.angle=pi
            man.stdAngle()
            movx=man.v*math.cos(man.angle)
            movy=man.v*math.sin(man.angle)
            man.rect.x+=movx
            man.rect.y+=movy
            map.drawMap(objS,screen)
            man.stdAngle()
            if(man.rect.x>800-50):
                man.rect.x=800-50
            if(man.rect.x<0):
                man.rect.x=0
            if(man.rect.y>600-50):
                man.rect.y=600-50
            if(man.rect.y<0):
                man.rect.y=0 
            if(man.angle>=pi/4 and man.angle<=3*pi/4):
                screen.blit(man.imgdown[man.frameDOWN],man.rect)
                man.setFrameDown()
            elif(man.angle>3*pi/4 and man.angle<=5*pi/4):
                screen.blit(man.imgleft[man.frameLEFT],man.rect)
                man.setFrameLeft()
            elif(man.angle>5*pi/4 and man.angle<=7*pi/4):
                screen.blit(man.imgup[man.frameUP],man.rect)
                man.setFrameUp()
            else:
                screen.blit(man.imgright[man.frameRIGHT],man.rect)
                man.setFrameRight()
            
        elif event.key==pygame.K_RIGHT or event.key==pygame.K_d:
            man.angle=0
            man.stdAngle()
            movx=man.v*math.cos(man.angle)
            movy=man.v*math.sin(man.angle)
            man.rect.x+=movx
            man.rect.y+=movy
            map.drawMap(objS,screen)
            man.stdAngle()
            if(man.rect.x>800-50):
                man.rect.x=800-50
            if(man.rect.x<0):
                man.rect.x=0
            if(man.rect.y>600-50):
                man.rect.y=600-50
            if(man.rect.y<0):
                man.rect.y=0 
            if(man.angle>=pi/4 and man.angle<=3*pi/4):
                screen.blit(man.imgdown[man.frameDOWN],man.rect)
                man.setFrameDown()
            elif(man.angle>3*pi/4 and man.angle<=5*pi/4):
                screen.blit(man.imgleft[man.frameLEFT],man.rect)
                man.setFrameLeft()
            elif(man.angle>5*pi/4 and man.angle<=7*pi/4):
                screen.blit(man.imgup[man.frameUP],man.rect)
                man.setFrameUp()
            else:
                screen.blit(man.imgright[man.frameRIGHT],man.rect)
                man.setFrameRight()
            
        elif event.key==pygame.K_w or event.key==pygame.K_UP:
            man.angle=3*pi/2
            man.stdAngle()
            movx=man.v*math.cos(man.angle)
            movy=man.v*math.sin(man.angle)
            man.rect.x+=movx
            man.rect.y+=movy
            map.drawMap(objS,screen)
            man.stdAngle()
            if(man.rect.x>800-50):
                man.rect.x=800-50
            if(man.rect.x<0):
                man.rect.x=0
            if(man.rect.y>600-50):
                man.rect.y=600-50
            if(man.rect.y<0):
                man.rect.y=0                
            if(man.angle>=pi/4 and man.angle<=3*pi/4):
                screen.blit(man.imgdown[man.frameDOWN],man.rect)
                man.setFrameDown()
            elif(man.angle>3*pi/4 and man.angle<=5*pi/4):
                screen.blit(man.imgleft[man.frameLEFT],man.rect)
                man.setFrameLeft()
            elif(man.angle>5*pi/4 and man.angle<=7*pi/4):
                screen.blit(man.imgup[man.frameUP],man.rect)
                man.setFrameUp()
            else:
                screen.blit(man.imgright[man.frameRIGHT],man.rect)
                man.setFrameRight()
            
        elif event.key==pygame.K_s or event.key==pygame.K_DOWN:#后退
            man.angle=pi/2
            man.stdAngle()
            movx=man.v*math.cos(man.angle)
            movy=man.v*math.sin(man.angle)
            man.rect.x+=movx
            man.rect.y+=movy
            if(man.rect.x>800-50):
                man.rect.x=800-50
            if(man.rect.x<0):
                man.rect.x=0
            if(man.rect.y>600-50):
                man.rect.y=600-50
            if(man.rect.y<0):
                man.rect.y=0 
            map.drawMap(objS,screen)
            man.stdAngle()
            if(man.angle>=pi/4 and man.angle<=3*pi/4):
                screen.blit(man.imgdown[man.frameDOWN],man.rect)
                man.setFrameDown()
            elif(man.angle>3*pi/4 and man.angle<=5*pi/4):
                screen.blit(man.imgleft[man.frameLEFT],man.rect)
                man.setFrameLeft()
            elif(man.angle>5*pi/4 and man.angle<=7*pi/4):
                screen.blit(man.imgup[man.frameUP],man.rect)
                man.setFrameUp()
            else:
                screen.blit(man.imgright[man.frameRIGHT],man.rect)
                man.setFrameRight()
    return True     
                    
            
def collisionToMove(objS):
    for i in range(objS.numOfBox):
        for j in range(objS.numOfMan):
            if(objS.man[j].isCollision(objS.box[i].rect)):
                objS.box[i].isPushed=True
                if(objS.box[i].isMoveable):
                    objS.box[i].angle=objS.man[j].angle
                    objS.box[i].v=objS.man[j].v
                    objS.box[i].stdAngle()
                    flage=0
                    for k in range (objS.numOfBox):
                        if(k!=i):
                            if(objS.box[i].isEdge==False):
                                for m in range(len(objS.box[i].collisionList)):
                                    if(objS.box[i].collisionList[m].isEdge==True):
                                        flage=1
                                       # objS.box[i].v=0
                                        break
                            else:
                                flage=1
                                #objS.box[i].v=0
                    
                    if(flage==1):
                        #print("edge")
                        movx=objS.man[j].v*math.cos(objS.man[j].angle)
                        movy=objS.man[j].v*math.sin(objS.man[j].angle)
                        objS.man[j].rect.x-=movx
                        objS.man[j].rect.y-=movy
                        objS.man[j].v=0
                        flage=0
                    if(flage==0):
                        movx=objS.box[i].v*math.cos(objS.box[i].angle)
                        movy=objS.box[i].v*math.sin(objS.box[i].angle)
                        objS.box[i].rect.x+=movx
                        objS.box[i].rect.y+=movy
                       # print("no edge")
            else:
                objS.box[i].isPushed=False
                
    for k in range(objS.numOfBox):
        for m in range(k+1,objS.numOfBox):
                if(objS.box[m].isCollision(objS.box[k].rect)):
                    if(objS.box[k].isMoveable):
                        if(objS.box[m].isPushed):
                            objS.box[k].isPushed=True
                            if(objS.box[k] not in objS.box[m].collisionList):
                                objS.box[m].collisionList.append(objS.box[k])
                            if(objS.box[m] in objS.box[k].collisionList):
                                objS.box[k].collisionList.remove(objS.box[m])
                                objS.box[m].collisionList.remove(objS.box[k])
                                objS.box[m].isPushed=False
                                objS.box[k].isPushed=False
                                continue
                            objS.box[k].angle=objS.box[m].angle
                            objS.box[k].v=objS.box[m].v
                            objS.box[k].stdAngle()
                            movx=objS.box[k].v*math.cos(objS.box[k].angle)
                            movy=objS.box[k].v*math.sin(objS.box[k].angle)
                            objS.box[k].rect.x+=movx
                            objS.box[k].rect.y+=movy
                        elif(objS.box[k].isPushed):
                            objS.box[m].isPushed=True
                            if(objS.box[m] not in objS.box[k].collisionList):
                                objS.box[k].collisionList.append(objS.box[m])
                            if(objS.box[k] in objS.box[m].collisionList):
                                objS.box[m].collisionList.remove(objS.box[k])
                                objS.box[k].collisionList.remove(objS.box[m])
                                objS.box[m].isPushed=False
                                objS.box[k].isPushed=False
                                continue
                            objS.box[m].angle=objS.box[k].angle
                            objS.box[m].v=objS.box[k].v
                            objS.box[m].stdAngle()
                            movx=objS.box[m].v*math.cos(objS.box[m].angle)
                            movy=objS.box[m].v*math.sin(objS.box[m].angle)
                            objS.box[m].rect.x+=movx
                            objS.box[m].rect.y+=movy
                    

    for k in range(objS.numOfBox):
        for m in range(k+1,objS.numOfBox):
            if(objS.box[m].isCollision(objS.box[k].rect)==False):
                if(objS.box[k] in objS.box[m].collisionList):
                        objS.box[m].collisionList.remove(objS.box[k])
                if(objS.box[m] in objS.box[k].collisionList):
                    objS.box[k].collisionList.remove(objS.box[m])
            if(objS.box[m].isCollision(objS.box[k].rect) and objS.box[k].isPushed==False and objS.box[m].isPushed==False):
                if(objS.box[k].v==0):
                    objS.box[k].angle=0
                if(objS.box[m].v==0):
                    objS.box[m].angle=0
                if(objS.box[k] not in objS.box[m].collisionList and objS.box[m] not in objS.box[k].collisionList):
                    objS.box[k].collisionList.append(objS.box[m])
                    objS.box[m].collisionList.append(objS.box[k])
                    temp=pygame.mixer.Sound("./audio/pang.mp3")
                    temp.set_volume(0.1)
                    temp.play()
                    setV(objS.box[k],objS.box[m])
                    movxm=objS.box[m].v*math.cos(objS.box[m].angle)
                    movym=objS.box[m].v*math.sin(objS.box[m].angle)
                    movxk=objS.box[k].v*math.cos(objS.box[k].angle)
                    movyk=objS.box[k].v*math.sin(objS.box[k].angle)
                    objS.box[m].rect.x+=movxm
                    objS.box[m].rect.y+=movym
                    objS.box[k].rect.x+=movxk
                    objS.box[k].rect.y+=movyk
                    if(objS.box[m].isCollision(objS.box[k].rect)):
                        #print("强制分离")
                        objS.box[m].rect.x+=movxm*10
                        objS.box[m].rect.y+=movym*10
                        objS.box[k].rect.x+=movxk*10
                        objS.box[k].rect.y+=movyk*10
            if(objS.box[m].isCollision(objS.box[k].rect)!=True and objS.box[k].isPushed==False and objS.box[m].isPushed==False):
                if(objS.box[k] in objS.box[m].collisionList):
                    objS.box[m].collisionList.remove(objS.box[k])
                if(objS.box[m] in objS.box[k].collisionList):
                    objS.box[k].collisionList.remove(objS.box[m])
    
    
                    
                    
    for i in range(objS.numOfBox):
        for j in range(objS.numOfWall):
            if(objS.box[i].isCollision(objS.wall[j]) and objS.box[i].isPushed==False):
                temp=pygame.mixer.Sound("./audio/pang.mp3")
                temp.set_volume(0.1)
                temp.play()
                setV(objS.box[i],objS.wall[j])
                movx=objS.box[i].v*math.cos(objS.box[i].angle)
                movy=objS.box[i].v*math.sin(objS.box[i].angle)
                objS.box[i].rect.x+=movx
                objS.box[i].rect.y+=movy
                while(objS.box[i].isCollision(objS.wall[j])):
                    objS.box[i].rect.x+=movx
                    objS.box[i].rect.y+=movy
    
    for i in range(objS.numOfMan):
        if(objS.man[i].transparent==False):
            for j in range(objS.numOfWall):
                while(objS.man[i].isCollision(objS.wall[j])):
                    movx=objS.man[i].v*math.cos(objS.man[i].angle)
                    movy=objS.man[i].v*math.sin(objS.man[i].angle)
                    objS.man[i].rect.x-=movx
                    objS.man[i].rect.y-=movy
    for j in range(objS.numOfMan):
        for i in range(objS.numOfBox):
            if(objS.box[i].isPushed):
                for k in range(objS.numOfWall):
                    if(objS.box[i].isCollision(objS.wall[k])):  
                        while(objS.man[j].isCollision(objS.box[i].rect)):
                            movx=objS.man[j].v*math.cos(objS.man[j].angle)
                            movy=objS.man[j].v*math.sin(objS.man[j].angle)
                            objS.man[j].rect.x-=movx
                            objS.man[j].rect.y-=movy              
                    
def movingBox(objS):
    a=False
    for i in range(objS.numOfBox):
        if(objS.box[i].isPushed==False and objS.box[i].v!=0):
            a=True
            objS.box[i].runtime+=1
            a=friction_force_a()
            objS.box[i].v+=a
            if(objS.box[i].v<=0):
                objS.box[i].v=0
                objS.box[i].runtime=0
            objS.box[i].stdAngle()
            movx=objS.box[i].v*math.cos(objS.box[i].angle)
            movy=objS.box[i].v*math.sin(objS.box[i].angle)
            objS.box[i].rect.x+=movx
            objS.box[i].rect.y+=movy
    return a

