import pygame, random, sys, math, os
pygame.init()

# Initial board settings (standard Tetris: 10x20)
COLS, ROWS = 10, 20
INIT_WIDTH, INIT_HEIGHT = 800, 600  # increased initial window size for better menu visibility
MIN_WIDTH, MIN_HEIGHT = 800, 600  # minimum window size to prevent scaling issues

# Create a resizable window
screen = pygame.display.set_mode((INIT_WIDTH, INIT_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("HyperTetris 4D Extreme")

# Global variables for dynamic sizing
WIDTH, HEIGHT = INIT_WIDTH, INIT_HEIGHT
CELL_SIZE = min(WIDTH // (COLS + 10), HEIGHT // ROWS)  # Adjusted to leave more space for UI

clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
PINK = (255, 105, 180)
TEAL = (0, 128, 128)
LIME = (50, 205, 50)
MAGENTA = (255, 0, 255)
BROWN = (165, 42, 42)
NAVY = (0, 0, 128)
colors = [CYAN, YELLOW, PURPLE, GREEN, RED, BLUE, ORANGE, PINK, TEAL, LIME, MAGENTA, BROWN, NAVY]

# Tetromino shapes (including unique ones)
tetrominoes = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1],
          [1, 1]],
    'T': [[0, 1, 0],
          [1, 1, 1]],
    'S': [[0, 1, 1],
          [1, 1, 0]],
    'Z': [[1, 1, 0],
          [0, 1, 1]],
    'J': [[1, 0, 0],
          [1, 1, 1]],
    'L': [[0, 0, 1],
          [1, 1, 1]],
    # Unique shapes
    'X': [[0, 1, 0],
          [1, 1, 1],
          [0, 1, 0]],
    'U': [[1, 0, 1],
          [1, 1, 1]],
    'P': [[1, 1],
          [1, 1],
          [1, 0]],
    'Plus': [[0, 1, 0],
             [1, 1, 1],
             [0, 1, 0]],
    'H': [[1, 0, 1],
          [1, 1, 1],
          [1, 0, 1]],
    'W': [[1, 0, 0, 0],
          [1, 0, 0, 0],
          [1, 1, 1, 1]],
    'C': [[1, 1, 1],
          [1, 0, 0],
          [1, 1, 1]],
    'Zigzag': [[1, 1, 0, 0],
               [0, 1, 1, 0],
               [0, 0, 1, 1]],
    'Cross': [[0, 1, 0],
              [1, 1, 1],
              [0, 1, 0]],
    'Donut': [[1, 1, 1],
              [1, 0, 1],
              [1, 1, 1]],
    'Stairs': [[1, 0, 0],
               [1, 1, 0],
               [0, 1, 1]],
    'Lightning': [[0, 1, 0],
                  [1, 1, 0],
                  [0, 1, 1]],
    'Snake': [[0, 1, 1],
              [1, 1, 0],
              [0, 1, 0]]
}

# Create a 3D representation of each tetromino shape with depth/height information
tetromino_3d = {
    'I': [[[1, 1, 1], [2, 1, 1], [3, 1, 1], [4, 1, 1]]],  # Horizontal bar
    'O': [[[1, 1, 1], [2, 1, 1]], 
          [[1, 2, 1], [2, 2, 1]]],  # Square
    'T': [[[2, 1, 1]], 
          [[1, 2, 1], [2, 2, 1], [3, 2, 1]]],
    'S': [[[2, 1, 1], [3, 1, 1]], 
          [[1, 2, 1], [2, 2, 1]]],
    'Z': [[[1, 1, 1], [2, 1, 1]], 
          [[2, 2, 1], [3, 2, 1]]],
    'J': [[[1, 1, 1]], 
          [[1, 2, 1], [2, 2, 1], [3, 2, 1]]],
    'L': [[[3, 1, 1]], 
          [[1, 2, 1], [2, 2, 1], [3, 2, 1]]],
    'X': [[[2, 1, 1]], 
          [[1, 2, 1], [2, 2, 1], [3, 2, 1]], 
          [[2, 3, 1]]],
    'U': [[[1, 1, 1], [3, 1, 1]], 
          [[1, 2, 1], [2, 2, 1], [3, 2, 1]]],
    'P': [[[1, 1, 1], [2, 1, 1]],
          [[1, 2, 1], [2, 2, 1]],
          [[1, 3, 1]]],
    'Plus': [[[2, 1, 1]],
             [[1, 2, 1], [2, 2, 2], [3, 2, 1]],
             [[2, 3, 1]]],
    'H': [[[1, 1, 1], [3, 1, 1]],
          [[1, 2, 2], [2, 2, 2], [3, 2, 2]],
          [[1, 3, 1], [3, 3, 1]]],
    'W': [[[1, 1, 1]],
          [[1, 2, 1]],
          [[1, 3, 1], [2, 3, 1], [3, 3, 1], [4, 3, 1]]],
    'C': [[[1, 1, 1], [2, 1, 1], [3, 1, 1]],
          [[1, 2, 1]],
          [[1, 3, 1], [2, 3, 1], [3, 3, 1]]],
    'Zigzag': [[[1, 1, 1], [2, 1, 1]],
               [[2, 2, 1], [3, 2, 1]],
               [[3, 3, 1], [4, 3, 1]]],
    'Cross': [[[2, 1, 1]],
              [[1, 2, 1], [2, 2, 2], [3, 2, 1]],
              [[2, 3, 1]]],
    'Donut': [[[1, 1, 1], [2, 1, 1], [3, 1, 1]],
              [[1, 2, 1], [3, 2, 1]],
              [[1, 3, 1], [2, 3, 1], [3, 3, 1]]],
    'Stairs': [[[1, 1, 1]],
               [[1, 2, 1], [2, 2, 1]],
               [[2, 3, 1], [3, 3, 1]]],
    'Lightning': [[[2, 1, 1]],
                 [[1, 2, 1], [2, 2, 1]],
                 [[2, 3, 1], [3, 3, 1]]],
    'Snake': [[[2, 1, 1], [3, 1, 1]],
             [[1, 2, 1], [2, 2, 1]],
             [[2, 3, 1]]]
}

