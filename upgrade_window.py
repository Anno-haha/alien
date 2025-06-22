"""
升级窗口模块
在主窗口中显示升级选择界面，使用简单的覆盖层
"""

import pygame
from config import *


class UpgradeWindow:
    """
    升级选择窗口
    在主游戏窗口中显示覆盖层，避免多线程问题
    """

    def __init__(self, screen, font):
        """
        初始化升级窗口
        参数:
            screen: 主游戏屏幕
            font: 字体对象
        """
        self.screen = screen
        self.font = font
        self.large_font = pygame.font.Font(None, UPGRADE_WINDOW_FONT_SIZE + 8)
        self.small_font = pygame.font.Font(None, UPGRADE_WINDOW_FONT_SIZE - 4)

    def show_upgrade_selection(self, current_score, available_upgrades):
        """
        显示升级选择界面
        参数:
            current_score: 当前分数
            available_upgrades: 可用的升级选项列表
        返回: 选择的升级选项 (1, 2, 或 3)
        """
        clock = pygame.time.Clock()

        while True:
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 1  # 默认选择第一个选项
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return 1
                    elif event.key == pygame.K_2:
                        return 2
                    elif event.key == pygame.K_3:
                        return 3
                    elif event.key == pygame.K_ESCAPE:
                        return 1

            # 绘制升级界面（覆盖在游戏画面上）
            self._draw_upgrade_overlay(current_score, available_upgrades)
            pygame.display.flip()
            clock.tick(60)
    
    def _draw_upgrade_overlay(self, current_score, available_upgrades):
        """
        绘制升级选择覆盖层
        """
        # 创建半透明覆盖层
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(220)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        # 计算升级窗口位置（屏幕中央）
        window_x = (SCREEN_WIDTH - UPGRADE_WINDOW_WIDTH) // 2
        window_y = (SCREEN_HEIGHT - UPGRADE_WINDOW_HEIGHT) // 2

        # 绘制升级窗口背景
        window_rect = pygame.Rect(window_x, window_y, UPGRADE_WINDOW_WIDTH, UPGRADE_WINDOW_HEIGHT)
        pygame.draw.rect(self.screen, BLACK, window_rect)
        pygame.draw.rect(self.screen, WHITE, window_rect, 3)

        # 计算文本位置
        center_x = window_x + UPGRADE_WINDOW_WIDTH // 2
        start_y = window_y + 30

        # 绘制分数信息
        score_text = self.font.render(f"Score: {current_score}", True, WHITE)
        score_rect = score_text.get_rect(center=(center_x, start_y))
        self.screen.blit(score_text, score_rect)

        # 绘制升级标题
        title_text = self.large_font.render("Choose Upgrade", True, YELLOW)
        title_rect = title_text.get_rect(center=(center_x, start_y + 40))
        self.screen.blit(title_text, title_rect)

        # 绘制升级选项
        if len(available_upgrades) >= 3:
            y_pos = start_y + 90

            for i, upgrade in enumerate(available_upgrades):
                option_text = f"{i+1}. {UPGRADE_DESCRIPTIONS[upgrade]}"

                # 如果文本太长，缩短描述
                if len(option_text) > 40:
                    option_text = option_text[:37] + "..."

                option_surface = self.small_font.render(option_text, True, WHITE)
                option_rect = option_surface.get_rect(center=(center_x, y_pos))
                self.screen.blit(option_surface, option_rect)
                y_pos += 35

        # 绘制操作说明
        instruction_text = self.small_font.render("Press 1, 2, or 3 to choose", True, GREEN)
        instruction_rect = instruction_text.get_rect(center=(center_x, window_y + UPGRADE_WINDOW_HEIGHT - 50))
        self.screen.blit(instruction_text, instruction_rect)

        # 绘制ESC提示
        esc_text = self.small_font.render("ESC: Default choice", True, LIGHT_GRAY)
        esc_rect = esc_text.get_rect(center=(center_x, window_y + UPGRADE_WINDOW_HEIGHT - 25))
        self.screen.blit(esc_text, esc_rect)
