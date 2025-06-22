"""
Alien Shooter Game - Main Program Entry
A simple shooting game developed with pygame
Player controls aircraft to shoot aliens, avoid collisions and prevent aliens from reaching the bottom
"""

import pygame
from game import Game
from versus_game import VersusGame
from menu import MenuManager
from config import *


def main():
    """
    Main program entry point
    Create game instance and start running
    """
    try:
        # 初始化pygame
        pygame.init()

        # 创建临时屏幕用于菜单显示
        temp_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)

        # 创建菜单管理器
        font = pygame.font.Font(None, FONT_SIZE)
        menu_manager = MenuManager(temp_screen, font)

        # 显示开始菜单
        game_mode = menu_manager.show_start_menu()

        # 关闭临时屏幕
        pygame.quit()

        if game_mode is None:
            return  # 用户选择退出

        # 根据选择的模式启动相应的游戏
        if game_mode == VERSUS_MODE:
            # 启动双人对战模式
            versus_game = VersusGame()
            versus_game.run()
        else:
            # 启动单人模式（经典或随机）
            game = Game()
            game.game_mode = game_mode  # 设置游戏模式
            game.run()

    except Exception as e:
        print(f"Game error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