# 3D visualization parameters
ISOMETRIC_ANGLE = 30  # Degrees for isometric view
SCALE_FACTOR = 0.8
DEPTH_FACTOR = 0.5

# Camera/view settings for 3D and 4D modes
camera_x = 0
camera_y = 0
camera_zoom = 1.0

# Sound effects
try:
    pygame.mixer.init()
    rotation_sound = pygame.mixer.Sound('sounds/rotate.wav')
    drop_sound = pygame.mixer.Sound('sounds/drop.wav')
    line_clear_sound = pygame.mixer.Sound('sounds/clear.wav')
    game_over_sound = pygame.mixer.Sound('sounds/gameover.wav')
    menu_select_sound = pygame.mixer.Sound('sounds/select.wav')
    sound_enabled = True
except:
    sound_enabled = False

# Font setup
try:
    font_small = pygame.font.Font(None, 36)
    font_medium = pygame.font.Font(None, 48)
    font_large = pygame.font.Font(None, 72)
except:
    print("Warning: Default font not found. Using system font.")
    font_small = pygame.font.SysFont("Arial", 36)
    font_medium = pygame.font.SysFont("Arial", 48)
    font_large = pygame.font.SysFont("Arial", 72)

def create_piece():
    shape = random.choice(list(tetrominoes.keys()))
    matrix = tetrominoes[shape]
    color = random.choice(colors)
    x = COLS // 2 - len(matrix[0]) // 2
    y = 0
    return {'matrix': matrix, 'shape': shape, 'x': x, 'y': y, 'color': color}

def rotate_piece(piece):
    matrix = piece['matrix']
    rotated = [list(row) for row in zip(*matrix[::-1])]
    piece['matrix'] = rotated
    if sound_enabled:
        rotation_sound.play()

def valid_position(piece, board, adj_x=0, adj_y=0):
    matrix = piece['matrix']
    for i, row in enumerate(matrix):
        for j, cell in enumerate(row):
            if cell:
                x = piece['x'] + j + adj_x
                y = piece['y'] + i + adj_y
                if x < 0 or x >= COLS or y < 0 or y >= ROWS:
                    return False
                if y >= 0 and board[y][x] != BLACK:  # Check y >= 0 to avoid index errors
                    return False
    return True

def add_piece_to_board(piece, board):
    matrix = piece['matrix']
    for i, row in enumerate(matrix):
        for j, cell in enumerate(row):
            if cell:
                if piece['y'] + i >= 0:  # Ensure we're not accessing negative indices
                    board[piece['y'] + i][piece['x'] + j] = piece['color']

def remove_complete_lines(board):
    new_board = [row for row in board if any(cell == BLACK for cell in row)]
    lines_removed = ROWS - len(new_board)
    while len(new_board) < ROWS:
        new_board.insert(0, [BLACK for _ in range(COLS)])
    return new_board, lines_removed

def transform_point_4d(x, y, mode, time_factor=0.002):
    """
    Improved 4D transformation with better boundary handling
    """
    global camera_x, camera_y, camera_zoom
    
    if mode == "4D":
        t = pygame.time.get_ticks() * time_factor
        
        # Apply camera offsets
        x = (x - camera_x) * camera_zoom
        y = (y - camera_y) * camera_zoom
        
        # Get board center
        center_x, center_y = COLS * CELL_SIZE / 2, ROWS * CELL_SIZE / 2
        
        # Calculate position relative to center
        rel_x = x - center_x
        rel_y = y - center_y
        
        # More controlled wave effect based on y position
        wave_intensity = 10 * camera_zoom  # Scale with zoom
        wave_x = math.sin(t + y/100) * (y/HEIGHT) * wave_intensity
        wave_y = math.cos(t + x/100) * (y/HEIGHT) * wave_intensity
        
        # Add slight rotation
        rotation = t * 0.1  # Slow rotation
        rx = rel_x * math.cos(rotation) - rel_y * math.sin(rotation)
        ry = rel_x * math.sin(rotation) + rel_y * math.cos(rotation)
        
        # Apply a gentle scale that varies with time
        pulse_scale = 1 + 0.05 * math.sin(t * 0.5)
        scale = pulse_scale * camera_zoom
        
        new_x = center_x + rx * scale + wave_x
        new_y = center_y + ry * scale + wave_y
        
        # Apply boundary constraints - clamp to visible area with padding
        padding = CELL_SIZE
        new_x = max(padding, min(WIDTH - CELL_SIZE - padding, new_x))
        new_y = max(padding, min(HEIGHT - CELL_SIZE - padding, new_y))
        
        return new_x, new_y
    
    # Apply camera adjustments even in 2D mode
    x = (x - camera_x) * camera_zoom
    y = (y - camera_y) * camera_zoom
    return x, y

