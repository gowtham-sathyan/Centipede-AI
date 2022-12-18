from tracemalloc import start
import pygame,random,time,pygame.event
import csv

from Player import *
from Fire import *
from Spider import *
from Bomb import *
from LilCenti import *
from Expo import *
from DT import *
import time

# Storing the start and end time
start_time_flag = True
start_time = 0.0
end_time = 0.0

# Parameters for the game
maxBullets=50
centipedeCounter=12
pygame.init()
bg =(25,25,25)
level=1
game_map=[]
empty=pygame.Surface([20,20])
empty.fill(bg)
mushroom_image = pygame.image.load('images/shroom/shroom1.png')
mushroom_image2 = pygame.image.load('images/shroom/shroom2.png')
mushroom_image3 = pygame.image.load('images/shroom/shroom3.png')
mushroom_image.set_colorkey((0,0,0))
mushroom_image2.set_colorkey((0,0,0))
mushroom_image3.set_colorkey((0,0,0))

###PREPARE YOUR AXIS
def setup_game_map():
    global game_map
    game_map = []
    for x in range(40):
        arrayOfZeros = [0]*30
        game_map.append(arrayOfZeros)
    for x in range (30):
        randomX=random.randint(0,29)
        randomY=random.randint(0,27)
        game_map[randomX][randomY] = 1

### SHROOM IT UP
def draw_game_map():
    for column in range(30):
        for row in range(40):
            spot = game_map[row][column]
            if spot == 1:
                screen.blit(empty,[column*20, row*20])
                screen.blit(mushroom_image, [column*20, row*20])
            if spot == 2:
                screen.blit(empty,[column*20, row*20])
                screen.blit(mushroom_image2, [column*20, row*20])
            if spot == 3:
                screen.blit(empty,[column*20, row*20])
                screen.blit(mushroom_image3, [column*20, row*20])
            if spot == 4:
                screen.blit(empty,[column*20, row*20])
                game_map[row][column] = 0

def get_key():
    while True:
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            return event.key
        else:
            pass

def reset_Centipede(gameover=False, speed_up=False):
    if gameover:
        centis.empty()
    for m in range(12):
        centi=LilCenti(20*m,-20)
        if speed_up:
            centi.speed_up()
            centis.add(centi)
    centipedeCounter=12

size=[600,800]
screen=pygame.display.set_mode(size)
pygame.display.set_caption("Centipede")

player=Player(300,700)
playerUpdateFlag=True
fire=Fire()
bomb=Bomb()
fireGroup=pygame.sprite.Group()
fireGroup.add(fire)
sampleFireGroup=pygame.sprite.Group()
fireRate=1 #The number of frames after which another bullet can be fired
fireCounter=0+fireRate #The counter to check how many frames have passed since last bullet was fired. Set to fireRate initially to trigger a bullet the first time
bombBulletFlag=False
spiderBulletFlag=False

clock=pygame.time.Clock()
going=True
#Drawing background
background=pygame.Surface(size)
background.fill(bg)
screen.blit(background,(0,0))

allsprites=pygame.sprite.Group()
allsprites.add(player)
# allsprites.add(fireGroup)
allsprites.add(bomb)
allsprites.add(sampleFireGroup)
expos=pygame.sprite.Group()

#Create THE ALMIGHTY
centis=pygame.sprite.Group()
for m in range(12):
    centi=LilCenti(20*m,-20)
    centis.add(centi)

spider=Spider()
rnd_list=[0]
allsprites.add(spider)
allsprites.add(centis)
allsprites.add(expos)
#spider.activate()
#bomb.activate()
#Program Loop!!
setup_game_map()
clock_tick=20
game_mode='menu'
tickCounter=0

