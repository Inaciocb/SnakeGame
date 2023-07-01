import pygame
from pygame.locals import *
from sys import exit
import random

pygame.init()
largura = 640
altura = 480
x = largura // 2
y = altura // 2
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Jogo')
relogio = pygame.time.Clock()

fonte = pygame.font.SysFont(None, 36)

IS_PRESSED = False
direction = None

fruit_x = random.randint(0, largura - 30)
fruit_y = random.randint(0, altura - 30)

speed = 2
growth_rate = 20  
score = 0

snake = []

game_over = False

while not game_over:
    while True:
        relogio.tick(240)
        tela.fill((0, 0, 0))
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            if event.type == KEYDOWN:
                if event.key == K_a or event.key == K_LEFT:
                    direction = 'left'
                    IS_PRESSED = True
                elif event.key == K_d or event.key == K_RIGHT:
                    direction = 'right'
                    IS_PRESSED = True
                elif event.key == K_w or event.key == K_UP:
                    direction = 'up'
                    IS_PRESSED = True
                elif event.key == K_s or event.key == K_DOWN:
                    direction = 'down'
                    IS_PRESSED = True

            if event.type == KEYUP:
                IS_PRESSED = False

        if direction == 'left' and x > 0 and not IS_PRESSED:
            x -= speed
        elif direction == 'right' and x < largura - 30 and not IS_PRESSED:
            x += speed
        elif direction == 'up' and y > 0 and not IS_PRESSED:
            y -= speed
        elif direction == 'down' and y < altura - 30 and not IS_PRESSED:
            y += speed

        snake.insert(0, (x, y))

        if len(snake) > score + 1:
            snake.pop()

        pygame.draw.rect(tela, (255, 0, 0), (fruit_x, fruit_y, 30, 30))

        for segment in snake:
            pygame.draw.rect(tela, (255, 125, 0), (segment[0], segment[1], 30, 30))

        snake_rect = pygame.Rect(x, y, 30, 30)

        if snake_rect.colliderect(pygame.Rect(fruit_x, fruit_y, 30, 30)):
            fruit_x = random.randint(0, largura - 30)
            fruit_y = random.randint(0, altura - 30)
            speed += 0.05
            score += 1
            for _ in range(growth_rate):
                snake.append(snake[-1])  

        # Check for collision with itself
        for segment in snake[1:]:
            if snake_rect.colliderect(pygame.Rect(segment[0], segment[1], 30, 30)):
                game_over = True

        score_text = fonte.render("Score: " + str(score), True, (255, 255, 255))
        tela.blit(score_text, (10, 10))

        pygame.display.update()

    # Game over screen
    tela.fill((0, 0, 0))
    game_over_text = fonte.render("Game Over", True, (255, 255, 255))
    play_again_text = fonte.render("Play Again", True, (255, 255, 255))
    quit_text = fonte.render("Quit", True, (255, 255, 255))

    game_over_rect = game_over_text.get_rect(center=(largura // 2, altura // 2 - 50))
    play_again_rect = play_again_text.get_rect(center=(largura // 2, altura // 2 + 20))
    quit_rect = quit_text.get_rect(center=(largura // 2, altura // 2 + 80))

    tela.blit(game_over_text, game_over_rect)
    tela.blit(play_again_text, play_again_rect)
    tela.blit(quit_text, quit_rect)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if play_again_rect.collidepoint(mouse_pos):
                x = largura // 2
                y = altura // 2
                speed = 2
                growth_rate = 1
                score = 0
                snake.clear()
                game_over = False
            elif quit_rect.collidepoint(mouse_pos):
                pygame.quit()
                exit()
