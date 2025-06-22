"""
游戏配置文件
包含所有游戏常量、颜色定义和配置参数
"""

# ==================== 屏幕配置 ====================
SCREEN_WIDTH = 600          # 屏幕宽度（像素）
SCREEN_HEIGHT = 750         # 屏幕高度（像素）
FPS = 60                    # 游戏帧率

# ==================== 双人对战屏幕配置 ====================
VERSUS_SCREEN_WIDTH = 1000  # 双人对战屏幕宽度
VERSUS_SCREEN_HEIGHT = 750  # 双人对战屏幕高度
VERSUS_SPLIT_X = VERSUS_SCREEN_WIDTH // 2  # 屏幕分割线x坐标

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
FONT_SIZE = 24              # 主窗口字体大小
SMALL_FONT_SIZE = 18        # 小字体大小
UPGRADE_WINDOW_FONT_SIZE = 28  # 升级窗口字体大小
SCORE_POSITION = (10, 10)   # 分数显示位置

# ==================== 升级窗口配置 ====================
UPGRADE_WINDOW_WIDTH = 400  # 升级窗口宽度
UPGRADE_WINDOW_HEIGHT = 300 # 升级窗口高度

# ==================== 游戏模式配置 ====================
CLASSIC_MODE = "classic"
RANDOM_MODE = "random"
VERSUS_MODE = "versus"
WIN_SCORE = 100                 # 经典模式胜利分数
VERSUS_WIN_SCORE = 500          # 双人对战胜利分数
POINTS_PER_KILL = 5             # 每击杀一个外星人获得的分数
UPGRADE_SCORE_INTERVAL = 100    # 每100分触发一次升级选择

# ==================== Upgrade System Configuration ====================
BULLET_SPEED_UPGRADE = 0.15     # Bullet speed upgrade 15%
ALIEN_SPAWN_UPGRADE = 0.2       # Alien count upgrade 10%

# ==================== New Upgrade Options ====================
CLEAR_SCREEN_COOLDOWN = 40000    # Clear screen ability cooldown (40 seconds in milliseconds)
CLEAR_SCREEN_COOLDOWN_REDUCTION = 10000  # Cooldown reduction per upgrade (10 seconds)
CLEAR_SCREEN_MIN_COOLDOWN = 20000  # Minimum cooldown (20 seconds)
TRIPLE_SHOT_SIDE_SPEED_RATIO = 0.5  # Side bullets speed ratio (50% of center bullet)
TRIPLE_SHOT_SIDE_DAMAGE = 10     # Initial side bullet damage
TRIPLE_SHOT_DAMAGE_MULTIPLIER = 1.5  # Damage multiplier for subsequent upgrades
TRIPLE_SHOT_MAX_DAMAGE = 100     # Maximum side bullet damage
PLAYER_SPEED_UPGRADE = 0.2       # Player speed upgrade 20%
SCORE_MULTIPLIER_UPGRADE = 0.15  # Score multiplier upgrade 15%

# ==================== Wingman Configuration ====================
WINGMAN_SIZE_RATIO = 0.25        # Wingman size ratio (1/4 of player size)
WINGMAN_BULLET_DAMAGE = 10       # Wingman bullet damage
WINGMAN_BULLET_SPEED_RATIO = 0.5 # Wingman bullet speed ratio (50% of player bullet)
WINGMAN_SPEED = 1                # Wingman movement speed (pixels per frame)
WINGMAN_Y_OFFSET = 5             # Wingman Y position offset from bottom
WINGMAN_BULLET_COLOR = (255, 20, 147)  # Pink color for wingman bullets

# ==================== Milestone System ====================
MILESTONE_SCORE_INTERVAL = 1000  # Every 1000 points
MILESTONE_ALIEN_INCREASE = 0.6   # 60% alien count increase at milestones

# ==================== End Game System ====================
UPGRADE_STOP_SCORE = 10000       # Score at which upgrades stop appearing
HEALTH_BOOST_INTERVAL = 500     # Every 500 points after 10000
HEALTH_BOOST_MULTIPLIER = 0.3   # 30% health increase per boost

# ==================== Upgrade Types ====================
UPGRADE_BULLET_SPEED = "bullet_speed"
UPGRADE_CLEAR_SCREEN = "clear_screen"
UPGRADE_TRIPLE_SHOT = "triple_shot"
UPGRADE_PLAYER_SPEED = "player_speed"
UPGRADE_SCORE_MULTIPLIER = "score_multiplier"
UPGRADE_WINGMAN = "wingman"

# ==================== Game Text ====================
GAME_TITLE = "Alien Shooter"
SCORE_TEXT = "Score: {}"
GAME_OVER_TEXT = "Game Over! Press R to restart"
VICTORY_TEXT = "Victory! Press R to restart"

# ==================== Menu Text ====================
MENU_TITLE = "Welcome to Alien Shooter!"
MENU_SUBTITLE = "Select Your Mode"
CLASSIC_MODE_TEXT = "1. Classic Mode"
RANDOM_MODE_TEXT = "2. Random Mode"
VERSUS_MODE_TEXT = "3. Versus Mode"
CLASSIC_MODE_DESC = 'Reach 100 points to win'
RANDOM_MODE_DESC = "Endless fun, upgrade every 100 points"
VERSUS_MODE_DESC = "2 players, first to 500 points wins"
MENU_INSTRUCTION = "Press 1, 2, or 3 to choose mode"

# ==================== Upgrade Menu Text ====================
UPGRADE_TITLE = "Choose Your Upgrade!"
UPGRADE_INSTRUCTION = "Press 1, 2 or 3 to choose upgrade"

# ==================== Upgrade Descriptions ====================
UPGRADE_DESCRIPTIONS = {
    UPGRADE_BULLET_SPEED: "Increase Bullet Speed (+15%)",
    UPGRADE_CLEAR_SCREEN: "Clear Screen Ability (40s cooldown, -10s per upgrade, min 20s)",
    UPGRADE_TRIPLE_SHOT: "Triple Shot (10 DMG sides, +50% DMG per upgrade, max 100)",
    UPGRADE_PLAYER_SPEED: "Increase Ship Speed (+20%)",
    UPGRADE_SCORE_MULTIPLIER: "Score Multiplier (+15%)",
    UPGRADE_WINGMAN: "Star Wingman (Pink bullets, 10 DMG, follows you)"
}
