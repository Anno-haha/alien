"""
背景效果管理模块
负责处理游戏背景的动态效果
"""

import pygame
import random
from config import *


class BackgroundManager:
    """
    背景管理器
    负责创建、更新和绘制移动的背景矩形效果
    """
    
    def __init__(self):
        """
        初始化背景管理器
        """
        self.background_rects = []  # 背景矩形列表
        self.init_background_rects()
    
    def init_background_rects(self):
        """
        初始化背景矩形
        在屏幕上创建均匀分布的背景矩形
        """
        self.background_rects = []
        
        # 在屏幕上创建多行多列的背景矩形
        for y in range(-BACKGROUND_RECT_HEIGHT, SCREEN_HEIGHT + BACKGROUND_SPACING, BACKGROUND_SPACING):
            for x in range(0, SCREEN_WIDTH, BACKGROUND_SPACING):
                # 添加一些随机偏移，让背景更自然
                offset_x = random.randint(-20, 20)
                offset_y = random.randint(-20, 20)
                rect = {
                    'x': x + offset_x,
                    'y': y + offset_y,
                    'width': BACKGROUND_RECT_WIDTH,
                    'height': BACKGROUND_RECT_HEIGHT
                }
                self.background_rects.append(rect)
    
    def update(self):
        """
        更新背景矩形位置
        让背景矩形向上移动，创造飞机前进的效果
        """
        # 移动所有背景矩形
        for rect in self.background_rects[:]:
            rect['y'] -= BACKGROUND_SPEED
            
            # 如果矩形移出屏幕上方，移除它
            if rect['y'] + rect['height'] < 0:
                self.background_rects.remove(rect)
        
        # 在屏幕底部添加新的背景矩形
        if len(self.background_rects) < MAX_BACKGROUND_RECTS:
            self._spawn_new_rects()
    
    def _spawn_new_rects(self):
        """
        在屏幕底部生成新的背景矩形
        私有方法，由update方法调用
        """
        for x in range(0, SCREEN_WIDTH, BACKGROUND_SPACING):
            offset_x = random.randint(-20, 20)
            rect = {
                'x': x + offset_x,
                'y': SCREEN_HEIGHT + random.randint(0, BACKGROUND_SPACING),
                'width': BACKGROUND_RECT_WIDTH,
                'height': BACKGROUND_RECT_HEIGHT
            }
            self.background_rects.append(rect)
    
    def draw(self, screen):
        """
        绘制所有背景矩形
        参数:
            screen: pygame屏幕对象
        """
        for rect in self.background_rects:
            pygame.draw.rect(screen, LIGHT_GRAY, 
                           (rect['x'], rect['y'], rect['width'], rect['height']))
    
    def reset(self):
        """
        重置背景效果
        清空现有矩形并重新初始化
        """
        self.init_background_rects()
