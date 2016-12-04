#SI 206
#final project
#hongjisu


import pygame



#size factor
SIZE_FACTOR = 6 #bug when changed to different factor for now

#colors
color_black = (0, 0, 0)
color_white = (255, 255, 255)
color_red = (255, 0, 0)
color_yellow = (255, 255, 0)
color_green = (0, 255, 0)
color_blue = (0, 0, 255)
color_purple = (255, 0, 255)

#seticon
player = pygame.image.load('pacman_r.gif')
pygame.display.set_icon(player)

#music
pygame.mixer.init()
pygame.mixer.music.load("pacman.mp3")
pygame.mixer.music.play(-1, 0.0)


#map unit
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y

#create bluewall
def createMap(sprites_list):
    # [x, y, width, height] from left corner
    wall_list = pygame.sprite.RenderPlain()


    walls = [[0, 0, 1, 100],
             [0, 0, 100, 1],
             [0, 100, 101, 1],
             [100, 0, 1, 101],
             [50, 0, 1, 11],
             [10, 10, 31, 1],
             [60, 10, 31, 1],
             [10, 20, 81, 1],
             [10, 20, 1, 21],
             [50, 20, 1, 11],
             [90, 20, 1, 21],
             [20, 30, 21, 1],
             [20, 30, 1, 21],
             [60, 30, 21, 1],
             [80, 30, 1, 21],
             [30, 40, 1, 21],
             [30, 60, 41, 1],
             [70, 40, 1, 21],
             [40, 40, 7, 1],
             [54, 40, 7, 1],
             [40, 40, 1, 11],
             [40, 50, 21, 1],
             [60, 40, 1, 11],
             [0, 50, 11, 1],
             [90, 50, 11, 1],
             [10, 60, 11, 1],
             [10, 60, 1, 31],
             [80, 60, 11, 1],
             [90, 60, 1, 31],
             [20, 70, 61, 1],
             [20, 70, 1, 11],
             [80, 70, 1, 11],
             [30, 80, 41, 1],
             [50, 80, 1, 11],
             [20, 90, 21, 1],
             [60, 90, 21, 1]
             ]

    # Create Map
    for item in walls:
        wall = Wall(item[0]*SIZE_FACTOR, item[1]*SIZE_FACTOR, item[2]*SIZE_FACTOR, item[3]*SIZE_FACTOR, color_blue)
        sprites_list.add(wall)
        wall_list.add(wall)

    return wall_list


#create white gate only passable by ghosts
def setupGate(all_sprites_list):
    gate = pygame.sprite.RenderPlain()
    gate.add(Wall(47*SIZE_FACTOR, 40*SIZE_FACTOR, 7*SIZE_FACTOR, 2, color_white))
    all_sprites_list.add(gate)
    return gate


#yellow balls
class Block(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        #contstruct
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        #circle code
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])

        #fill anywhere possible with ball
        self.rect = self.image.get_rect()



class Player(pygame.sprite.Sprite):
    # Set speed vector
    change_x = 0
    change_y = 0

    def __init__(self, x, y, filename):
        #default
        pygame.sprite.Sprite.__init__(self)

        #set height& width
        self.image = pygame.image.load(filename).convert()

        #left = y top = x
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.prev_x = x
        self.prev_y = y

        #change pic by the movement of pacman
    def changePic(self, filename):
        self.image = pygame.image.load(filename).convert()

    #player speed change X
    def prev_xy(self):
        self.prev_x = self.change_x
        self.prev_y = self.change_y

    #player speed change O
    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y

    #block player avoding map
    def update(self, walls, gate):


        old_x = self.rect.left
        new_x = old_x + self.change_x
        self.rect.left = new_x

        old_y = self.rect.top
        new_y = old_y + self.change_y


        #CHECK wall hit
        x_collide = pygame.sprite.spritecollide(self, walls, False)
        if x_collide:
            self.rect.left = old_x
        else:
            self.rect.top = new_y
            y_collide = pygame.sprite.spritecollide(self, walls, False)
            if y_collide:
                self.rect.top = old_y

        if gate != False:
            gate_hit = pygame.sprite.spritecollide(self, gate, False)
            if gate_hit:
                self.rect.left = old_x
                self.rect.top = old_y


class Ghost(Player):
    # Change the speed of the ghost
    def changespeed(self, list, turn, steps, l):
        try:
            z = list[turn][2]
            if steps < z:
                self.change_x = list[turn][0]
                self.change_y = list[turn][1]
                steps += 1
            else:
                if turn < l:
                    turn += 1
                else:
                    turn = 0
                self.change_x = list[turn][0]
                self.change_y = list[turn][1]
                steps = 0
            return [turn, steps]
        except IndexError:
            return [0, 0]

