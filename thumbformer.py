import time
from thumby import *

import sys
import os
os.chdir("/Games/thumbformer/")

from sprites import *

player_anim = player_1 + player_2 + player_3 + player_4 + player_5 + player_6
player_spritecount = 0

menu_anim = menu_1

player = Sprite(4, 6, player_anim)
menu = Sprite(72, 40, menu_anim)


all_platform = []

all_items_to_draw = [player]

player.y = 26
player.x = 39.6

GRAVITY = 0.08
JUMP_POWER = 1.2

cameraX = 0
cameraY = 0
cameraSpeedX = 0.8
cameraSpeedY = 4

class Platform:
    def __init__(self, sprite):
        self.sprite = sprite

    def check_collision(self, player):
        if (
            self.sprite.y <= player.y + 8 <= self.sprite.y + 8
            and self.sprite.x - 2 <= player.x <= self.sprite.x + 12
        ):
            player.yVel = 0
            player.y = self.sprite.y - 7

class Map:
    def create_platform(self, x, y):
        platform = Sprite(16, 8, platform_b)
        platform.x, platform.y = x, y
        obj_platform = Platform(platform)
        all_platform.append(obj_platform)

class Game:
    def __init__(self):
        player.xVel = 0
        player.yVel = 0
        self.map = Map()
        display.setFPS(30)
        
        self.STATE = "game"
        
        while True:
            if self.STATE == "menu":
                self.state_menu()
            elif self.STATE == "game":
                self.state_game()
            elif self.STATE == "end":
                self.state_end()
            else:
                self.state_broke()
        
            
    def state_menu(self):
        if buttonA.justPressed():
            self.STATE = "game"
        
        display.drawSprite(menu)
        
        display.update()
            
    def state_game(self):
        global cameraX, cameraY

        t0 = time.ticks_ms()  

        if buttonA.justPressed():
            player.yVel = JUMP_POWER
            player.y -= player.yVel
            player.setFrame(1)
        else:
            player.yVel -= GRAVITY

        if buttonL.pressed():
            player.xVel += cameraSpeedX
            player.mirrorX = 1
            player.setFrame(player.getFrame() + 1)
        elif buttonR.pressed():
            player.xVel -= cameraSpeedX
            player.mirrorX = 0
            player.setFrame(player.getFrame() + 1)
            
        if not buttonR.pressed() and not buttonL.pressed():
            if player.getFrame() <= 3:
                player.setFrame(1)

        player.y -= player.yVel
        player.x -= player.xVel

        player.xVel = 0
        display.fill(0)
        self.map.create_platform(50, 20)
        self.map.create_platform(12, 22)
        self.map.create_platform(68, 4)
        self.map.create_platform(8, 8)
        self.map.create_platform(39, 39)

        cameraX = player.x - display.width // 2
        cameraY = player.y - display.height // 2

        for plat in all_platform:
            plat.sprite.x -= int(cameraX)
            plat.sprite.y -= int(cameraY)
            plat.check_collision(player)
            display.drawSprite(plat.sprite)
        
        display.drawSprite(player)
        display.update()
        all_platform.clear()
        
    def state_end(self):
        pass
    
    def state_broke(self):
            display.fill(0)
            display.setFont("/lib/font5x7.bin", 5, 7, 1)
            display.drawText("Something", 5, 0, 1)
            display.drawText("went", 5, 10, 1)
            display.drawText("wrong", 5, 20, 1)
            
            display.setFont("/lib/font3x5.bin", 3, 5, 1)
            display.drawText("Please Restart", 5, 34, 1)
            display.update()

Game()