def transform_point_3d(x, y, height, width, depth=1):
    """
    Transform 2D coordinates to isometric 3D view with camera control
    """
    global camera_x, camera_y, camera_zoom
    
    # Apply camera adjustments
    x = (x - camera_x) * camera_zoom
    y = (y - camera_y) * camera_zoom
    
    # Convert to isometric projection
    angle_rad = math.radians(ISOMETRIC_ANGLE)
    
    # Center of the board for rotation
    center_x = COLS * CELL_SIZE / 2
    center_y = ROWS * CELL_SIZE / 2
    
    # Offset from center
    rel_x = x - center_x
    rel_y = y - center_y
    
    # Apply isometric transformation
    iso_x = (rel_x - rel_y) * math.cos(angle_rad)
    iso_y = (rel_x + rel_y) * math.sin(angle_rad) - (depth * DEPTH_FACTOR * CELL_SIZE)
    
    # Scale and add back center offset
    new_x = center_x + iso_x * SCALE_FACTOR * camera_zoom
    new_y = center_y + iso_y * SCALE_FACTOR * camera_zoom
    
    # Apply boundary constraints - clamp to visible area with padding
    padding = CELL_SIZE
    new_x = max(padding, min(WIDTH - CELL_SIZE - padding, new_x))
    new_y = max(padding, min(HEIGHT - CELL_SIZE - padding, new_y))
    
    return new_x, new_y

def draw_board(board, view_mode):
    # Draw grid lines first (only in 2D mode)
    if view_mode == "2D":
        for y in range(ROWS + 1):
            pygame.draw.line(screen, GRAY, (0, y * CELL_SIZE), (COLS * CELL_SIZE, y * CELL_SIZE))
        for x in range(COLS + 1):
            pygame.draw.line(screen, GRAY, (x * CELL_SIZE, 0), (x * CELL_SIZE, ROWS * CELL_SIZE))
    
    # Draw filled cells
    for y, row in enumerate(board):
        for x, color in enumerate(row):
            if color != BLACK:
                if view_mode == "4D":
                    tx, ty = transform_point_4d(x * CELL_SIZE, y * CELL_SIZE, view_mode)
                    pygame.draw.rect(screen, color, (tx, ty, CELL_SIZE * camera_zoom, CELL_SIZE * camera_zoom))
                    pygame.draw.rect(screen, WHITE, (tx, ty, CELL_SIZE * camera_zoom, CELL_SIZE * camera_zoom), 1)
                elif view_mode == "3D":
                    # Draw as 3D block
                    draw_3d_block(x, y, color)
                else:  # 2D mode
                    cx = (x * CELL_SIZE - camera_x) * camera_zoom
                    cy = (y * CELL_SIZE - camera_y) * camera_zoom
                    pygame.draw.rect(screen, color, (cx, cy, CELL_SIZE * camera_zoom, CELL_SIZE * camera_zoom))
                    pygame.draw.rect(screen, WHITE, (cx, cy, CELL_SIZE * camera_zoom, CELL_SIZE * camera_zoom), 1)