Pinky_directions = [
            [30, 0, 2],
            [0, -15, 4],
            [15, 0, 10],
            [0, 15, 7],
            [15, 0, 3],
            [0, -15, 3],
            [15, 0, 3],
            [0, -15, 15],
            [-15, 0, 15],
            [0, 15, 3],
            [15, 0, 15],
            [0, 15, 11],
            [-15, 0, 3],
            [0, -15, 7],
            [-15, 0, 11],
            [0, 15, 3],
            [-15, 0, 11],
            [0, 15, 7],
            [-15, 0, 3],
            [0, -15, 3],
            [-15, 0, 3],
            [0, -15, 15],
            [15, 0, 15],
            [0, 15, 3],
            [-15, 0, 15],
            [0, 15, 11],
            [15, 0, 3],
            [0, -15, 11],
            [15, 0, 11],
            [0, 15, 3],
            [15, 0, 1]
        ]

Blinky_directions = [
            [30, 0, 2],
            [0, -15, 4],
            [-15, 0, 10],
            [0, 15, 7],
            [-15, 0, 3],
            [0, -15, 3],
            [-15, 0, 3],
            [0, -15, 15],
            [15, 0, 15],
            [0, 15, 3],
            [-15, 0, 15],
            [0, 15, 11],
            [15, 0, 3],
            [0, -15, 7],
            [15, 0, 11],
            [0, 15, 3],
            [15, 0, 11],
            [0, 15, 7],
            [15, 0, 3],
            [0, -15, 3],
            [15, 0, 3],
            [0, -15, 15],
            [-15, 0, 15],
            [0, 15, 3],
            [15, 0, 15],
            [0, 15, 11],
            [-15, 0, 3],
            [0, -15, 11],
            [-15, 0, 11],
            [0, 15, 3],
            [-15, 0, 1],
            [-30, 0, 2],
            [0, 15, 4],
        ]

Inky_directions = [
            [30, 0, 2],
            [0, -15, 4],
            [15, 0, 9],
            [0, 15, 11],
            [-15, 0, 23],
            [0, 15, 7],
            [15, 0, 3],
            [0, -15, 3],
            [15, 0, 19],
            [0, 15, 3],
            [15, 0, 3],
            [0, 15, 3],
            [15, 0, 3],
            [0, -15, 15],
            [-15, 0, 7],
            [0, 15, 3],
            [-15, 0, 19],
            [0, -15, 11],
            [15, 0, 9]
        ]

Clyde_directions = [
            [30, 0, 2],
            [0, -15, 4],
            [-15, 0, 9],
            [0, 15, 11],
            [15, 0, 23],
            [0, 15, 7],
            [-15, 0, 3],
            [0, -15, 3],
            [-15, 0, 19],
            [0, 15, 3],
            [-15, 0, 3],
            [0, 15, 3],
            [-15, 0, 3],
            [0, -15, 15],
            [15, 0, 7],
            [0, 15, 3],
            [15, 0, 19],
            [0, -15, 11],
            [-15, 0, 9],
            [-30, 0, 2],
            [0, 15, 4],
        ]


#length of monster's movement array
pl = len(Pinky_directions) - 1
bl = len(Blinky_directions) - 1
il = len(Inky_directions) - 1
cl = len(Clyde_directions) - 1

#py init
pygame.init()

# 101 * screen size
screen = pygame.display.set_mode([101*SIZE_FACTOR, 101*SIZE_FACTOR + 30])

#Dubman at top
pygame.display.set_caption('Dubman')
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(color_black)

clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.Font("freesansbold.ttf", 24)

# default locations for Pacman and monsters
p_w = 287  # Width
p_h = 439  # Pacman height
m_h = 259  # Monster height
m_w = 255  # Monster width


