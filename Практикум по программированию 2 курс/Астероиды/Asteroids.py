import pygame
import math
import random
import os
pygame.init()

# Различные константы
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

display_width = 800
display_height = 600

ship_size = 40
fd_fric = 0.5
bd_fric = 0.1
ship_max_speed = 10
ship_max_rtspd = 2
bullet_speed = 15

# Создание экрана
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Asteroids")
world = pygame.Surface((800, 600))

timer = pygame.time.Clock()

path = os.getcwd()

abs_path_sound = path + "\Asteroids\Sounds\\"
abs_path_image = path + "\Asteroids\Images\\"


# Импорт звуков
snd_fire = pygame.mixer.Sound(abs_path_sound.replace("\\","/") + "fire.wav")
snd_bangL = pygame.mixer.Sound(abs_path_sound.replace("\\","/") + "bangLarge.wav")
snd_bangM = pygame.mixer.Sound(abs_path_sound.replace("\\","/") + "bangMedium.wav")
snd_bangS = pygame.mixer.Sound(abs_path_sound.replace("\\","/") + "bangSmall.wav")
snd_extra = pygame.mixer.Sound(abs_path_sound.replace("\\","/") + "extra.wav")
main_music = pygame.mixer.Sound(abs_path_sound.replace("\\","/") + "main_music.mp3")

# Импорт картинок
background = pygame.transform.scale(pygame.image.load(abs_path_image.replace("\\","/") + "background.png"), (display_width, display_height) )
aster_image = pygame.image.load(abs_path_image.replace("\\","/") + "aster.png").convert_alpha()

rotate_num = -90

spaceship = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(abs_path_image.replace("\\","/") + "spaceship.png").convert_alpha(), (ship_size, ship_size)), rotate_num)
spaceship_stop = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(abs_path_image.replace("\\","/") + "spaceship_stop.png").convert_alpha(), (ship_size, ship_size)), rotate_num)

def drawText(msg, color, x, y, s, center=True):
    screen_text = pygame.font.SysFont("Calibri", s).render(msg, True, color)
    if center:
        rect = screen_text.get_rect()
        rect.center = (x, y)
    else:
        rect = (x, y)
    world.blit(screen_text, rect)
    gameDisplay.blit(world, pygame.rect.Rect(0,0, display_width, display_height))


def isColliding(x, y, xTo, yTo, size):
    if x > xTo - size and x < xTo + size and y > yTo - size and y < yTo + size:
        return True
    return False  


# Класс Астероид
class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        if type == "Large":
            self.size = 40
        elif type == "Normal":
            self.size = 30
        else:
            self.size = 20
        self.type = type

        self.image = pygame.transform.scale(aster_image, (self.size, self.size))
        self.rect = self.image.get_rect(center=(self.size/2, self.size/2))

        self.speed = random.uniform(1, (40 - self.size) * 4 / 15)
        self.dir = random.randrange(0, 360) * math.pi / 180
    
    def updateAsteroid(self):
        self.x += self.speed * math.cos(self.dir)
        self.y += self.speed * math.sin(self.dir)

        # Проверка выхода за границы
        if self.x > display_width:
            self.x = 0
        elif self.x < 0:
            self.x = display_width
        elif self.y > display_height:
            self.y = 0
        elif self.y < 0:
            self.y = display_height

        world.blit(self.image, (self.x, self.y))
        gameDisplay.blit(world, pygame.rect.Rect(0,0, display_width, display_height))
    

# Класс пули
class Bullet:
    def __init__(self, x, y, direction):
        self.x = x + ship_size/2
        self.y = y + ship_size
        self.dir = direction
        self.life = 30

    def updateBullet(self):
        # Вычисление координат
        self.x += bullet_speed * math.cos(self.dir * math.pi / 180)
        self.y += bullet_speed * math.sin(self.dir * math.pi / 180)

        # Отрисовка
        pygame.draw.circle(world, red, (int(self.x), int(self.y)), 3)
        gameDisplay.blit(world, pygame.rect.Rect(0,0, display_width, display_height))

        # Столкновение со стенками
        if self.x > display_width:
            self.x = 0
        elif self.x < 0:
            self.x = display_width
        elif self.y > display_height:
            self.y = 0
        elif self.y < 0:
            self.y = display_height
        self.life -= 1


# Мертвый корабль
class deadShip:
    def __init__(self, x, y, l):
        self.angle = random.randrange(0, 360) * math.pi / 180
        self.dir = random.randrange(0, 360) * math.pi / 180
        self.rtspd = random.uniform(-0.25, 0.25)
        self.x = x
        self.y = y
        self.lenght = l
        self.speed = random.randint(2, 8)

    def updateDeadShip(self):
        pygame.draw.line(gameDisplay, white,
                         (self.x + self.lenght * math.cos(self.angle) / 2,
                          self.y + self.lenght * math.sin(self.angle) / 2),
                         (self.x - self.lenght * math.cos(self.angle) / 2,
                          self.y - self.lenght * math.sin(self.angle) / 2))
        self.angle += self.rtspd
        self.x += self.speed * math.cos(self.dir)
        self.y += self.speed * math.sin(self.dir)