def draw_3d_block(x, y, color, depth=1):
    """Draw a 3D block with top, front and side faces"""
    # Base position for the block
    block_size = CELL_SIZE * SCALE_FACTOR * camera_zoom
    
    # Calculate lighter and darker shades for 3D effect
    top_color = lighten_color(color, 30)
    right_color = darken_color(color, 30)
    front_color = color
    
    # Define the corners of the cube
    # Top face
    top_front_left = transform_point_3d(x * CELL_SIZE, y * CELL_SIZE, 0, 0, depth)
    top_front_right = transform_point_3d((x+1) * CELL_SIZE, y * CELL_SIZE, 0, 0, depth)
    top_back_left = transform_point_3d(x * CELL_SIZE, (y+1) * CELL_SIZE, 0, 0, depth)
    top_back_right = transform_point_3d((x+1) * CELL_SIZE, (y+1) * CELL_SIZE, 0, 0, depth)
    
    # Bottom face (with height)
    bottom_front_left = transform_point_3d(x * CELL_SIZE, y * CELL_SIZE, 0, 0, depth+1)
    bottom_front_right = transform_point_3d((x+1) * CELL_SIZE, y * CELL_SIZE, 0, 0, depth+1)
    bottom_back_left = transform_point_3d(x * CELL_SIZE, (y+1) * CELL_SIZE, 0, 0, depth+1)
    bottom_back_right = transform_point_3d((x+1) * CELL_SIZE, (y+1) * CELL_SIZE, 0, 0, depth+1)
    
    # Draw top face
    pygame.draw.polygon(screen, top_color, [top_front_left, top_front_right, top_back_right, top_back_left])
    
    # Draw right face
    pygame.draw.polygon(screen, right_color, [top_front_right, bottom_front_right, bottom_back_right, top_back_right])
    
    # Draw front face
    pygame.draw.polygon(screen, front_color, [top_front_left, top_front_right, bottom_front_right, bottom_front_left])
    
    # Draw edges
    pygame.draw.line(screen, WHITE, top_front_left, top_front_right, 1)
    pygame.draw.line(screen, WHITE, top_front_right, top_back_right, 1)
    pygame.draw.line(screen, WHITE, top_back_right, top_back_left, 1)
    pygame.draw.line(screen, WHITE, top_back_left, top_front_left, 1)
    
    pygame.draw.line(screen, WHITE, top_front_left, bottom_front_left, 1)
    pygame.draw.line(screen, WHITE, top_front_right, bottom_front_right, 1)
    pygame.draw.line(screen, WHITE, top_back_right, bottom_back_right, 1)
    pygame.draw.line(screen, WHITE, top_back_left, bottom_back_left, 1)

def lighten_color(color, amount=30):
    """Return a lighter version of the color"""
    r, g, b = color
    return (min(r + amount, 255), min(g + amount, 255), min(b + amount, 255))

def darken_color(color, amount=30):
    """Return a darker version of the color"""
    r, g, b = color
    return (max(r - amount, 0), max(g - amount, 0), max(b - amount, 0))

def draw_piece(piece, view_mode):
    matrix = piece['matrix']
    for i, row in enumerate(matrix):
        for j, cell in enumerate(row):
            if cell:
                x = piece['x'] + j
                y = piece['y'] + i
                
                if y < 0:  # Skip drawing blocks above the top of the board
                    continue
                
                if view_mode == "4D":
                    tx, ty = transform_point_4d(x * CELL_SIZE, y * CELL_SIZE, view_mode)
                    pygame.draw.rect(screen, piece['color'], (tx, ty, CELL_SIZE * camera_zoom, CELL_SIZE * camera_zoom))
                    pygame.draw.rect(screen, WHITE, (tx, ty, CELL_SIZE * camera_zoom, CELL_SIZE * camera_zoom), 1)
                elif view_mode == "3D":
                    # For 3D mode, draw blocks with height
                    if piece['shape'] in tetromino_3d:
                        # Get the relative height for this block (default to 1)
                        block_height = 1
                        for shape_row in tetromino_3d[piece['shape']]:
                            for block in shape_row:
                                if block[0] == j+1 and block[1] == i+1:
                                    block_height = block[2]
                        draw_3d_block(x, y, piece['color'], block_height)
                    else:
                        # Fallback for shapes without 3D definition
                        draw_3d_block(x, y, piece['color'])
                else:  # 2D mode
                    cx = (x * CELL_SIZE - camera_x) * camera_zoom
                    cy = (y * CELL_SIZE - camera_y) * camera_zoom
                    pygame.draw.rect(screen, piece['color'], 
                                    (cx, cy, CELL_SIZE * camera_zoom, CELL_SIZE * camera_zoom))
                    pygame.draw.rect(screen, WHITE, 
                                    (cx, cy, CELL_SIZE * camera_zoom, CELL_SIZE * camera_zoom), 1)

def draw_ghost_piece(piece, board, view_mode):
    # Create a ghost piece that shows where the current piece will land
    ghost = {'matrix': piece['matrix'], 'x': piece['x'], 'y': piece['y'], 
             'color': (50, 50, 50), 'shape': piece['shape']}
    
    # Find how far the piece can drop
    drop_distance = 0
    while valid_position(ghost, board, adj_y=drop_distance+1):
        drop_distance += 1
    
    ghost['y'] += drop_distance
    
    # Draw the ghost piece with transparency
    matrix = ghost['matrix']
    for i, row in enumerate(matrix):
        for j, cell in enumerate(row):
            if cell:
                x = ghost['x'] + j
                y = ghost['y'] + i
                
                # Skip if above the visible board
                if y < 0:
                    continue
                
                # Create a semi-transparent surface
                s = pygame.Surface((CELL_SIZE * camera_zoom, CELL_SIZE * camera_zoom))
                s.set_alpha(80)  # transparency
                s.fill(piece['color'])
                
                if view_mode == "4D":
                    tx, ty = transform_point_4d(x * CELL_SIZE, y * CELL_SIZE, view_mode)
                    screen.blit(s, (tx, ty))
                    pygame.draw.rect(screen, WHITE, (tx, ty, CELL_SIZE * camera_zoom, CELL_SIZE * camera_zoom), 1)
                elif view_mode == "3D":
                    # For 3D mode, we'll use a simplified transparent version
                    # Just outline where it will land
                    if ghost['shape'] in tetromino_3d:
                        # Get the relative height for this block (default to 1)
                        block_height = 1
                        for shape_row in tetromino_3d[ghost['shape']]:
                            for block in shape_row:
                                if block[0] == j+1 and block[1] == i+1:
                                    block_height = block[2]
                        
                        tx, ty = transform_point_3d(x * CELL_SIZE, y * CELL_SIZE, 0, 0, block_height)
                        pygame.draw.rect(screen, WHITE, 
                                        (tx-1, ty-1, CELL_SIZE*SCALE_FACTOR*camera_zoom+2, 
                                         CELL_SIZE*SCALE_FACTOR*camera_zoom+2), 1)
                else:
                    cx = (x * CELL_SIZE - camera_x) * camera_zoom
                    cy = (y * CELL_SIZE - camera_y) * camera_zoom
                    screen.blit(s, (cx, cy))
                    pygame.draw.rect(screen, WHITE, 
                                    (cx, cy, CELL_SIZE * camera_zoom, CELL_SIZE * camera_zoom), 1)

