"""
游戏实体类
包含玩家、外星人、子弹等游戏对象的定义
"""

import pygame
import random
from config import *


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

        # 升级相关属性
        self.speed_multiplier = 1.0     # 速度倍数
        self.has_triple_shot = False    # 是否有三排子弹
        self.triple_shot_side_damage = TRIPLE_SHOT_SIDE_DAMAGE  # 侧边子弹伤害
        self.has_clear_screen = False   # 是否有清屏能力
        self.clear_screen_cooldown = CLEAR_SCREEN_COOLDOWN  # 清屏冷却时间
        self.score_multiplier = 1.0     # 分数倍数

    def move(self, dx, dy):
        """
        移动玩家飞机
        参数:
            dx: x方向移动量（-1左移，1右移，0不移动）
            dy: y方向移动量（-1上移，1下移，0不移动）
        """
        # 根据方向和速度计算新位置（应用速度升级）
        effective_speed = self.speed * self.speed_multiplier
        self.x += dx * effective_speed
        self.y += dy * effective_speed

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


class Alien:
    """
    外星人类
    负责处理外星人的位置、移动、血量、绘制等功能
    """
    def __init__(self, x, y, health_multiplier=1.0):
        """
        初始化外星人
        参数:
            x: 初始x坐标
            y: 初始y坐标
            health_multiplier: 血量倍数
        """
        self.x = x                      # 外星人x坐标
        self.y = y                      # 外星人y坐标
        self.width = ALIEN_SIZE         # 外星人宽度
        self.height = ALIEN_SIZE        # 外星人高度
        self.speed = ALIEN_SPEED        # 外星人向下移动速度
        base_health = int(ALIEN_HEALTH * health_multiplier)  # 应用血量倍数
        self.health = base_health       # 外星人当前血量
        self.max_health = base_health   # 外星人最大血量

        # 左右移动相关属性
        self.horizontal_speed = ALIEN_HORIZONTAL_SPEED  # 左右移动速度
        self.horizontal_direction = random.choice([-1, 1])  # 随机选择左(-1)或右(1)移动
        self.direction_change_timer = 0  # 方向改变计时器
        self.direction_change_interval = random.randint(
            ALIEN_DIRECTION_CHANGE_MIN, ALIEN_DIRECTION_CHANGE_MAX
        )  # 随机方向改变间隔

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
            self.direction_change_interval = random.randint(
                ALIEN_DIRECTION_CHANGE_MIN, ALIEN_DIRECTION_CHANGE_MAX
            )

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
        health_bar_width = self.width * (self.health / self.max_health)
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


class Bullet:
    """
    子弹类
    负责处理子弹的位置、移动、绘制等功能
    支持颜色循环显示（红、绿、蓝）
    """
    def __init__(self, x, y, color_index=0, damage=BULLET_DAMAGE):
        """
        初始化子弹
        参数:
            x: 初始x坐标
            y: 初始y坐标
            color_index: 颜色索引，用于颜色循环
            damage: 子弹伤害
        """
        self.x = x                      # 子弹x坐标
        self.y = y                      # 子弹y坐标
        self.width = BULLET_WIDTH       # 子弹宽度
        self.height = BULLET_HEIGHT     # 子弹高度
        self.speed = BULLET_SPEED       # 子弹移动速度
        self.damage = damage            # 子弹伤害
        self.color = BULLET_COLORS[color_index % len(BULLET_COLORS)]  # 根据索引设置颜色

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
        pygame.draw.rect(screen, self.color, self.get_rect())


