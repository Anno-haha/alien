"""
射击外星人游戏
一个使用pygame开发的简单射击游戏
玩家控制飞机击杀外星人，避免碰撞和外星人到达底部
"""

import pygame
import random
import sys

# 初始化pygame库
pygame.init()

# ==================== 游戏常量配置 ====================
SCREEN_WIDTH = 600          # 屏幕宽度（像素）
SCREEN_HEIGHT = 800         # 屏幕高度（像素）
PLAYER_SIZE = 30            # 玩家飞机大小（正方形边长）
ALIEN_SIZE = 30             # 外星人大小（正方形边长）
PLAYER_SPEED = 4          # 玩家移动速度（像素/帧）
ALIEN_SPEED = 1             # 外星人移动速度（像素/帧）
BULLET_SPEED = 10            # 子弹移动速度（像素/帧）
BULLETS_PER_SECOND = 5      # 每秒发射子弹数量
BULLET_DAMAGE = 50          # 每发子弹伤害
ALIEN_HEALTH = 100          # 外星人血量
POINTS_PER_KILL = 5         # 击杀外星人获得分数
WIN_SCORE = 100             # 获胜所需分数

# ==================== 颜色定义 ====================
BLACK = (0, 0, 0)           # 黑色
WHITE = (255, 255, 255)     # 白色（背景色）
LIGHT_GRAY = (200, 200, 200) # 淡灰色（背景矩形）
GREEN = (0, 255, 0)         # 绿色（玩家飞机和血量条）
RED = (255, 0, 0)           # 红色（外星人）
BLUE = (0, 0, 255)          # 蓝色
YELLOW = (0, 0, 0)      # 黑色（子弹）

# ==================== 背景效果常量 ====================
BACKGROUND_RECT_WIDTH = 20   # 背景矩形宽度
BACKGROUND_RECT_HEIGHT = 60  # 背景矩形高度
BACKGROUND_SPEED = 2         # 背景矩形移动速度（像素/帧）
BACKGROUND_SPACING = 100     # 背景矩形间距

# ==================== 外星人移动常量 ====================
ALIEN_HORIZONTAL_SPEED = 0.5 # 外星人左右移动速度（像素/帧）