#FONTS------------------
gameOverFont = pygame.font.Font('ARDARLING.ttf' ,70)
clickToStart = pygame.font.Font('ARDARLING.ttf',40)
highScore = pygame.font.Font('ARDARLING.ttf',50)
#-----------------------
#MENU IMAGES
#0 centi
#200 play
#325 high
#425 ins
#525 quit
#700 footer
menu_header=[]
menu_header.append(pygame.image.load("images/menu/menu_centi1.png"))
menu_header.append(pygame.image.load("images/menu/menu_centi2.png"))
menu_high=[]
menu_high.append(pygame.image.load("images/menu/menu_high1.png"))
menu_high.append(pygame.image.load("images/menu/menu_high2.png"))
menu_ins=[]
menu_ins.append(pygame.image.load("images/menu/menu_ins1.png"))
menu_ins.append(pygame.image.load("images/menu/menu_ins2.png"))
menu_play=[]
menu_play.append(pygame.image.load("images/menu/menu_play1.png"))
menu_play.append(pygame.image.load("images/menu/menu_play2.png"))
menu_quit=[]
menu_quit.append(pygame.image.load("images/menu/menu_quit1.png"))
menu_quit.append(pygame.image.load("images/menu/menu_quit2.png"))
menu_footer=pygame.image.load("images/menu/menu_footer.png")
#INSTRUCTIONS IMAGES
inst_space=[]
for i in range(1,5):
    inst_space.append(pygame.image.load("images/instructions/instructions%d.png" % i))
inst_up=[]
for i in range(1,5):
    inst_up.append(pygame.image.load("images/instructions/instructions_up%d.png" % i))
inst_shroom=[]
for i in range(1,7):
    inst_shroom.append(pygame.image.load("images/instructions/instructions_shroom%d.png" % i))
inst_bomb=[]
for i in range(1,5):
    inst_bomb.append(pygame.image.load("images/instructions/instructions_bomb%d.png" % i))
inst_spider=[]
for i in range(1,5):
    inst_spider.append(pygame.image.load("images/instructions/instructions_sp%d.png" % i))
inst_centi=[]
for i in range(1,5):
    inst_centi.append(pygame.image.load("images/instructions/instructions_centi%d.png" % i))
inst_footer=pygame.image.load("images/instructions/instructions_footerAAA.png")

high_score_number = 9
high_footer=pygame.image.load("images/high_footer.png")
#OWASP TOP 10

playerNames = []
playerScores = []
playerDuration = []
playerLevel = []
with open('high_scores.csv', mode = 'r', newline = '') as csv_file:  
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        playerNames.append(row['player_name'])
        playerScores.append(row['score'])
        playerDuration.append(row['duration'])
        playerLevel.append(row['level'])

currentUser=['B','O','T']
currentCharacter=0
currentScore=0
lastScore=0

