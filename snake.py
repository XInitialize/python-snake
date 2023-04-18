import os
import random
import sys
import threading
import time

import keyboard
from colorama import Back, Fore, Style, init

init(autoreset=True)

# 游戏区域大小


def get_terminal_size():
    rows, columns = os.popen("stty size", "r").read().split()
    return int(rows)-3, int(columns)


HEIGHT, WIDTH = get_terminal_size()

# 蛇初始化
center_y, center_x = int(HEIGHT/2), int(WIDTH/2)
snake = [[center_y, center_x+1], [center_y, center_x], [center_y, center_x-1]]
direction = (0, 1)

# 食物初始化
food = [random.randint(1, HEIGHT - 2), random.randint(1, WIDTH - 2)]

# 初始方向
is_horize = True

# 变量
HORI = "■"
HORI_HEAD = f"{Fore.GREEN}■{Style.RESET_ALL}"
VERT = "█"
VERT_HEAD = f"{Fore.GREEN}█{Style.RESET_ALL}"

CORNOR = [
    ["╔", "╗"],
    ["╚", "╝"],
]
FOOD = f"{Fore.RED}■{Style.RESET_ALL}"
BORDER = f"{Fore.WHITE}█{Style.RESET_ALL}"

SLEEP_DRAW = 0.3
SLEEP_PRESS_DRAW = 0.1


def clear_screen():
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")


def get_snake_color(color_code: float, char: str) -> str:
    """根据颜色代码生成蛇身部分的颜色。

    Args:
        color_code (float): 颜色代码（范围：0-1）。

    Returns:
        str: 返回带有指定颜色的蛇身部分。
    """
    return f"\033[38;2;0;0;{int(color_code*225)}m{char}{Style.RESET_ALL}"


def draw_board():
    board = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]

    # 绘制蛇
    lensnake = len(snake)
    for i, segment in enumerate(snake):
        if i == 0:  # 头部
            board[segment[0]][segment[1]] = HORI_HEAD if is_horize else VERT_HEAD
        else:
            prev_segment = snake[i - 1]

            if segment[0] != prev_segment[0]:
                char = VERT
            else:
                char = HORI

            if i < len(snake)-1:
                next_segment = snake[i + 1]
                ys = [prev_segment[0], segment[0], next_segment[0]]
                xs = [prev_segment[1], segment[1], next_segment[1]]
                if (ys.count(max(ys)) != 3) and (xs.count(max(xs)) != 3):
                    char = CORNOR[ys.count(max(ys))-1][xs.count(max(xs))-1]
            board[segment[0]][segment[1]] = get_snake_color(i/lensnake, char)
    # 绘制食物
    board[food[0]][food[1]] = FOOD

    # 绘制边界
    for i in range(HEIGHT):
        board[i][0], board[i][-1] = BORDER, BORDER
    for i in range(WIDTH):
        board[0][i], board[-1][i] = BORDER, BORDER

    # 其他输出
    clear_screen()
    print("\n".join(["".join(row) for row in board]))
    print(f"Score[{WIDTH}x{HEIGHT}]:", len(snake) - 3)


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
        print("Game over! Final score:", len(snake) - 3)
        os._exit(0)


def main_call(sleep=SLEEP_PRESS_DRAW):
    move_snake()
    draw_board()
    check_collision()
    time.sleep(sleep)


def draw_thread():
    while True:
        main_call(SLEEP_DRAW)


def main():
    global direction, is_horize

    # 开启绘制线程
    draw_thread_instance = threading.Thread(target=draw_thread)
    draw_thread_instance.daemon = True
    draw_thread_instance.start()

    while True:
        if (keyboard.is_pressed("w") or keyboard.is_pressed("up")) and direction != (1, 0):
            direction = (-1, 0)
            is_horize = False
            main_call()
        elif (keyboard.is_pressed("s") or keyboard.is_pressed("down")) and direction != (-1, 0):
            direction = (1, 0)
            is_horize = False
            main_call()
        elif (keyboard.is_pressed("a") or keyboard.is_pressed("left")) and direction != (0, 1):
            direction = (0, -1)
            is_horize = True
            main_call()
        elif (keyboard.is_pressed("d") or keyboard.is_pressed("right")) and direction != (0, -1):
            direction = (0, 1)
            is_horize = True
            main_call()


if __name__ == "__main__":
    main()
