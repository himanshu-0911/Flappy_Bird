import random #For random Heights
import sys  #To exit sys.exit()
import pygame   
from pygame.locals import *


#Global Variables
FPS = 32
Screen_Width = 289
Screen_Height = 511
Screen = pygame.display.set_mode((Screen_Width,Screen_Height))
Groundy = Screen_Height*0.8
Game_img = {}
Game_snd = {}
Player = 'gallery/images/bird.png'
Background = 'gallery/images/background.png'
Hurdle = 'gallery/images/pipe.png'


def WelcomeScreen():
    # Show Welcome Screen
    pl_x = int(Screen_Width/5)
    pl_y = int((Screen_Height-Game_img['player'].get_height())/2)

    msg_x = int((Screen_Width-Game_img['msg'].get_width())/2)
    msg_y = int(Screen_Height*0.13)
    base_x = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                return
            
            else:
                Screen.blit(Game_img['background'],(0,0))
                Screen.blit(Game_img['player'],(pl_x,pl_y))
                Screen.blit(Game_img['msg'],(msg_x,msg_y))
                Screen.blit(Game_img['base'],(base_x,Groundy))
                pygame.display.update()
                FPS_Clock.tick(FPS)

def isCollide(playerx,playery,upperpipes,lowerpipes):
    if(playery>Groundy - 25  or playery<0):
        Game_snd['hit'].play()
        return True
    for pipe in upperpipes:
        pipeHeight = Game_img['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y']) and abs(playerx - pipe['x'])<Game_img['pipe'][0].get_width():
            Game_snd['hit'].play()
            return True

    for pipe in lowerpipes:
        if(playery + Game_img['player'].get_height()>pipe['y']) and abs(playerx - pipe['x'])<Game_img['pipe'][0].get_width():
            Game_snd['hit'].play()
            return True

def getRandomPipes():
    pipeHeight = Game_img['pipe'][0].get_height()
    offSet = Screen_Height/3
    y2 = offSet + random.randrange(0,int(Screen_Height - Game_img['base'].get_height()- 1.2*offSet))
    pipeX = Screen_Width+10
    y1 = pipeHeight - y2 + offSet
    pipe = [{'x':pipeX,'y': -y1},{'x':pipeX,'y':y2}]
    return pipe


def mainGame():
    Score = 0
    pl_x = int(Screen_Width/5)
    pl_y = int(Screen_Height/2)
    base_x = 0

    # Creating Hurdles
    newPipe1 = getRandomPipes()
    newPipe2 = getRandomPipes()

    upperpipes = [
        {'x':Screen_Width+200,'y':newPipe1[0]['y']},
        {'x':Screen_Width+200+(Screen_Width/2),'y':newPipe2[0]['y']}
    ]

    lowerpipes = [
        {'x':Screen_Width+200,'y':newPipe1[1]['y']},
        {'x':Screen_Width+200+(Screen_Width/2),'y':newPipe2[1]['y']}
    ]

    pipe_velocity_x = -4

    player_velocity_y = -9
    player_max_velocity_y = 10
    player_mix_velocity_y = -8
    player_acc_y = 1

    player_flap_accv = -8
    player_flapped = False

    while True:
        for event in pygame.event.get():
            if(event.type == QUIT) or (event.type== KEYDOWN and event.key == K_ESCAPE):
                pygame.exit()
                sys.exit()

            if(event.type == KEYDOWN) and (event.key == K_SPACE or event.key == K_UP):
                player_velocity_y = player_flap_accv
                player_flapped = True
                Game_snd['wing'].play()

        crash_Test = isCollide(pl_x,pl_y,upperpipes,lowerpipes)
        if crash_Test:
            return

        playerMidpos = pl_x + Game_img['player'].get_width()/2
        for pipe in upperpipes:
            pipeMidpos = pipe['x'] + Game_img['pipe'][0].get_width()/2
            if(pipeMidpos<=playerMidpos<pipeMidpos+4):
                Score+=1
                print("Your Score is : ",Score)
                Game_snd['point'].play()

        if(player_velocity_y<player_max_velocity_y) and not(player_flapped):
            player_velocity_y += player_acc_y

        if player_flapped:
            player_flapped = False
        
        playerHeight = Game_img['player'].get_height()
        pl_y = pl_y + min(player_velocity_y,Groundy-pl_y-playerHeight)

        for upperpipe ,lowerpipe in zip(upperpipes,lowerpipes):
            upperpipe['x'] += pipe_velocity_x
            lowerpipe['x'] += pipe_velocity_x

        if 0<upperpipes[0]['x']<5:
            newPipe = getRandomPipes()
            upperpipes.append(newPipe[0])
            lowerpipes.append(newPipe[1])

        if(upperpipes[0]['x']< -Game_img['pipe'][0].get_width()):
            upperpipes.pop(0)
            lowerpipes.pop(0)

        Screen.blit(Game_img['background'],(0,0))
        for upperpipe,lowerpipe in zip(upperpipes,lowerpipes):
            Screen.blit(Game_img['pipe'][0],(upperpipe['x'],upperpipe['y']))
            Screen.blit(Game_img['pipe'][1],(lowerpipe['x'],lowerpipe['y']))
        Screen.blit(Game_img['player'],(pl_x,pl_y))
        Screen.blit(Game_img['base'],(base_x,Groundy))

        myDigits = [int(x) for x in list(str(Score))]
        width = 0
        for digit in myDigits:
            width += Game_img['numbers'][digit].get_width()

        XoffSet = (Screen_Width - width)/2

        for digit in myDigits:
            Screen.blit(Game_img['numbers'][digit],(XoffSet,Screen_Height*0.12))
            XoffSet += Game_img['numbers'][digit].get_width() 

        pygame.display.update()
        FPS_Clock.tick(FPS)



if __name__ == "__main__":
    pygame.init()
    FPS_Clock = pygame.time.Clock()
    pygame.display.set_caption("Himanshu Gaming")
    Game_img['numbers'] = (pygame.image.load('gallery/images/0.png').convert_alpha(),
    pygame.image.load('gallery/images/1.png').convert_alpha(),
    pygame.image.load('gallery/images/2.png').convert_alpha(),
    pygame.image.load('gallery/images/3.png').convert_alpha(),
    pygame.image.load('gallery/images/4.png').convert_alpha(),
    pygame.image.load('gallery/images/5.png').convert_alpha(),
    pygame.image.load('gallery/images/6.png').convert_alpha(),
    pygame.image.load('gallery/images/7.png').convert_alpha(),
    pygame.image.load('gallery/images/8.png').convert_alpha(),
    pygame.image.load('gallery/images/9.png').convert_alpha(),
    )

    Game_img['msg'] = pygame.image.load('gallery/images/message.png').convert_alpha()
    Game_img['base'] = pygame.image.load('gallery/images/base.png').convert_alpha()
    Game_img['pipe'] = ( pygame.transform.rotate(pygame.image.load(Hurdle).convert_alpha(),180),
                            pygame.image.load(Hurdle).convert_alpha()
    )

    Game_img['background'] = pygame.image.load(Background).convert()
    Game_img['player'] = pygame.image.load(Player).convert_alpha()


    #Game Sound
    Game_snd['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    Game_snd['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    Game_snd['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    Game_snd['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    Game_snd['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    while True:
        WelcomeScreen()
        mainGame()
