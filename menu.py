"""
游戏菜单模块
包含开始菜单和升级选择菜单
"""

import pygame
from config import *


class MenuManager:
    """
    菜单管理器
    负责处理游戏开始菜单和升级选择菜单
    """
    
    def __init__(self, screen, font):
        """
        初始化菜单管理器
        参数:
            screen: pygame屏幕对象
            font: 字体对象
        """
        self.screen = screen
        self.font = font
        self.large_font = pygame.font.Font(None, 36)  # 大字体用于标题
        self.small_font = pygame.font.Font(None, 20)  # 小字体用于描述
        
    def show_start_menu(self):
        """
        显示开始菜单
        返回: 选择的游戏模式 (CLASSIC_MODE 或 RANDOM_MODE)，如果退出返回None
        """
        while True:
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return CLASSIC_MODE
                    elif event.key == pygame.K_2:
                        return RANDOM_MODE
                    elif event.key == pygame.K_3:
                        return VERSUS_MODE
            
            # 绘制菜单
            self._draw_start_menu()
            pygame.display.flip()
    
    def show_upgrade_menu(self, current_score, available_upgrades):
        """
        显示升级选择菜单
        参数:
            current_score: 当前分数
            available_upgrades: 可用的升级选项列表
        返回: 选择的升级选项 (1, 2, 或 3)
        """
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

            # 绘制升级菜单
            self._draw_upgrade_menu(current_score, available_upgrades)
            pygame.display.flip()
    
    def _draw_start_menu(self):
        """
        绘制开始菜单
        """
        # 填充背景
        self.screen.fill(WHITE)
        
        # 计算居中位置
        center_x = SCREEN_WIDTH // 2
        start_y = SCREEN_HEIGHT // 4
        
        # 绘制标题
        title_text = self.large_font.render(MENU_TITLE, True, BLACK)
        title_rect = title_text.get_rect(center=(center_x, start_y))
        self.screen.blit(title_text, title_rect)
        
        # 绘制副标题
        subtitle_text = self.font.render(MENU_SUBTITLE, True, BLACK)
        subtitle_rect = subtitle_text.get_rect(center=(center_x, start_y + 60))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # 绘制经典模式选项
        classic_text = self.font.render(CLASSIC_MODE_TEXT, True, BLUE)
        classic_rect = classic_text.get_rect(center=(center_x, start_y + 120))
        self.screen.blit(classic_text, classic_rect)
        
        # 绘制经典模式描述
        classic_desc = self.small_font.render(CLASSIC_MODE_DESC, True, BLACK)
        classic_desc_rect = classic_desc.get_rect(center=(center_x, start_y + 145))
        self.screen.blit(classic_desc, classic_desc_rect)
        
        # 绘制随机模式选项
        random_text = self.font.render(RANDOM_MODE_TEXT, True, RED)
        random_rect = random_text.get_rect(center=(center_x, start_y + 180))
        self.screen.blit(random_text, random_rect)
        
        # 绘制随机模式描述
        random_desc = self.small_font.render(RANDOM_MODE_DESC, True, BLACK)
        random_desc_rect = random_desc.get_rect(center=(center_x, start_y + 205))
        self.screen.blit(random_desc, random_desc_rect)

        # 绘制双人对战选项
        versus_text = self.font.render(VERSUS_MODE_TEXT, True, YELLOW)
        versus_rect = versus_text.get_rect(center=(center_x, start_y + 240))
        self.screen.blit(versus_text, versus_rect)

        # 绘制双人对战描述
        versus_desc = self.small_font.render(VERSUS_MODE_DESC, True, BLACK)
        versus_desc_rect = versus_desc.get_rect(center=(center_x, start_y + 265))
        self.screen.blit(versus_desc, versus_desc_rect)

        # 绘制操作说明
        instruction_text = self.font.render(MENU_INSTRUCTION, True, GREEN)
        instruction_rect = instruction_text.get_rect(center=(center_x, start_y + 320))
        self.screen.blit(instruction_text, instruction_rect)
    
    def _draw_upgrade_menu(self, current_score, available_upgrades):
        """
        绘制升级选择菜单
        参数:
            current_score: 当前分数
            available_upgrades: 可用的升级选项列表
        """
        # 填充半透明背景
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        # 计算居中位置
        center_x = SCREEN_WIDTH // 2
        start_y = SCREEN_HEIGHT // 3

        # 绘制分数信息
        score_text = self.font.render(f"Score reached {current_score}!", True, WHITE)
        score_rect = score_text.get_rect(center=(center_x, start_y - 40))
        self.screen.blit(score_text, score_rect)

        # 绘制升级标题
        title_text = self.large_font.render(UPGRADE_TITLE, True, YELLOW)
        title_rect = title_text.get_rect(center=(center_x, start_y))
        self.screen.blit(title_text, title_rect)

        # 绘制动态升级选项
        if len(available_upgrades) >= 3:
            option1_text = f"1. {UPGRADE_DESCRIPTIONS[available_upgrades[0]]}"
            option1_surface = self.font.render(option1_text, True, WHITE)
            option1_rect = option1_surface.get_rect(center=(center_x, start_y + 60))
            self.screen.blit(option1_surface, option1_rect)

            option2_text = f"2. {UPGRADE_DESCRIPTIONS[available_upgrades[1]]}"
            option2_surface = self.font.render(option2_text, True, WHITE)
            option2_rect = option2_surface.get_rect(center=(center_x, start_y + 90))
            self.screen.blit(option2_surface, option2_rect)

            option3_text = f"3. {UPGRADE_DESCRIPTIONS[available_upgrades[2]]}"
            option3_surface = self.font.render(option3_text, True, WHITE)
            option3_rect = option3_surface.get_rect(center=(center_x, start_y + 120))
            self.screen.blit(option3_surface, option3_rect)

        # 绘制操作说明
        instruction_text = self.font.render(UPGRADE_INSTRUCTION, True, GREEN)
        instruction_rect = instruction_text.get_rect(center=(center_x, start_y + 170))
        self.screen.blit(instruction_text, instruction_rect)
