import pygame
import sys
import time

pygame.init()

# Настройки экрана
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Арканоид")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (192, 192, 192)
DARK_GRAY = (64, 64, 64)

# Часы для контроля FPS
clock = pygame.time.Clock()
FPS = 60

# Загрузка звуков
paddle_sound = pygame.mixer.Sound("paddle_hit.wav")
block_sound = pygame.mixer.Sound("block_hit.wav")
wall_sound = pygame.mixer.Sound("wall_hit.wav")

# Переменные для управления звуком
music_enabled = True
sound_effects_enabled = True

# Музыка
tracks = [
    "track1.mp3", "track2.mp3", "track3.mp3",
    "track4.mp3", "track5.mp3", "track6.mp3",
    "track7.mp3", "track8.mp3", "track9.mp3"
]
current_track_index = 0
pygame.mixer.music.load(tracks[current_track_index])
pygame.mixer.music.set_volume(0.5)

# Цвета платформы и мяча
paddle_color = BLUE
ball_color = RED

# Таймер уровня
start_time = None

# Пропадающая надпись
notification_text = ""
notification_timer = 0

# Открытые уровни
unlocked_levels = [True] + [False] * 7


# Функция для отрисовки текста
def draw_text(text, font_size, color, x, y):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)


# Функция для отрисовки счета
def draw_score(score):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Счет: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))


