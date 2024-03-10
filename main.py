import enum

import pygame
pygame.init()

SIZE = 80
WORLD_SIZE = 10

screen = pygame.display.set_mode((SIZE * WORLD_SIZE, SIZE * WORLD_SIZE))
clock = pygame.time.Clock()


class State(enum.IntEnum):
    PLAY = enum.auto()
    PAUSE = enum.auto()
    GAME_OVER = enum.auto()


state = State.PLAY


snake = [(6 - i, 5) for i in range(3)]
move_timer = 0
MOVE_TIME = 60

last_move_dir = (0, 0)


def move(x: int, y: int) -> bool:
    if x != 0 and y != 0:
        raise ValueError
    if x == 0 and y == 0:
        raise ValueError

    global last_move_dir
    moved = (x, y) == last_move_dir
    last_move_dir = (x, y)
    if moved:
        return False

    global snake

    new_pos = (snake[-1][0] + x, snake[-1][1] + y)
    if new_pos in snake:
        global state
        state = State.GAME_OVER
        return False

    for i in range(len(snake) - 1):
        snake[i] = snake[i+1]
    snake[-1] = new_pos

    return True


run = True
while run:
    clock.tick(60)
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.KEYDOWN:
            if state == State.PLAY:
                if event.key == pygame.K_w:
                    move(0, -1)
                elif event.key == pygame.K_s:
                    move(0, 1)

                elif event.key == pygame.K_a:
                    move(-1, 0)
                elif event.key == pygame.K_d:
                    move(1, 0)

    for part in snake:
        pygame.draw.rect(screen, (0, 255, 0), (part[0] * SIZE, part[1] * SIZE, SIZE, SIZE))
    pygame.draw.circle(screen, (0, 0, 0), (snake[-1][0] * SIZE + SIZE // 2, snake[-1][1] * SIZE + SIZE // 2), SIZE // 3)

    pygame.display.update()

pygame.quit()
