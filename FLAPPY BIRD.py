import random 
import sys
import pygame
from pygame.locals import * 

FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_pictures = {}
GAME_SOUNDS = {}
PLAYER = 'ESSENTIAL DATA/pictures/bird.png'
BACKGROUND = 'ESSENTIAL DATA/pictures/background.png'
PIPE = 'ESSENTIAL DATA/pictures/pipe.png'

def welcomeScreen():
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_pictures['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_pictures['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
        
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_pictures['background'], (0, 0))    
                SCREEN.blit(GAME_pictures['player'], (playerx, playery))    
                SCREEN.blit(GAME_pictures['message'], (messagex,messagey ))    
                SCREEN.blit(GAME_pictures['base'], (basex, GROUNDY))    
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[0]['y']},
    ]
 
    lowerPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
    ]

    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8 
    playerFlapped = False 


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()


        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
        if crashTest:
            return     

        playerMidPos = playerx + GAME_pictures['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_pictures['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos +4:
                score +=1
                print(f"Your score is {score}") 
                GAME_SOUNDS['point'].play()


        if playerVelY <playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False            
        playerHeight = GAME_pictures['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        
        if upperPipes[0]['x'] < -GAME_pictures['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
        
        SCREEN.blit(GAME_pictures['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_pictures['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_pictures['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_pictures['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_pictures['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_pictures['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_pictures['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_pictures['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery> GROUNDY - 25  or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_pictures['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_pictures['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_pictures['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_pictures['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False

def getRandomPipe():
    """
    Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    """
    pipeHeight = GAME_pictures['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_pictures['base'].get_height()  - 1.2 *offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, 
        {'x': pipeX, 'y': y2} 
    ]
    return pipe


if __name__ == "__main__":
    pygame.init() 
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird by Anushka')
    GAME_pictures['numbers'] = ( 
        pygame.image.load('ESSENTIAL DATA/pictures/0.png').convert_alpha(),
        pygame.image.load('ESSENTIAL DATA/pictures/1.png').convert_alpha(),
        pygame.image.load('ESSENTIAL DATA/pictures/2.png').convert_alpha(),
        pygame.image.load('ESSENTIAL DATA/pictures/3.png').convert_alpha(),
        pygame.image.load('ESSENTIAL DATA/pictures/4.png').convert_alpha(),
        pygame.image.load('ESSENTIAL DATA/pictures/5.png').convert_alpha(),
        pygame.image.load('ESSENTIAL DATA/pictures/6.png').convert_alpha(),
        pygame.image.load('ESSENTIAL DATA/pictures/7.png').convert_alpha(),
        pygame.image.load('ESSENTIAL DATA/pictures/8.png').convert_alpha(),
        pygame.image.load('ESSENTIAL DATA/pictures/9.png').convert_alpha(),
    )

    GAME_pictures['message'] =pygame.image.load('ESSENTIAL DATA/pictures/message.png').convert_alpha()
    GAME_pictures['base'] =pygame.image.load('ESSENTIAL DATA/pictures/base.png').convert_alpha()
    GAME_pictures['pipe'] =(pygame.transform.rotate(pygame.image.load( PIPE).convert_alpha(), 180), 
    pygame.image.load(PIPE).convert_alpha()
    )

    # Game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('ESSENTIAL DATA/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('ESSENTIAL DATA/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('ESSENTIAL DATA/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('ESSENTIAL DATA/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('ESSENTIAL DATA/audio/wing.wav')

    GAME_pictures['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_pictures['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen() 
        mainGame() 