# Функция для отрисовки таймера
def draw_timer(start_timer):
    if start_timer is not None:
        elapsed_time = int(start_timer.time() - start_timer)
        font = pygame.font.Font(None, 36)
        timer_text = font.render(f"Таймер: {elapsed_time}s", True, WHITE)
        screen.blit(timer_text, (SCREEN_WIDTH // 2 - 50, 10))


# Функция для отрисовки кнопок
def draw_button(text, x, y, width, height, hovered, font_size=36):
    color = LIGHT_GRAY if hovered else GRAY
    pygame.draw.rect(screen, color, (x, y, width, height))
    draw_text(text, font_size, WHITE, x + width // 2, y + height // 2)


# Класс платформы
class Paddle(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.width = 100
        self.height = 20
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30)
        self.speed = 8
        self.locked = True

    def update(self, keys):
        if not self.locked:
            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0:
                self.rect.x -= self.speed
            if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < SCREEN_WIDTH:
                self.rect.x += self.speed


# Класс мяча
class Ball(pygame.sprite.Sprite):
    def __init__(self, color, dx=4, dy=-4):
        super().__init__()
        self.radius = 10
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.dx = dx
        self.dy = dy
        self.launched = False

    def launch(self):
        if not self.launched:
            self.launched = True

    def update(self):
        if self.launched:
            self.rect.x += self.dx
            self.rect.y += self.dy

            if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
                self.dx = -self.dx
                if sound_effects_enabled:
                    wall_sound.play()
            if self.rect.top <= 0:
                self.dy = -self.dy
                if sound_effects_enabled:
                    wall_sound.play()


# Класс блока
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, hits=1, indestructible=False):
        super().__init__()
        self.width = 50
        self.height = 50
        self.hits = hits
        self.indestructible = indestructible
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(WHITE if not indestructible else GRAY)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def hit(self):
        if self.indestructible:
            return False
        self.hits -= 1
        if self.hits <= 0:
            return True
        else:
            self.image.fill((255, 0, 0))
            return False


# Начальный экран
def start_screen():
    global music_enabled
    if music_enabled:
        pygame.mixer.music.play(-1)
    while True:
        screen.fill(BLACK)
        draw_text("Арканоид", 72, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
        draw_text("Нажмите любую клавишу для продолжения", 24, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return

        pygame.display.flip()
        clock.tick(FPS)


# Главное меню
def main_menu():
    menu_running = True
    while menu_running:
        screen.fill(BLACK)
        draw_text("Главное меню", 48, WHITE, SCREEN_WIDTH // 2, 100)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Кнопка "Играть"
        play_hovered = (SCREEN_WIDTH // 2 - 100 < mouse_x < SCREEN_WIDTH // 2 + 100 and 200 < mouse_y < 250)
        draw_button("Играть", SCREEN_WIDTH // 2 - 100, 200, 200, 50, play_hovered)

        # Кнопка "Настройки"
        settings_hovered = (SCREEN_WIDTH // 2 - 100 < mouse_x < SCREEN_WIDTH // 2 + 100 and 300 < mouse_y < 350)
        draw_button("Настройки", SCREEN_WIDTH // 2 - 100, 300, 200, 50, settings_hovered)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_hovered:
                    level_selection()
                elif settings_hovered:
                    settings_menu()

        pygame.display.flip()
        clock.tick(FPS)


# Окно выбора уровней
def level_selection():
    levels_running = True
    while levels_running:
        screen.fill(BLACK)
        draw_text("Выбор уровня", 48, WHITE, SCREEN_WIDTH // 2, 50)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Кнопка "Меню"
        menu_hovered = (10 < mouse_x < 110 and 10 < mouse_y < 60)
        draw_button("Меню", 10, 10, 100, 50, menu_hovered, font_size=24)

        # Кнопки уровней
        for i in range(8):
            button_hovered = (
                    SCREEN_WIDTH // 2 - 100 < mouse_x < SCREEN_WIDTH // 2 + 100 and 100 + i * 60
                    < mouse_y < 150 + i * 60)
            draw_button(f"Уровень {i + 1}", SCREEN_WIDTH // 2 - 100, 100 + i * 60, 200, 50,
                        button_hovered and unlocked_levels[i], font_size=36)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_hovered:
                    levels_running = False
                for i in range(8):
                    if (unlocked_levels[i] and SCREEN_WIDTH // 2 - 100 < mouse_x < SCREEN_WIDTH // 2 + 100 and 100 + i *
                            60 < mouse_y < 150 + i * 60):
                        play_level(i + 1)

        pygame.display.flip()
        clock.tick(FPS)


# Игра на уровне
def play_level(level):
    global paddle_color, ball_color, start_time, notification_text, notification_timer, unlocked_levels

    start_time = time.time()
    notification_text = ""
    notification_timer = 0

    paddle = Paddle(paddle_color)
    balls = pygame.sprite.Group()
    initial_ball = Ball(ball_color)
    balls.add(initial_ball)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(paddle)
    all_sprites.add(initial_ball)

    blocks = pygame.sprite.Group()
    if level == 1:
        for row in range(3):
            for col in range(SCREEN_WIDTH // (50 + 5)):  # 50 - ширина кирпича, 5 - отступ
                block = Block(col * (50 + 5), row * (50 + 5) + 50)  # 50 - отступ сверху
                blocks.add(block)
                all_sprites.add(block)
    elif level == 2:
        for row in range(5):
            for col in range(SCREEN_WIDTH // (50 + 5)):  # 50 - ширина кирпича, 5 - отступ
                block = Block(col * (50 + 5), row * (50 + 5) + 50, hits=2)  # 50 - отступ сверху
                blocks.add(block)
                all_sprites.add(block)
    elif level == 3:
        for row in range(6):
            for col in range(SCREEN_WIDTH // (50 + 5)):
                if row % 2 == 0:
                    block = Block(col * (50 + 5), row * (50 + 5) + 50, indestructible=True)
                else:
                    block = Block(col * (50 + 5), row * (50 + 5) + 50, hits=2)
                blocks.add(block)
                all_sprites.add(block)
    elif level == 4:
        for row in range(7):
            for col in range(SCREEN_WIDTH // (50 + 5)):
                if col % 2 == 0:
                    block = Block(col * (50 + 5), row * (50 + 5) + 50, indestructible=True)
                else:
                    block = Block(col * (50 + 5), row * (50 + 5) + 50, hits=3)
                blocks.add(block)
                all_sprites.add(block)
    elif level == 5:
        for row in range(8):
            for col in range(SCREEN_WIDTH // (50 + 5)):
                block = Block(col * (50 + 5), row * (50 + 5) + 50, hits=3)
                blocks.add(block)
                all_sprites.add(block)
    elif level == 6:
        for row in range(9):
            for col in range(SCREEN_WIDTH // (50 + 5)):
                if row == 0 or row == 8:
                    block = Block(col * (50 + 5), row * (50 + 5) + 50, indestructible=True)
                else:
                    block = Block(col * (50 + 5), row * (50 + 5) + 50, hits=4)
                blocks.add(block)
                all_sprites.add(block)
    elif level == 7:
        for row in range(10):
            for col in range(SCREEN_WIDTH // (50 + 5)):
                if col % 2 == 0:
                    block = Block(col * (50 + 5), row * (50 + 5) + 50, indestructible=True)
                else:
                    block = Block(col * (50 + 5), row * (50 + 5) + 50, hits=5)
                blocks.add(block)
                all_sprites.add(block)
    elif level == 8:
        for row in range(12):
            for col in range(SCREEN_WIDTH // (50 + 5)):
                block = Block(col * (50 + 5), row * (50 + 5) + 50, hits=6)
                blocks.add(block)
                all_sprites.add(block)

    score = 0
    running = True
    while running:
        screen.fill(BLACK)
        all_sprites.draw(screen)
        draw_score(score)
        draw_timer(start_time)
        # Отрисовка пропадающей надписи
        if notification_timer > 0:
            notification_timer -= 1
            draw_text(notification_text, 24, WHITE, SCREEN_WIDTH // 2, 30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not initial_ball.launched:
                    initial_ball.launch()
                    paddle.locked = False
                elif event.key == pygame.K_ESCAPE:
                    pause_menu()

        keys = pygame.key.get_pressed()
        paddle.update(keys)
        balls.update()

        # Проверка столкновений
        for ball in balls:
            if pygame.sprite.collide_rect(ball, paddle):
                ball.dy = -ball.dy
                if sound_effects_enabled:
                    paddle_sound.play()

            hit_blocks = pygame.sprite.spritecollide(ball, blocks, False)
            for block in hit_blocks:
                if block.hit():
                    blocks.remove(block)
                    all_sprites.remove(block)
                    score += 10
                ball.dy = -ball.dy
                if sound_effects_enabled:
                    block_sound.play()

            if ball.rect.top > SCREEN_HEIGHT:
                pygame.mixer.music.stop()
                game_over_screen(level)

        if len(blocks) == 0:
            pygame.mixer.music.stop()
            if level < 8:
                unlocked_levels[level] = True
            victory_screen(level)

        pygame.display.flip()
        clock.tick(FPS)


# Пауза
def pause_menu():
    paused = True
    while paused:
        screen.fill(BLACK)
        draw_text("Пауза", 48, WHITE, SCREEN_WIDTH // 2, 200)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Кнопка "Продолжить"
        resume_hovered = (SCREEN_WIDTH // 2 - 150 < mouse_x < SCREEN_WIDTH // 2 + 150 and 300 < mouse_y < 350)
        draw_button("Продолжить", SCREEN_WIDTH // 2 - 150, 300, 300, 50, resume_hovered)

        # Кнопка "Выбор уровней"
        level_select_hovered = (SCREEN_WIDTH // 2 - 150 < mouse_x < SCREEN_WIDTH // 2 + 150 and 400 < mouse_y < 450)
        draw_button("Выбор уровней", SCREEN_WIDTH // 2 - 150, 400, 300, 50, level_select_hovered)

        # Кнопка "Настройки"
        settings_hovered = (SCREEN_WIDTH // 2 - 150 < mouse_x < SCREEN_WIDTH // 2 + 150 and 500 < mouse_y < 550)
        draw_button("Настройки", SCREEN_WIDTH // 2 - 150, 500, 300, 50, settings_hovered)

        # Кнопка "Меню"
        menu_hovered = (SCREEN_WIDTH // 2 - 150 < mouse_x < SCREEN_WIDTH // 2 + 150 and 600 < mouse_y < 650)
        draw_button("Меню", SCREEN_WIDTH // 2 - 150, 600, 300, 50, menu_hovered)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                paused = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_hovered:
                    paused = False
                elif level_select_hovered:
                    level_selection()
                elif settings_hovered:
                    settings_menu()
                elif menu_hovered:
                    main_menu()

        pygame.display.flip()
        clock.tick(FPS)


# Окно "Вы победили"
def victory_screen(level):
    while True:
        screen.fill(BLACK)
        draw_text("Вы победили!", 72, WHITE, SCREEN_WIDTH // 2, 200)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Кнопка "Сыграть снова"
        play_again_hovered = (SCREEN_WIDTH // 2 - 150 < mouse_x < SCREEN_WIDTH // 2 + 150 and 300 < mouse_y < 350)
        draw_button("Сыграть снова", SCREEN_WIDTH // 2 - 150, 300, 300, 50, play_again_hovered)

        # Кнопка "Выбор уровней"
        level_select_hovered = (SCREEN_WIDTH // 2 - 150 < mouse_x < SCREEN_WIDTH // 2 + 150 and 400 < mouse_y < 450)
        draw_button("Выбор уровней", SCREEN_WIDTH // 2 - 150, 400, 300, 50, level_select_hovered)

        # Кнопка "Главное меню"
        main_menu_hovered = (SCREEN_WIDTH // 2 - 150 < mouse_x < SCREEN_WIDTH // 2 + 150 and 500 < mouse_y < 550)
        draw_button("Главное меню", SCREEN_WIDTH // 2 - 150, 500, 300, 50, main_menu_hovered)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_hovered:
                    play_level(level)
                elif level_select_hovered:
                    level_selection()
                elif main_menu_hovered:
                    main_menu()

        pygame.display.flip()
        clock.tick(FPS)


# Окно "Вы проиграли"
def game_over_screen(level):
    while True:
        screen.fill(BLACK)
        draw_text("Вы проиграли!", 72, WHITE, SCREEN_WIDTH // 2, 200)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Кнопка "Сыграть снова"
        play_again_hovered = (SCREEN_WIDTH // 2 - 150 < mouse_x < SCREEN_WIDTH // 2 + 150 and 300 < mouse_y < 350)
        draw_button("Сыграть снова", SCREEN_WIDTH // 2 - 150, 300, 300, 50, play_again_hovered)

        # Кнопка "Выбор уровней"
        level_select_hovered = (SCREEN_WIDTH // 2 - 150 < mouse_x < SCREEN_WIDTH // 2 + 150 and 400 < mouse_y < 450)
        draw_button("Выбор уровней", SCREEN_WIDTH // 2 - 150, 400, 300, 50, level_select_hovered)

        # Кнопка "Главное меню"
        main_menu_hovered = (SCREEN_WIDTH // 2 - 150 < mouse_x < SCREEN_WIDTH // 2 + 150 and 500 < mouse_y < 550)
        draw_button("Главное меню", SCREEN_WIDTH // 2 - 150, 500, 300, 50, main_menu_hovered)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_hovered:
                    play_level(level)
                elif level_select_hovered:
                    level_selection()
                elif main_menu_hovered:
                    main_menu()

        pygame.display.flip()
        clock.tick(FPS)


# Окно настроек
def settings_menu():
    global music_enabled, sound_effects_enabled, paddle_color, ball_color, notification_text, notification_timer, \
        current_track_index

    settings_running = True
    volume_slider_x = SCREEN_WIDTH * 3 // 4
    volume_slider_width = 10
    volume_slider_height = 150
    volume_slider_y = SCREEN_HEIGHT // 2 + 100
    volume_slider_grabbed = False
    volume = pygame.mixer.music.get_volume()

    while settings_running:
        screen.fill(BLACK)
        draw_text("Настройки", 48, WHITE, SCREEN_WIDTH // 2, 50)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Левая колонка кнопок
        left_column_x = SCREEN_WIDTH // 4

        # Кнопка "Включить/выключить музыку"
        music_hovered = (left_column_x - 100 < mouse_x < left_column_x + 100 and 100 < mouse_y < 150)
        draw_button("Выключить музыку" if music_enabled else "Включить музыку", left_column_x - 100, 100, 200, 50,
                    music_hovered, font_size=24)

        # Кнопка "Включить/выключить звуковые эффекты" (продолжение)
        sound_effects_hovered = (left_column_x - 100 < mouse_x < left_column_x + 100 and 200 < mouse_y < 250)
        draw_button("Выключить звуковые эффекты" if sound_effects_enabled else "Включить звуковые эффекты",
                    left_column_x - 100, 200, 200, 50, sound_effects_hovered, font_size=24)

        # Кнопка "Управление"
        controls_hovered = (left_column_x - 100 < mouse_x < left_column_x + 100 and 300 < mouse_y < 350)
        draw_button("Управление", left_column_x - 100, 300, 200, 50, controls_hovered, font_size=24)

        # Правая колонка кнопок
        right_column_x = SCREEN_WIDTH * 3 // 4

        # Кнопка "Цвет платформы"
        paddle_color_hovered = (right_column_x - 100 < mouse_x < right_column_x + 100 and 100 < mouse_y < 150)
        draw_button("Цвет платформы", right_column_x - 100, 100, 200, 50, paddle_color_hovered, font_size=24)

        # Кнопка "Цвет мяча"
        ball_color_hovered = (right_column_x - 100 < mouse_x < right_column_x + 100 and 200 < mouse_y < 250)
        draw_button("Цвет мяча", right_column_x - 100, 200, 200, 50, ball_color_hovered, font_size=24)

        # Музыка
        track_text = f"Трек: {current_track_index + 1}"
        draw_text(track_text, 24, WHITE, SCREEN_WIDTH // 2, 350)

        # Стрелки для переключения треков
        left_arrow_hovered = (SCREEN_WIDTH // 2 - 100 < mouse_x < SCREEN_WIDTH // 2 - 50 and 400 < mouse_y < 450)
        pygame.draw.polygon(screen, LIGHT_GRAY if left_arrow_hovered else GRAY,
                            [(SCREEN_WIDTH // 2 - 100, 425), (SCREEN_WIDTH // 2 - 50, 400),
                             (SCREEN_WIDTH // 2 - 50, 450)])

        right_arrow_hovered = (SCREEN_WIDTH // 2 + 50 < mouse_x < SCREEN_WIDTH // 2 + 100 and 400 < mouse_y < 450)
        pygame.draw.polygon(screen, LIGHT_GRAY if right_arrow_hovered else GRAY,
                            [(SCREEN_WIDTH // 2 + 100, 425), (SCREEN_WIDTH // 2 + 50, 400),
                             (SCREEN_WIDTH // 2 + 50, 450)])

        # Ползунок громкости
        pygame.draw.rect(screen, GRAY, (volume_slider_x, volume_slider_y, volume_slider_width, volume_slider_height))
        slider_handle_y = volume_slider_y + int((1 - volume) * volume_slider_height)
        pygame.draw.circle(screen, WHITE, (volume_slider_x + volume_slider_width // 2, slider_handle_y), 10)

        # Кнопка "Назад"
        back_hovered = (SCREEN_WIDTH // 2 - 100 < mouse_x < SCREEN_WIDTH // 2 + 100 and 550 < mouse_y < 600)
        draw_button("Назад", SCREEN_WIDTH // 2 - 100, 550, 200, 50, back_hovered, font_size=36)

        # Логи
        if notification_timer > 0:
            notification_timer -= 1
            draw_text(notification_text, 24, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if music_hovered:
                    music_enabled = not music_enabled
                    if music_enabled:
                        pygame.mixer.music.unpause()
                    else:
                        pygame.mixer.music.pause()
                    notification_text = "- Музыка включена" if music_enabled else "- Музыка выключена"
                    notification_timer = FPS * 3
                elif sound_effects_hovered:
                    sound_effects_enabled = not sound_effects_enabled
                    notification_text = "- Звуковые эффекты включены" if sound_effects_enabled \
                        else "- Звуковые эффекты выключены"
                    notification_timer = FPS * 3
                elif paddle_color_hovered:
                    paddle_color = BLUE if paddle_color == RED else RED
                    notification_text = "- Цвет платформы изменен на: " + (
                        "СИНИЙ" if paddle_color == BLUE else "КРАСНЫЙ")
                    notification_timer = FPS * 3
                elif ball_color_hovered:
                    ball_color = RED if ball_color == BLUE else BLUE
                    notification_text = "- Цвет мяча изменен на: " + ("КРАСНЫЙ" if ball_color == RED else "СИНИЙ")
                    notification_timer = FPS * 3
                elif left_arrow_hovered:
                    current_track_index = (current_track_index - 1) % len(tracks)
                    pygame.mixer.music.load(tracks[current_track_index])
                    if music_enabled:
                        pygame.mixer.music.play(-1)
                    notification_text = f"- Трек изменен на: {current_track_index + 1}"
                    notification_timer = FPS * 3
                elif right_arrow_hovered:
                    current_track_index = (current_track_index + 1) % len(tracks)
                    pygame.mixer.music.load(tracks[current_track_index])
                    if music_enabled:
                        pygame.mixer.music.play(-1)
                    notification_text = f"- Трек изменен на: {current_track_index + 1}"
                    notification_timer = FPS * 3
                elif back_hovered:
                    settings_running = False
                elif controls_hovered:
                    controls_screen()
                elif (volume_slider_x < mouse_x < volume_slider_x + volume_slider_width
                      and volume_slider_y < mouse_y < volume_slider_y + volume_slider_height):
                    volume_slider_grabbed = True
            if event.type == pygame.MOUSEBUTTONUP:
                volume_slider_grabbed = False
            if event.type == pygame.MOUSEMOTION and volume_slider_grabbed:
                slider_handle_y = max(volume_slider_y, min(mouse_y, volume_slider_y + volume_slider_height))
                volume = 1 - (slider_handle_y - volume_slider_y) / volume_slider_height
                pygame.mixer.music.set_volume(volume)

        pygame.display.flip()
        clock.tick(FPS)


# Окно управления
def controls_screen():
    controls_running = True
    while controls_running:
        screen.fill(BLACK)
        draw_text("Управление", 48, WHITE, SCREEN_WIDTH // 2, 100)
        draw_text("A - Влево", 36, WHITE, SCREEN_WIDTH // 2, 200)
        draw_text("D - Вправо", 36, WHITE, SCREEN_WIDTH // 2, 250)
        draw_text("SPACE - Начать игру", 36, WHITE, SCREEN_WIDTH // 2, 300)
        draw_text("ESC - Пауза", 36, WHITE, SCREEN_WIDTH // 2, 350)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Кнопка "Назад"
        back_hovered = (SCREEN_WIDTH // 2 - 100 < mouse_x < SCREEN_WIDTH // 2 + 100 and 450 < mouse_y < 500)
        draw_button("Назад", SCREEN_WIDTH // 2 - 100, 450, 200, 50, back_hovered, font_size=36)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_hovered:
                    controls_running = False

        pygame.display.flip()
        clock.tick(FPS)


# Запуск игры
start_screen()
main_menu()
pygame.quit()
sys.exit()
