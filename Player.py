import pygame

class Player(pygame.sprite.Sprite):
    gif=[]
    gifDelay=0
    gifCounter=0
    left_right=1
    def __init__(self,X,Y):
        pygame.sprite.Sprite.__init__(self)
        self.imgSize=(20,20)
        self.image=pygame.image.load("images/player/player1.png")
        self.gif.append(pygame.image.load("images/player/player1.png"))
        self.gif.append(pygame.image.load("images/player/player2.png"))
        self.gif.append(pygame.image.load("images/player/player3.png"))
        self.gif.append(pygame.image.load("images/player/player4.png"))
        self.gif.append(pygame.image.load("images/player/player5.png"))
        self.gif.append(pygame.image.load("images/player/player6.png"))
        for i in range(6):
            self.gif[i].set_colorkey((0,0,0))
        self.rect=self.image.get_rect()
        self.rect.x=X
        self.rect.y=Y
        self.left_right=1
        
    def update(self):
        self.gifDelay+=1
        if(self.gifDelay%4==0):
            self.image=self.gif[self.gifCounter]
            self.gifCounter+=1
            self.gifDelay=0
            if self.gifCounter==6:
                self.gifCounter=0
        if self.left_right==1:
            if self.rect.x>=580:
                self.rect.x=580
                self.left_right=0
                # print("Set true")
            else:
                self.rect.x+=20
                if self.rect.x>=580:
                    self.left_right=0
                    # print("Set true")
        else:
            if self.rect.x<=0:
                self.rect.x=0
                self.left_right=1
            else:
                self.rect.x-=20
                if self.rect.x<=0:
                    self.left_right=1
    
    def get_left_right(self):
        return self.left_right
    def set_left_right(self, counter):
        self.left_right=counter
