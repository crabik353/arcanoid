import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Арканоид")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)

background = pygame.image.load("background_first.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

def start_screen():
    while True:
        screen.blit(background, (0, 0))
        text = font.render('Для начала игры нажмите на любую клавишу', True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return

def level_selection():
    while True:
        screen.fill(BLACK)
        text = font.render('Выберите уровень', True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 50))

        level1_button = pygame.Rect(WIDTH // 2 - 50, 200, 100, 100)
        level2_button = pygame.Rect(WIDTH // 2 - 50, 350, 100, 100)

        pygame.draw.rect(screen, ORANGE, level1_button)
        pygame.draw.rect(screen, ORANGE, level2_button)

        level1_text = small_font.render('1', True, WHITE)
        level2_text = small_font.render('2', True, WHITE)

        screen.blit(level1_text, (level1_button.x + 40, level1_button.y + 35))
        screen.blit(level2_text, (level2_button.x + 40, level2_button.y + 35))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if level1_button.collidepoint(event.pos):
                    return 1
                if level2_button.collidepoint(event.pos):
                    return 2

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.type = type
        self.image = pygame.Surface((40, 40))
        if type == 1:
            self.image.fill((0, 255, 0))
        elif type == 2:
            self.image.fill((255, 255, 0))
        elif type == 3:
            self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hits = 0

    def update(self):
        if self.type == 2 and self.hits == 1:
            self.image.fill((0, 255, 0))
            self.type = 1

class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((100, 20))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2 - 50
        self.rect.y = HEIGHT - 30

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > WIDTH - 100:
            self.rect.x = WIDTH - 100

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2 - 10
        self.rect.y = HEIGHT - 50
        self.speed_x = 0
        self.speed_y = 0

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.x <= 0 or self.rect.x >= WIDTH - 20:
            self.speed_x = -self.speed_x
        if self.rect.y <= 0:
            self.speed_y = -self.speed_y

    def launch(self):
        self.speed_x = 4
        self.speed_y = -4

class Bonus(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.type = type
        self.image = pygame.Surface((20, 20))
        if type == 1:
            self.image.fill((255, 0, 255))
        elif type == 2:
            self.image.fill((0, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += 2

def game_over_screen():
    while True:
        screen.fill(BLACK)
        text = font.render('Вы проиграли!', True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 100))

        restart_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
        menu_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 70, 200, 50)

        pygame.draw.rect(screen, ORANGE, restart_button)
        pygame.draw.rect(screen, ORANGE, menu_button)

        restart_text = small_font.render('Играть заново', True, WHITE)
        menu_text = small_font.render('Вернуться в меню', True, WHITE)

        screen.blit(restart_text, (restart_button.x + 20, restart_button.y + 15))
        screen.blit(menu_text, (menu_button.x + 10, menu_button.y + 15))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    return "restart"
                if menu_button.collidepoint(event.pos):
                    return "menu"

def pause_screen():
    while True:
        screen.fill(BLACK)
        text = font.render('Пауза', True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 100))

        continue_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
        menu_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 70, 200, 50)

        pygame.draw.rect(screen, ORANGE, continue_button)
        pygame.draw.rect(screen, ORANGE, menu_button)

        continue_text = small_font.render('Продолжить', True, WHITE)
        menu_text = small_font.render('Вернуться в меню', True, WHITE)

        screen.blit(continue_text, (continue_button.x + 20, continue_button.y + 15))
        screen.blit(menu_text, (menu_button.x + 10, menu_button.y + 15))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.collidepoint(event.pos):
                    return "continue"
                if menu_button.collidepoint(event.pos):
                    return "menu"

def game_loop(level):
    pygame.mixer.music.load("track1.mp3")
    pygame.mixer.music.play(-1)

    all_sprites = pygame.sprite.Group()
    bricks = pygame.sprite.Group()
    balls = pygame.sprite.Group()
    bonuses = pygame.sprite.Group()
    paddle = Paddle()
    ball = Ball()
    all_sprites.add(paddle)
    all_sprites.add(ball)
    balls.add(ball)

    if level == 1:
        for i in range(10):
            for j in range(2):
                brick = Brick(i * 45 + 10, j * 45 + 50, 1)
                all_sprites.add(brick)
                bricks.add(brick)
    elif level == 2:
        for i in range(4):
            for j in range(10):
                brick = Brick(i * 45 + 10, j * 45 + 50, 1)
                all_sprites.add(brick)
                bricks.add(brick)
                brick = Brick(WIDTH - (i + 1) * 45 - 10, j * 45 + 50, 1)
                all_sprites.add(brick)
                bricks.add(brick)
        for i in range(10):
            brick = Brick(4 * 45 + 10, i * 45 + 50, 3)
            all_sprites.add(brick)
            bricks.add(brick)
        for i in range(10):
            brick = Brick(WIDTH - 5 * 45 - 10, i * 45 + 50, 3)
            all_sprites.add(brick)
            bricks.add(brick)
        brick = Brick(4 * 45 + 10, 0, 1)
        all_sprites.add(brick)
        bricks.add(brick)

    running = True
    paused = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = True
                if event.key == pygame.K_SPACE and ball.speed_x == 0 and ball.speed_y == 0:
                    ball.launch()

        if paused:
            result = pause_screen()
            if result == "continue":
                paused = False
            elif result == "menu":
                pygame.mixer.music.stop()
                return "menu"

        all_sprites.update()

        for ball in balls:
            if pygame.sprite.collide_rect(ball, paddle):
                ball.speed_y = -ball.speed_y

            brick_collisions = pygame.sprite.spritecollide(ball, bricks, False)
            for brick in brick_collisions:
                if brick.type == 1:
                    if random.random() < 0.1:
                        bonus = Bonus(brick.rect.x, brick.rect.y, random.randint(1, 2))
                        all_sprites.add(bonus)
                        bonuses.add(bonus)
                    brick.kill()
                elif brick.type == 2:
                    brick.hits += 1
                    if brick.hits == 2:
                        brick.kill()
                ball.speed_y = -ball.speed_y

            if ball.rect.y >= HEIGHT - 20:
                balls.remove(ball)
                all_sprites.remove(ball)
                if len(balls) == 0:
                    pygame.mixer.music.stop()
                    result = game_over_screen()
                    if result == "restart":
                        return "restart"
                    elif result == "menu":
                        return "menu"

        bonus_collisions = pygame.sprite.spritecollide(paddle, bonuses, True)
        for bonus in bonus_collisions:
            if bonus.type == 1:
                new_balls = []
                for ball in balls:
                    for _ in range(2):
                        new_ball = Ball()
                        new_ball.rect.x = ball.rect.x
                        new_ball.rect.y = ball.rect.y
                        new_ball.speed_x = ball.speed_x
                        new_ball.speed_y = ball.speed_y
                        new_balls.append(new_ball)
                balls.add(new_balls)
                all_sprites.add(new_balls)
            elif bonus.type == 2:
                for _ in range(2):
                    new_ball = Ball()
                    new_ball.rect.x = paddle.rect.x + paddle.rect.width // 2
                    new_ball.rect.y = paddle.rect.y - 20
                    new_ball.speed_x = random.choice([-4, 4])
                    new_ball.speed_y = -4
                    balls.add(new_ball)
                    all_sprites.add(new_ball)

        if len(bricks) == 0:
            running = False

        screen.fill(BLACK)
        all_sprites.draw(screen)
        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.mixer.music.stop()
    return "menu"

start_screen()
while True:
    selected_level = level_selection()
    result = game_loop(selected_level)
    if result == "menu":
        continue
    elif result == "restart":
        result = game_loop(selected_level)
        if result == "menu":
            continue