menu_selection=1
slowDownAnimation=0
while going:   
    clock.tick(clock_tick)
    tickCounter+=1
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            going=False
            if game_mode != 'gameover':
                end_time = time.time()
                playerNames.append(('').join(currentUser))
                playerScores.append(currentScore)
                playerDuration.append(end_time - start_time)
                playerLevel.append(level)
                playerScores = [int(x) for x in playerScores]

                playerScores, playerNames, playerDuration, playerLevel = (list(l) for l in zip( *sorted(zip(playerScores, playerNames, playerDuration, playerLevel), reverse = True) ))

                with open('high_scores.csv', mode = 'w', newline = '') as csv_file:
                    csv_writer = csv.writer(csv_file, delimiter = ',')
                    csv_writer.writerow(['player_name', 'score','duration', 'level'])
                    for i in range( min(len(playerNames), high_score_number)):
                        csv_writer.writerow([playerNames[i], playerScores[i], playerDuration[i], playerLevel[i]])


    if game_mode=='savescore':
        end_time = time.time()
        lastScore=currentScore
        currentCharacter=0
        userText=''
        for i in range(len(currentUser)):
            userText+=currentUser[i]
        text = gameOverFont.render(userText, True, (255,255,255))
        text_rect = text.get_rect()
        text_x = screen.get_width() / 2 - text_rect.width / 2
        screen.blit(text, [text_x, text_y+300])
        pygame.display.flip()
        while currentCharacter<3:
            inkey=get_key()
            if inkey == pygame.K_RETURN:
                game_mode='menu'
                break
            userText=''
            if inkey == pygame.K_BACKSPACE:
                currentUser=currentUser[0:-1]
            elif inkey <= 127:
                currentUser[currentCharacter]=chr(inkey-32)
                currentCharacter+=1
                
                for i in range(len(currentUser)):
                    userText+=currentUser[i]
                    
                text = gameOverFont.render(userText, True, (255,255,255))
                text_rect = text.get_rect()
                text_x = screen.get_width() / 2 - text_rect.width / 2
                refresh=pygame.Surface([text_rect.width,text_rect.height])
                refresh.fill(bg)
                screen.blit(refresh,[text_x, text_y+300])
                screen.blit(text, [text_x, text_y+300])
                pygame.display.flip()

        playerNames.append(('').join(currentUser))
        playerScores.append(currentScore)
        playerDuration.append(end_time - start_time)
        playerLevel.append(level)
        playerScores, playerNames, playerDuration, playerLevel = (list(l) for l in zip( *sorted(zip(playerScores, playerNames, playerDuration, playerLevel), reverse = True) ))

        with open('high_scores.csv', mode = 'w', newline = '') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter = ',')
            csv_writer.writerow(['player_name', 'score','duration','level'])
            for i in range( min(len(playerNames), high_score_number)):
                csv_writer.writerow([playerNames[i], playerScores[i], playerDuration[i], playerLevel[i]])
                
        print('name done')
##        if lastScore>=playerScores[0]:
##            playerScores[0:0]=[lastScore]
        print(lastScore)
        print(userText)
        for i in range(9):
            if lastScore>=playerScores[i]:
