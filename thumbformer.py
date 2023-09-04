import time
from thumby import *

# BITMAP: width: 4, height: 6
player_1 = bytearray([63,31,25,63])
# BITMAP: width: 4, height: 6
player_2 = bytearray([63,31,25,63])
# BITMAP: width: 4, height: 6
player_3 = bytearray([31,63,57,31])
# BITMAP: width: 4, height: 6
player_4 = bytearray([31,63,57,31])
# BITMAP: width: 4, height: 6
player_5 = bytearray([63,31,25,63])
# BITMAP: width: 4, height: 6
player_6 = bytearray([63,31,25,63])

player_anim = player_1 + player_2 + player_3 + player_4 + player_5 + player_6
player_spritecount = 0

platform_b = bytearray([0, 0, 21, 42, 21, 42, 21, 42, 21, 42, 21, 42, 21, 42, 0, 0])

player = Sprite(4, 6, player_anim)

all_platform = []

all_items_to_draw = [player]

player.y = 30
player.x = 62

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
        
            
    def state_menu():
        pass
            
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
        else:
            if player.getFrame() == 3 or player.getFrame() == 4:
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

        # Adjust camera coordinates to follow the player
        cameraX = player.x - display.width // 2
        cameraY = player.y - display.height // 2

        for plat in all_platform:
            plat.sprite.x -= int(cameraX)
            plat.sprite.y -= int(cameraY)
            plat.check_collision(player)
            display.drawSprite(plat.sprite)

        #player.x -= int(cameraX)
        #player.y -= int(cameraY)
        display.drawSprite(player)
        display.update()
        all_platform.clear()
        
    def state_end():
        pass
    
    def state_broke():
        pass
    

Game()