# Корабль
class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y

        #self.x = x - ship_size/2
        #self.y = y - ship_size/2

        self.hspeed = 0
        self.vspeed = 0
        self.dir = -90
        self.rtspd = 0
        self.thrust = False

        self.image = pygame.transform.rotate(spaceship_stop, 90)
        self.rect = self.image.get_rect(center=(ship_size/2, ship_size/2))

    def updateShip(self):
        # Движение корабля
        speed = math.sqrt(self.hspeed**2 + self.vspeed**2)
        if self.thrust:
            if speed + fd_fric < ship_max_speed:
                self.hspeed += fd_fric * math.cos(self.dir * math.pi / 180)
                self.vspeed += fd_fric * math.sin(self.dir * math.pi / 180)
            else:
                self.hspeed = ship_max_speed * math.cos(self.dir * math.pi / 180)
                self.vspeed = ship_max_speed * math.sin(self.dir * math.pi / 180)
        else:
            if speed - bd_fric > 0:
                change_in_hspeed = (bd_fric * math.cos(self.vspeed / self.hspeed))
                change_in_vspeed = (bd_fric * math.sin(self.vspeed / self.hspeed))
                if self.hspeed != 0:
                    if change_in_hspeed / abs(change_in_hspeed) == self.hspeed / abs(self.hspeed):
                        self.hspeed -= change_in_hspeed
                    else:
                        self.hspeed += change_in_hspeed
                if self.vspeed != 0:
                    if change_in_vspeed / abs(change_in_vspeed) == self.vspeed / abs(self.vspeed):
                        self.vspeed -= change_in_vspeed
                    else:
                        self.vspeed += change_in_vspeed
            else:
                self.hspeed = 0
                self.vspeed = 0
        self.x += self.hspeed
        self.y += self.vspeed

        # Столкновение со стенками
        if self.x > display_width:
            self.x = 0
        elif self.x < 0:
            self.x = display_width
        elif self.y > display_height:
            self.y = 0
        elif self.y < 0:
            self.y = display_height

        # Поворот
        self.dir += self.rtspd

    def drawShip(self):
        x = self.x
        y = self.y
        t = self.thrust

        # Отрисовка корабля
        if t:
            self.image = spaceship
        else:
            self.image = spaceship_stop
        
        rotated_image = pygame.transform.rotate(self.image, -self.dir)

        world.blit(rotated_image, (x, y))

        gameDisplay.blit(world, pygame.rect.Rect(0,0, display_width, display_height))


    def killShip(self):
        # Возрождение
        self.x = display_width / 2
        self.y = display_height / 2
        self.thrust = False
        self.dir = -90
        self.hspeed = 0
        self.vspeed = 0

        self.image = spaceship_stop