# ==================== 玩家飞机类 ====================
class Player:
    """
    玩家飞机类
    负责处理玩家飞机的位置、移动、绘制等功能
    """
    def __init__(self, x, y):
        """
        初始化玩家飞机
        参数:
            x: 初始x坐标
            y: 初始y坐标
        """
        self.x = x                      # 飞机x坐标
        self.y = y                      # 飞机y坐标
        self.width = PLAYER_SIZE        # 飞机宽度
        self.height = PLAYER_SIZE       # 飞机高度
        self.speed = PLAYER_SPEED       # 飞机移动速度

    def move(self, dx, dy):
        """
        移动玩家飞机
        参数:
            dx: x方向移动量（-1左移，1右移，0不移动）
            dy: y方向移动量（-1上移，1下移，0不移动）
        """
        # 根据方向和速度计算新位置
        self.x += dx * self.speed
        self.y += dy * self.speed

        # 边界检查：确保飞机不会移出屏幕
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
        self.y = max(0, min(SCREEN_HEIGHT - self.height, self.y))

    def get_rect(self):
        """
        获取飞机的矩形碰撞区域
        返回: pygame.Rect对象，用于碰撞检测
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        """
        在屏幕上绘制玩家飞机
        参数:
            screen: pygame屏幕对象
        """
        pygame.draw.rect(screen, GREEN, self.get_rect())

# ==================== 外星人类 ====================
class Alien:
    """
    外星人类
    负责处理外星人的位置、移动、血量、绘制等功能
    """
    def __init__(self, x, y):
        """
        初始化外星人
        参数:
            x: 初始x坐标
            y: 初始y坐标
        """
        self.x = x                      # 外星人x坐标
        self.y = y                      # 外星人y坐标
        self.width = ALIEN_SIZE         # 外星人宽度
        self.height = ALIEN_SIZE        # 外星人高度
        self.speed = ALIEN_SPEED        # 外星人向下移动速度
        self.health = ALIEN_HEALTH      # 外星人当前血量

        # 左右移动相关属性
        self.horizontal_speed = ALIEN_HORIZONTAL_SPEED  # 左右移动速度
        self.horizontal_direction = random.choice([-1, 1])  # 随机选择左(-1)或右(1)移动
        self.direction_change_timer = 0  # 方向改变计时器
        self.direction_change_interval = random.randint(60, 180)  # 随机1-3秒改变方向(60帧=1秒)

    def move(self):
        """
        移动外星人（向下移动 + 左右随机移动）
        """
        # 向下移动
        self.y += self.speed

        # 左右随机移动
        self.x += self.horizontal_direction * self.horizontal_speed

        # 边界检查：如果碰到屏幕边缘，反向移动
        if self.x <= 0 or self.x >= SCREEN_WIDTH - self.width:
            self.horizontal_direction *= -1

        # 随机改变移动方向
        self.direction_change_timer += 1
        if self.direction_change_timer >= self.direction_change_interval:
            self.horizontal_direction = random.choice([-1, 1])
            self.direction_change_timer = 0
            self.direction_change_interval = random.randint(60, 180)  # 重新设置随机间隔

    def get_rect(self):
        """
        获取外星人的矩形碰撞区域
        返回: pygame.Rect对象，用于碰撞检测
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        """
        在屏幕上绘制外星人和血量条
        参数:
            screen: pygame屏幕对象
        """
        # 绘制外星人主体（红色矩形）
        pygame.draw.rect(screen, RED, self.get_rect())

        # 绘制血量条（绿色，位于外星人上方）
        health_bar_width = self.width * (self.health / ALIEN_HEALTH)
        pygame.draw.rect(screen, GREEN, (self.x, self.y - 5, health_bar_width, 3))

    def take_damage(self, damage):
        """
        外星人受到伤害
        参数:
            damage: 受到的伤害值
        返回:
            bool: 如果外星人死亡返回True，否则返回False
        """
        self.health -= damage
        return self.health <= 0  # 血量<=0时死亡

