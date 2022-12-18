import pygame

class Fire(pygame.sprite.Sprite):
    active=False
    canFire=True
    x=-100
    y=-100
    bombBullet=False
    spiderBullet=False
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface([4,8])
        self.image.fill((0,255,0))
        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y
        self.bombBullet=False
        self.spiderBullet=False
    def update(self):
        self.x=self.rect.x
        self.y=self.rect.y
        if(self.rect.y <= -20):
            self.rect.y=-20
            self.canFire=True
        else:
            self.rect.y-=20
    def activate(self,x,y):
        self.canFire=False
        active=True
        self.rect.x=x
        self.rect.y=y

    def deactivate(self):
        self.rect.y=-100
        self.canFire=True

    def checkOutOfBounds(self):
        if self.rect.y<=0:
            return True
        else:
            return False
    
    def setBombBullet(self,flag):
        self.bombBullet=flag
    
    def setSpiderBullet(self,flag):
        self.spiderBullet=flag