##                playerScores[9].remove()
                playerScores.insert(i,lastScore)
                playerNames.insert(i,userText)
                print(userText)
                break
        game_mode='menu'        
    if game_mode=='high':
        pygame.display.set_caption("Centipede")
        #ITEMS ON THE MIDDLE
        title=gameOverFont.render('High Scores',True,(255,255,255))
        screen.blit(high_footer,(0,719))
        
        #LEFT SIDE OF SCREEN
        title_rect = title.get_rect()
        title_x = screen.get_width() / 2 - title_rect.width / 2
        title_y = 40
        screen.blit(title, [title_x, title_y])
        for i in range(len(playerNames)):
            name = highScore.render(str(i+1)+'. '+playerNames[i],True,(255,255,255))
            text_rect = name.get_rect()
            name_x = screen.get_width() / 4 - text_rect.width / 2
            name_y = 150 + 60*(i)
            screen.blit(name,[name_x,name_y])
            
        #RIGHT SIDE OF SCREEN
        for i in range(len(playerScores)):
            name = highScore.render(str(playerScores[i]),True,(255,255,255))
            text_rect = name.get_rect()
            name_x = 3*(screen.get_width() / 4) - text_rect.width / 2
            name_y = 150 + 60*(i)
            screen.blit(name,[name_x,name_y])
        keys=pygame.key.get_pressed()
        if(keys[pygame.K_ESCAPE]):
            game_mode='menu'
            refresh=pygame.Surface([600,800])
            refresh.fill(bg)
            screen.blit(refresh,[0,0])
            menu_selection=2
        
        
    if game_mode=='inst':
        pygame.display.set_caption("Centipede")
        if(tickCounter%10==0):
            slowDownAnimation+=1
            screen.blit(inst_footer,(0,600))
            screen.blit(inst_space[slowDownAnimation%4],(0,0))
            screen.blit(inst_up[slowDownAnimation%4],(300,0))
            screen.blit(inst_shroom[slowDownAnimation%6],(0,200))
            screen.blit(inst_bomb[slowDownAnimation%4],(300,200))
            screen.blit(inst_spider[slowDownAnimation%4],(0,400))
            screen.blit(inst_centi[slowDownAnimation%4],(300,400))
        keys=pygame.key.get_pressed()
        if(keys[pygame.K_ESCAPE]):
            game_mode='menu'
            refresh=pygame.Surface([600,800])
            refresh.fill(bg)
            screen.blit(refresh,[0,0])
            menu_selection=3
            ###inst gifleri menuye donup tekrar gırınce kaldıgı yerden devam edıyodu beyın erımıs amk
            slowDownAnimation=0
    ###CHOOSE YOUR DESTINY
    if game_mode=='menu':
        pygame.display.set_caption("Centipede")
        keys=pygame.key.get_pressed()
        if(keys[pygame.K_DOWN] and menu_selection<4):
            menu_selection+=1

        if(keys[pygame.K_UP] and menu_selection>1):
            menu_selection-=1
        
        screen.blit(menu_header[tickCounter%2],(0,0))
        screen.blit(menu_footer,(0,625))
        if menu_selection==1:
            screen.blit(menu_play[1],(0,200))
        else:
            screen.blit(menu_play[0],(0,200))

        if menu_selection==2:
            screen.blit(menu_high[1],(0,325))
        else:
            screen.blit(menu_high[0],(0,325))

        if menu_selection==3:
            screen.blit(menu_ins[1],(0,425))
        else:
            screen.blit(menu_ins[0],(0,425))

        if menu_selection==4:
            screen.blit(menu_quit[1],(0,525))
        else:
            screen.blit(menu_quit[0],(0,525))
        ###bunu tekrar space yapmısın merte gosterırken ates edıp basladı begenmedı ıt
        if(keys[pygame.K_RETURN]):
            refresh=pygame.Surface([600,800])
            refresh.fill(bg)
            screen.blit(refresh,[0,0])
            if menu_selection==1:
                game_mode='play'
            elif menu_selection==2:
                game_mode='high'
            elif menu_selection==3:
                game_mode='inst'
            elif menu_selection==4:
                going=False
    elif game_mode=='gameover':
        ###NAB
##        global lastScore
        lastScore = currentScore