def startGame():
    all_sprites_list = pygame.sprite.RenderPlain()
    block_list = pygame.sprite.RenderPlain()
    ghost_list = pygame.sprite.RenderPlain()
    collision = pygame.sprite.RenderPlain()
    wall_list = createMap(all_sprites_list)
    gate = setupGate(all_sprites_list)

    p_turn = 0
    p_steps = 0
    b_turn = 0
    b_steps = 0
    i_turn = 0
    i_steps = 0
    c_turn = 0
    c_steps = 0

    # Create the player paddle object
    Pacman = Player(p_w, p_h, "pacman_r.gif")
    all_sprites_list.add(Pacman)
    collision.add(Pacman)

    Blinky = Ghost(m_w, m_h, "images/Blinky.png")
    ghost_list.add(Blinky)
    all_sprites_list.add(Blinky)

    Pinky = Ghost(m_w, m_h, "images/Pinky.png")
    ghost_list.add(Pinky)
    all_sprites_list.add(Pinky)

    Inky = Ghost(m_w, m_h, "images/Inky.png")
    ghost_list.add(Inky)
    all_sprites_list.add(Inky)

    Clyde = Ghost(m_w, m_h, "images/Clyde.png")
    ghost_list.add(Clyde)
    all_sprites_list.add(Clyde)

    #Draw map
    for row in range(19):
        for column in range(19):
            if (row>6 and row <9) and (column>7 and column <11):
                continue
            else:
                block = Block(color_yellow, 4, 4)

                #fill blocks in the map
                block.rect.x = (30 * column + 6) + 26
                block.rect.y = (30 * row + 6) + 26

                b_collide = pygame.sprite.spritecollide(block, wall_list, False)
                p_collide = pygame.sprite.spritecollide(block, collision, False)
                if b_collide:
                    continue
                elif p_collide:
                    continue
                else:
                    block_list.add(block)
                    all_sprites_list.add(block)

    block_len = len(block_list)

    score = 0

    check = False

    while check == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                check = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    Pacman.changespeed(-30, 0)
                    Pacman.changePic("pacman_l.gif")

                if event.key == pygame.K_RIGHT:
                    Pacman.changespeed(30, 0)
                    Pacman.changePic("pacman_r.gif")

                if event.key == pygame.K_UP:
                    Pacman.changespeed(0, -30)
                    Pacman.changePic("pacman_u.gif")

                if event.key == pygame.K_DOWN:
                    Pacman.changespeed(0, 30)
                    Pacman.changePic("pacman_d.gif")


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    Pacman.changespeed(30, 0)
                if event.key == pygame.K_RIGHT:
                    Pacman.changespeed(-30, 0)
                if event.key == pygame.K_UP:
                    Pacman.changespeed(0, 30)
                if event.key == pygame.K_DOWN:
                    Pacman.changespeed(0, -30)

        Pacman.update(wall_list, gate)

        returned = Pinky.changespeed(Pinky_directions, p_turn, p_steps, pl)
        p_turn = returned[0]
        p_steps = returned[1]
        Pinky.changespeed(Pinky_directions, p_turn, p_steps, pl)
        Pinky.update(wall_list, False)

        returned = Blinky.changespeed(Blinky_directions, b_turn, b_steps, bl)
        b_turn = returned[0]
        b_steps = returned[1]
        Blinky.changespeed(Blinky_directions, b_turn, b_steps, bl)
        Blinky.update(wall_list, False)

        returned = Inky.changespeed(Inky_directions, i_turn, i_steps, il)
        i_turn = returned[0]
        i_steps = returned[1]
        Inky.changespeed(Inky_directions, i_turn, i_steps, il)
        Inky.update(wall_list, False)

        returned = Clyde.changespeed(Clyde_directions,c_turn, c_steps, cl)
        c_turn = returned[0]
        c_steps = returned[1]
        Clyde.changespeed(Clyde_directions, c_turn, c_steps, cl)
        Clyde.update(wall_list, False)

        #blocks that collided
        blocks_hit_list = pygame.sprite.spritecollide(Pacman, block_list, True)

        #find score
        if len(blocks_hit_list) > 0:
            score += len(blocks_hit_list)

        screen.fill(color_black)

        wall_list.draw(screen)
        gate.draw(screen)
        all_sprites_list.draw(screen)
        ghost_list.draw(screen)

        text = font.render("SCORE  " + str(score * 100), True, color_red)
        #left block + " blocks:" + str(block_len - score)
        #slowly bring forward the end text
        screen.blit(text, [10, 610])

        if score == block_len:
            restart("CLEAR!", 255, all_sprites_list, block_list, ghost_list, collision,
                    wall_list, gate)

        game_over_check = pygame.sprite.spritecollide(Pacman, ghost_list, False)

        if game_over_check:
            restart("Game Over", 235, all_sprites_list, block_list, ghost_list, collision, wall_list, gate)
        pygame.display.flip()

        clock.tick(10)


def restart(message, left, all_sprites_list, block_list, ghost_list, collision, wall_list, gate):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_RETURN:
                    del all_sprites_list
                    del block_list
                    del ghost_list
                    del collision
                    del wall_list
                    del gate
                    startGame()

        size_rect = pygame.Surface((400, 200))  # the size of rect
        size_rect.set_alpha(10)
        size_rect.fill((128, 128, 128))  # fill entire space
        screen.blit(size_rect, (100, 200))


        text1 = font.render(message, True, color_white)
        screen.blit(text1, [left, 233])
        text2 = font.render("press ENTER to restart", True, color_white)
        screen.blit(text2, [180, 303])
        text3 = font.render("press ESC to quit", True, color_white)
        screen.blit(text3, [200, 333])
        pygame.display.flip()
        clock.tick(10) #clock speed

startGame()

pygame.quit()
