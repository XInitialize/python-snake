import os
import random
import sys
import threading
import time

import keyboard
from colorama import Back, Fore, Style, init

init(autoreset=True)

# 游戏区域大小

HEIGHT, WIDTH = 30, 100

# 蛇初始化
snake = [[5, 27], [5, 26], [5, 25]]
direction = (0, 1)

# 食物初始化
food = [random.randint(1, HEIGHT - 2), random.randint(1, WIDTH - 2)]


def clear_screen():
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")


is_horize = True
HORI = f"{Fore.GREEN}■{Style.RESET_ALL}"
VERT = f"{Fore.GREEN}█{Style.RESET_ALL}"

CORNOR = [
    [f"{Fore.GREEN}╔{Style.RESET_ALL}", f"{Fore.GREEN}╗{Style.RESET_ALL}"],
    [f"{Fore.GREEN}╚{Style.RESET_ALL}", f"{Fore.GREEN}╝{Style.RESET_ALL}"],
]


def draw_board():
    board = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]

    # # 绘制蛇
    # for segment in snake:
    #     board[segment[0]][segment[1]] = f"{Fore.GREEN}█{Style.RESET_ALL}"
    # 绘制蛇
    for i, segment in enumerate(snake):
        if i == 0:  # 头部
            board[segment[0]][segment[1]] = HORI if is_horize else VERT
        else:
            prev_segment = snake[i - 1]

            if segment[0] != prev_segment[0]:
                board[segment[0]][segment[1]] = VERT
            else:
                board[segment[0]][segment[1]] = HORI

            if i < len(snake)-1:
                next_segment = snake[i + 1]
                ys = [prev_segment[0], segment[0], next_segment[0]]
                xs = [prev_segment[1], segment[1], next_segment[1]]
                if (ys.count(max(ys)) != 3) and (xs.count(max(xs)) != 3):
                    board[segment[0]][segment[1]] = CORNOR[ys.count(max(ys))-1][xs.count(max(xs))-1]

    # 绘制食物
    board[food[0]][food[1]] = f"{Fore.RED}■{Style.RESET_ALL}"

    # 绘制边界
    for i in range(HEIGHT):
        board[i][0] = f"{Fore.WHITE}█{Style.RESET_ALL}"
        board[i][-1] = f"{Fore.WHITE}█{Style.RESET_ALL}"
    for i in range(WIDTH):
        board[0][i] = f"{Fore.WHITE}█{Style.RESET_ALL}"
        board[-1][i] = f"{Fore.WHITE}█{Style.RESET_ALL}"

    clear_screen()
    print("\n".join(["".join(row) for row in board]))
    print("Score:", len(snake) - 3)


def move_snake():
    global snake, food
    head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]

    if head == food:
        food = [random.randint(1, HEIGHT - 2), random.randint(1, WIDTH - 2)]
    else:
        snake.pop()

    snake.insert(0, head)


def check_collision():
    head = snake[0]
    if head in snake[1:] or head[0] in [0, HEIGHT - 1] or head[1] in [0, WIDTH - 1]:
        return True
    return False


def draw_thread():
    while True:
        move_snake()
        draw_board()

        if check_collision():
            print("Game over! Final score:", len(snake) - 3)
            sys.exit(0)

        time.sleep(0.2)


def main():
    global direction, is_horize

    # 开启绘制线程
    draw_thread_instance = threading.Thread(target=draw_thread)
    draw_thread_instance.daemon = True
    draw_thread_instance.start()

    while True:
        if keyboard.is_pressed("w") and direction != (1, 0):
            direction = (-1, 0)
            is_horize = False
            move_snake()
            draw_board()
            time.sleep(0.1)
        elif keyboard.is_pressed("s") and direction != (-1, 0):
            direction = (1, 0)
            is_horize = False
            move_snake()
            draw_board()
            time.sleep(0.1)
        elif keyboard.is_pressed("a") and direction != (0, 1):
            direction = (0, -1)
            is_horize = True
            move_snake()
            draw_board()
            time.sleep(0.1)
        elif keyboard.is_pressed("d") and direction != (0, -1):
            direction = (0, 1)
            is_horize = True
            move_snake()
            draw_board()
            time.sleep(0.1)


if __name__ == "__main__":
    main()
