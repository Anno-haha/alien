"""
游戏主逻辑模块
包含游戏的核心逻辑、状态管理和主循环
"""

import pygame
import random
import sys
from config import *
from entities import Player, Alien, Bullet, Explosion
from background import BackgroundManager


class Game:
    """
    游戏主类
    负责管理整个游戏的运行，包括初始化、输入处理、游戏逻辑更新、绘制等
    """
    
    def __init__(self):
        """
        初始化游戏
        设置屏幕、创建游戏对象、初始化游戏状态
        """
        # 初始化pygame
        pygame.init()
        
        # 创建游戏窗口
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()  # 用于控制游戏帧率

        # ==================== 游戏对象 ====================
        self._init_game_objects()

        # ==================== 游戏状态 ====================
        self._init_game_state()

        # ==================== 时间控制 ====================
        self._init_timing()

        # ==================== UI设置 ====================
        self.font = pygame.font.Font(None, FONT_SIZE)  # 用于显示文字的字体

        # ==================== 背景效果 ====================
        self.background_manager = BackgroundManager()
    
    def _init_game_objects(self):
        """初始化游戏对象"""
        # 创建玩家飞机（位于屏幕底部中央）
        self.player = Player(SCREEN_WIDTH // 2 - PLAYER_SIZE // 2, SCREEN_HEIGHT - 50)
        self.aliens = []        # 外星人列表
        self.bullets = []       # 子弹列表
        self.explosions = []    # 爆炸特效列表
    
    def _init_game_state(self):
        """初始化游戏状态"""
        self.score = 0          # 当前分数
        self.game_over = False  # 游戏是否结束（失败）
        self.game_won = False   # 游戏是否获胜
    
    def _init_timing(self):
        """初始化时间控制"""
        self.last_bullet_time = 0          # 上次发射子弹的时间
        self.last_alien_spawn_time = 0     # 上次生成外星人的时间
        self.bullet_color_index = 0        # 子弹颜色循环索引

    def handle_input(self):
        """
        处理玩家输入
        检测方向键按下状态，控制玩家飞机移动
        """
        keys = pygame.key.get_pressed()  # 获取当前按键状态
        dx = dy = 0  # 初始化移动方向

        # 检测方向键并设置移动方向
        if keys[pygame.K_LEFT]:     # 左方向键：向左移动
            dx = -1
        if keys[pygame.K_RIGHT]:    # 右方向键：向右移动
            dx = 1
        if keys[pygame.K_UP]:       # 上方向键：向上移动
            dy = -1
        if keys[pygame.K_DOWN]:     # 下方向键：向下移动
            dy = 1

        # 移动玩家飞机
        self.player.move(dx, dy)

    def spawn_aliens(self):
        """
        生成外星人
        每隔指定时间间隔，在屏幕上方随机位置生成1-5个外星人
        """
        current_time = pygame.time.get_ticks()  # 获取当前时间（毫秒）

        # 检查是否到了生成外星人的时间
        if current_time - self.last_alien_spawn_time >= ALIEN_SPAWN_INTERVAL:
            # 随机生成指定数量的外星人
            num_aliens = random.randint(MIN_ALIENS_PER_SPAWN, MAX_ALIENS_PER_SPAWN)
            for _ in range(num_aliens):
                # 在屏幕上方随机x位置生成外星人
                x = random.randint(0, SCREEN_WIDTH - ALIEN_SIZE)
                alien = Alien(x, -ALIEN_SIZE)  # y坐标为负数，从屏幕上方开始
                self.aliens.append(alien)

            # 更新上次生成时间
            self.last_alien_spawn_time = current_time

    def spawn_bullets(self):
        """
        生成子弹
        按照指定频率自动从玩家飞机位置发射子弹
        子弹颜色按红、绿、蓝循环
        """
        current_time = pygame.time.get_ticks()  # 获取当前时间（毫秒）
        bullet_interval = 1000 // BULLETS_PER_SECOND  # 计算子弹发射间隔

        # 检查是否到了发射子弹的时间
        if current_time - self.last_bullet_time >= bullet_interval:
            # 计算子弹发射位置（玩家飞机中央）
            bullet_x = self.player.x + self.player.width // 2 - BULLET_WIDTH // 2
            bullet_y = self.player.y

            # 创建新子弹并添加到子弹列表（使用颜色循环）
            bullet = Bullet(bullet_x, bullet_y, self.bullet_color_index)
            self.bullets.append(bullet)

            # 更新颜色索引（循环：红->绿->蓝->红...）
            self.bullet_color_index = (self.bullet_color_index + 1) % len(BULLET_COLORS)

            # 更新上次发射时间
            self.last_bullet_time = current_time

    def update_bullets(self):
        """
        更新所有子弹的位置
        移动子弹并移除飞出屏幕的子弹
        """
        # 遍历子弹列表的副本，避免在遍历时修改列表
        for bullet in self.bullets[:]:
            bullet.move()  # 移动子弹

            # 如果子弹飞出屏幕上方，则移除它
            if bullet.y < 0:
                self.bullets.remove(bullet)

    def update_aliens(self):
        """
        更新所有外星人的位置
        移动外星人，如果外星人到达屏幕底部则游戏失败
        """
        # 遍历外星人列表的副本，避免在遍历时修改列表
        for alien in self.aliens[:]:
            alien.move()  # 移动外星人

            # 如果外星人到达屏幕底部
            if alien.y > SCREEN_HEIGHT:
                self.aliens.remove(alien)
                # 外星人到达屏幕底部判负
                self.game_over = True

    def update_explosions(self):
        """
        更新所有爆炸特效
        移除已结束的爆炸动画
        """
        # 遍历爆炸列表的副本，避免在遍历时修改列表
        for explosion in self.explosions[:]:
            # 更新爆炸特效，如果结束则移除
            if explosion.update():
                self.explosions.remove(explosion)

    def check_collisions(self):
        """
        检查所有碰撞事件
        包括：子弹击中外星人、玩家与外星人碰撞、胜利条件检查
        """
        # ==================== 子弹击中外星人 ====================
        for bullet in self.bullets[:]:
            for alien in self.aliens[:]:
                # 检查子弹和外星人是否碰撞
                if bullet.get_rect().colliderect(alien.get_rect()):
                    self.bullets.remove(bullet)  # 移除子弹

                    # 外星人受到伤害
                    if alien.take_damage(BULLET_DAMAGE):
                        # 外星人死亡，创建爆炸特效
                        explosion = Explosion(alien.x, alien.y)
                        self.explosions.append(explosion)

                        # 移除外星人并加分
                        self.aliens.remove(alien)
                        self.score += POINTS_PER_KILL
                    break  # 一发子弹只能击中一个外星人

        # ==================== 玩家与外星人碰撞 ====================
        player_rect = self.player.get_rect()
        for alien in self.aliens:
            if player_rect.colliderect(alien.get_rect()):
                self.game_over = True  # 碰撞后游戏结束
                return

        # ==================== 检查胜利条件 ====================
        if self.score >= WIN_SCORE:
            self.game_won = True  # 达到目标分数获胜

    def draw(self):
        """
        绘制游戏画面
        包括背景、游戏对象、UI文字等
        """
        # 填充白色背景
        self.screen.fill(WHITE)

        # ==================== 绘制背景效果 ====================
        self.background_manager.draw(self.screen)

        # ==================== 绘制游戏对象 ====================
        # 绘制玩家飞机
        self.player.draw(self.screen)

        # 绘制所有外星人
        for alien in self.aliens:
            alien.draw(self.screen)

        # 绘制所有子弹
        for bullet in self.bullets:
            bullet.draw(self.screen)

        # 绘制所有爆炸特效
        for explosion in self.explosions:
            explosion.draw(self.screen)

        # ==================== 绘制UI信息 ====================
        self._draw_ui()

        # 更新屏幕显示
        pygame.display.flip()

    def _draw_ui(self):
        """
        绘制用户界面元素
        包括分数、游戏状态信息等
        """
        # 绘制分数（左上角）
        score_text = self.font.render(SCORE_TEXT.format(self.score), True, BLACK)
        self.screen.blit(score_text, SCORE_POSITION)

        # ==================== 绘制游戏状态信息 ====================
        if self.game_over:
            # 游戏失败信息
            game_over_text = self.font.render(GAME_OVER_TEXT, True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(game_over_text, text_rect)
        elif self.game_won:
            # 游戏胜利信息
            win_text = self.font.render(VICTORY_TEXT, True, GREEN)
            text_rect = win_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(win_text, text_rect)

    def reset_game(self):
        """
        重置游戏到初始状态
        清空所有游戏对象，重置分数和状态
        """
        # 重新初始化游戏对象
        self._init_game_objects()

        # 重置游戏状态
        self._init_game_state()

        # 重置时间控制
        self._init_timing()

        # 重置背景效果
        self.background_manager.reset()

    def run(self):
        """
        游戏主循环
        处理事件、更新游戏逻辑、绘制画面
        """
        running = True  # 游戏运行标志

        # ==================== 主游戏循环 ====================
        while running:
            # ==================== 事件处理 ====================
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # 点击关闭按钮退出游戏
                    running = False
                elif event.type == pygame.KEYDOWN:
                    # 按键事件处理
                    if event.key == pygame.K_r and (self.game_over or self.game_won):
                        # 游戏结束后按R键重新开始
                        self.reset_game()

            # ==================== 游戏逻辑更新 ====================
            # 背景效果始终更新（即使游戏暂停也保持动画效果）
            self.background_manager.update()

            # 爆炸特效始终更新（即使游戏暂停也保持动画效果）
            self.update_explosions()

            # 只有在游戏进行中才更新游戏逻辑
            if not self.game_over and not self.game_won:
                self.handle_input()     # 处理玩家输入
                self.spawn_aliens()     # 生成外星人
                self.spawn_bullets()    # 生成子弹
                self.update_bullets()   # 更新子弹位置
                self.update_aliens()    # 更新外星人位置
                self.check_collisions() # 检查碰撞

            # ==================== 绘制画面 ====================
            self.draw()  # 绘制所有游戏元素

            # ==================== 帧率控制 ====================
            self.clock.tick(FPS)  # 限制游戏运行在指定FPS

        # ==================== 游戏退出 ====================
        pygame.quit()  # 退出pygame
        sys.exit()     # 退出程序
