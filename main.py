import sys
from gameModel import *
from pygame.locals import *
start=True
screen=None
gameFrame=0
gameOver=False
#time 1 frame is 1s

#文本输入

input_box = pygame.Rect(100, 100, 200, 32)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
textActive = False
text = ''

#背景音乐
pygame.mixer.init()
pygame.mixer.music.load("./music/back/girl_not_sad.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(100)
#音效
pangSound=pygame.mixer.Sound("./audio/pang.mp3")
pangSound.set_volume(0.1)

#游戏主程序函数模块
#游戏初始化
def gameInit(width,height,title,icon):#初始化游戏，窗口宽度，高度，和标题，icon
    global screen
    pygame.init()
    size=width,height
    screen=pygame.display.set_mode(size)
    headImage=pygame.image.load(icon)
    pygame.display.set_icon(headImage)
    pygame.display.set_caption(title, "PushBox")

    
def setFPS(fps):#设置游戏帧数
    return pygame.time.Clock().tick(fps)

endsImage=[]
endsImage.append(pygame.transform.scale(pygame.image.load("./image/over/1.png"),(800,600)))
endsImage.append(pygame.transform.scale(pygame.image.load("./image/over/2.png"),(800,600)))
endsImage.append(pygame.transform.scale(pygame.image.load("./image/over/3.png"),(800,600)))
endsImage.append(pygame.transform.scale(pygame.image.load("./image/over/4.png"),(800,600)))
endsImage.append(pygame.transform.scale(pygame.image.load("./image/over/5.png"),(800,600)))
endsFrame=0
def StdEndFrame():
    global endsFrame
    if(endsFrame>4):
        endsFrame=0

def gameAgain(endsImage):#结束游戏
    global screen,endsFrame
    pygame.key.set_repeat(0, 0)#使得可以连续按键
    input_box = pygame.Rect(100, 100, 200, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    #是否继续文本输入框
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == KEYDOWN:
                if active:
                    if event.key == K_RETURN:
                        print(text)
                        text = ''
                    elif event.key == K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
        StdEndFrame()
        screen.blit(endsImage[endsFrame],(0,0))
        endsFrame+=1
        TEXT=font.render(f"Do you wan to continue?(YES OR NO)",True,(0,0,0),(255,255,255))
        screen.blit(TEXT,(0,50))
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()
        pygame.display.update()
        if(text=='YES'):
            return True
        elif(text=='NO'):
            return False
    
                
def updateScreen():#刷新屏幕
    if(gameFrame%100==0):#每次150帧显示一次帧数
        if(movingBox(objS)):
            for i in range(objS.numOfBox):
                if(box[i].rect.x>800-50):
                    box[i].rect.x=800-50
                    if(box[i].v>0):
                        box[i].angle=pi-box[i].angle
                        box[i].stdAngle()
                        box[i].isEdge=True
                if(box[i].rect.x<0):
                    box[i].rect.x=0
                    if(box[i].v>0):
                        box[i].angle=pi-box[i].angle
                        box[i].stdAngle()
                        box[i].isEdge=True
                if(box[i].rect.y>600-50):
                    box[i].rect.y=600-50
                    if(box[i].v>0):
                        box[i].angle=-box[i].angle
                        box[i].stdAngle()
                        box[i].isEdge=True
                if(box[i].rect.y<0):
                    box[i].rect.y=0
                    if(box[i].v>0):
                        box[i].angle=-box[i].angle
                        box[i].stdAngle()
                        box[i].isEdge=True
                else:
                    
                    if(box[i].rect.x>0 and box[i].rect.x<800-50 and box[i].rect.y>0 and box[i].rect.y<600-50):
                        box[i].isEdge=False

        map.drawMap(objS,screen)
        if(man.v>0):
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
                
        else:
            if(man.angle>=pi/4 and man.angle<=3*pi/4):
                screen.blit(man.imgdown[0],man.rect)
            elif(man.angle>3*pi/4 and man.angle<=5*pi/4):
                screen.blit(man.imgleft[0],man.rect)
            elif(man.angle>5*pi/4 and man.angle<=7*pi/4):
                screen.blit(man.imgup[0],man.rect)
            else:
                screen.blit(man.imgright[0],man.rect)
    for i in range(objS.numOfBox):
        box[i].draw(screen)  
    text=font.render(f"Now your score: {g.getScore(objS)}",True,(0,0,0),(255,255,255))
    screen.blit(text,(0,0))
        
#初始化游戏
#################################################################
#################################################################
gameInit(800,600,"一起来推箱子！","./image/icon/head.jpg")

pygame.key.set_repeat(15, 15)#使得可以连续按键
#游戏开始操作

#单独作为主程序运行，不需要函数
print("Game Start!")#可换页操作
print("Loading map...")
#初始化地图，人物，箱子，目标等
map=Map()
map.load_map("./map/map1/map1.txt")#加载地图文件
objS=objectStore("./map/map1/info1.txt")

man=objS.man[0]#得到初始化主角
image1=pygame.transform.scale(pygame.image.load("./image/man/2.png").convert(),(50,50))
image2=pygame.transform.scale(pygame.image.load("./image/man/1.png").convert(),(50,50))
image3=pygame.transform.scale(pygame.image.load("./image/man/3.png").convert(),(50,50))
man.appendImgdown(image1);man.appendImgdown(image2);man.appendImgdown(image3)
image1=pygame.transform.scale(pygame.image.load("./image/man/4.png").convert(),(50,50))
image2=pygame.transform.scale(pygame.image.load("./image/man/5.png").convert(),(50,50))
image3=pygame.transform.scale(pygame.image.load("./image/man/6.png").convert(),(50,50))
man.appendImgleft(image1);man.appendImgleft(image2);man.appendImgleft(image3)    
image1=pygame.transform.scale(pygame.image.load("./image/man/7.png").convert(),(50,50))
image2=pygame.transform.scale(pygame.image.load("./image/man/8.png").convert(),(50,50))
image3=pygame.transform.scale(pygame.image.load("./image/man/9.png").convert(),(50,50))
man.appendImgright(image1);man.appendImgright(image2);man.appendImgright(image3)
image1=pygame.transform.scale(pygame.image.load("./image/man/10.png").convert(),(50,50))
image2=pygame.transform.scale(pygame.image.load("./image/man/11.png").convert(),(50,50))
image3=pygame.transform.scale(pygame.image.load("./image/man/12.png").convert(),(50,50))
man.appendImgup(image1);man.appendImgup(image2);man.appendImgup(image3)  
box=[]#得到初始化箱子
for i in range(objS.numOfBox):
    box.append(objS.box[i])
map.drawMapFirst(objS,screen)
objS.put(man,screen)
for i in range(objS.numOfBox):
    objS.put(box[i],screen)
man.v=5
g=Goal(objS)
#游戏分数#score
#游戏字体
font=pygame.font.Font(None, 36)
text=font.render(f"Now your score :{g.getScore(objS)}",True,(0,0,0),(255,255,255))


setFPS(60)
############################################
############################################


while start:
    if(gameFrame==5):
        a=pygame.mixer.Sound("./audio/okay.mp3")
        a.set_volume(0.1)
        a.play()
    if(g.judge(objS)):#是否胜利，是否重新开始
        if(gameAgain(endsImage)==False):
            bgSurface = pygame.image.load("./image/over/win.png").convert()
            bgSurface = pygame.transform.scale(bgSurface, (800, 600))
            bgSurface1 = pygame.transform.flip(bgSurface, False, False)
            frameRect = bgSurface.get_rect()
            clock = pygame.time.Clock()
            i = 0
            while True:
                # 将背景图像绘制于窗口表面screen
                for event in pygame.event.get():
                    # 处理退出事件
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                screen.blit(bgSurface1, (-i, 0))
                screen.blit(bgSurface, (frameRect.width-i, 0))
                i = (i+1) % frameRect.width

                # frameRect.x += 1
                # 绘制结束，刷新界面
                pygame.display.flip()
                # 时钟停留一帧的时长
                clock.tick(60)

        else:#重新开始初始化
            pygame.key.set_repeat(15, 15)#使得可以连续按键
            screen.fill((0,0,0))
            pygame.display.update()
            gameFrame=0
            #游戏开始操作
            #单独作为主程序运行，不需要函数
            print("Game Start!")#可换页操作
            print("Loading map...")
            #初始化地图，人物，箱子，目标等
            map=Map()
            map.load_map("./map/map1/map1.txt")#加载地图文件
            objS=objectStore("./map/map1/info1.txt")
            man=objS.man[0]#得到初始化主角
            image1=pygame.transform.scale(pygame.image.load("./image/man/2.png").convert(),(50,50))
            image2=pygame.transform.scale(pygame.image.load("./image/man/1.png").convert(),(50,50))
            image3=pygame.transform.scale(pygame.image.load("./image/man/3.png").convert(),(50,50))
            man.appendImgdown(image1);man.appendImgdown(image2);man.appendImgdown(image3)
            image1=pygame.transform.scale(pygame.image.load("./image/man/4.png").convert(),(50,50))
            image2=pygame.transform.scale(pygame.image.load("./image/man/5.png").convert(),(50,50))
            image3=pygame.transform.scale(pygame.image.load("./image/man/6.png").convert(),(50,50))
            man.appendImgleft(image1);man.appendImgleft(image2);man.appendImgleft(image3)    
            image1=pygame.transform.scale(pygame.image.load("./image/man/7.png").convert(),(50,50))
            image2=pygame.transform.scale(pygame.image.load("./image/man/8.png").convert(),(50,50))
            image3=pygame.transform.scale(pygame.image.load("./image/man/9.png").convert(),(50,50))
            man.appendImgright(image1);man.appendImgright(image2);man.appendImgright(image3)
            image1=pygame.transform.scale(pygame.image.load("./image/man/10.png").convert(),(50,50))
            image2=pygame.transform.scale(pygame.image.load("./image/man/11.png").convert(),(50,50))
            image3=pygame.transform.scale(pygame.image.load("./image/man/12.png").convert(),(50,50))
            man.appendImgup(image1);man.appendImgup(image2);man.appendImgup(image3)  
            box=[]#初始化箱子
            for i in range(objS.numOfBox):
                box.append(objS.box[i])
            map.drawMapFirst(objS,screen)
            objS.put(man,screen)
            for i in range(objS.numOfBox):
                objS.put(box[i],screen)
            man.v=5
            g=Goal(objS)
            gameFrame+=1
    else:#游戏进行中，主进程
        gameFrame+=1
        #setFPS(self.FPS) #后面请显示帧数
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            #移动操作
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LSHIFT:
                    man.v=5
                if(event.key==pygame.K_LCTRL):
                    man.v=0
                if(event.key==pygame.K_t):
                    man.rect.y-=5
                if(event.key==pygame.K_g):
                    man.rect.y+=5
                if(event.key==pygame.K_f):
                    man.rect.x-=5
                if(event.key==pygame.K_h):
                    man.rect.x+=5
                if(event.key==pygame.K_q):
                    man.transparent=True
                if(event.key==pygame.K_z):
                    man.transparent=False
            move(event,man,box,objS,map,screen)
            
            
        #碰撞检测
        collisionToMove(objS)
        for i in range (objS.numOfBox):
            for j in range(objS.numOfWall):
                if(objS.box[i].rect.colliderect(objS.wall[j].rect)):
                    pangSound.play()
        for i in range (objS.numOfBox):
            for j in range(objS.numOfBox):
                if(i!=j):
                    if(objS.box[i].rect.colliderect(objS.box[j].rect)):
                        pangSound.play()
        updateScreen()
        
        
        
        pygame.display.update()