# ==================== 子弹类 ====================
class Bullet:
    """
    子弹类
    负责处理子弹的位置、移动、绘制等功能
    """
    def __init__(self, x, y):
        """
        初始化子弹
        参数:
            x: 初始x坐标
            y: 初始y坐标
        """
        self.x = x                      # 子弹x坐标
        self.y = y                      # 子弹y坐标
        self.width = 3                  # 子弹宽度
        self.height = 10                # 子弹高度
        self.speed = BULLET_SPEED       # 子弹移动速度

    def move(self):
        """
        移动子弹（向上移动）
        """
        self.y -= self.speed

    def get_rect(self):
        """
        获取子弹的矩形碰撞区域
        返回: pygame.Rect对象，用于碰撞检测
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        """
        在屏幕上绘制子弹
        参数:
            screen: pygame屏幕对象
        """
        pygame.draw.rect(screen, YELLOW, self.get_rect())

# ==================== 游戏主类 ====================
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
        # 创建游戏窗口
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("射击外星人")
        self.clock = pygame.time.Clock()  # 用于控制游戏帧率

        # ==================== 游戏对象 ====================
        # 创建玩家飞机（位于屏幕底部中央）
        self.player = Player(SCREEN_WIDTH // 2 - PLAYER_SIZE // 2, SCREEN_HEIGHT - 50)
        self.aliens = []        # 外星人列表
        self.bullets = []       # 子弹列表
        self.background_rects = []  # 背景矩形列表

        # ==================== 游戏状态 ====================
        self.score = 0          # 当前分数
        self.game_over = False  # 游戏是否结束（失败）
        self.game_won = False   # 游戏是否获胜

        # ==================== 时间控制 ====================
        self.last_bullet_time = 0          # 上次发射子弹的时间
        self.last_alien_spawn_time = 0     # 上次生成外星人的时间
        self.alien_spawn_interval = 5000   # 外星人生成间隔（毫秒）

        # ==================== 字体设置 ====================
        self.font = pygame.font.Font(None, 36)  # 用于显示文字的字体

        # ==================== 背景效果初始化 ====================
        self.init_background_rects()  # 初始化背景矩形
        
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
        if current_time - self.last_alien_spawn_time >= self.alien_spawn_interval:
            # 随机生成1-5个外星人
            num_aliens = random.randint(1, 5)
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
        """
        current_time = pygame.time.get_ticks()  # 获取当前时间（毫秒）
        bullet_interval = 1000 // BULLETS_PER_SECOND  # 计算子弹发射间隔

        # 检查是否到了发射子弹的时间
        if current_time - self.last_bullet_time >= bullet_interval:
            # 计算子弹发射位置（玩家飞机中央）
            bullet_x = self.player.x + self.player.width // 2 - 1
            bullet_y = self.player.y

            # 创建新子弹并添加到子弹列表
            bullet = Bullet(bullet_x, bullet_y)
            self.bullets.append(bullet)

            # 更新上次发射时间
            self.last_bullet_time = current_time

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

    def update_background(self):
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
        if len(self.background_rects) < 50:  # 保持一定数量的背景矩形
            for x in range(0, SCREEN_WIDTH, BACKGROUND_SPACING):
                offset_x = random.randint(-20, 20)
                rect = {
                    'x': x + offset_x,
                    'y': SCREEN_HEIGHT + random.randint(0, BACKGROUND_SPACING),
                    'width': BACKGROUND_RECT_WIDTH,
                    'height': BACKGROUND_RECT_HEIGHT
                }
                self.background_rects.append(rect)

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
                        # 外星人死亡，移除并加分
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
        # 绘制移动的背景矩形
        for rect in self.background_rects:
            pygame.draw.rect(self.screen, LIGHT_GRAY,
                           (rect['x'], rect['y'], rect['width'], rect['height']))

        # ==================== 绘制游戏对象 ====================
        # 绘制玩家飞机
        self.player.draw(self.screen)

        # 绘制所有外星人
        for alien in self.aliens:
            alien.draw(self.screen)

        # 绘制所有子弹
        for bullet in self.bullets:
            bullet.draw(self.screen)

        # ==================== 绘制UI信息 ====================
        # 绘制分数（左上角）
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))

        # ==================== 绘制游戏状态信息 ====================
        if self.game_over:
            # 游戏失败信息
            game_over_text = self.font.render("Defeat", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(game_over_text, text_rect)
        elif self.game_won:
            # 游戏胜利信息
            win_text = self.font.render("Victory!", True, GREEN)
            text_rect = win_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(win_text, text_rect)

        # 更新屏幕显示
        pygame.display.flip()

    def reset_game(self):
        """
        重置游戏到初始状态
        清空所有游戏对象，重置分数和状态
        """
        # 重新创建玩家飞机
        self.player = Player(SCREEN_WIDTH // 2 - PLAYER_SIZE // 2, SCREEN_HEIGHT - 50)

        # 清空游戏对象列表
        self.aliens = []
        self.bullets = []

        # 重置游戏状态
        self.score = 0
        self.game_over = False
        self.game_won = False

        # 重置时间控制
        self.last_bullet_time = 0
        self.last_alien_spawn_time = 0

        # 重新初始化背景
        self.init_background_rects()
    
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
            self.update_background()    # 更新背景矩形位置

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
            self.clock.tick(60)  # 限制游戏运行在60FPS

        # ==================== 游戏退出 ====================
        pygame.quit()  # 退出pygame
        sys.exit()     # 退出程序

# ==================== 程序入口 ====================
if __name__ == "__main__":
    """
    程序入口点
    创建游戏实例并开始运行
    """
    game = Game()  # 创建游戏对象
    game.run()     # 开始游戏循环
