import pygame
import random
import sys

pygame.init()

# Налаштування екрану
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Гонки")

# Кольори
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GRAY = (50, 50, 50)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
DARK_GRAY = (30, 30, 30)  # Темно-сірий
LIGHT_GRAY = (70, 70, 70)  # Світло-сірий

# Шрифт
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)  # Менший шрифт для інструкцій

# Глобальні змінні
lives = 3
speed = 5
enemy_speed = 2
enemy_speed_increment = 0.1
max_enemies = 5  # Максимальна кількість ворогів

def draw_text(text, x, y, font_type=font):
    text_surface = font_type.render(text, True, WHITE)
    screen.blit(text_surface, (x, y))

class Button:
    def __init__(self, text, x, y, width, height, color, hover_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
    
    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.rect(screen, self.hover_color if self.rect.collidepoint(mouse_pos) else self.color, self.rect)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

def settings_menu():
    global lives, speed
    
    while True:
        screen.fill((0, 0, 0))
        draw_text("Налаштування", 180, 100)
        
        button_plus_lives = Button("+", 260, 200, 40, 40, GREEN, (0, 255, 0))
        button_minus_lives = Button("-", 200, 200, 40, 40, RED, (255, 0, 0))
        button_plus_speed = Button("+", 260, 300, 40, 40, GREEN, (0, 255, 0))
        button_minus_speed = Button("-", 200, 300, 40, 40, RED, (255, 0, 0))
        button_back = Button("Назад", 150, 400, 200, 50, BLUE, (0, 0, 255))
        
        for button in [button_plus_lives, button_minus_lives, button_plus_speed, button_minus_speed, button_back]:
            button.draw()
        
        draw_text(f"Життя: {lives}", 220, 160)
        draw_text(f"Швидкість: {speed}", 200, 260)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_plus_lives.is_clicked(event) and lives < 50:
                    lives += 1
                if button_minus_lives.is_clicked(event) and lives > 1:
                    lives -= 1
                if button_plus_speed.is_clicked(event) and speed < 40:
                    speed += 1
                if button_minus_speed.is_clicked(event) and speed > 1:
                    speed -= 1
                if button_back.is_clicked(event):
                    return

def instructions_menu():
    while True:
        screen.fill((0, 0, 0))
        draw_text("Інструкції", 200, 50, font)
        draw_text("Керування:", 150, 100, small_font)
        draw_text("Лівий курсор - вліво", 150, 140, small_font)
        draw_text("Правий курсор - вправо", 150, 180, small_font)
        draw_text("Уникайте ворогів і збирайте очки!", 150, 220, small_font)
        draw_text("Натисніть 'Назад' для повернення", 150, 300, small_font)

        button_back = Button("Назад", 150, 400, 200, 50, DARK_GRAY, LIGHT_GRAY)
        button_back.draw()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_back.is_clicked(event):
                    return

def game_loop():
    global lives, speed, enemy_speed
    
    player_x = WIDTH // 2 - 25
    player_y = HEIGHT - 90
    clock = pygame.time.Clock()
    enemies = []
    enemy_timer = 0
    score = 0
    running = True
    start_time = pygame.time.get_ticks()  # Зберігаємо час початку гри
    
    while running:
        screen.fill(GRAY)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= speed  
        if keys[pygame.K_RIGHT] and player_x < WIDTH - 50:
            player_x += speed  
        
        enemy_timer += 1
        if enemy_timer > 60 and len(enemies) < max_enemies:
            enemies.append([random.randint(0, WIDTH - 50), 0])
            enemy_timer = 0
        
        for enemy in enemies:
            enemy[1] += enemy_speed
            if enemy[1] > HEIGHT:
                enemies.remove(enemy)
                score += 10  
        
        if score % 10 == 0 and score > 0:
            enemy_speed += enemy_speed_increment
            score += 1  # Запобігає постійному додаванню швидкості
        
        for enemy in enemies:
            if pygame.Rect(player_x, player_y, 50, 80).colliderect(pygame.Rect(enemy[0], enemy[1], 50, 50)):
                lives -= 1
                enemies.remove(enemy)
                if lives <= 0:
                    running = False
        
        # Обчислюємо час, що минув
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # Перетворюємо в секунди
        
        draw_text(f"Життя: {lives}", 10, 10)
        draw_text(f"Очки: {score}", 10, 50)
        draw_text(f"Час: {elapsed_time} с", 10, 90)  # Відображаємо час
        pygame.draw.rect(screen, YELLOW, (player_x, player_y, 50, 80))
        for enemy in enemies:
            pygame.draw.rect(screen, RED, (enemy[0], enemy[1], 50, 50))
        
        pygame.display.flip()
        clock.tick(60)
    
    main_menu()

def main_menu():
    while True:
        screen.fill((0, 0, 0))
        draw_text("Гонки", 200, 100)
        
        button_start = Button("Почати гру", 150, 250, 200, 50, DARK_GRAY, LIGHT_GRAY)
        button_settings = Button("Налаштування", 150, 320, 200, 50, DARK_GRAY, LIGHT_GRAY)
        button_instructions = Button("Інструкція", 150, 390, 200, 50, DARK_GRAY, LIGHT_GRAY)
        button_exit = Button("Вийти", 150, 460, 200, 50, RED, (255, 0, 0))
        
        for button in [button_start, button_settings, button_instructions, button_exit]:
            button.draw()
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_start.is_clicked(event):
                    game_loop()
                if button_settings.is_clicked(event):
                    settings_menu()
                if button_instructions.is_clicked(event):
                    instructions_menu()
                if button_exit.is_clicked(event):
                    pygame.quit()
                    sys.exit()

main_menu()
