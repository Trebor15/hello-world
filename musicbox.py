## My Music Box
import pygame
import time
import os
import random

dw = 340         ## width of display area
dh = 170         ## height  of display area
bty = dh * 0.60  ## y reference position of button

##  Color RGB value
cyan  = (0, 255, 255)
white = (255, 255, 255)
azure = (240, 255, 255)
black = (0, 0, 0)
red   = (240, 10, 10)
chocolate  = (210, 105, 30)
khaki  = (240, 230, 140)

paused = False

pygame.init()
gameDisplay = pygame.display.set_mode((dw,dh))
pygame.display.set_caption('My Music box')
gameDisplay.fill(cyan)

clock = pygame.time.Clock()
## global SONG_END
SONG_END = pygame.USEREVENT + 1
showFont   = pygame.font.SysFont("comicsansms", 12)
buttonFont = pygame.font.SysFont("comicsansms", 12)
headerFont = pygame.font.SysFont("comicsansms", 20)

##  Text and font of button and display area  
def text_objects(text, font):
    textSurface = font.render(text,True, black)
    return textSurface, textSurface.get_rect()

##   display currently playing music file 
def show_playing(rx, mp3):
    pygame.draw.rect(gameDisplay,azure,(dw/2 - 120 ,dh/2 - 10,254,20))
    songSurf, songRect = text_objects( (str(rx) + ' - ' + mp3), showFont)
    songRect.center = ( dw/2 , dh/2 )
    pygame.display.flip()
    gameDisplay.blit(songSurf, songRect)
    pygame.display.update()

## display text on button area 
def show_button(txt,x,y,w,h):
    buttonSurf, buttonRect = text_objects(txt, buttonFont)
    buttonRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(buttonSurf, buttonRect)

##  determine mouse position when clicked over a button
##   and take appropriate action
def button(txt, x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x,y,w,h))
        if event.type == pygame.MOUSEBUTTONDOWN and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))
    show_button(txt,x,y,w,h)

##  Action when RANDOM button is clicked
def play_random():
    global rx, mp3, paused
    paused = False
    prev_rx = rx
    rx = random.randrange(0,lenx)
    if rx == prev_rx:
       rx = random.randrange(0,lenx) 
    mp3 = str(mp3Files[rx])
    print('playing random...', rx , mp3)

    pygame.mixer.music.load(mp3)
    pygame.mixer.music.play()
 
## Action when NEXT button is clicked
def play_next():
    global rx, paused, mp3
    paused = False
    if rx >= lenx:
        rx = 0
    else:
        rx += 1
    mp3 = str(mp3Files[rx])    
    print('playing NEXT...', rx,  mp3) 
    pygame.mixer.music.load(mp3)
    pygame.mixer.music.play()

## Action when PREVIOUS button is clicked
def play_previous():
    global rx, paused, mp3
    paused = False
    if rx <= 0:
        rx = lenx
    else:
        rx -= 1
    mp3 = str(mp3Files[rx])
    print('playing PREVIOUS...', rx , mp3) 
    pygame.mixer.music.load(mp3)
    pygame.mixer.music.play()

## Action when PAUSE button is clicked
def play_pause():
    print(' pause...')
    global paused
    paused = True
    pygame.mixer.music.pause()
   
## Action when RESUME button is clicked   
def play_resume():
    print(' resume playing...')
    global paused
    paused = False
    pygame.mixer.music.unpause()

## Action when STOP button is clicked
def stop_bye():
    global playing
    print('... STOP BYE...')
    pygame.mixer.music.stop()
    playing = False
 
## Buttons parameters and appropriate action when clicked
def display_buttons():
    global mp3
    global playing
    playing = True
    button ('PREVIOUS',(dw/2 - 110),bty,     70,20, chocolate,khaki, play_previous)     
    button ('RANDOM',  (dw/2 - 30) ,bty,     70,20, chocolate,khaki, play_random)
    button ('NEXT',    (dw/2 + 50) ,bty,     70,20, chocolate,khaki, play_next)
    button ('STOP',    (dw/2 + 50) ,bty + 24,70,20, chocolate,khaki, stop_bye)
    if playing:    
        if paused:
            button ('RESUME',(dw/2 - 110),bty + 24,70,20, khaki,khaki, play_resume)
        else:
            button ('PAUSE', (dw/2 - 110),bty + 24,70,20, chocolate,khaki, play_pause)
    show_playing(rx, mp3)

## Initializes pygame and declare variables
##  Read the music file from a folder 
def musicbox_init(mFolder, fileExt):
    global rx, lenx, mp3Files, mp3
    rx = -1
    mp3Files = [x for x in os.listdir(mFolder) if x.endswith(fileExt)]
##    print(mp3Files)
    lenx = len(mp3Files)-1
    print('max index of music files = ', lenx)
    pygame.mixer.init()
##
    pygame.mixer.music.set_endevent(SONG_END)
## 
##   largeText = pygame.font.SysFont("comicsans",40)
    headerSurf, headerRect = text_objects("Music Box", headerFont)
    headerRect.center = ((dw/2), (dh/4))
    gameDisplay.blit(headerSurf, headerRect)

    mp3 = (' ** Welcome ***')
    display_buttons()
    play_random()

## main routine of Music Box apps
def musicbox_play():
    print('Music box Play...')
    global event
    global playing 
    playing = True
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                print(' *** QUIT ***')
                break
                
            if event.type == SONG_END:
                play_next()
                show_playing(rx, mp3)
                pygame.display.flip()
                pygame.display.update()

            display_buttons()
            pygame.display.flip()
            pygame.display.update()
    print(' playing stop....')            
    pygame.quit()

##            clock.tick(60) 

     
## Let's see what this python pygame can do...
musicbox_init('.','.mp3')        
musicbox_play()


    
    