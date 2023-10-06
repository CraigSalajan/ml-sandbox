import math

import pygame

from environments.Snake.entities.Color import Color


def normalize(x, y):
    c = math.sqrt(x*x + y*y)
    return x/c, y/c


def handle_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            return None
    key_list = pygame.key.get_pressed()
    if key_list[pygame.K_ESCAPE]:
        pygame.display.quit()
        pygame.quit()
        return None
    key_list = pygame.key.get_pressed()
    u, d, l, r = key_list[pygame.K_UP] or key_list[pygame.K_w], \
        key_list[pygame.K_DOWN] or key_list[pygame.K_s], \
        key_list[pygame.K_LEFT] or key_list[pygame.K_a], \
        key_list[pygame.K_RIGHT] or key_list[pygame.K_d]
    if u:
        return 0
    if d:
        return 1
    if l:
        return 2
    if r:
        return 3
    return None


def update_screen(screen, snake, human_playing=False):
    if not pygame.display.get_init():
        return
    width = screen.get_width()
    height = screen.get_height() - 40
    font = pygame.font.SysFont('microsoft Yahei', 30, True)
    score = font.render('Scores: '+str(snake.score), False, Color.purple)
    # episode = font.render('Episodes: '+str(snake.episode), False, Color.purple)
    # step_remain = font.render(
    #     'Steps Remain: '+str(snake.max_step-snake.current_step), False, Color.purple)
    screen.fill(Color.orange)
    screen.blit(score, (20, height))
    if human_playing:
        fps = font.render('Speed: '+str(snake.fps), False, Color.purple)
        screen.blit(fps, (200, height))
    # else:
        # screen.blit(episode, (200, height))
        # screen.blit(step_remain, (500, height))

    for block in snake.blocks:
        pygame.draw.rect(screen, block.color, pygame.Rect(block.rect))
    pygame.draw.line(screen, Color.purple, (0, height),
                     (width, height), 2)
    pygame.display.flip()


def game_start(width, height, score_board=40):
    pygame.init()
    pygame.display.set_caption('Snake')
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height + score_board))
    return screen, clock
