# Alien Shooter Game
#求求你点个赞吧，我什么都会愿意的...(这是我的第一个项目，虽然是ai写的...)
A simple shooting game developed with Python and Pygame.

## Game Features

### 🎮 **Game Modes**
- **Classic Mode**: Traditional gameplay, win at 100 points
- **Random Mode**: Endless game, upgrade selection every 100 points

### 🚀 **Core Features**
- **Screen Size**: 600x800 pixels
- **Player Aircraft**: 30x30 pixel green rectangle
- **Aliens**: 30x30 pixel red rectangles with health bars, intelligent left-right movement
- **Movement Speed**: Player 4 pixels/frame, aliens 1 pixel/frame
- **Shooting System**: Auto-fire 5 colored bullets per second, 50 damage each
- **Colored Bullets**: Bullet colors cycle through red, green, blue for visibility
- **Explosion Effects**: Particle explosion animation when aliens are defeated
- **Dynamic Background**: Light gray rectangles moving upward, simulating aircraft forward motion

### 📈 **Upgrade System** (Random Mode)
- **Trigger Condition**: Every multiple of 100 points
- **Selection Method**: 3 random upgrades chosen from 5 available options
- **Milestone System**: Every 1000 points, alien count increases by 60%
- **Upgrade Options**:
  - **Bullet Speed**: +15% bullet speed (alien count +10%)
  - **Clear Screen**: 40s cooldown initially, -15s per upgrade (SPACE key)
  - **Triple Shot**: First: 3 bullets (sides 10 DMG), Later: +50% side damage
  - **Ship Speed**: +20% movement speed
  - **Score Multiplier**: +15% points per kill
- **Progressive Upgrades**: Many upgrades improve with multiple selections

### 🎯 **Game Rules**
- **Alien Spawning**: Randomly spawn 1-5 aliens every 5 seconds
- **Scoring System**: 5 points per alien killed
- **Failure Conditions**: Player collision with aliens or aliens reaching the bottom

## Game Controls

### 🎮 **Start Menu**
- **1 Key**: Select Classic Mode
- **2 Key**: Select Random Mode
- **3 Key**: Select Versus Mode

### 🕹️ **In Game**
- **Arrow Keys**: Control aircraft movement (up, down, left, right)
- **Auto Shooting**: Bullets fire automatically
- **SPACE Key**: Clear screen ability (if unlocked, 20s cooldown)
- **R Key**: Restart after game over or victory

### ⚔️ **Versus Mode Controls**
- **Player 1**: WASD keys for movement (left half of screen)
- **Player 2**: Arrow keys for movement (right half of screen)
- **Auto Shooting**: Both players fire automatically
- **Boundary Wall**: Center divider prevents aliens from crossing between player areas
- **R Key**: Restart after game over

### ⬆️ **Upgrade Menu** (Random Mode)
- **1, 2, 3 Keys**: Select upgrade options

## Installation and Running

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the game:
```bash
python main.py
```

## Game Rules

### 🎯 **Basic Gameplay**
1. Select mode (Classic or Random) at game start
2. Use arrow keys to control the green aircraft
3. Aircraft automatically fires colored bullets (red, green, blue cycle)
4. Hit red aliens to deal damage (aliens have health bars)
5. Aliens produce explosion effects when defeated
6. Earn 5 points for each alien killed

### 🏆 **Win/Loss Conditions**
- **Classic Mode**: Win at 100 points
- **Random Mode**: No victory condition, challenge for highest score
- **Versus Mode**: First player to reach 500 points wins, or opponent loses
- **Loss Condition**: Aircraft collision with aliens or aliens reaching the bottom

### ⬆️ **Upgrade System** (Random Mode)
1. **Early Game (0-9999 points)**: Overlay upgrade menu appears every 100 points
2. **Game Pause**: Game pauses during upgrade selection for focused decision-making
3. **Milestone System**: Every 1000 points, alien spawn rate increases by 60% (stops at 10000 points)
4. **Selection Process**: 3 random upgrades chosen from 6 available options
5. **Progressive Upgrades**: Many upgrades improve with multiple selections:
   - **Bullet Speed**: +15% speed each time (aliens +10%)
   - **Clear Screen**: Starts at 40s cooldown, reduces by 10s each upgrade (min 20s)
   - **Triple Shot**: First gives 3 bullets (10 DMG sides), +50% side damage (max 100 DMG)
   - **Ship Speed**: +20% movement speed each time
   - **Score Multiplier**: +15% points per kill each time
   - **Star Wingman**: Adds a star-shaped ally that fires pink bullets (10 DMG)
6. **Endgame (10000+ points)**: No more upgrades, alien health increases by 30% every 500 points
7. **Smart Filtering**: Maxed upgrades are automatically removed from selection
8. **Strategic Depth**: Choose between immediate power or long-term growth

### 🔄 **Restart**
- Press R key to restart after game over
- Restart returns to mode selection menu

## Project Structure

```
alien_shooter/
├── main.py          # Program entry point
├── game.py          # Single-player game logic and state management
├── versus_game.py   # Versus mode game logic and state management
├── entities.py      # Game entity classes (Player, Alien, Bullet)
├── background.py    # Background effects management
├── menu.py          # Menu system management
├── upgrade_window.py # Independent upgrade selection window
├── config.py        # Game configuration and constants
├── requirements.txt # Dependency list
└── README.md       # Project documentation
```

## Technical Implementation

- **Modular Design**: Code separated into different modules by function for easy maintenance and extension
- **Object-Oriented**: Uses classes to encapsulate game entities and managers
- **Configuration Separation**: All game parameters centralized in config.py for easy adjustment
- **Pygame Library**: Used for graphics rendering, event handling, and collision detection
- **60FPS Game Loop**: Ensures smooth gaming experience
