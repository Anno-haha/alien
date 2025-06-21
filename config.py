"""
游戏配置文件
包含所有游戏常量、颜色定义和配置参数
"""

# ==================== 屏幕配置 ====================
SCREEN_WIDTH = 600          # 屏幕宽度（像素）
SCREEN_HEIGHT = 800         # 屏幕高度（像素）
FPS = 60                    # 游戏帧率

# ==================== 游戏对象尺寸 ====================
PLAYER_SIZE = 30            # 玩家飞机大小（正方形边长）
ALIEN_SIZE = 30             # 外星人大小（正方形边长）
BULLET_WIDTH = 3            # 子弹宽度
BULLET_HEIGHT = 10          # 子弹高度

# ==================== 移动速度配置 ====================
PLAYER_SPEED = 4            # 玩家移动速度（像素/帧）
ALIEN_SPEED = 1             # 外星人向下移动速度（像素/帧）
ALIEN_HORIZONTAL_SPEED = 0.5 # 外星人左右移动速度（像素/帧）
BULLET_SPEED = 10           # 子弹移动速度（像素/帧）

# ==================== 战斗系统配置 ====================
BULLETS_PER_SECOND = 5      # 每秒发射子弹数量
BULLET_DAMAGE = 50          # 每发子弹伤害
ALIEN_HEALTH = 100          # 外星人血量
POINTS_PER_KILL = 5         # 击杀外星人获得分数
WIN_SCORE = 100             # 获胜所需分数

# ==================== 生成系统配置 ====================
ALIEN_SPAWN_INTERVAL = 5000 # 外星人生成间隔（毫秒）
MIN_ALIENS_PER_SPAWN = 1    # 每次生成最少外星人数量
MAX_ALIENS_PER_SPAWN = 5    # 每次生成最多外星人数量

# ==================== 背景效果配置 ====================
BACKGROUND_RECT_WIDTH = 20   # 背景矩形宽度
BACKGROUND_RECT_HEIGHT = 60  # 背景矩形高度
BACKGROUND_SPEED = 2         # 背景矩形移动速度（像素/帧）
BACKGROUND_SPACING = 100     # 背景矩形间距
MAX_BACKGROUND_RECTS = 50    # 最大背景矩形数量

# ==================== 外星人AI配置 ====================
ALIEN_DIRECTION_CHANGE_MIN = 60   # 外星人方向改变最小间隔（帧）
ALIEN_DIRECTION_CHANGE_MAX = 180  # 外星人方向改变最大间隔（帧）

# ==================== 颜色定义 ====================
BLACK = (0, 0, 0)           # 黑色
WHITE = (255, 255, 255)     # 白色（背景色）
LIGHT_GRAY = (200, 200, 200) # 淡灰色（背景矩形）
GREEN = (0, 255, 0)         # 绿色（玩家飞机和血量条）
RED = (255, 0, 0)           # 红色（外星人）
BLUE = (0, 0, 255)          # 蓝色
YELLOW = (255, 255, 0)      # 黄色
ORANGE = (255, 165, 0)      # 橙色（爆炸效果）

# ==================== 子弹颜色循环 ====================
BULLET_COLORS = [RED, GREEN, BLUE]  # 子弹颜色循环：红、绿、蓝

# ==================== 爆炸特效配置 ====================
EXPLOSION_DURATION = 30     # 爆炸特效持续时间（帧）
EXPLOSION_PARTICLES = 8     # 爆炸粒子数量
EXPLOSION_SPEED = 3         # 爆炸粒子扩散速度
EXPLOSION_COLORS = [RED, ORANGE, YELLOW]  # 爆炸颜色

# ==================== UI配置 ====================
FONT_SIZE = 36              # 字体大小
SCORE_POSITION = (10, 10)   # 分数显示位置

# ==================== 游戏文本 ====================
GAME_TITLE = "射击外星人"
SCORE_TEXT = "Score: {}"
GAME_OVER_TEXT = "Defeat"
VICTORY_TEXT = "Victory! Press R to restart"
