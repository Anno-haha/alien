"""
游戏主逻辑模块
包含游戏的核心逻辑、状态管理和主循环
"""

import pygame
import random
import sys
from config import *
from entities import Player, Alien, Bullet, Explosion, Wingman
from background import BackgroundManager
from menu import MenuManager
from upgrade_window import UpgradeWindow


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
        self.font = pygame.font.Font(None, FONT_SIZE)  # 主字体
        self.small_font = pygame.font.Font(None, SMALL_FONT_SIZE)  # 小字体
        self.menu_manager = MenuManager(self.screen, self.font)  # 菜单管理器
        self.upgrade_window = UpgradeWindow(self.screen, self.font)  # 升级窗口

        # ==================== 游戏模式 ====================
        self.game_mode = None           # 当前游戏模式
        self.show_upgrade_menu = False  # 是否显示升级菜单
        self.last_upgrade_score = 0     # 上次升级时的分数

        # ==================== 升级系统 ====================
        self.bullet_speed_multiplier = 1.0    # 子弹速度倍数
        self.max_aliens_multiplier = 1.0      # 外星人最大数量倍数
        self.milestone_aliens_multiplier = 1.0 # 里程碑外星人数量倍数
        self.alien_health_multiplier = 1.0    # 外星人血量倍数
        self.last_clear_screen_time = 0        # 上次清屏时间
        self.available_upgrades = []           # 当前可用的升级选项
        self.last_milestone_score = 0         # 上次里程碑分数
        self.last_health_boost_score = 0      # 上次血量提升分数

        # ==================== 背景效果 ====================
        self.background_manager = BackgroundManager()
    
    def _init_game_objects(self):
        """初始化游戏对象"""
        # 创建玩家飞机（位于屏幕底部中央）
        self.player = Player(SCREEN_WIDTH // 2 - PLAYER_SIZE // 2, SCREEN_HEIGHT - 50)
        self.aliens = []        # 外星人列表
        self.bullets = []       # 子弹列表
        self.explosions = []    # 爆炸特效列表
        self.wingmen = []       # 僚机列表
    
    def _init_game_state(self):
        """初始化游戏状态"""
        self.score = 0          # 当前分数
        self.game_over = False  # 游戏是否结束（失败）
        self.game_won = False   # 游戏是否获胜
    
    def _init_timing(self):
        """初始化时间控制"""
        self.last_bullet_time = 0          # 上次发射子弹的时间
        self.last_alien_spawn_time = 0     # 上次生成外星人的时间
        self.last_wingman_bullet_time = 0  # 上次僚机发射子弹的时间
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

        # 检测空格键清屏
        if keys[pygame.K_SPACE]:
            self.clear_screen_aliens()

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
            # 计算升级后的外星人最大数量（包括里程碑加成）
            total_multiplier = self.max_aliens_multiplier * self.milestone_aliens_multiplier
            max_aliens = int(MAX_ALIENS_PER_SPAWN * total_multiplier)
            # 随机生成指定数量的外星人
            num_aliens = random.randint(MIN_ALIENS_PER_SPAWN, max_aliens)
            for _ in range(num_aliens):
                # 在屏幕上方随机x位置生成外星人
                x = random.randint(0, SCREEN_WIDTH - ALIEN_SIZE)
                alien = Alien(x, -ALIEN_SIZE, self.alien_health_multiplier)  # 应用血量倍数
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
            center_x = self.player.x + self.player.width // 2 - BULLET_WIDTH // 2
            bullet_y = self.player.y

            if self.player.has_triple_shot:
                # 三排子弹模式
                # 中间子弹（正常伤害）
                center_bullet = Bullet(center_x, bullet_y, self.bullet_color_index, BULLET_DAMAGE)
                center_bullet.speed = int(BULLET_SPEED * self.bullet_speed_multiplier)
                self.bullets.append(center_bullet)

                # 左侧子弹（自定义伤害）
                left_bullet = Bullet(center_x - 15, bullet_y, self.bullet_color_index, self.player.triple_shot_side_damage)
                left_bullet.speed = int(BULLET_SPEED * self.bullet_speed_multiplier * TRIPLE_SHOT_SIDE_SPEED_RATIO)
                self.bullets.append(left_bullet)

                # 右侧子弹（自定义伤害）
                right_bullet = Bullet(center_x + 15, bullet_y, self.bullet_color_index, self.player.triple_shot_side_damage)
                right_bullet.speed = int(BULLET_SPEED * self.bullet_speed_multiplier * TRIPLE_SHOT_SIDE_SPEED_RATIO)
                self.bullets.append(right_bullet)
            else:
                # 单排子弹模式
                bullet = Bullet(center_x, bullet_y, self.bullet_color_index, BULLET_DAMAGE)
                bullet.speed = int(BULLET_SPEED * self.bullet_speed_multiplier)
                self.bullets.append(bullet)

            # 更新颜色索引（循环：红->绿->蓝->红...）
            self.bullet_color_index = (self.bullet_color_index + 1) % len(BULLET_COLORS)

            # 更新上次发射时间
            self.last_bullet_time = current_time

    def spawn_wingman_bullets(self):
        """
        生成僚机子弹
        僚机按照指定频率发射粉色子弹
        """
        if not self.wingmen:  # 如果没有僚机，直接返回
            return

        current_time = pygame.time.get_ticks()
        bullet_interval = 1000 // BULLETS_PER_SECOND  # 与玩家相同的发射频率

        # 检查是否到了发射子弹的时间
        if current_time - self.last_wingman_bullet_time >= bullet_interval:
            for wingman in self.wingmen:
                # 计算僚机子弹发射位置
                bullet_x, bullet_y = wingman.get_bullet_spawn_pos()

                # 创建僚机子弹（粉色，特殊伤害和速度）
                bullet = Bullet(bullet_x, bullet_y, 0, WINGMAN_BULLET_DAMAGE)  # 使用红色索引但会被覆盖
                bullet.color = WINGMAN_BULLET_COLOR  # 设置为粉色
                bullet.speed = int(BULLET_SPEED * WINGMAN_BULLET_SPEED_RATIO)  # 50%速度
                self.bullets.append(bullet)

            # 更新上次发射时间
            self.last_wingman_bullet_time = current_time

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

    def update_wingmen(self):
        """
        更新所有僚机的位置
        """
        for wingman in self.wingmen:
            wingman.update()

    def generate_random_upgrades(self):
        """
        生成三个随机升级选项
        过滤掉已达到上限的升级
        """
        import random
        all_upgrades = [
            UPGRADE_BULLET_SPEED,
            UPGRADE_CLEAR_SCREEN,
            UPGRADE_TRIPLE_SHOT,
            UPGRADE_PLAYER_SPEED,
            UPGRADE_SCORE_MULTIPLIER,
            UPGRADE_WINGMAN
        ]

        # 过滤掉已达到上限的升级选项
        available_upgrades = []
        for upgrade in all_upgrades:
            if upgrade == UPGRADE_TRIPLE_SHOT:
                # 检查三向子弹是否已达到最大伤害
                if not self.player.has_triple_shot or self.player.triple_shot_side_damage < TRIPLE_SHOT_MAX_DAMAGE:
                    available_upgrades.append(upgrade)
            else:
                available_upgrades.append(upgrade)

        # 确保至少有3个选项，如果不足则重复一些选项
        if len(available_upgrades) < 3:
            # 添加其他可重复的升级
            while len(available_upgrades) < 3:
                available_upgrades.append(UPGRADE_BULLET_SPEED)  # 子弹速度可以无限升级

        # 随机选择3个不同的升级选项
        self.available_upgrades = random.sample(available_upgrades, min(3, len(available_upgrades)))

        # 如果选项不足3个，用其他升级补充
        while len(self.available_upgrades) < 3:
            remaining_upgrades = [u for u in available_upgrades if u not in self.available_upgrades]
            if remaining_upgrades:
                self.available_upgrades.append(random.choice(remaining_upgrades))
            else:
                self.available_upgrades.append(UPGRADE_BULLET_SPEED)

    def apply_upgrade(self, upgrade_type):
        """
        应用选择的升级
        参数:
            upgrade_type: 升级类型
        """
        if upgrade_type == UPGRADE_BULLET_SPEED:
            self.bullet_speed_multiplier += BULLET_SPEED_UPGRADE
            self.max_aliens_multiplier += ALIEN_SPAWN_UPGRADE

        elif upgrade_type == UPGRADE_CLEAR_SCREEN:
            if not self.player.has_clear_screen:
                # 第一次获得清屏能力
                self.player.has_clear_screen = True
            else:
                # 后续升级减少冷却时间（最小值改为20秒）
                self.player.clear_screen_cooldown = max(CLEAR_SCREEN_MIN_COOLDOWN,
                    self.player.clear_screen_cooldown - CLEAR_SCREEN_COOLDOWN_REDUCTION)

        elif upgrade_type == UPGRADE_TRIPLE_SHOT:
            if not self.player.has_triple_shot:
                # 第一次获得三排子弹
                self.player.has_triple_shot = True
            else:
                # 后续升级增加侧边子弹伤害，但不超过最大值
                new_damage = int(self.player.triple_shot_side_damage * TRIPLE_SHOT_DAMAGE_MULTIPLIER)
                self.player.triple_shot_side_damage = min(new_damage, TRIPLE_SHOT_MAX_DAMAGE)

        elif upgrade_type == UPGRADE_PLAYER_SPEED:
            self.player.speed_multiplier += PLAYER_SPEED_UPGRADE

        elif upgrade_type == UPGRADE_SCORE_MULTIPLIER:
            self.player.score_multiplier += SCORE_MULTIPLIER_UPGRADE

        elif upgrade_type == UPGRADE_WINGMAN:
            # 添加一架新僚机
            wingman = Wingman(self.player.x, self.player.y)
            self.wingmen.append(wingman)

    def clear_screen_aliens(self):
        """
        清除屏幕上所有外星人
        """
        current_time = pygame.time.get_ticks()
        if (self.player.has_clear_screen and
            current_time - self.last_clear_screen_time >= self.player.clear_screen_cooldown):

            # 为每个外星人创建爆炸特效
            for alien in self.aliens:
                explosion = Explosion(alien.x, alien.y)
                self.explosions.append(explosion)
                # 获得分数
                points = int(POINTS_PER_KILL * self.player.score_multiplier)
                self.score += points

            # 清除所有外星人
            self.aliens.clear()
            self.last_clear_screen_time = current_time
            return True
        return False

    def handle_upgrade(self):
        """
        处理升级选择
        """
        if self.show_upgrade_menu:
            # 生成随机升级选项
            if not self.available_upgrades:
                self.generate_random_upgrades()

            # 显示升级选择界面并获取选择
            choice = self.upgrade_window.show_upgrade_selection(self.score, self.available_upgrades)

            # 应用选择的升级
            if 1 <= choice <= 3:
                selected_upgrade = self.available_upgrades[choice - 1]
                self.apply_upgrade(selected_upgrade)

            # 更新上次升级分数
            self.last_upgrade_score = self.score
            self.show_upgrade_menu = False
            self.available_upgrades = []

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

                    # 外星人受到伤害（使用子弹的伤害值）
                    if alien.take_damage(bullet.damage):
                        # 外星人死亡，创建爆炸特效
                        explosion = Explosion(alien.x, alien.y)
                        self.explosions.append(explosion)

                        # 移除外星人并加分（应用分数倍数）
                        self.aliens.remove(alien)
                        points = int(POINTS_PER_KILL * self.player.score_multiplier)
                        self.score += points
                    break  # 一发子弹只能击中一个外星人

        # ==================== 玩家与外星人碰撞 ====================
        player_rect = self.player.get_rect()
        for alien in self.aliens:
            if player_rect.colliderect(alien.get_rect()):
                self.game_over = True  # 碰撞后游戏结束
                return

        # ==================== 检查里程碑 ====================
        if self.game_mode == RANDOM_MODE:
            # 检查1000分里程碑（但在10000分后停止增加外星人数量）
            if (self.score < UPGRADE_STOP_SCORE and
                (self.score // MILESTONE_SCORE_INTERVAL) > (self.last_milestone_score // MILESTONE_SCORE_INTERVAL)):
                self.milestone_aliens_multiplier += MILESTONE_ALIEN_INCREASE
                self.last_milestone_score = self.score

            # 检查血量提升（1000分后每500分）
            if self.score >= UPGRADE_STOP_SCORE:
                health_boost_count = (self.score - UPGRADE_STOP_SCORE) // HEALTH_BOOST_INTERVAL
                expected_health_boost_count = (self.last_health_boost_score - UPGRADE_STOP_SCORE) // HEALTH_BOOST_INTERVAL if self.last_health_boost_score >= UPGRADE_STOP_SCORE else 0

                if health_boost_count > expected_health_boost_count:
                    self.alien_health_multiplier += HEALTH_BOOST_MULTIPLIER
                    self.last_health_boost_score = self.score

        # ==================== 检查胜利条件 ====================
        if self.game_mode == CLASSIC_MODE and self.score >= WIN_SCORE:
            self.game_won = True  # 经典模式：达到目标分数获胜
        elif self.game_mode == RANDOM_MODE:
            # 随机模式：检查是否需要升级（1000分前）
            if (self.score < UPGRADE_STOP_SCORE and
                (self.score // UPGRADE_SCORE_INTERVAL) > (self.last_upgrade_score // UPGRADE_SCORE_INTERVAL)):
                self.show_upgrade_menu = True

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

        # 绘制所有僚机
        for wingman in self.wingmen:
            wingman.draw(self.screen)

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

        # 绘制游戏模式信息（右上角）
        if self.game_mode == CLASSIC_MODE:
            mode_text = f"Classic Mode (Target: {WIN_SCORE})"
        else:
            if self.score < UPGRADE_STOP_SCORE:
                mode_text = f"Random Mode (Next Upgrade: {((self.score // UPGRADE_SCORE_INTERVAL) + 1) * UPGRADE_SCORE_INTERVAL})"
            else:
                next_health_boost = UPGRADE_STOP_SCORE + ((self.score - UPGRADE_STOP_SCORE) // HEALTH_BOOST_INTERVAL + 1) * HEALTH_BOOST_INTERVAL
                mode_text = f"Endgame Mode (Next Health Boost: {next_health_boost})"

        mode_surface = self.font.render(mode_text, True, BLUE)
        mode_rect = mode_surface.get_rect()
        mode_rect.topright = (SCREEN_WIDTH - 10, 10)
        self.screen.blit(mode_surface, mode_rect)

        # 显示升级信息（使用小字体）
        y_offset = 40
        line_height = 20

        if self.bullet_speed_multiplier > 1.0:
            upgrade_text = f"Bullet Speed: +{int((self.bullet_speed_multiplier - 1) * 100)}%"
            upgrade_surface = self.small_font.render(upgrade_text, True, GREEN)
            self.screen.blit(upgrade_surface, (10, y_offset))
            y_offset += line_height

        if self.player.speed_multiplier > 1.0:
            speed_text = f"Ship Speed: +{int((self.player.speed_multiplier - 1) * 100)}%"
            speed_surface = self.small_font.render(speed_text, True, GREEN)
            self.screen.blit(speed_surface, (10, y_offset))
            y_offset += line_height

        if self.player.score_multiplier > 1.0:
            score_text = f"Score Mult: +{int((self.player.score_multiplier - 1) * 100)}%"
            score_surface = self.small_font.render(score_text, True, GREEN)
            self.screen.blit(score_surface, (10, y_offset))
            y_offset += line_height

        if self.player.has_triple_shot:
            max_reached = " (MAX)" if self.player.triple_shot_side_damage >= TRIPLE_SHOT_MAX_DAMAGE else ""
            triple_text = f"Triple Shot: Side {self.player.triple_shot_side_damage} DMG{max_reached}"
            color = YELLOW if self.player.triple_shot_side_damage >= TRIPLE_SHOT_MAX_DAMAGE else GREEN
            triple_surface = self.small_font.render(triple_text, True, color)
            self.screen.blit(triple_surface, (10, y_offset))
            y_offset += line_height

        if self.player.has_clear_screen:
            current_time = pygame.time.get_ticks()
            cooldown_remaining = max(0, self.player.clear_screen_cooldown - (current_time - self.last_clear_screen_time))
            if cooldown_remaining > 0:
                clear_text = f"Clear: {cooldown_remaining // 1000}s (CD: {self.player.clear_screen_cooldown // 1000}s)"
                color = RED
            else:
                clear_text = f"Clear: READY (SPACE) - CD: {self.player.clear_screen_cooldown // 1000}s"
                color = GREEN
            clear_surface = self.small_font.render(clear_text, True, color)
            self.screen.blit(clear_surface, (10, y_offset))
            y_offset += line_height

        # 显示僚机信息
        if self.wingmen:
            wingman_text = f"Wingmen: {len(self.wingmen)}"
            wingman_surface = self.small_font.render(wingman_text, True, BLUE)
            self.screen.blit(wingman_surface, (10, y_offset))
            y_offset += line_height

        # 显示血量倍数信息
        if self.game_mode == RANDOM_MODE and self.alien_health_multiplier > 1.0:
            health_text = f"Alien Health: +{int((self.alien_health_multiplier - 1) * 100)}%"
            health_surface = self.small_font.render(health_text, True, RED)
            self.screen.blit(health_surface, (10, y_offset))
            y_offset += line_height

        # 显示里程碑信息
        if self.game_mode == RANDOM_MODE and self.milestone_aliens_multiplier > 1.0:
            milestone_text = f"Milestone: +{int((self.milestone_aliens_multiplier - 1) * 100)}% Aliens"
            milestone_surface = self.small_font.render(milestone_text, True, YELLOW)
            self.screen.blit(milestone_surface, (10, y_offset))

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

        # 重置升级系统
        self.bullet_speed_multiplier = 1.0
        self.max_aliens_multiplier = 1.0
        self.milestone_aliens_multiplier = 1.0
        self.alien_health_multiplier = 1.0
        self.show_upgrade_menu = False
        self.last_upgrade_score = 0
        self.last_milestone_score = 0
        self.last_health_boost_score = 0
        self.last_clear_screen_time = 0
        self.available_upgrades = []

        # 重置玩家升级
        self.player.speed_multiplier = 1.0
        self.player.has_triple_shot = False
        self.player.triple_shot_side_damage = TRIPLE_SHOT_SIDE_DAMAGE
        self.player.has_clear_screen = False
        self.player.clear_screen_cooldown = CLEAR_SCREEN_COOLDOWN
        self.player.score_multiplier = 1.0

        # 重置背景效果
        self.background_manager.reset()

    def run(self):
        """
        游戏主循环
        处理事件、更新游戏逻辑、绘制画面
        """
        # 如果没有设置游戏模式，默认为经典模式
        if not hasattr(self, 'game_mode') or self.game_mode is None:
            self.game_mode = CLASSIC_MODE

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
            # 背景效果始终更新
            self.background_manager.update()

            # 爆炸特效始终更新
            self.update_explosions()

            # 处理升级菜单（会暂停游戏）
            if self.show_upgrade_menu:
                self.handle_upgrade()

            # 游戏逻辑更新（升级时暂停）
            elif not self.game_over and not self.game_won:
                self.handle_input()     # 处理玩家输入
                self.spawn_aliens()     # 生成外星人
                self.spawn_bullets()    # 生成子弹
                self.spawn_wingman_bullets()  # 生成僚机子弹
                self.update_bullets()   # 更新子弹位置
                self.update_aliens()    # 更新外星人位置
                self.update_wingmen()   # 更新僚机位置
                self.check_collisions() # 检查碰撞

            # ==================== 绘制画面 ====================
            self.draw()  # 绘制所有游戏元素

            # ==================== 帧率控制 ====================
            self.clock.tick(FPS)  # 限制游戏运行在指定FPS

        # ==================== 游戏退出 ====================
        pygame.quit()  # 退出pygame
        sys.exit()     # 退出程序