class Explosion:
    """
    爆炸特效类
    负责处理外星人死亡时的爆炸动画效果
    """
    def __init__(self, x, y):
        """
        初始化爆炸特效
        参数:
            x: 爆炸中心x坐标
            y: 爆炸中心y坐标
        """
        self.center_x = x + ALIEN_SIZE // 2  # 爆炸中心x坐标
        self.center_y = y + ALIEN_SIZE // 2  # 爆炸中心y坐标
        self.timer = 0                       # 爆炸计时器
        self.particles = []                  # 爆炸粒子列表

        # 创建爆炸粒子
        self._create_particles()

    def _create_particles(self):
        """
        创建爆炸粒子
        在爆炸中心周围生成多个粒子
        """
        import math

        for i in range(EXPLOSION_PARTICLES):
            # 计算粒子的角度和方向
            angle = (2 * math.pi * i) / EXPLOSION_PARTICLES

            particle = {
                'x': self.center_x,
                'y': self.center_y,
                'dx': math.cos(angle) * EXPLOSION_SPEED,  # x方向速度
                'dy': math.sin(angle) * EXPLOSION_SPEED,  # y方向速度
                'color': random.choice(EXPLOSION_COLORS), # 随机爆炸颜色
                'size': random.randint(2, 5)             # 随机粒子大小
            }
            self.particles.append(particle)

    def update(self):
        """
        更新爆炸特效
        移动粒子并更新计时器
        返回: bool - 如果爆炸结束返回True，否则返回False
        """
        self.timer += 1

        # 更新所有粒子位置
        for particle in self.particles:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']

            # 粒子逐渐减速
            particle['dx'] *= 0.95
            particle['dy'] *= 0.95

        # 检查爆炸是否结束
        return self.timer >= EXPLOSION_DURATION

    def draw(self, screen):
        """
        绘制爆炸特效
        参数:
            screen: pygame屏幕对象
        """
        for particle in self.particles:
            # 绘制粒子（圆形）
            pygame.draw.circle(screen, particle['color'],
                             (int(particle['x']), int(particle['y'])),
                             particle['size'])


class Wingman:
    """
    僚机类
    星形僚机，发射粉色子弹，跟随玩家移动
    """
    def __init__(self, player_x, player_y=None):
        """
        初始化僚机
        参数:
            player_x: 玩家x坐标
            player_y: 玩家y坐标（未使用，保留接口兼容性）
        """
        self.size = int(PLAYER_SIZE * WINGMAN_SIZE_RATIO)  # 僚机大小（玩家的1/4）
        self.x = player_x + PLAYER_SIZE // 2 - self.size // 2  # 初始位置在玩家中央
        self.y = SCREEN_HEIGHT - WINGMAN_Y_OFFSET - self.size  # 屏幕底部上方5像素
        self.speed = WINGMAN_SPEED  # 移动速度
        self.direction = random.choice([-1, 1])  # 随机初始移动方向
        self.direction_change_timer = 0  # 方向改变计时器
        self.direction_change_interval = random.randint(60, 180)  # 随机方向改变间隔

    def update(self):
        """
        更新僚机位置
        """
        # 左右随机移动
        self.x += self.direction * self.speed

        # 边界检查：如果碰到屏幕边缘，反向移动
        if self.x <= 0 or self.x >= SCREEN_WIDTH - self.size:
            self.direction *= -1

        # 随机改变移动方向
        self.direction_change_timer += 1
        if self.direction_change_timer >= self.direction_change_interval:
            self.direction = random.choice([-1, 1])
            self.direction_change_timer = 0
            self.direction_change_interval = random.randint(60, 180)

    def get_rect(self):
        """
        获取僚机的矩形碰撞区域
        返回: pygame.Rect对象，用于碰撞检测
        """
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def draw(self, screen):
        """
        在屏幕上绘制星形僚机
        参数:
            screen: pygame屏幕对象
        """
        # 绘制星形僚机
        center_x = self.x + self.size // 2
        center_y = self.y + self.size // 2
        radius = self.size // 2

        # 绘制星形（5个点）
        import math
        points = []
        for i in range(10):  # 10个点（5个外点 + 5个内点）
            angle = (i * math.pi) / 5
            if i % 2 == 0:  # 外点
                x = center_x + radius * math.cos(angle - math.pi/2)
                y = center_y + radius * math.sin(angle - math.pi/2)
            else:  # 内点
                x = center_x + (radius * 0.5) * math.cos(angle - math.pi/2)
                y = center_y + (radius * 0.5) * math.sin(angle - math.pi/2)
            points.append((int(x), int(y)))

        # 绘制星形
        pygame.draw.polygon(screen, BLUE, points)
        pygame.draw.polygon(screen, WHITE, points, 1)  # 白色边框

    def get_bullet_spawn_pos(self):
        """
        获取僚机子弹发射位置
        返回: (x, y) 坐标
        """
        bullet_x = self.x + self.size // 2 - BULLET_WIDTH // 2
        bullet_y = self.y
        return bullet_x, bullet_y