def create_board():
    return [[BLACK for _ in range(COLS)] for _ in range(ROWS)]

def draw_next_piece(next_piece, x, y):
    # Draw a preview of the next piece
    matrix = next_piece['matrix']
    scale = 1.5  # Smaller scale for preview
    
    for i, row in enumerate(matrix):
        for j, cell in enumerate(row):
            if cell:
                rect_x = x + j * (CELL_SIZE // scale)
                rect_y = y + i * (CELL_SIZE // scale)
                pygame.draw.rect(screen, next_piece['color'], 
                                (rect_x, rect_y, CELL_SIZE // scale, CELL_SIZE // scale))
                pygame.draw.rect(screen, WHITE, 
                                (rect_x, rect_y, CELL_SIZE // scale, CELL_SIZE // scale), 1)

def is_game_over(board):
    # Check if any blocks are in the top row
    return any(cell != BLACK for cell in board[0])

# Generate a custom background
def create_custom_background(width, height):
    """Generate a custom unique background with a spacey, dynamic look"""
    bg = pygame.Surface((width, height))
    
    # Fill with dark base color
    bg.fill((10, 5, 20))  # Very dark purple-blue
    
    # Create a grid of stars with various brightnesses
    for _ in range(200):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        size = random.randint(1, 3)
        brightness = random.randint(150, 255)
        pygame.draw.circle(bg, (brightness, brightness, brightness), (x, y), size)
    
    # Add some nebula-like color patches
    for _ in range(10):
        center_x = random.randint(0, width)
        center_y = random.randint(0, height)
        radius = random.randint(50, 150)
        color_r = random.randint(0, 100)
        color_g = random.randint(0, 100)
        color_b = random.randint(50, 150)
        
        # Create a surface with per-pixel alpha
        nebula = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        
        # Draw radial gradient
        for r in range(radius):
            alpha = 100 - int((r / radius) * 100)
            pygame.draw.circle(nebula, (color_r, color_g, color_b, alpha), (radius, radius), radius - r)
        
        # Blit the nebula onto the background
        bg.blit(nebula, (center_x - radius, center_y - radius))
    
    # Add some horizontal line effects (like scan lines)
    for y in range(0, height, 4):
        for x in range(width):
            if x % 2 == 0:
                # Get current pixel color
                r, g, b = bg.get_at((x, y))[:3]
                # Darken it slightly
                bg.set_at((x, y), (max(0, r-10), max(0, g-10), max(0, b-10)))
    
    return bg

# Create custom background
background = create_custom_background(INIT_WIDTH, INIT_HEIGHT)

# Menu options
menu_options = ["Play Game", "How to Play", "Options", "Quit"]
selected_option = 0

# Game states
MENU = 0
GAME = 1
TUTORIAL = 2
OPTIONS = 3
game_state = MENU  # Start with menu

# Global game variables
board = create_board()
current_piece = create_piece()
next_piece = create_piece()
fall_time = 0
difficulty_levels = {"Easy": 500, "Medium": 300, "Hard": 200, "Extreme": 150, "Impossible": 80}
current_difficulty = "Medium"
base_fall_speed = difficulty_levels[current_difficulty]
view_mode = "2D"  # "2D", "3D", or "4D"
score = 0
lines_cleared = 0
game_over = False
paused = False
show_ghost = True  # Option to show ghost piece
high_score = 0

# 4D effect parameters - customizable to reduce glitchiness
_4d_time_factor = 0.001  # Slow down the 4D animation
_4d_wave_intensity = 0.3  # Reduce wave effect intensity

# Try to load high score from file
try:
    with open("highscore.txt", "r") as f:
        high_score = int(f.read())
except FileNotFoundError:
    pass

# Function to save high score
def save_high_score():
    global high_score
    with open("highscore.txt", "w") as f:
        f.write(str(high_score))

# Function to draw text with a shadow for better visibility
def draw_text_with_shadow(text, font, color, position, shadow_offset=2):
    shadow = font.render(text, True, BLACK)
    text_surface = font.render(text, True, color)
    screen.blit(shadow, (position[0] + shadow_offset, position[1] + shadow_offset))
    screen.blit(text_surface, position)

# Game loop
running = True
while running:
    # Handle window resizing
    if WIDTH != screen.get_width() or HEIGHT != screen.get_height():
        WIDTH, HEIGHT = screen.get_width(), screen.get_height()
        CELL_SIZE = min(WIDTH // (COLS + 10), HEIGHT // ROWS)
        # Recreate background if window size changes
        background = create_custom_background(WIDTH, HEIGHT)
    
    # Scale and draw background
    scaled_background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    screen.blit(scaled_background, (0, 0))
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Handle window resize
        elif event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            WIDTH = max(WIDTH, MIN_WIDTH)
            HEIGHT = max(HEIGHT, MIN_HEIGHT)
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            CELL_SIZE = min(WIDTH // (COLS + 10), HEIGHT // ROWS)
            background = create_custom_background(WIDTH, HEIGHT)
        
        # Handle keyboard events
        elif event.type == pygame.KEYDOWN:
            if game_state == MENU:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                    if sound_enabled:
                        menu_select_sound.play()
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                    if sound_enabled:
                        menu_select_sound.play()
                elif event.key == pygame.K_RETURN:
                    if menu_options[selected_option] == "Play Game":
                        game_state = GAME
                        board = create_board()
                        current_piece = create_piece()
                        next_piece = create_piece()
                        score = 0
                        lines_cleared = 0
                        game_over = False
                        fall_time = 0
                        if sound_enabled:
                            menu_select_sound.play()
                    elif menu_options[selected_option] == "How to Play":
                        game_state = TUTORIAL
                        if sound_enabled:
                            menu_select_sound.play()
                    elif menu_options[selected_option] == "Options":
                        game_state = OPTIONS
                        if sound_enabled:
                            menu_select_sound.play()
                    elif menu_options[selected_option] == "Quit":
                        running = False
            
            elif game_state == TUTORIAL:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    game_state = MENU
                    if sound_enabled:
                        menu_select_sound.play()
            
            elif game_state == OPTIONS:
                if event.key == pygame.K_ESCAPE:
                    game_state = MENU
                    if sound_enabled:
                        menu_select_sound.play()
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % 5  # 5 options in the options menu
                    if sound_enabled:
                        menu_select_sound.play()
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % 5
                    if sound_enabled:
                        menu_select_sound.play()
                elif event.key == pygame.K_LEFT:
                    if selected_option == 0:  # Difficulty
                        difficulties = list(difficulty_levels.keys())
                        current_index = difficulties.index(current_difficulty)
                        current_difficulty = difficulties[(current_index - 1) % len(difficulties)]
                        base_fall_speed = difficulty_levels[current_difficulty]
                    elif selected_option == 1:  # View Mode
                        view_modes = ["2D", "3D", "4D"]
                        current_index = view_modes.index(view_mode)
                        view_mode = view_modes[(current_index - 1) % len(view_modes)]
                    elif selected_option == 2:  # Sound
                        sound_enabled = not sound_enabled
                    elif selected_option == 3:  # Ghost Piece
                        show_ghost = not show_ghost
                    if sound_enabled:
                        menu_select_sound.play()
                elif event.key == pygame.K_RIGHT:
                    if selected_option == 0:  # Difficulty
                        difficulties = list(difficulty_levels.keys())
                        current_index = difficulties.index(current_difficulty)
                        current_difficulty = difficulties[(current_index + 1) % len(difficulties)]
                        base_fall_speed = difficulty_levels[current_difficulty]
                    elif selected_option == 1:  # View Mode
                        view_modes = ["2D", "3D", "4D"]
                        current_index = view_modes.index(view_mode)
                        view_mode = view_modes[(current_index + 1) % len(view_modes)]
                    elif selected_option == 2:  # Sound
                        sound_enabled = not sound_enabled
                    elif selected_option == 3:  # Ghost Piece
                        show_ghost = not show_ghost
                    if sound_enabled:
                        menu_select_sound.play()
                elif event.key == pygame.K_RETURN and selected_option == 4:  # Return to Menu
                    game_state = MENU
                    selected_option = 0
                    if sound_enabled:
                        menu_select_sound.play()
            
            elif game_state == GAME and not game_over:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                
                if not paused:
                    if event.key == pygame.K_LEFT:
                        if valid_position(current_piece, board, adj_x=-1):
                            current_piece['x'] -= 1
                    elif event.key == pygame.K_RIGHT:
                        if valid_position(current_piece, board, adj_x=1):
                            current_piece['x'] += 1
                    elif event.key == pygame.K_DOWN:
                        if valid_position(current_piece, board, adj_y=1):
                            current_piece['y'] += 1
                    elif event.key == pygame.K_UP:
                        # Store the original matrix to restore if rotation is invalid
                        original_matrix = current_piece['matrix'].copy()
                        rotate_piece(current_piece)
                        if not valid_position(current_piece, board):
                            # Undo rotation if it results in an invalid position
                            current_piece['matrix'] = original_matrix
                    elif event.key == pygame.K_SPACE:
                        # Hard drop
                        while valid_position(current_piece, board, adj_y=1):
                            current_piece['y'] += 1
                        if sound_enabled:
                            drop_sound.play()
                        
                        # Add the piece to the board
                        add_piece_to_board(current_piece, board)
                        
                        # Check for completed lines
                        board, cleared_lines = remove_complete_lines(board)
                        lines_cleared += cleared_lines
                        
                        # Award points
                        if cleared_lines > 0:
                            score += (cleared_lines * 100) * (cleared_lines * 0.5)  # Bonus for multiple lines
                            if sound_enabled:
                                line_clear_sound.play()
                        
                        # Update high score
                        if score > high_score:
                            high_score = score
                            save_high_score()
                        
                        # Get the next piece
                        current_piece = next_piece
                        next_piece = create_piece()
                        
                        # Check for game over
                        if not valid_position(current_piece, board):
                            game_over = True
                            if sound_enabled:
                                game_over_sound.play()
                    
                    # Camera controls
                    elif event.key == pygame.K_a:
                        camera_x -= 10
                    elif event.key == pygame.K_d:
                        camera_x += 10
                    elif event.key == pygame.K_w:
                        camera_y -= 10
                    elif event.key == pygame.K_s:
                        camera_y += 10
                    elif event.key == pygame.K_q:
                        camera_zoom = max(0.5, camera_zoom - 0.1)
                    elif event.key == pygame.K_e:
                        camera_zoom = min(2.0, camera_zoom + 0.1)
                    elif event.key == pygame.K_r:
                        # Reset camera
                        camera_x, camera_y = 0, 0
                        camera_zoom = 1.0
                    
                    # Switch view mode on the fly
                    elif event.key == pygame.K_1:
                        view_mode = "2D"
                    elif event.key == pygame.K_2:
                        view_mode = "3D"
                    elif event.key == pygame.K_3:
                        view_mode = "4D"
                    elif event.key == pygame.K_g:
                        show_ghost = not show_ghost
            elif game_over and event.key == pygame.K_RETURN:
                game_state = MENU
                selected_option = 0
    
    # MENU STATE
    if game_state == MENU:
        # Draw fancy title
        title = font_large.render("HyperTetris 4D", True, CYAN)
        subtitle = font_medium.render("EXTREME EDITION", True, MAGENTA)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//4 - title.get_height()//2))
        screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, HEIGHT//4 + title.get_height()))
        
        # Draw menu options
        menu_y = HEIGHT//2
        for i, option in enumerate(menu_options):
            color = YELLOW if i == selected_option else WHITE
            text = font_medium.render(option, True, color)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, menu_y))
            menu_y += 60
        
        # Draw high score
        high_score_text = font_small.render(f"High Score: {high_score}", True, GREEN)
        screen.blit(high_score_text, (WIDTH//2 - high_score_text.get_width()//2, HEIGHT - 100))
    
    # TUTORIAL STATE
    elif game_state == TUTORIAL:
        # Draw tutorial text
        title = font_large.render("How to Play", True, YELLOW)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        
        instructions = [
            "Arrow Keys: Move and rotate pieces",
            "Space: Hard drop",
            "Escape: Pause game",
            "WASD: Pan camera view",
            "Q/E: Zoom in/out",
            "R: Reset camera",
            "1/2/3: Switch between 2D/3D/4D views",
            "G: Toggle ghost piece",
            "",
            "Clear lines to score points!",
            "The game gets harder as you progress."
        ]
        
        y_pos = 150
        for line in instructions:
            text = font_small.render(line, True, WHITE)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, y_pos))
            y_pos += 40
        
        # Draw "Press Enter to return" at the bottom
        back_text = font_small.render("Press Enter to return to menu", True, GREEN)
        screen.blit(back_text, (WIDTH//2 - back_text.get_width()//2, HEIGHT - 100))
    
    # OPTIONS STATE
    elif game_state == OPTIONS:
        title = font_large.render("Options", True, YELLOW)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        
        options = [
            f"Difficulty: {current_difficulty}",
            f"View Mode: {view_mode}",
            f"Sound: {'On' if sound_enabled else 'Off'}",
            f"Ghost Piece: {'On' if show_ghost else 'Off'}",
            "Return to Menu"
        ]
        
        y_pos = 150
        for i, option in enumerate(options):
            color = CYAN if i == selected_option else WHITE
            text = font_medium.render(option, True, color)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, y_pos))
            y_pos += 60
        
        # Draw controls help
        controls_text = font_small.render("Use Arrow Keys to navigate and change options", True, GREEN)
        screen.blit(controls_text, (WIDTH//2 - controls_text.get_width()//2, HEIGHT - 100))
    
    # GAME STATE
    elif game_state == GAME:
        # Calculate game board position (center it if in 3D/4D mode)
        board_x = (WIDTH - COLS * CELL_SIZE) // 2 if view_mode in ["3D", "4D"] else 0
        board_y = 0
        
        # Draw game board (offset by camera position)
        draw_board(board, view_mode)
        
        if not game_over and not paused:
            # Draw ghost piece (preview of where the piece will land)
            if show_ghost:
                draw_ghost_piece(current_piece, board, view_mode)
            
            # Draw the current piece
            draw_piece(current_piece, view_mode)
            
            # Automatic falling
            current_time = pygame.time.get_ticks()
            if current_time - fall_time > base_fall_speed:
                fall_time = current_time
                if valid_position(current_piece, board, adj_y=1):
                    current_piece['y'] += 1
                else:
                    # Add the piece to the board
                    add_piece_to_board(current_piece, board)
                    
                    # Check for completed lines
                    board, cleared_lines = remove_complete_lines(board)
                    lines_cleared += cleared_lines
                    
                    # Award points
                    if cleared_lines > 0:
                        score += (cleared_lines * 100) * (cleared_lines * 0.5)
                        if sound_enabled:
                            line_clear_sound.play()
                    
                    # Update high score
                    if score > high_score:
                        high_score = score
                        save_high_score()
                    
                    # Get the next piece
                    current_piece = next_piece
                    next_piece = create_piece()
                    
                    # Check for game over
                    if not valid_position(current_piece, board):
                        game_over = True
                        if sound_enabled:
                            game_over_sound.play()
        
        # Draw UI panel
        ui_panel = pygame.Surface((WIDTH - (board_x + COLS * CELL_SIZE), HEIGHT))
        ui_panel.fill((30, 30, 40))
        ui_panel.set_alpha(200)  # Semi-transparent
        screen.blit(ui_panel, (board_x + COLS * CELL_SIZE, 0))
        
        # Draw score and other info
        score_text = font_medium.render(f"Score: {int(score)}", True, WHITE)
        screen.blit(score_text, (board_x + COLS * CELL_SIZE + 20, 20))
        
        lines_text = font_small.render(f"Lines: {lines_cleared}", True, WHITE)
        screen.blit(lines_text, (board_x + COLS * CELL_SIZE + 20, 80))
        
        high_score_text = font_small.render(f"High Score: {high_score}", True, GREEN)
        screen.blit(high_score_text, (board_x + COLS * CELL_SIZE + 20, 120))
        
        difficulty_text = font_small.render(f"Difficulty: {current_difficulty}", True, WHITE)
        screen.blit(difficulty_text, (board_x + COLS * CELL_SIZE + 20, 160))
        
        view_text = font_small.render(f"View: {view_mode}", True, WHITE)
        screen.blit(view_text, (board_x + COLS * CELL_SIZE + 20, 200))
        
        # Draw next piece preview
        next_text = font_small.render("Next Piece:", True, WHITE)
        screen.blit(next_text, (board_x + COLS * CELL_SIZE + 20, 260))
        
        next_piece_x = board_x + COLS * CELL_SIZE + 50
        next_piece_y = 300
        draw_next_piece(next_piece, next_piece_x, next_piece_y)
        
        # Controls reminder
        controls_y = HEIGHT - 200
        controls_text = [
            "Controls:",
            "Arrows: Move/Rotate",
            "Space: Hard Drop",
            "WASD: Move Camera",
            "Q/E: Zoom",
            "R: Reset Camera",
            "1-3: Change View",
            "ESC: Pause"
        ]
        
        for line in controls_text:
            text = font_small.render(line, True, WHITE)
            screen.blit(text, (board_x + COLS * CELL_SIZE + 20, controls_y))
            controls_y += 25
        
        # Draw game over or paused overlay
        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.fill(BLACK)
            overlay.set_alpha(180)
            screen.blit(overlay, (0, 0))
            
            game_over_text = font_large.render("GAME OVER", True, RED)
            screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 100))
            
            final_score_text = font_medium.render(f"Final Score: {int(score)}", True, WHITE)
            screen.blit(final_score_text, (WIDTH//2 - final_score_text.get_width()//2, HEIGHT//2))
            
            continue_text = font_small.render("Press ENTER to continue", True, GREEN)
            screen.blit(continue_text, (WIDTH//2 - continue_text.get_width()//2, HEIGHT//2 + 100))
        
        elif paused:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.fill(BLACK)
            overlay.set_alpha(180)
            screen.blit(overlay, (0, 0))
            
            paused_text = font_large.render("PAUSED", True, YELLOW)
            screen.blit(paused_text, (WIDTH//2 - paused_text.get_width()//2, HEIGHT//2 - 50))
            
            continue_text = font_small.render("Press ESC to continue", True, WHITE)
            screen.blit(continue_text, (WIDTH//2 - continue_text.get_width()//2, HEIGHT//2 + 50))
    
    # Update the display
    pygame.display.flip()
    clock.tick(60)  # 60 FPS

# Clean up before exit
pygame.quit()
save_high_score()
sys.exit()