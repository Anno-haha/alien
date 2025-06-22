"""
双人对战游戏模块
实现双人对战模式的游戏逻辑
"""

import pygame
import random
import sys
from config import *
from entities import Player, Alien, Bullet, Explosion
from background import BackgroundManager


class VersusGame:
    """
    双人对战游戏类
    管理双人对战模式的游戏逻辑、状态和渲染
    """
    
    def __init__(self):
        """
        初始化双人对战游戏
        """
        # 初始化pygame
        pygame.init()
        
        # 创建双人对战屏幕
        self.screen = pygame.display.set_mode((VERSUS_SCREEN_WIDTH, VERSUS_SCREEN_HEIGHT))
        pygame.display.set_caption(f"{GAME_TITLE} - Versus Mode")
        
        # 初始化字体
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.small_font = pygame.font.Font(None, SMALL_FONT_SIZE)
        
        # 初始化时钟
        self.clock = pygame.time.Clock()
        
        # 初始化游戏对象
        self._init_game_objects()
        
        # 初始化游戏状态
        self._init_game_state()
        
        # 初始化时间控制
        self._init_timing()
        
        # 初始化背景管理器（为双人对战模式适配）
        self.background_manager = BackgroundManager(VERSUS_SCREEN_WIDTH, VERSUS_SCREEN_HEIGHT)
    
    def _init_game_objects(self):
        """初始化游戏对象"""
        # 创建两个玩家
        # 玩家1在左半屏
        self.player1 = Player(VERSUS_SPLIT_X // 2 - PLAYER_SIZE // 2, VERSUS_SCREEN_HEIGHT - 50)
        # 玩家2在右半屏
        self.player2 = Player(VERSUS_SPLIT_X + VERSUS_SPLIT_X // 2 - PLAYER_SIZE // 2, VERSUS_SCREEN_HEIGHT - 50)
        
        # 分别为两个玩家创建游戏对象列表
        self.aliens1 = []       # 玩家1区域的外星人
        self.aliens2 = []       # 玩家2区域的外星人
        self.bullets1 = []      # 玩家1的子弹
        self.bullets2 = []      # 玩家2的子弹
        self.explosions1 = []   # 玩家1区域的爆炸特效
        self.explosions2 = []   # 玩家2区域的爆炸特效
    
    def _init_game_state(self):
        """初始化游戏状态"""
        self.score1 = 0         # 玩家1分数
        self.score2 = 0         # 玩家2分数
        self.game_over = False  # 游戏结束标志
        self.winner = None      # 获胜者 (1 或 2)
    
    def _init_timing(self):
        """初始化时间控制"""
        self.last_bullet_time1 = 0      # 玩家1上次发射子弹的时间
        self.last_bullet_time2 = 0      # 玩家2上次发射子弹的时间
        self.last_alien_spawn_time1 = 0 # 玩家1区域上次生成外星人的时间
        self.last_alien_spawn_time2 = 0 # 玩家2区域上次生成外星人的时间
        self.bullet_color_index1 = 0    # 玩家1子弹颜色循环索引
        self.bullet_color_index2 = 0    # 玩家2子弹颜色循环索引
    
    def handle_input(self):
        """
        处理双人输入
        玩家1: WASD控制
        玩家2: 方向键控制
        """
        keys = pygame.key.get_pressed()

        # 玩家1控制 (WASD)
        dx1 = dy1 = 0
        if keys[pygame.K_a]:    # A键：向左移动
            dx1 = -1
        if keys[pygame.K_d]:    # D键：向右移动
            dx1 = 1
        if keys[pygame.K_w]:    # W键：向上移动
            dy1 = -1
        if keys[pygame.K_s]:    # S键：向下移动
            dy1 = 1

        # 移动玩家1（直接修改坐标以避免边界检查冲突）
        if dx1 != 0 or dy1 != 0:
            # 计算新位置
            effective_speed = self.player1.speed * self.player1.speed_multiplier
            new_x1 = self.player1.x + dx1 * effective_speed
            new_y1 = self.player1.y + dy1 * effective_speed

            # 检查边界限制（左半屏）
            if (0 <= new_x1 <= VERSUS_SPLIT_X - PLAYER_SIZE and
                0 <= new_y1 <= VERSUS_SCREEN_HEIGHT - PLAYER_SIZE):
                self.player1.x = new_x1
                self.player1.y = new_y1

        # 玩家2控制 (方向键)
        dx2 = dy2 = 0
        if keys[pygame.K_LEFT]:     # 左方向键：向左移动
            dx2 = -1
        if keys[pygame.K_RIGHT]:    # 右方向键：向右移动
            dx2 = 1
        if keys[pygame.K_UP]:       # 上方向键：向上移动
            dy2 = -1
        if keys[pygame.K_DOWN]:     # 下方向键：向下移动
            dy2 = 1

        # 移动玩家2（直接修改坐标以避免边界检查冲突）
        if dx2 != 0 or dy2 != 0:
            # 计算新位置
            effective_speed = self.player2.speed * self.player2.speed_multiplier
            new_x2 = self.player2.x + dx2 * effective_speed
            new_y2 = self.player2.y + dy2 * effective_speed

            # 检查边界限制（右半屏）
            if (VERSUS_SPLIT_X <= new_x2 <= VERSUS_SCREEN_WIDTH - PLAYER_SIZE and
                0 <= new_y2 <= VERSUS_SCREEN_HEIGHT - PLAYER_SIZE):
                self.player2.x = new_x2
                self.player2.y = new_y2
    
    def spawn_aliens(self):
        """
        为两个玩家区域生成外星人
        """
        current_time = pygame.time.get_ticks()
        
        # 为玩家1区域生成外星人
        if current_time - self.last_alien_spawn_time1 >= ALIEN_SPAWN_INTERVAL:
            num_aliens = random.randint(MIN_ALIENS_PER_SPAWN, MAX_ALIENS_PER_SPAWN)
            for _ in range(num_aliens):
                # 在左半屏生成外星人
                x = random.randint(0, VERSUS_SPLIT_X - ALIEN_SIZE)
                alien = Alien(x, -ALIEN_SIZE)
                self.aliens1.append(alien)
            self.last_alien_spawn_time1 = current_time
        
        # 为玩家2区域生成外星人
        if current_time - self.last_alien_spawn_time2 >= ALIEN_SPAWN_INTERVAL:
            num_aliens = random.randint(MIN_ALIENS_PER_SPAWN, MAX_ALIENS_PER_SPAWN)
            for _ in range(num_aliens):
                # 在右半屏生成外星人
                x = random.randint(VERSUS_SPLIT_X, VERSUS_SCREEN_WIDTH - ALIEN_SIZE)
                alien = Alien(x, -ALIEN_SIZE)
                self.aliens2.append(alien)
            self.last_alien_spawn_time2 = current_time
    
    def spawn_bullets(self):
        """
        为两个玩家生成子弹
        """
        current_time = pygame.time.get_ticks()
        bullet_interval = 1000 // BULLETS_PER_SECOND
        
        # 玩家1发射子弹
        if current_time - self.last_bullet_time1 >= bullet_interval:
            center_x = self.player1.x + self.player1.width // 2 - BULLET_WIDTH // 2
            bullet_y = self.player1.y
            bullet = Bullet(center_x, bullet_y, self.bullet_color_index1)
            self.bullets1.append(bullet)
            self.bullet_color_index1 = (self.bullet_color_index1 + 1) % len(BULLET_COLORS)
            self.last_bullet_time1 = current_time
        
        # 玩家2发射子弹
        if current_time - self.last_bullet_time2 >= bullet_interval:
            center_x = self.player2.x + self.player2.width // 2 - BULLET_WIDTH // 2
            bullet_y = self.player2.y
            bullet = Bullet(center_x, bullet_y, self.bullet_color_index2)
            self.bullets2.append(bullet)
            self.bullet_color_index2 = (self.bullet_color_index2 + 1) % len(BULLET_COLORS)
            self.last_bullet_time2 = current_time

    def update_bullets(self):
        """更新所有子弹的位置"""
        # 更新玩家1的子弹
        for bullet in self.bullets1[:]:
            bullet.move()
            if bullet.y < 0:
                self.bullets1.remove(bullet)

        # 更新玩家2的子弹
        for bullet in self.bullets2[:]:
            bullet.move()
            if bullet.y < 0:
                self.bullets2.remove(bullet)

    def update_aliens(self):
        """更新所有外星人的位置"""
        # 更新玩家1区域的外星人
        for alien in self.aliens1[:]:
            self._move_alien_with_boundary(alien, 0, VERSUS_SPLIT_X)

            # 检查是否超出屏幕底部
            if alien.y > VERSUS_SCREEN_HEIGHT:
                self.aliens1.remove(alien)
                # 玩家1失败
                self.game_over = True
                self.winner = 2

        # 更新玩家2区域的外星人
        for alien in self.aliens2[:]:
            self._move_alien_with_boundary(alien, VERSUS_SPLIT_X, VERSUS_SCREEN_WIDTH)

            # 检查是否超出屏幕底部
            if alien.y > VERSUS_SCREEN_HEIGHT:
                self.aliens2.remove(alien)
                # 玩家2失败
                self.game_over = True
                self.winner = 1

    def _move_alien_with_boundary(self, alien, left_bound, right_bound):
        """
        移动外星人并限制在指定边界内
        参数:
            alien: 外星人对象
            left_bound: 左边界
            right_bound: 右边界
        """
        # 向下移动
        alien.y += alien.speed

        # 左右随机移动
        alien.x += alien.horizontal_direction * alien.horizontal_speed

        # 边界检查：如果碰到区域边缘，反向移动
        if alien.x <= left_bound or alien.x >= right_bound - alien.width:
            alien.horizontal_direction *= -1
            # 确保外星人在边界内
            alien.x = max(left_bound, min(right_bound - alien.width, alien.x))

        # 随机改变移动方向
        alien.direction_change_timer += 1
        if alien.direction_change_timer >= alien.direction_change_interval:
            alien.horizontal_direction = random.choice([-1, 1])
            alien.direction_change_timer = 0
            alien.direction_change_interval = random.randint(
                ALIEN_DIRECTION_CHANGE_MIN, ALIEN_DIRECTION_CHANGE_MAX
            )

    def update_explosions(self):
        """更新所有爆炸特效"""
        # 更新玩家1区域的爆炸特效
        for explosion in self.explosions1[:]:
            if explosion.update():
                self.explosions1.remove(explosion)

        # 更新玩家2区域的爆炸特效
        for explosion in self.explosions2[:]:
            if explosion.update():
                self.explosions2.remove(explosion)

    def check_collisions(self):
        """检查所有碰撞事件"""
        # 检查玩家1的子弹击中外星人
        for bullet in self.bullets1[:]:
            for alien in self.aliens1[:]:
                if bullet.get_rect().colliderect(alien.get_rect()):
                    self.bullets1.remove(bullet)
                    if alien.take_damage(bullet.damage):
                        explosion = Explosion(alien.x, alien.y)
                        self.explosions1.append(explosion)
                        self.aliens1.remove(alien)
                        self.score1 += POINTS_PER_KILL
                    break

        # 检查玩家2的子弹击中外星人
        for bullet in self.bullets2[:]:
            for alien in self.aliens2[:]:
                if bullet.get_rect().colliderect(alien.get_rect()):
                    self.bullets2.remove(bullet)
                    if alien.take_damage(bullet.damage):
                        explosion = Explosion(alien.x, alien.y)
                        self.explosions2.append(explosion)
                        self.aliens2.remove(alien)
                        self.score2 += POINTS_PER_KILL
                    break

        # 检查玩家1与外星人碰撞
        player1_rect = self.player1.get_rect()
        for alien in self.aliens1:
            if player1_rect.colliderect(alien.get_rect()):
                self.game_over = True
                self.winner = 2
                return

        # 检查玩家2与外星人碰撞
        player2_rect = self.player2.get_rect()
        for alien in self.aliens2:
            if player2_rect.colliderect(alien.get_rect()):
                self.game_over = True
                self.winner = 1
                return

        # 检查胜利条件
        if self.score1 >= VERSUS_WIN_SCORE:
            self.game_over = True
            self.winner = 1
        elif self.score2 >= VERSUS_WIN_SCORE:
            self.game_over = True
            self.winner = 2

    def draw(self):
        """绘制游戏画面"""
        # 填充白色背景
        self.screen.fill(WHITE)

        # 绘制分割线（更明显的墙效果）
        # 主分割线
        pygame.draw.line(self.screen, BLACK, (VERSUS_SPLIT_X, 0), (VERSUS_SPLIT_X, VERSUS_SCREEN_HEIGHT), 5)
        # 左侧阴影线
        pygame.draw.line(self.screen, LIGHT_GRAY, (VERSUS_SPLIT_X - 2, 0), (VERSUS_SPLIT_X - 2, VERSUS_SCREEN_HEIGHT), 2)
        # 右侧阴影线
        pygame.draw.line(self.screen, LIGHT_GRAY, (VERSUS_SPLIT_X + 2, 0), (VERSUS_SPLIT_X + 2, VERSUS_SCREEN_HEIGHT), 2)

        # 绘制背景效果
        self.background_manager.draw(self.screen)

        # 绘制玩家
        self.player1.draw(self.screen)
        self.player2.draw(self.screen)

        # 绘制外星人
        for alien in self.aliens1:
            alien.draw(self.screen)
        for alien in self.aliens2:
            alien.draw(self.screen)

        # 绘制子弹
        for bullet in self.bullets1:
            bullet.draw(self.screen)
        for bullet in self.bullets2:
            bullet.draw(self.screen)

        # 绘制爆炸特效
        for explosion in self.explosions1:
            explosion.draw(self.screen)
        for explosion in self.explosions2:
            explosion.draw(self.screen)

        # 绘制UI
        self._draw_ui()

        # 更新屏幕显示
        pygame.display.flip()

    def _draw_ui(self):
        """绘制用户界面"""
        # 绘制玩家1分数 (左上角)
        score1_text = self.font.render(f"Player 1: {self.score1}", True, BLUE)
        self.screen.blit(score1_text, (10, 10))

        # 绘制玩家2分数 (右上角)
        score2_text = self.font.render(f"Player 2: {self.score2}", True, RED)
        score2_rect = score2_text.get_rect()
        score2_rect.topright = (VERSUS_SCREEN_WIDTH - 10, 10)
        self.screen.blit(score2_text, score2_rect)

        # 绘制目标分数
        target_text = self.small_font.render(f"Target: {VERSUS_WIN_SCORE} points", True, BLACK)
        target_rect = target_text.get_rect(center=(VERSUS_SPLIT_X, 30))
        self.screen.blit(target_text, target_rect)

        # 绘制控制说明
        control1_text = self.small_font.render("Player 1: WASD", True, BLUE)
        self.screen.blit(control1_text, (10, 50))

        control2_text = self.small_font.render("Player 2: Arrow Keys", True, RED)
        control2_rect = control2_text.get_rect()
        control2_rect.topright = (VERSUS_SCREEN_WIDTH - 10, 50)
        self.screen.blit(control2_text, control2_rect)

        # 绘制游戏结束信息
        if self.game_over:
            if self.winner:
                win_text = f"Player {self.winner} Wins!"
                color = BLUE if self.winner == 1 else RED
            else:
                win_text = "Draw!"
                color = BLACK

            win_surface = self.font.render(win_text, True, color)
            win_rect = win_surface.get_rect(center=(VERSUS_SPLIT_X, VERSUS_SCREEN_HEIGHT // 2))
            self.screen.blit(win_surface, win_rect)

            restart_text = self.small_font.render("Press R to restart", True, GREEN)
            restart_rect = restart_text.get_rect(center=(VERSUS_SPLIT_X, VERSUS_SCREEN_HEIGHT // 2 + 40))
            self.screen.blit(restart_text, restart_rect)

    def reset_game(self):
        """重置游戏到初始状态"""
        # 重新初始化游戏对象
        self._init_game_objects()

        # 重置游戏状态
        self._init_game_state()

        # 重置时间控制
        self._init_timing()

        # 重置背景效果
        self.background_manager.reset()

    def run(self):
        """游戏主循环"""
        running = True

        while running:
            # 事件处理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.game_over:
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        running = False

            # 游戏逻辑更新
            self.background_manager.update()
            self.update_explosions()

            if not self.game_over:
                self.handle_input()
                self.spawn_aliens()
                self.spawn_bullets()
                self.update_bullets()
                self.update_aliens()
                self.check_collisions()

            # 绘制画面
            self.draw()

            # 帧率控制
            self.clock.tick(FPS)

        # 游戏退出
        pygame.quit()
        sys.exit()