##        currentScore=0
        
        text = gameOverFont.render("GAME OVER!", True, (255,255,255))
        text_rect = text.get_rect()
        text_x = screen.get_width() / 2 - text_rect.width / 2
        text_y = screen.get_height() / 2 - text_rect.height / 2
        screen.blit(text, [text_x, text_y-200])

        text = clickToStart.render("Hit [S] to Save", True, (255,255,255))
        text_rect = text.get_rect()
        text_x = screen.get_width() / 2 - text_rect.width / 2
        screen.blit(text, [text_x, text_y+210])
        
        text = clickToStart.render("Hit Enter to Start Again", True, (255,255,255))
        text_rect = text.get_rect()
        text_x = screen.get_width() / 2 - text_rect.width / 2
        screen.blit(text, [text_x, text_y+90])

        text = clickToStart.render("Hit Escape for Menu", True, (255,255,255))
        text_rect = text.get_rect()
        text_x = screen.get_width() / 2 - text_rect.width / 2
        screen.blit(text, [text_x, text_y+150])
        
        keys=pygame.key.get_pressed()
        if(keys[pygame.K_RETURN]):
            game_mode='play'
            level=0
            refresh=pygame.Surface([600,800])
            refresh.fill(bg)
            screen.blit(refresh,[0,0])
            for i in sampleFireGroup:
                i.deactivate()
            sampleFireGroup.empty()
            spider.deactivate()
            bomb.deactivate()
            reset_Centipede(True)
            expos.empty()
            setup_game_map()
            draw_game_map()
            #Create THE ALMIGHTY
            # centis=pygame.sprite.Group()
            # for m in range(12):
            #     centi=LilCenti(20*m,-20)
            #     centis.add(centi)
            #     setup_game_map()
            #     allsprites.add(centis)
            allsprites.empty()
            allsprites=pygame.sprite.Group()
            allsprites.add(player)
            # allsprites.add(fireGroup)
            allsprites.add(bomb)
            allsprites.add(spider)
            allsprites.add(centis)
            allsprites.add(expos)
            allsprites.add(sampleFireGroup)
            i=0
            # fire.deactivate()
        if(keys[pygame.K_ESCAPE]):
            game_mode='menu'
            refresh=pygame.Surface([600,800])
            refresh.fill(bg)
            screen.blit(refresh,[0,0])
            #Create THE ALMIGHTY
            centis=pygame.sprite.Group()
            for m in range(12):
                centi=LilCenti(20*m,-20)
                centis.add(centi)
                setup_game_map()
                allsprites.add(centis)
            allsprites=pygame.sprite.Group()
            allsprites.add(player)
            allsprites.add(fireGroup)
            allsprites.add(bomb)
            allsprites.add(spider)
            allsprites.add(centis)
            allsprites.add(expos)
            spider.deactivate()
            bomb.deactivate()
            fire.deactivate()
            menu_selection=1

        if(keys[pygame.K_s]):
            game_mode='savescore'
            #Create THE ALMIGHTY
            centis=pygame.sprite.Group()
            for m in range(12):
                centi=LilCenti(20*m,-20)
                centis.add(centi)
                setup_game_map()
                allsprites.add(centis)
            allsprites=pygame.sprite.Group()
            allsprites.add(player)
            allsprites.add(fireGroup)
            allsprites.add(bomb)
            allsprites.add(spider)
            allsprites.add(centis)
            allsprites.add(expos)
            spider.deactivate()
            bomb.deactivate()
            fire.deactivate()
            
            end_time = time.time()
            playerNames.append(('').join(currentUser))
            playerScores.append(currentScore)
            playerDuration.append(end_time - start_time)
            playerLevel.append(level)
            playerScores, playerNames, playerDuration, playerLevel = (list(l) for l in zip( *sorted(zip(playerScores, playerNames, playerDuration, playerLevel), reverse = True) ))

            with open('high_scores.csv', mode = 'w', newline = '') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter = ',')
                csv_writer.writerow(['player_name', 'score','duration','level'])
                for i in range( min(len(playerNames), high_score_number)):
                    csv_writer.writerow([playerNames[i], playerScores[i], playerDuration[i], playerLevel[i]])
                
    if game_mode=='play':
        if start_time_flag:
            start_time = time.time()
            start_time_flag = False
        if pygame.sprite.spritecollide(player,centis,False):
            expo=Explode(player.rect.x,player.rect.y)
            allsprites.add(expo)
            expos.add(expo)
            game_mode='gameover'
        # if pygame.sprite.collide_rect(player,spider):
        if player.rect.colliderect(spider.rect):
            expo=Explode(player.rect.x,player.rect.y)
            allsprites.add(expo)
            expos.add(expo)
            game_mode='gameover'
        # if pygame.sprite.collide_rect(player,bomb):
        if player.rect.colliderect(bomb.rect):
            expo=Explode(player.rect.x,player.rect.y)
            allsprites.add(expo)
            expos.add(expo)
            game_mode='gameover'
        else:
            allsprites.remove(sampleFireGroup)
            allsprites.remove(centis)
            if len(centis)<=0:
                reset_Centipede(gameover=False, speed_up=True)
                level+=1
                print(level)
                rnd_list=[i for i in range(level)]
                bomb.speed_up()
            #Fire
            keys=pygame.key.get_pressed()
            bulletsRemovable=[]

            #Remove bullets that have left the screen
            for i in sampleFireGroup:
                if i.checkOutOfBounds():
                    i.deactivate()
                    bulletsRemovable.append(i)

            #Track and shoot spider first if it is on screen
            if spider.isActive==1:
                spiderBulletFlag=False
                playerUpdateFlag=False
                #If spider is well above the player and moving up, move to it and shoot
                if spider.rect.x>0 and spider.rect.x<580 and spider.rect.y<=player.rect.y-50 and spider.direction in [2,3]:
                    for i in sampleFireGroup:
                        if i.spiderBullet==True and i.rect.y<spider.rect.y:
                            spiderBulletFlag=True
                            break
                    if not spiderBulletFlag:
                        print("Yes")
                        player.rect.x=spider.rect.x+20
                    elif bomb.isActive==1:
                        bombBulletFlag=False
                        for i in sampleFireGroup:
                            if i.bombBullet==True:
                                bombBulletFlag=True
                                break
                        if not bombBulletFlag:
                            if bomb.rect.x>=0 and bomb.rect.x<=580 and bomb.rect.y<player.rect.y-30:
                                player.rect.x=bomb.rect.x
                            elif player.rect.x>=bomb.rect.x-50 and player.rect.x<=bomb.rect.x+50:
                                if player.rect.x<bomb.rect.x:
                                    player.rect.x=max(player.rect.x-50,0)
                                else:
                                    player.rect.x=min(player.rect.x+50,600)
                            else:
                                playerUpdateFlag=True
                        else:
                            playerUpdateFlag=True
                    else:
                        playerUpdateFlag=True


                #Else if player is in 50 px radius of the spider
                elif player.rect.x>=spider.rect.x-50 and player.rect.x<=spider.rect.x+50:
                    
                    #evade if spider is coming up from under the player or coming down from over the player
                    if (spider.rect.y>=player.rect.y-30 and spider.direction in [2,3]) or (spider.rect.y<=player.rect.y+30 and spider.direction in [1,4]):
                        if player.rect.x<=spider.rect.x:
                            player.rect.x=max(player.rect.x-50,0)
                            player.set_left_right(0)
                        else:
                            player.rect.x=min(player.rect.x+50,600)
                            player.set_left_right(1)
                    else:
                        playerUpdateFlag=True
                else:
                    playerUpdateFlag=True
            elif bomb.isActive==1:
                bombBulletFlag=False
                for i in sampleFireGroup:
                    if i.bombBullet==True:
                        bombBulletFlag=True
                if not bombBulletFlag:
                    if bomb.rect.x>=0 and bomb.rect.x<=580 and bomb.rect.y<player.rect.y-30:
                        player.rect.x=bomb.rect.x
                    elif player.rect.x>=bomb.rect.x-50 and player.rect.x<=bomb.rect.x+50:
                        if player.rect.x<bomb.rect.x:
                            player.rect.x=max(player.rect.x-50,0)
                        else:
                            player.rect.x=min(player.rect.x+50,600)
                    else:
                        playerUpdateFlag=True
                else:
                    playerUpdateFlag=True
            else:
                playerUpdateFlag=True

            #Fire new bullets
            # if (len(sampleFireGroup)-len(bulletsRemovable)<maxBullets) and fireCounter==fireRate:
            if (len(sampleFireGroup)-len(bulletsRemovable)<maxBullets):
                tempFire=Fire()
                # if spiderBulletFlag==False and spider.isActive==1:
                #     tempFire.setSpiderBullet(True)
                if bombBulletFlag==False and bomb.isActive==1:
                    tempFire.setBombBullet(True)
                sampleFireGroup.add(tempFire)
                tempFire.activate(player.rect.x+8,player.rect.y+6)

            #Kill centipedes that are shot by the bullets. Turn the centipedes that collide with a wall/mushroom.
            removeFlag=False
            centi_counter=0
            while centi_counter<len(centis):
                c=centis.sprites()[centi_counter]
                for i in sampleFireGroup:
                    if c.rect.colliderect(i.rect):
                        removeFlag=True
                        shootTileX=min(int(i.x/20),29)
                        shootTileY=min(int(i.y/20),39)
                        game_map[shootTileY-1][shootTileX]=1 #Marking spot to spawn mushroom
                        currentScore+=10
                        i.deactivate()
                        break
                if removeFlag:
                    sampleFireGroup.remove(i)
                    removeFlag=False
                    centis.remove(c)
                    centis.update()
                else:
                    if c.left_right==1 and c.rect.x<580:
                        if game_map[min(int(c.rect.y/20),29)][min(int(c.rect.x/20)+1,39)]:
                            c.collide()
                    else:
                        if game_map[min(int(c.rect.y/20),29)][min(int(c.rect.x/20)-1,39)]:
                            c.collide()
                    centi_counter+=1
                    

            #Creating mushrooms in places where a part of the centipede was killed
            try:
                for i in sampleFireGroup:
                    shootTileX=min(int(i.x/20),29)
                    shootTileY=min(int(i.y/20),39)
                    if game_map[shootTileY-1][shootTileX]>0:
                        game_map[shootTileY-1][shootTileX]=game_map[shootTileY-1][shootTileX]+1
                        currentScore+=3
                        i.deactivate()
                        bulletsRemovable.append(i)
            except:
                print("Exception")
                print(shootTileY-1,shootTileX)

            #move spider if it is on screen
            if spider.isActive==0:
                rnd=random.randint(0,int(1000/level))
                if rnd in rnd_list:
                    spider.activate()
            
            #Check if bullets hit the spider
            bulletSpiderCollision=pygame.sprite.spritecollide(spider,sampleFireGroup,False)
            if bulletSpiderCollision:
                expo=Explode(spider.rect.x,spider.rect.y)
                allsprites.add(expo)
                expos.add(expo)
                spider.deactivate()
                for i in bulletSpiderCollision:
                    i.deactivate()
                    bulletsRemovable.append(i)
                currentScore+=50

            #Spawn bomb.
            if bomb.isActive==0:
                rnd=random.randint(0,int(20/level))
                if rnd in rnd_list:
                    bomb.activate()
            else:   #Drop mushrooms from bomb if bomb is on screen
                if(bomb.drop):
                    rnd=random.randint(1,5)
                    if(rnd==1 and bomb.ay>0 and bomb.isActive):
                        game_map[min(int(bomb.ay/20)+1,29)][min(int(bomb.ax/20),39)]=1
                        bomb.drop=0

            #Check if bullet hits bomb
            bulletBombCollision=pygame.sprite.spritecollide(bomb,sampleFireGroup,False)
            if bulletBombCollision:
                expo=Explode(bomb.rect.x,bomb.rect.y)
                allsprites.add(expo)
                expos.add(expo)
                bomb.deactivate()
                for i in bulletBombCollision:
                    i.deactivate()
                    bulletsRemovable.append(i)
                currentScore+=30
                bomb.resetPreviousShroomCounter()

            #Remove any bullets that have hit anything
            for i in bulletsRemovable:
                sampleFireGroup.remove(i)
            #Check if player collides with centipede, spider or bomb
            

            #Update direction of movement for player
            # if playerUpdateFlag:
            #     if player.get_left_right():
            #         player.update("right")
            #     else:
            #         player.update("left")
            # player.update(keys)
            pygame.display.set_caption("Score : "+str(currentScore))
            
            allsprites.clear(screen,background)
            #Update all sprites
            for i in sampleFireGroup:
                i.update()
            if playerUpdateFlag:
                player.update()
            allsprites.add(sampleFireGroup)
            allsprites.add(centis)
            spider.update()
            bomb.update()
            centis.update()
            expos.update()
            draw_game_map()
        allsprites.draw(screen)
    pygame.display.flip()
pygame.quit()
