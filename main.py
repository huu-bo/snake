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

score = 0


def gen_apple() -> tuple[int, int]:
    board = [[0 for i in range(WORLD_SIZE)] for j in range(WORLD_SIZE)]
    for p in snake:
        board[p[1]][p[0]] = 1
    choices = []
    for i in range(WORLD_SIZE):
        for j in range(WORLD_SIZE):
            if board[j][i] == 0:
                choices.append((i, j))

    for corner in (
            (0, 0), (WORLD_SIZE - 1, 0),
            (0, WORLD_SIZE - 1), (WORLD_SIZE - 1, WORLD_SIZE - 1)
    ):
        if corner in choices:
            choices.remove(corner)

    if not choices:
        print('you won')  # TODO: display on-screen

    return random.choice(choices)


apple = gen_apple()

last_move_dir = (0, 0)


def move(x: int, y: int) -> bool:
    moved = _move(x, y)
    if moved:
        global move_timer
        move_timer = 0
    return moved


def _move(x: int, y: int) -> bool:
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


def draw_snake_piece(offset: tuple[int, int]) -> None:
    offset = (
        offset[0] * (SNAKE_OFFSET * 2),
        offset[1] * (SNAKE_OFFSET * 2)
    )
    pygame.draw.rect(screen, (0, 255, 0),
                     (part[0] * SIZE + SNAKE_OFFSET + offset[0], part[1] * SIZE + SNAKE_OFFSET + offset[1],
                      SIZE - SNAKE_OFFSET * 2, SIZE - SNAKE_OFFSET * 2))


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
                last_move_dir = (0, 0)
                score = 0

    pygame.draw.rect(screen, (255, 0, 0), (apple[0] * SIZE, apple[1] * SIZE, SIZE, SIZE))
    if apple == snake[-1]:
        apple = gen_apple()
        snake.insert(0, snake[0])
        score += 1

    prev = None
    for part in snake:
        if prev is not None:
            offset = ((prev[0] - part[0]), (prev[1] - part[1]))
            draw_snake_piece(offset)

        pygame.draw.rect(screen, (0, 255, 0),
                         (part[0] * SIZE + SNAKE_OFFSET, part[1] * SIZE + SNAKE_OFFSET,
                          SIZE - SNAKE_OFFSET * 2, SIZE - SNAKE_OFFSET * 2))
        prev = part

    offset_strength = SNAKE_OFFSET // 3
    if state == State.GAME_OVER:
        offset_strength = SNAKE_OFFSET
    offset = (last_move_dir[0] * offset_strength, last_move_dir[1] * offset_strength)
    pygame.draw.circle(screen, (0, 0, 0),
                       (snake[-1][0] * SIZE + SIZE // 2 + offset[0], snake[-1][1] * SIZE + SIZE // 2 + offset[1]), SIZE // 3)

    render_score = True
    if state == State.GAME_OVER:
        pos = (min(apple[0] * SIZE, SIZE * (WORLD_SIZE // 3 * 2)), apple[1] * SIZE)
        s = 'Game over'
        if pos[0] < SIZE * 2:
            s = f'Game over, score: {score}'
            render_score = False
        screen.blit(font.render(s, True, (255, 255, 255)),
                    pos)

    if render_score:
        screen.blit(font.render(f'{score}', True, (255, 255, 255)), (0, 0))

    timer_offset = int(move_timer / MOVE_TIME * 2)
    pygame.draw.rect(screen, (255, 255, 255),
                     (0, screen.get_height() - timer_offset, move_timer / MOVE_TIME * screen.get_width(), timer_offset))
    move_timer += 1
    pygame.display.update()

pygame.quit()
