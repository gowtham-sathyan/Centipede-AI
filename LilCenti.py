import pygame,random

class LilCenti(pygame.sprite.Sprite):
    gifDelay=0
    gifCounter=0
    gif=[]
    speed=0
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.imgSize=(20,20)
        self.image=pygame.image.load("images/centipede/centipede1.png")
        self.gif.append(pygame.image.load("images/centipede/centipede1.png"))
        self.gif.append(pygame.image.load("images/centipede/centipede2.png"))
        transColor=self.image.get_at((1,1))
        self.image.set_colorkey(transColor)
        for i in range(2):
            self.gif[i].set_colorkey((0,0,0))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.left_right=1
        self.up_down=1
        self.vertical_move=0
        self.speed=20
    def update(self):
        #Gif
        self.gifDelay+=1
        if(self.gifDelay%4==0):
            self.image=self.gif[self.gifCounter]
            self.gifCounter+=1
            self.gifDelay=0
            if self.gifCounter==2:
                self.gifCounter=0
        #left to right
        if self.vertical_move>0:
            self.vertical_move-=1
        
        if(self.left_right==1 and self.vertical_move==0):
            self.rect.x+=self.speed
            #right wall
            if(self.rect.x>580):
                self.rect.x-=self.speed
                self.collide()
                self.vertical_move-=1
                #last row
                if(self.rect.y>=780):
                    self.up_down=0
                    self.rect.x-=self.speed
        elif(self.left_right==0 and self.vertical_move==0):
            self.rect.x-=self.speed
            #left wall
            if(self.rect.x<0):
                self.rect.x+=self.speed
                self.collide()
                self.vertical_move-=1
                #last row
                if(self.rect.y>=780):
                    self.up_down=0
    def collide(self):
        self.vertical_move=2
        if(self.left_right==1):
            self.left_right=0
            if(self.up_down==1):
                self.rect.y+=self.speed
            else:
                self.rect.y-=self.speed
        elif(self.left_right==0):
            self.left_right=1
            if(self.up_down==1):
                self.rect.y+=self.speed
            else:
                self.rect.y-=self.speed
    def speed_up(self):
        self.speed+=random.randint(1,2)
