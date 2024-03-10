import enum
import random

import pygame
pygame.init()

SIZE = 80
WORLD_SIZE = 10

SNAKE_OFFSET = 10

font = pygame.font.SysFont('ubuntu', SIZE)
screen = pygame.display.set_mode((SIZE * WORLD_SIZE, SIZE * WORLD_SIZE))
clock = pygame.time.Clock()


class State(enum.IntEnum):
    PLAY = enum.auto()
    PAUSE = enum.auto()
    GAME_OVER = enum.auto()


state = State.PLAY


def gen_snake() -> list[tuple[int, int]]:
    return [(6 - i, 5) for i in range(3)]


snake = gen_snake()

move_timer = 0
MOVE_TIME = 60


def gen_apple() -> tuple[int, int]:
    board = [[0 for i in range(WORLD_SIZE)] for j in range(WORLD_SIZE)]
    for p in snake:
        board[p[1]][p[0]] = 1
    choices = []
    for i in range(WORLD_SIZE):
        for j in range(WORLD_SIZE):
            if board[j][i] == 0:
                choices.append((i, j))
    return random.choice(choices)


apple = gen_apple()

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
    if new_pos == snake[-2]:
        return False

    if (
            new_pos in snake
            or new_pos[0] < 0
            or new_pos[0] >= WORLD_SIZE
            or new_pos[1] < 0
            or new_pos[1] >= WORLD_SIZE
    ):
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

            if event.key == pygame.K_r:
                state = State.PLAY
                apple = gen_apple()
                snake = gen_snake()

    pygame.draw.rect(screen, (255, 0, 0), (apple[0] * SIZE, apple[1] * SIZE, SIZE, SIZE))
    if apple == snake[-1]:
        apple = gen_apple()
        snake.insert(0, snake[0])

    prev = None
    for part in snake:
        if prev is not None:
            offset = ((prev[0] - part[0]) * (SNAKE_OFFSET * 2), (prev[1] - part[1]) * (SNAKE_OFFSET * 2))
            pygame.draw.rect(screen, (0, 255, 0),
                             (part[0] * SIZE + SNAKE_OFFSET + offset[0], part[1] * SIZE + SNAKE_OFFSET + offset[1],
                              SIZE - SNAKE_OFFSET * 2, SIZE - SNAKE_OFFSET * 2))

        pygame.draw.rect(screen, (0, 255, 0),
                         (part[0] * SIZE + SNAKE_OFFSET, part[1] * SIZE + SNAKE_OFFSET,
                          SIZE - SNAKE_OFFSET * 2, SIZE - SNAKE_OFFSET * 2))
        prev = part

    pygame.draw.circle(screen, (0, 0, 0), (snake[-1][0] * SIZE + SIZE // 2, snake[-1][1] * SIZE + SIZE // 2), SIZE // 3)

    if state == State.GAME_OVER:
        screen.blit(font.render('Game over', True, (255, 255, 255)), (min(apple[0] * SIZE, SIZE * (WORLD_SIZE // 3 * 2)), apple[1] * SIZE))

    pygame.display.update()

pygame.quit()
