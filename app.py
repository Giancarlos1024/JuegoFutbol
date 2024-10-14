import pygame
import random
import math

# Inicializamos pygame
pygame.init()

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# Dimensiones de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Crear la pantalla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Juego de Fútbol Mejorado con Gráficos Vectoriales")

# Jugador
player_size = 40
player_x = 50  # Posición inicial del jugador
player_y = SCREEN_HEIGHT // 2
player_speed = 5
player_name = "Álvaro"  # Nombre del jugador

# Pelota
ball_size = 20
ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2
ball_speed_x = 0
ball_speed_y = 0
ball_moving = False  # La pelota está en movimiento o no
ball_owned = False   # El jugador tiene la pelota

# Enemigos
num_enemies = 4  # Número inicial de enemigos
enemy_size = 40
enemies = []

# Crear enemigos en posiciones aleatorias
def create_enemies(num):
    enemies = []
    for i in range(num):
        enemy_x = random.randint(200, SCREEN_WIDTH - enemy_size)
        enemy_y = random.randint(0, SCREEN_HEIGHT - enemy_size)
        enemies.append([enemy_x, enemy_y])
    return enemies

enemies = create_enemies(num_enemies)

# Área de gol (meta) en la parte derecha de la pantalla
goal_area_right = pygame.Rect(SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2 - 100, 50, 200)
goal_area_left = pygame.Rect(0, SCREEN_HEIGHT // 2 - 100, 50, 200)

# Porteros (incluyendo compañero)
goalkeeper_size = 50
goalkeeper_x = SCREEN_WIDTH - 60  # El portero enemigo se mueve cerca del área de gol
goalkeeper_y = SCREEN_HEIGHT // 2 - goalkeeper_size // 2
goalkeeper_speed = 5
goalkeeper_direction = 1  # Direcciones: 1 (abajo), -1 (arriba)

# Compañero en el arco
partner_goalkeeper_x = SCREEN_WIDTH - 790  # Posición del compañero
partner_goalkeeper_y = SCREEN_HEIGHT // 2 - goalkeeper_size // 2
partner_name = "Martín"  # Nombre del compañero

# Niveles
level = 1
max_level = 3
goals_player = 0
goals_enemy = 0
goals_to_win = 3  # Goles necesarios para pasar al siguiente nivel

# Tiempo por nivel
time_limit = 60  # 60 segundos por nivel
start_time = pygame.time.get_ticks()  # Guardar el tiempo de inicio

# Puntaje total
total_score = 0

# Función para mover al jugador
def move_player(keys, x, y, speed):
    if keys[pygame.K_LEFT]:
        x -= speed
    if keys[pygame.K_RIGHT]:
        x += speed
    if keys[pygame.K_UP]:
        y -= speed
    if keys[pygame.K_DOWN]:
        y += speed
    # Limitar movimiento dentro de la pantalla
    x = max(0, min(SCREEN_WIDTH - player_size, x))
    y = max(0, min(SCREEN_HEIGHT - player_size, y))
    return x, y

# Función para mover enemigos hacia el jugador
def move_enemies(player_x, player_y, enemies, speed):
    for enemy in enemies:
        direction_x = player_x - enemy[0]
        direction_y = player_y - enemy[1]
        distance = math.sqrt(direction_x ** 2 + direction_y ** 2)
        if distance > 0:
            enemy[0] += (direction_x / distance) * speed
            enemy[1] += (direction_y / distance) * speed

# Verificar si el jugador está cerca de la pelota
def check_ball_possession(player_x, player_y, ball_x, ball_y, distance=30):
    dx = player_x - ball_x
    dy = player_y - ball_y
    return math.sqrt(dx**2 + dy**2) < distance

# Verificar si un enemigo roba la pelota
def check_enemy_steal(player_x, player_y, enemies, ball_owned):
    if ball_owned:
        for enemy in enemies:
            if check_ball_possession(enemy[0], enemy[1], player_x, player_y, distance=30):
                return True, enemy[0], enemy[1]  # El enemigo roba la pelota
    return False, None, None

# Función para disparar la pelota
def shoot_ball(player_x, player_y):
    direction_x = SCREEN_WIDTH - player_x
    direction_y = random.choice([-1, 1]) * 3  # Movimiento aleatorio hacia arriba o abajo
    distance = math.sqrt(direction_x ** 2 + direction_y ** 2)
    return (direction_x / distance) * 10, (direction_y / distance) * 10  # Velocidad de disparo

# Función para mover el portero
def move_goalkeeper(y, speed, direction):
    y += speed * direction
    if y <= SCREEN_HEIGHT // 2 - 100 or y >= SCREEN_HEIGHT // 2 + 100 - goalkeeper_size:
        direction *= -1  # Cambiar la dirección cuando toca los límites del área de gol
    return y, direction

# Dibujar gráficos vectoriales
def draw_player(x, y):
    pygame.draw.circle(screen, RED, (x + player_size // 2, y + player_size // 2), player_size // 2)

def draw_ball(x, y):
    pygame.draw.circle(screen, BLACK, (x + ball_size // 2, y + ball_size // 2), ball_size // 2)

def draw_enemy(x, y):
    pygame.draw.rect(screen, BLUE, (x, y, enemy_size, enemy_size))

def draw_goalkeeper(x, y):
    pygame.draw.rect(screen, RED, (x, y, goalkeeper_size, goalkeeper_size))  # Cambiado a rojo

# Función para dibujar el puntaje y el tiempo
def draw_score_and_time(score_player, score_enemy, time_left):
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Puntaje Jugador: {score_player}  |  Puntaje Enemigos: {score_enemy}", True, BLACK)
    time_text = font.render(f"Tiempo: {time_left}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(time_text, (SCREEN_WIDTH - 250, 10))

# Mensaje de nivel
def display_message(text):
    font = pygame.font.SysFont(None, 48)
    message = font.render(text, True, BLACK)
    screen.blit(message, (SCREEN_WIDTH // 2 - message.get_width() // 2, SCREEN_HEIGHT // 2 - message.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(2000)  # Esperar 2 segundos para que el jugador vea el mensaje

# Función para dibujar los nombres de los jugadores
def draw_names():
    font = pygame.font.SysFont(None, 24)
    player_name_text = font.render(player_name, True, BLACK)
    partner_name_text = font.render(partner_name, True, BLACK)
    goalkeeper_name_text = font.render("Courtois", True, BLACK)
    screen.blit(player_name_text, (player_x, player_y - 20))
    screen.blit(partner_name_text, (partner_goalkeeper_x, partner_goalkeeper_y - 20))
    screen.blit(goalkeeper_name_text, (goalkeeper_x, goalkeeper_y - 20))

# Bucle principal del juego
running = True
clock = pygame.time.Clock()

while running:
    # Manejar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Detectar teclas presionadas
    keys = pygame.key.get_pressed()

    # Mover al jugador
    player_x, player_y = move_player(keys, player_x, player_y, player_speed)

    # Mover a los enemigos
    move_enemies(player_x, player_y, enemies, level + 1)

    # Verificar si el jugador está cerca de la pelota
    if check_ball_possession(player_x, player_y, ball_x, ball_y) and not ball_moving:
        ball_owned = True  # El jugador tiene la pelota

    # Verificar si un enemigo roba la pelota
    enemy_steals, new_ball_x, new_ball_y = check_enemy_steal(player_x, player_y, enemies, ball_owned)
    if enemy_steals:
        ball_owned = False  # El enemigo roba la pelota
        ball_x = new_ball_x
        ball_y = new_ball_y
        ball_speed_x = 0
        ball_speed_y = 0

    # Si el jugador tiene la pelota, la pelota sigue al jugador
    if ball_owned:
        ball_x = player_x + player_size // 2
        ball_y = player_y + player_size // 2

    # Si el jugador presiona espacio, dispara la pelota
    if keys[pygame.K_SPACE] and ball_owned:
        ball_speed_x, ball_speed_y = shoot_ball(player_x, player_y)
        ball_moving = True
        ball_owned = False  # El jugador ya no tiene la pelota

    # Mover la pelota si está en movimiento
    if ball_moving:
        ball_x += ball_speed_x
        ball_y += ball_speed_y
        # Verificar si la pelota sale de la pantalla
        if ball_x < 0 or ball_x > SCREEN_WIDTH:
            ball_moving = False  # La pelota deja de moverse
            ball_x = SCREEN_WIDTH // 2
            ball_y = SCREEN_HEIGHT // 2

    # Mover el portero enemigo
    goalkeeper_y, goalkeeper_direction = move_goalkeeper(goalkeeper_y, goalkeeper_speed, goalkeeper_direction)

    # Verificar si el jugador marca un gol
    if ball_x >= goal_area_right.left and goal_area_right.top < ball_y < goal_area_right.bottom:
        goals_player += 1
        total_score += 1
        ball_x = SCREEN_WIDTH // 2
        ball_y = SCREEN_HEIGHT // 2
        ball_moving = False
        ball_owned = False  # El jugador no tiene la pelota después de marcar
        if goals_player >= goals_to_win:
            level += 1
            if level > max_level:
                display_message("¡Has ganado el juego!")
                running = False
            else:
                goals_player = 0
                display_message(f"¡Has pasado al nivel {level}!")

    # Verificar si el portero detiene la pelota
    if ball_x >= goalkeeper_x and goalkeeper_y < ball_y < goalkeeper_y + goalkeeper_size:
        ball_moving = False  # La pelota deja de moverse
        ball_x = SCREEN_WIDTH // 2
        ball_y = SCREEN_HEIGHT // 2

    # Verificar el tiempo
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
    time_left = max(0, time_limit - elapsed_time)

    if time_left <= 0:
        goals_enemy += 1
        ball_x = SCREEN_WIDTH // 2
        ball_y = SCREEN_HEIGHT // 2
        ball_moving = False
        ball_owned = False  # El jugador no tiene la pelota después de marcar

        if goals_enemy >= 3:  # Si los enemigos marcan 3 goles
            display_message("¡Has perdido el juego!")
            running = False
        else:
            start_time = pygame.time.get_ticks()  # Reiniciar el tiempo

    # Dibujar en la pantalla
    screen.fill(WHITE)
    draw_player(player_x, player_y)
    draw_ball(ball_x, ball_y)
    draw_goalkeeper(goalkeeper_x, goalkeeper_y)
    draw_goalkeeper(partner_goalkeeper_x, partner_goalkeeper_y)  # Dibujar compañero

    for enemy in enemies:
        draw_enemy(enemy[0], enemy[1])

    # Dibujar los arcos
    pygame.draw.rect(screen, YELLOW, goal_area_right, 2)
    pygame.draw.rect(screen, YELLOW, goal_area_left, 2)

    # Dibujar el puntaje y el tiempo
    draw_score_and_time(goals_player, goals_enemy, int(time_left))

    # Dibujar nombres de los jugadores
    draw_names()

    # Actualizar la pantalla
    pygame.display.flip()
    clock.tick(60)  # Limitar a 60 FPS

# Cerrar pygame
pygame.quit()
