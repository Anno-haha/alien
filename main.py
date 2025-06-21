"""
射击外星人游戏 - 主程序入口
一个使用pygame开发的简单射击游戏
玩家控制飞机击杀外星人，避免碰撞和外星人到达底部
"""

from game import Game


def main():
    """
    程序主入口点
    创建游戏实例并开始运行
    """
    try:
        # 创建游戏对象
        game = Game()
        
        # 开始游戏循环
        game.run()
        
    except Exception as e:
        print(f"游戏运行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