def gameLoop(startingState):
    gameState = startingState
    ship_state = "Alive"
    ship_blink = 0
    ship_pieces = []
    ship_dying_delay = 0
    ship_invi_dur = 0
    hyperspace = 0
    next_level_delay = 0
    bullet_capacity = 4
    bullets = []
    asteroids = []
    stage = 3
    score = 0
    live = 2
    oneUp_multiplier = 1
    playOneUpSFX = 0
    intensity = 0
    ship = Ship(display_width / 2, display_height / 2)

    pygame.mixer.Sound.play(main_music)

    # Главный цикл
    while gameState != "Exit":
        # Стартовое меню
        while gameState == "Menu":
            world.blit(background, (1, 1))
            gameDisplay.blit(world, pygame.rect.Rect(0,0, display_width, display_height))
            drawText("ASTEROIDS", white, display_width / 2, display_height / 2, 100)
            drawText("Press any key to START", white, display_width / 2, display_height / 2 + 100, 50)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameState = "Exit"
                if event.type == pygame.KEYDOWN:
                    gameState = "Playing"
            pygame.display.update()
            timer.tick(5)

        # Сама игра
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameState = "Exit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    ship.thrust = True
                if event.key == pygame.K_LEFT:
                    ship.rtspd = -(ship_max_rtspd**2)
                if event.key == pygame.K_RIGHT:
                    ship.rtspd = (ship_max_rtspd**2)
                if event.key == pygame.K_SPACE and ship_dying_delay == 0 and len(bullets) < bullet_capacity:
                    bullets.append(Bullet(ship.x, ship.y, ship.dir))
                    # Звуковые эффекты
                    pygame.mixer.Sound.play(snd_fire)
                if gameState == "Game Over":
                    if event.key == pygame.K_r:
                        gameState = "Exit"
                        gameLoop("Playing")
                if event.key == pygame.K_LSHIFT:
                    hyperspace = 30
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    ship.thrust = False
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    ship.rtspd = 0

        ship.updateShip()

        if ship_invi_dur != 0:
            ship_invi_dur -= 1
        elif hyperspace == 0:
            ship_state = "Alive"

        # Перерисовка дисплея
        gameDisplay.fill(black)
        world.blit(background, (1, 1))
        gameDisplay.blit(world, pygame.rect.Rect(0,0, display_width, display_height))

        # Гиперскорость
        if hyperspace != 0:
            ship_state = "Died"
            hyperspace -= 1
            if hyperspace == 1:
                ship.x = random.randrange(0, display_width)
                ship.y = random.randrange(0, display_height)

        # Проверка на столкновение корабля с астероидом
        for a in asteroids:
            a.updateAsteroid()
            if ship_state != "Died":
                if isColliding(ship.x, ship.y, a.x, a.y, a.size):
                    # Create ship fragments
                    ship_pieces.append(deadShip(ship.x, ship.y, 5 * ship_size / (2 * math.cos(math.atan(1 / 3)))))
                    ship_pieces.append(deadShip(ship.x, ship.y, 5 * ship_size / (2 * math.cos(math.atan(1 / 3)))))
                    ship_pieces.append(deadShip(ship.x, ship.y, ship_size))

                    # Уничтожение корабля
                    ship_state = "Died"
                    ship_dying_delay = 30
                    ship_invi_dur = 120
                    ship.killShip()

                    if live != 0:
                        live -= 1
                    else:
                        gameState = "Game Over"

                    # Разделение астероида
                    if a.type == "Large":
                        asteroids.append(Asteroid(a.x, a.y, "Normal"))
                        asteroids.append(Asteroid(a.x, a.y, "Normal"))
                        score += 20
                        # Звуковые эффекты
                        pygame.mixer.Sound.play(snd_bangL)
                    elif a.type == "Normal":
                        asteroids.append(Asteroid(a.x, a.y, "Small"))
                        asteroids.append(Asteroid(a.x, a.y, "Small"))
                        score += 50
                        # Звуковые эффекты
                        pygame.mixer.Sound.play(snd_bangM)
                    else:
                        score += 100
                        # Звуковые эффекты
                        pygame.mixer.Sound.play(snd_bangS)
                    asteroids.remove(a)

        # Обновление фрагментов корабля
        for f in ship_pieces:
            f.updateDeadShip()
            if f.x > display_width or f.x < 0 or f.y > display_height or f.y < 0:
                ship_pieces.remove(f)

        # Проверка на конец уровня
        if len(asteroids) == 0:
            if next_level_delay < 30:
                next_level_delay += 1
            else:
                stage += 1
                intensity = 0
                # Астероиды создаются вне центральной части экрана
                for i in range(stage*2):
                    xTo = display_width / 2
                    yTo = display_height / 2
                    while xTo - display_width / 2 < display_width / 4 and yTo - display_height / 2 < display_height / 4:
                        xTo = random.randrange(0, display_width)
                        yTo = random.randrange(0, display_height)
                    asteroids.append(Asteroid(xTo, yTo, "Large"))
                next_level_delay = 0

        # Повышение общей скорости игры
        if intensity < stage * 450:
            intensity += 1

        for b in bullets:
            b.updateBullet()

            # Проверка на столкновение пули с астероидом
            for a in asteroids:
                if b.x > a.x - a.size and b.x < a.x + a.size and b.y > a.y - a.size and b.y < a.y + a.size:
                    # Разделение астероида
                    if a.type == "Large":
                        asteroids.append(Asteroid(a.x, a.y, "Normal"))
                        asteroids.append(Asteroid(a.x, a.y, "Normal"))
                        score += 20
                        # Звуковые эффекты
                        pygame.mixer.Sound.play(snd_bangL)
                    elif a.type == "Normal":
                        asteroids.append(Asteroid(a.x, a.y, "Small"))
                        asteroids.append(Asteroid(a.x, a.y, "Small"))
                        score += 50
                        # Звуковые эффекты
                        pygame.mixer.Sound.play(snd_bangM)
                    else:
                        score += 100
                        # Звуковые эффекты
                        pygame.mixer.Sound.play(snd_bangS)
                    asteroids.remove(a)
                    bullets.remove(b)

                    break

            # Самоуничтожение пули
            if b.life <= 0:
                try:
                    bullets.remove(b)
                except ValueError:
                    continue

        # Доп жизнь
        if score > oneUp_multiplier * 5000:
            oneUp_multiplier += 1
            live += 1
            playOneUpSFX = 60
        # Звуковые эффекты
        if playOneUpSFX > 0:
            playOneUpSFX -= 1
            pygame.mixer.Sound.play(snd_extra)

        # Отрисовка счета
        drawText("Score = " + str(score), white, 550, 40, 40, False)

        # Отрисовка корабля
        if gameState != "Game Over":
            if ship_state == "Died":
                if hyperspace == 0:
                    if ship_dying_delay == 0:
                        if ship_blink < 5:
                            if ship_blink == 0:
                                ship_blink = 10
                            else:
                                ship.drawShip()
                        ship_blink -= 1
                    else:
                        ship_dying_delay -= 1
            else:
                ship.drawShip()
        else:
            drawText("Game Over", white, display_width / 2, display_height / 2, 100)
            drawText("Press \"R\" to restart!", white, display_width / 2, display_height / 2 + 100, 50)
            live = -1

        # Отрисовка жизней
        for l in range(live + 1):
            Ship(75 + l * 25, 30).drawShip()

        # Обновление
        pygame.display.update()

        timer.tick(30)

gameLoop("Menu")

pygame.quit()
quit()