import pygame
import math
import os
import random

# Setting buffer audio aman & ringan
pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.init()
pygame.mixer.init()

# Channel Audio Khusus
shoot_channel = pygame.mixer.Channel(0)
damage_channel = pygame.mixer.Channel(1)
turret_channel = pygame.mixer.Channel(2)

# Resolusi Layar Samsung Galaxy M53 5G
SCREEN_WIDTH = 2400
SCREEN_HEIGHT = 1080

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Zidan - Chest & Turret Edition")

font = pygame.font.SysFont("sans-serif", 45)
font_small = pygame.font.SysFont("sans-serif", 35)
font_name = pygame.font.SysFont("sans-serif", 45, bold=True)
font_large = pygame.font.SysFont("sans-serif", 100)

FOLDER_PATH = "/storage/emulated/0/Gameyuika"
DOWNLOAD_PATH = "/storage/emulated/0/Download"

def load_image_alpha_safe(filename, size):
    paths_to_check = [
        os.path.join(FOLDER_PATH, filename),
        os.path.join(DOWNLOAD_PATH, filename),
        filename,
        os.path.join(os.getcwd(), filename)
    ]
    for p in paths_to_check:
        if os.path.exists(p):
            try:
                img = pygame.image.load(p).convert_alpha()
                return pygame.transform.scale(img, size)
            except Exception:
                pass
    return None

# --- LOAD EFEK SUARA AMAN ---
shoot_sound = None
for s_file in ["sound tembakan.mp3", "shoot.mp3", "sound_tembakan.mp3"]:
    s_path = os.path.join(FOLDER_PATH, s_file)
    if not os.path.exists(s_path): s_path = os.path.join(DOWNLOAD_PATH, s_file)
    if os.path.exists(s_path):
        try:
            shoot_sound = pygame.mixer.Sound(s_path)
            break
        except Exception: pass

damage_sound = None
for d_file in ["sound pas kena damage.mp3", "sound_mati.mp3", "mati.mp3"]:
    d_path = os.path.join(FOLDER_PATH, d_file)
    if not os.path.exists(d_path): d_path = os.path.join(DOWNLOAD_PATH, d_file)
    if os.path.exists(d_path):
        try:
            damage_sound = pygame.mixer.Sound(d_path)
            break
        except Exception: pass

turret_sound = None
for t_file in ["sound listrik.mp3", "listrik.mp3"]:
    t_path = os.path.join(DOWNLOAD_PATH, t_file)
    if not os.path.exists(t_path): t_path = os.path.join(FOLDER_PATH, t_file)
    if os.path.exists(t_path):
        try:
            turret_sound = pygame.mixer.Sound(t_path)
            break
        except Exception: pass

# --- LOAD ANIMASI IDLE YUIKA ---
yuika_idle_right, yuika_idle_left = [], []
idle_files = [
    "Tak berjudul17_20261018152939.png",
    "Tak berjudul17_20261018152941.png",
    "Tak berjudul17_20261018152943.png",
    "Tak berjudul17_20261018152938.png",
    "Tak berjudul17_20261018152945.png",
    "Tak berjudul17_20261018152948.png"
]
for file in idle_files:
    img = load_image_alpha_safe(file, (220, 220))
    if img:
        yuika_idle_right.append(img)
        yuika_idle_left.append(pygame.transform.flip(img, True, False))

if not yuika_idle_right:
    fallback_idle = load_image_alpha_safe("23470-removebg-preview.png", (220, 220))
    if fallback_img := fallback_idle:
        yuika_idle_right.append(fallback_idle)
        yuika_idle_left.append(pygame.transform.flip(fallback_idle, True, False))

# 1. Load Frame Animasi Berjalan (Yuika)
yuika_walk_right, yuika_walk_left = [], []
for file in ["23470-removebg-preview.png", "23471-removebg-preview.png", "23472-removebg-preview.png", "23473-removebg-preview.png"]:
    img = load_image_alpha_safe(file, (220, 220))
    if img:
        yuika_walk_right.append(img)
        yuika_walk_left.append(pygame.transform.flip(img, True, False))

# 2. Load Frame Animasi Nembak (Pistol)
yuika_shoot_right, yuika_shoot_left = [], []
for file in ["23820-removebg-preview.png", "23821-removebg-preview.png", "23822-removebg-preview.png", "23823-removebg-preview.png", "23824-removebg-preview.png", "23825-removebg-preview.png"]:
    img = load_image_alpha_safe(file, (220, 220))
    if img:
        yuika_shoot_right.append(img)
        yuika_shoot_left.append(pygame.transform.flip(img, True, False))

# 3. Load Gambar Lempar Bom
bomb_pose_img = load_image_alpha_safe("Tak berjudul10_20261016214846.png", (220, 220))
yuika_bomb_right = [bomb_pose_img] if bomb_pose_img else yuika_walk_right
yuika_bomb_left = [pygame.transform.flip(bomb_pose_img, True, False)] if bomb_pose_img else yuika_walk_left

# 4. Load Frame Animasi Loncat
yuika_jump_right, yuika_jump_left = [], []
for file in ["23916-removebg-preview.png", "23917-removebg-preview.png", "23918-removebg-preview.png", "23919-removebg-preview.png", "23920-removebg-preview.png", "23921-removebg-preview.png"]:
    img = load_image_alpha_safe(file, (220, 220))
    if img:
        yuika_jump_right.append(img)
        yuika_jump_left.append(pygame.transform.flip(img, True, False))

if not yuika_walk_right:
    fallback_img = load_image_alpha_safe("Yuika Saionji.png", (220, 220)) or load_image_alpha_safe("yuika.png", (220, 220))
    if fallback_img:
        yuika_walk_right.append(fallback_img)
        yuika_walk_left.append(pygame.transform.flip(fallback_img, True, False))

if not yuika_shoot_right: yuika_shoot_right, yuika_shoot_left = yuika_walk_right, yuika_walk_left
if not yuika_jump_right: yuika_jump_right, yuika_jump_left = yuika_walk_right, yuika_walk_left

hud_avatar = load_image_alpha_safe("23470-removebg-preview.png", (90, 90))
if hud_avatar is None:
    hud_avatar = yuika_walk_right[0] if yuika_walk_right else None

# --- 5. LOAD ANIMASI BERJALAN MONSTER ---
monster_walk_right, monster_walk_left = [], []
walk_monster_files = [
    "Tak berjudul12_20261017054143.png",
    "Tak berjudul12_20261017054145.png",
    "Tak berjudul12_20261017054147.png",
    "Tak berjudul12_20261017054149.png",
    "Tak berjudul12_20261017054154.png"
]
for m_file in walk_monster_files:
    m_img = load_image_alpha_safe(m_file, (220, 220))
    if m_img:
        monster_walk_right.append(m_img)
        monster_walk_left.append(pygame.transform.flip(m_img, True, False))

if not monster_walk_right:
    fallback_monster = load_image_alpha_safe("tengkorak.png", (220, 220))
    if fallback_monster:
        monster_walk_right.append(fallback_monster)
        monster_walk_left.append(pygame.transform.flip(fallback_monster, True, False))

# --- 6. LOAD GAMBAR TURRET & CHEST (PETI) ---
electric_turret_img = load_image_alpha_safe("Tak berjudul15_20261018061953.png", (160, 160))
if electric_turret_img is None:
    electric_turret_img = load_image_alpha_safe("26371-removebg-preview.png", (160, 160))

# Load Gambar Peti Harta (27039-removebg-preview.png)
chest_img = load_image_alpha_safe("27039-removebg-preview.png", (140, 140))

# --- 7. LOAD GAMBAR ITEM / POTION ---
item_def = load_image_alpha_safe("26387-removebg-preview (1).png", (80, 80))
item_atk = load_image_alpha_safe("26388-removebg-preview (1).png", (80, 80))
item_immune = load_image_alpha_safe("26389-removebg-preview (1).png", (80, 80))

# Posisi Karakter & Status Game
world_x = 2000
y = 850
ground_y = 850
y_velocity = 0
is_jumping = False
gravity = 1.2
jump_strength = -24

radius = 50
speed = 14
max_health = 100
health = 100

max_stamina = 100
stamina = 100
stamina_regen_timer = 0

world_width = 20000

current_frame = 0
anim_speed = 0.15
facing_right = True

is_shooting_anim = False
shoot_anim_timer = 0
is_bomb_anim = False
bomb_anim_timer = 0

is_inventory_open = False
inventory_items = []
dropped_items = []

active_buff_text = ""
buff_timer = 0

bullets = []
bullet_speed = 25

bombs = []
bomb_speed = 12

active_beams = []

# List Turret Musuh (y = 730)
turrets = [
    {'x': 1800, 'y': 730, 'max_hp': 12, 'hp': 12, 'cooldown': 0, 'facing': 'left'},
    {'x': 5000, 'y': 730, 'max_hp': 12, 'hp': 12, 'cooldown': 0, 'facing': 'left'},
    {'x': 9000, 'y': 730, 'max_hp': 12, 'hp': 12, 'cooldown': 0, 'facing': 'left'},
    {'x': 14000, 'y': 730, 'max_hp': 12, 'hp': 12, 'cooldown': 0, 'facing': 'left'},
]

# List Peti Harta (Chest) di Map (y = 740 agar menapak di tanah)
chests = [
    {'x': 3200, 'y': 740, 'max_hp': 8, 'hp': 8},
    {'x': 7500, 'y': 740, 'max_hp': 8, 'hp': 8},
    {'x': 11500, 'y': 740, 'max_hp': 8, 'hp': 8},
    {'x': 17000, 'y': 740, 'max_hp': 8, 'hp': 8},
]

enemies = []
enemy_w, enemy_h = 220, 220
enemy_bullets = []
enemy_bullet_speed = 14

def spawn_enemy():
    enemies.append({
        'x': random.randint(1000, 19000),
        'y': 780,
        'max_hp': 5,
        'hp': 5,
        'speed': random.randint(4, 7),
        'stamina': 100,
        'max_stamina': 100,
        'tired_timer': 0,
        'anim_frame': random.uniform(0, 5),
        'shoot_timer': 0,
        'shoot_interval': random.randint(120, 200)
    })

for _ in range(6):
    spawn_enemy()

start_ticks = pygame.time.get_ticks()

joystick_center = (300, 800)
joystick_bg_radius = 150
joystick_knob_radius = 65
joystick_knob_pos = list(joystick_center)
is_joystick_active = False

btn_reset = pygame.Rect(1100, 750, 420, 140)
btn_jump = pygame.Rect(1350, 720, 180, 180)
btn_shoot = pygame.Rect(1600, 680, 200, 200)
btn_bomb = pygame.Rect(1850, 680, 200, 200)
btn_bag = pygame.Rect(520, 25, 140, 85)

btn_use_item = pygame.Rect(850, 800, 220, 70)
btn_drop_item = pygame.Rect(1130, 800, 220, 70)
selected_slot = None

running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)
    current_ticks = pygame.time.get_ticks()
    elapsed_seconds = (current_ticks - start_ticks) // 1000

    if buff_timer > 0:
        buff_timer -= 1
        if buff_timer == 0:
            active_buff_text = ""

    stamina_regen_timer += 1
    if stamina_regen_timer >= 180:
        stamina = max_stamina
        stamina_regen_timer = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            
            if btn_bag.collidepoint(pos) and health > 0:
                is_inventory_open = not is_inventory_open
                selected_slot = None
                continue

            if is_inventory_open:
                if btn_use_item.collidepoint(pos) and selected_slot is not None:
                    if selected_slot < len(inventory_items):
                        used_type = inventory_items.pop(selected_slot)
                        if used_type == 'def':
                            active_buff_text = "DEF + 5 DETIK AKTIF!"
                        elif used_type == 'atk':
                            active_buff_text = "ATK SPD + 20 DETIK AKTIF!"
                        elif used_type == 'immune':
                            active_buff_text = "IMMUNE SERANGAN AKTIF!"
                        buff_timer = 300
                        selected_slot = None
                    continue

                if btn_drop_item.collidepoint(pos) and selected_slot is not None:
                    if selected_slot < len(inventory_items):
                        dropped_type = inventory_items.pop(selected_slot)
                        dropped_items.append({'x': world_x, 'y': 800, 'type': dropped_type})
                        selected_slot = None
                    continue

                slot_size = 110
                start_x = 600 + 175
                start_y = 180 + 150
                slot_idx = 0
                clicked_slot = None
                for row in range(3):
                    for col in range(4):
                        sx = start_x + col * (slot_size + 30)
                        sy = start_y + row * (slot_size + 30)
                        slot_rect = pygame.Rect(sx, sy, slot_size, slot_size)
                        if slot_rect.collidepoint(pos):
                            clicked_slot = slot_idx
                        slot_idx += 1
                if clicked_slot is not None:
                    selected_slot = clicked_slot if clicked_slot < len(inventory_items) else None
                continue

            camera_x = world_x - SCREEN_WIDTH // 3
            clicked_item = None
            for item in dropped_items:
                screen_item_x = item['x'] - camera_x
                item_rect = pygame.Rect(screen_item_x, item['y'], 80, 80)
                if item_rect.collidepoint(pos):
                    clicked_item = item
                    break
            if clicked_item:
                if len(inventory_items) < 12:
                    inventory_items.append(clicked_item['type'])
                    dropped_items.remove(clicked_item)
                continue

            dx = pos[0] - joystick_center[0]
            dy = pos[1] - joystick_center[1]
            if math.hypot(dx, dy) <= joystick_bg_radius:
                is_joystick_active = True
            
            if btn_shoot.collidepoint(pos) and health > 0:
                if stamina >= 20:
                    b_dx = bullet_speed if facing_right else -bullet_speed
                    bullets.append({'x': world_x + (radius if facing_right else -radius), 'y': y - 12, 'dx': b_dx})
                    stamina -= 20
                    is_shooting_anim = True
                    is_bomb_anim = False
                    shoot_anim_timer = 25
                    current_frame = 0
                    if shoot_sound:
                        shoot_channel.stop()
                        shoot_channel.play(shoot_sound)
                        shoot_channel.fadeout(300)

            if btn_bomb.collidepoint(pos) and health > 0:
                if stamina >= 40:
                    b_dx = bomb_speed if facing_right else -bomb_speed
                    bombs.append({'x': world_x, 'y': y - 40, 'dx': b_dx, 'dy': -10})
                    is_bomb_anim = True
                    is_shooting_anim = False
                    bomb_anim_timer = 30
                    current_frame = 0
            
            if btn_jump.collidepoint(pos) and health > 0 and not is_jumping:
                is_jumping = True
                y_velocity = jump_strength
                current_frame = 0

            if btn_reset.collidepoint(pos) and health <= 0:
                health = 100
                stamina = 100
                world_x = 2000
                y = 850
                is_jumping = False
                y_velocity = 0
                bullets.clear()
                bombs.clear()
                enemy_bullets.clear()
                active_beams.clear()
                dropped_items.clear()
                inventory_items.clear()
                enemies.clear()
                is_inventory_open = False
                selected_slot = None
                for t in turrets: t['hp'] = t['max_hp']
                for c in chests: c['hp'] = c['max_hp']
                for _ in range(6): spawn_enemy()
                start_ticks = pygame.time.get_ticks()
                
        elif event.type == pygame.MOUSEBUTTONUP:
            is_joystick_active = False
            joystick_knob_pos = list(joystick_center)

    is_moving = False
    if is_joystick_active and health > 0 and not is_inventory_open:
        mouse_pos = pygame.mouse.get_pos()
        dx = mouse_pos[0] - joystick_center[0]
        dy = mouse_pos[1] - joystick_center[1]
        distance = math.hypot(dx, dy)
        
        if distance > joystick_bg_radius:
            angle = math.atan2(dy, dx)
            joystick_knob_pos[0] = joystick_center[0] + int(math.cos(angle) * joystick_bg_radius)
            joystick_knob_pos[1] = joystick_center[1] + int(math.sin(angle) * joystick_bg_radius)
        else:
            joystick_knob_pos = list(mouse_pos)
            
        if distance > 10:
            norm_dx = dx / (distance if distance > joystick_bg_radius else joystick_bg_radius)
            world_x += norm_dx * speed
            is_moving = True
            
            if norm_dx > 0: facing_right = True
            elif norm_dx < 0: facing_right = False

    if is_jumping:
        y += y_velocity
        y_velocity += gravity
        if y >= ground_y:
            y = ground_y
            is_jumping = False
            y_velocity = 0

    if is_jumping:
        current_frame += anim_speed
        frames = yuika_jump_right if facing_right else yuika_jump_left
        if current_frame >= len(frames): current_frame = len(frames) - 1
    elif is_bomb_anim:
        bomb_anim_timer -= 1
        current_frame += anim_speed
        frames = yuika_bomb_right if facing_right else yuika_bomb_left
        if current_frame >= len(frames): current_frame = 0
        if bomb_anim_timer <= 0: is_bomb_anim = False
    elif is_shooting_anim:
        shoot_anim_timer -= 1
        current_frame += anim_speed
        frames = yuika_shoot_right if facing_right else yuika_shoot_left
        if current_frame >= len(frames): current_frame = 0
        if shoot_anim_timer <= 0: is_shooting_anim = False
    elif is_moving:
        frames = yuika_walk_right if facing_right else yuika_walk_left
        current_frame += anim_speed
        if current_frame >= len(frames): current_frame = 0
    else:
        current_frame += anim_speed
        frames = yuika_idle_right if facing_right else yuika_idle_left
        if current_frame >= len(frames): current_frame = 0

    if world_x < 0:
        world_x = world_width
    elif world_x > world_width:
        world_x = 0

    player_rect = pygame.Rect(int(world_x - radius), int(y - radius), radius * 2, radius * 2)
    camera_x = world_x - SCREEN_WIDTH // 3

    active_beams.clear()
    turret_fired_this_frame = False

    for turret in turrets:
        if turret['hp'] > 0:
            if world_x > turret['x']:
                turret['facing'] = 'right'
            else:
                turret['facing'] = 'left'

            dist_to_player = abs(turret['x'] - world_x)
            if dist_to_player < 1400:
                turret['cooldown'] += 1
                if turret['cooldown'] >= 50:
                    l_x = turret['x'] + (130 if turret['facing'] == 'right' else 30)
                    l_y = turret['y'] + 65
                    target_x = world_x
                    target_y = y - 10

                    active_beams.append({'start_x': l_x, 'start_y': l_y, 'end_x': target_x, 'end_y': target_y})
                    turret_fired_this_frame = True

                    if health > 0 and "IMMUNE" not in active_buff_text:
                        health -= 6
                        if health < 0: health = 0
                        if damage_sound:
                            damage_channel.stop()
                            damage_channel.play(damage_sound)

                    turret['cooldown'] = 0

    if turret_fired_this_frame and turret_sound:
        if not turret_channel.get_busy():
            turret_channel.play(turret_sound)

    if health > 0 and not is_inventory_open:
        for enemy in enemies:
            if enemy['tired_timer'] > 0:
                enemy['tired_timer'] -= 1
                if enemy['tired_timer'] == 0:
                    enemy['stamina'] = enemy['max_stamina']
                continue

            if enemy['x'] < world_x:
                enemy['x'] += enemy['speed']
            elif enemy['x'] > world_x:
                enemy['x'] -= enemy['speed']

            enemy['stamina'] -= 0.35
            if enemy['stamina'] <= 0:
                enemy['tired_timer'] = 120

            enemy['anim_frame'] += anim_speed

            enemy['shoot_timer'] += 1
            if enemy['shoot_timer'] >= enemy['shoot_interval'] and enemy['tired_timer'] == 0:
                e_dx = -enemy_bullet_speed if enemy['x'] > world_x else enemy_bullet_speed
                enemy_bullets.append({'x': enemy['x'], 'y': enemy['y'] + 60, 'dx': e_dx})
                enemy['shoot_timer'] = 0
                enemy['shoot_interval'] = random.randint(120, 200)

    for e_bullet in enemy_bullets[:]:
        e_bullet['x'] += e_bullet['dx']
        e_bullet_rect = pygame.Rect(e_bullet['x'], e_bullet['y'], 50, 30)
        if health > 0 and e_bullet_rect.colliderect(player_rect):
            if "IMMUNE" not in active_buff_text:
                health -= 6
                if health < 0: health = 0
                if damage_sound:
                    damage_channel.stop()
                    damage_channel.play(damage_sound)
            enemy_bullets.remove(e_bullet)
            continue
        if abs(e_bullet['x'] - world_x) > SCREEN_WIDTH:
            enemy_bullets.remove(e_bullet)

    for bullet in bullets[:]:
        bullet['x'] += bullet['dx']
        bullet_rect = pygame.Rect(int(bullet['x']), int(bullet['y']), 40, 20)
        bullet_hit = False
        
        for enemy in enemies:
            enemy_rect = pygame.Rect(enemy['x'], enemy['y'], enemy_w, enemy_h)
            if bullet_rect.colliderect(enemy_rect):
                damage = 2 if "ATK SPD" in active_buff_text else 1
                enemy['hp'] -= damage
                bullet_hit = True
                break

        if not bullet_hit:
            for turret in turrets:
                if turret['hp'] > 0:
                    t_rect = pygame.Rect(turret['x'], turret['y'], 160, 160)
                    if bullet_rect.colliderect(t_rect):
                        damage = 2 if "ATK SPD" in active_buff_text else 1
                        turret['hp'] -= damage
                        bullet_hit = True
                        break

        if not bullet_hit:
            for chest in chests:
                if chest['hp'] > 0:
                    c_rect = pygame.Rect(chest['x'], chest['y'], 140, 140)
                    if bullet_rect.colliderect(c_rect):
                        damage = 2 if "ATK SPD" in active_buff_text else 1
                        chest['hp'] -= damage
                        bullet_hit = True
                        break
        
        if bullet_hit:
            bullets.remove(bullet)
            continue
        if abs(bullet['x'] - world_x) > SCREEN_WIDTH:
            bullets.remove(bullet)

    for bomb in bombs[:]:
        bomb['x'] += bomb['dx']
        bomb['y'] += bomb['dy']
        bomb['dy'] += 0.5
        
        if bomb['y'] >= ground_y:
            bomb_rect = pygame.Rect(int(bomb['x'] - 30), int(ground_y - 30), 60, 60)
            for enemy in enemies:
                enemy_rect = pygame.Rect(enemy['x'], enemy['y'], enemy_w, enemy_h)
                if bomb_rect.colliderect(enemy_rect):
                    enemy['hp'] -= 3
            for turret in turrets:
                if turret['hp'] > 0:
                    t_rect = pygame.Rect(turret['x'], turret['y'], 160, 160)
                    if bomb_rect.colliderect(t_rect):
                        turret['hp'] -= 3
            for chest in chests:
                if chest['hp'] > 0:
                    c_rect = pygame.Rect(chest['x'], chest['y'], 140, 140)
                    if bomb_rect.colliderect(c_rect):
                        chest['hp'] -= 3
            bombs.remove(bomb)
            continue
        if abs(bomb['x'] - world_x) > SCREEN_WIDTH:
            bombs.remove(bomb)

    for enemy in enemies:
        if enemy['hp'] <= 0:
            item_type = random.choice(['def', 'atk', 'immune'])
            dropped_items.append({'x': enemy['x'] + 50, 'y': 800, 'type': item_type})

    for turret in turrets:
        if turret['hp'] <= 0 and turret['hp'] != -999:
            item_type = random.choice(['def', 'atk', 'immune'])
            dropped_items.append({'x': turret['x'] + 80, 'y': 800, 'type': item_type})
            turret['hp'] = -999

    # Ketika Peti Harta (Chest) Hancur, Keluarkan Item Ramuan!
    for chest in chests:
        if chest['hp'] <= 0 and chest['hp'] != -999:
            item_type = random.choice(['def', 'atk', 'immune'])
            dropped_items.append({'x': chest['x'] + 40, 'y': 800, 'type': item_type})
            chest['hp'] = -999

    enemies = [e for e in enemies if e['hp'] > 0]
    if len(enemies) < 5 and health > 0: spawn_enemy()

    if health > 0 and not is_inventory_open:
        for enemy in enemies:
            enemy_rect = pygame.Rect(enemy['x'], enemy['y'], enemy_w, enemy_h)
            if player_rect.colliderect(enemy_rect):
                if "IMMUNE" not in active_buff_text:
                    dmg = 1 if "DEF" not in active_buff_text else 0
                    health -= dmg
                    if health < 0: health = 0
                    if damage_sound and health % 20 == 0:
                        damage_channel.stop()
                        damage_channel.play(damage_sound)

    # --- RENDER GRAFIS ---
    screen.fill((135, 206, 235))

    mountain_offset = int(camera_x * 0.3) % SCREEN_WIDTH
    pygame.draw.polygon(screen, (100, 160, 210), [(0 - mountain_offset, 850), (400 - mountain_offset, 450), (800 - mountain_offset, 850)])
    pygame.draw.polygon(screen, (90, 150, 200), [(700 - mountain_offset, 850), (1200 - mountain_offset, 380), (1700 - mountain_offset, 850)])

    pygame.draw.rect(screen, (74, 160, 44), (0, 850, SCREEN_WIDTH, 230))
    pygame.draw.rect(screen, (160, 110, 60), (0, 930, SCREEN_WIDTH, 150))

    # Render Peti Harta (Chest) + HP Bar Peti
    for chest in chests:
        if chest['hp'] > 0:
            screen_c_x = chest['x'] - camera_x
            if -250 <= screen_c_x <= SCREEN_WIDTH + 250:
                if chest_img:
                    screen.blit(chest_img, (int(screen_c_x), int(chest['y'])))
                else:
                    pygame.draw.rect(screen, (150, 90, 40), (int(screen_c_x), int(chest['y']), 140, 140), border_radius=15)
                
                c_bar_w = 100
                c_bar_h = 10
                c_bar_x = int(screen_c_x + 70 - (c_bar_w // 2))
                c_bar_y = int(chest['y'] - 20)
                
                pygame.draw.rect(screen, (0, 0, 0), (c_bar_x - 2, c_bar_y - 2, c_bar_w + 4, c_bar_h + 4), border_radius=3)
                pygame.draw.rect(screen, (100, 0, 0), (c_bar_x, c_bar_y, c_bar_w, c_bar_h), border_radius=2)
                c_current_bar_w = int(c_bar_w * (chest['hp'] / chest['max_hp']))
                if c_current_bar_w > 0:
                    pygame.draw.rect(screen, (255, 215, 0), (c_bar_x, c_bar_y, c_current_bar_w, c_bar_h), border_radius=2)

    # Render Turret Listrik Musuh
    for turret in turrets:
        if turret['hp'] > 0:
            screen_t_x = turret['x'] - camera_x
            if -250 <= screen_t_x <= SCREEN_WIDTH + 250:
                if electric_turret_img:
                    draw_t_img = electric_turret_img if turret['facing'] == 'right' else pygame.transform.flip(electric_turret_img, True, False)
                    screen.blit(draw_t_img, (int(screen_t_x), int(turret['y'])))
                else:
                    pygame.draw.rect(screen, (70, 70, 90), (int(screen_t_x), int(turret['y']), 160, 160), border_radius=15)
                
                t_bar_w = 110
                t_bar_h = 12
                t_bar_x = int(screen_t_x + 80 - (t_bar_w // 2))
                t_bar_y = int(turret['y'] - 20)
                
                pygame.draw.rect(screen, (0, 0, 0), (t_bar_x - 2, t_bar_y - 2, t_bar_w + 4, t_bar_h + 4), border_radius=3)
                pygame.draw.rect(screen, (100, 0, 0), (t_bar_x, t_bar_y, t_bar_w, t_bar_h), border_radius=2)
                t_current_bar_w = int(t_bar_w * (turret['hp'] / turret['max_hp']))
                if t_current_bar_w > 0:
                    pygame.draw.rect(screen, (220, 0, 0), (t_bar_x, t_bar_y, t_current_bar_w, t_bar_h), border_radius=2)

    # Render Sambungan Laser Petir
    for beam in active_beams:
        screen_start_x = beam['start_x'] - camera_x
        screen_start_y = beam['start_y']
        screen_end_x = beam['end_x'] - camera_x
        screen_end_y = beam['end_y']

        pygame.draw.line(screen, (0, 150, 255), (screen_start_x, screen_start_y), (screen_end_x, screen_end_y), 14)
        pygame.draw.line(screen, (255, 255, 255), (screen_start_x, screen_start_y), (screen_end_x, screen_end_y), 6)

    for item in dropped_items:
        screen_item_x = item['x'] - camera_x
        if -100 <= screen_item_x <= SCREEN_WIDTH + 100:
            img_to_draw = item_def if item['type'] == 'def' else (item_atk if item['type'] == 'atk' else item_immune)
            if img_to_draw:
                screen.blit(img_to_draw, (int(screen_item_x), int(item['y'])))
            else:
                pygame.draw.circle(screen, (255, 215, 0), (int(screen_item_x) + 40, int(item['y']) + 40), 30)

    for bullet in bullets:
        screen_bullet_x = bullet['x'] - camera_x
        pygame.draw.rect(screen, (255, 230, 0), (int(screen_bullet_x), int(bullet['y']), 40, 20), border_radius=6)

    for bomb in bombs:
        screen_bomb_x = bomb['x'] - camera_x
        pygame.draw.circle(screen, (30, 30, 30), (int(screen_bomb_x), int(bomb['y'])), 15)
        pygame.draw.circle(screen, (255, 100, 0), (int(screen_bomb_x) + 5, int(bomb['y']) - 5), 4)

    for e_bullet in enemy_bullets:
        screen_ebullet_x = e_bullet['x'] - camera_x
        pygame.draw.rect(screen, (100, 200, 255), (int(screen_ebullet_x), int(e_bullet['y']), 50, 20), border_radius=6)

    for enemy in enemies:
        screen_enemy_x = enemy['x'] - camera_x
        if -200 <= screen_enemy_x <= SCREEN_WIDTH + 200:
            is_facing_right_enemy = enemy['x'] < world_x
            m_frames = monster_walk_right if is_facing_right_enemy else monster_walk_left
            
            if m_frames:
                m_idx = int(enemy['anim_frame']) % len(m_frames)
                screen.blit(m_frames[m_idx], (int(screen_enemy_x), int(enemy['y'])))
            else:
                pygame.draw.rect(screen, (240, 40, 40), (int(screen_enemy_x), int(enemy['y']), enemy_w, enemy_h), border_radius=20)
            
            e_bar_w = 110
            e_bar_h = 10
            e_bar_x = int(screen_enemy_x + (enemy_w // 2) - (e_bar_w // 2))
            e_bar_y = int(enemy['y'] - 28)
            
            pygame.draw.rect(screen, (0, 0, 0), (e_bar_x - 2, e_bar_y - 2, e_bar_w + 4, e_bar_h + 4), border_radius=3)
            pygame.draw.rect(screen, (100, 0, 0), (e_bar_x, e_bar_y, e_bar_w, e_bar_h), border_radius=2)
            e_current_bar_w = int(e_bar_w * (enemy['hp'] / enemy['max_hp']))
            if e_current_bar_w > 0:
                pygame.draw.rect(screen, (220, 0, 0), (e_bar_x, e_bar_y, e_current_bar_w, e_bar_h), border_radius=2)

            e_stamina_y = e_bar_y + 12
            pygame.draw.rect(screen, (0, 0, 0), (e_bar_x - 2, e_stamina_y - 2, e_bar_w + 4, e_bar_h + 4), border_radius=3)
            pygame.draw.rect(screen, (50, 50, 50), (e_bar_x, e_stamina_y, e_bar_w, e_bar_h), border_radius=2)
            e_current_stamina_w = int(e_bar_w * (max(0, enemy['stamina']) / enemy['max_stamina']))
            if e_current_stamina_w > 0:
                pygame.draw.rect(screen, (255, 165, 0), (e_bar_x, e_stamina_y, e_current_stamina_w, e_bar_h), border_radius=2)
    
    if health > 0:
        screen_player_x = world_x - camera_x
        frame_idx = int(current_frame)
        
        if is_jumping:
            frames_to_use = yuika_jump_right if facing_right else yuika_jump_left
        elif is_bomb_anim:
            frames_to_use = yuika_bomb_right if facing_right else yuika_bomb_left
        elif is_shooting_anim:
            frames_to_use = yuika_shoot_right if facing_right else yuika_shoot_left
        elif is_moving:
            frames_to_use = yuika_walk_right if facing_right else yuika_walk_left
        else:
            frames_to_use = yuika_idle_right if facing_right else yuika_idle_left
            
        if frames_to_use:
            screen.blit(frames_to_use[frame_idx % len(frames_to_use)], (int(screen_player_x - radius), int(y - radius)))
        else:
            pygame.draw.circle(screen, (0, 230, 130), (int(screen_player_x), int(y)), radius)
            
        name_surface = font_name.render("Yuika", True, (255, 255, 255))
        name_rect = name_surface.get_rect(center=(int(screen_player_x), int(y - radius - 55)))
        shadow_surface = font_name.render("Yuika", True, (0, 0, 0))
        screen.blit(shadow_surface, (name_rect.x + 2, name_rect.y + 2))
        screen.blit(name_surface, name_rect)

        bar_w = 120
        bar_h = 16
        bar_x = int(screen_player_x - bar_w // 2)
        bar_y = int(y - radius - 25)
        
        pygame.draw.rect(screen, (0, 0, 0), (bar_x - 2, bar_y - 2, bar_w + 4, bar_h + 4), border_radius=4)
        pygame.draw.rect(screen, (100, 0, 0), (bar_x, bar_y, bar_w, bar_h), border_radius=3)
        
        current_bar_w = int(bar_w * (health / max_health))
        if current_bar_w > 0:
            bar_color = (0, 220, 0) if health > 40 else (220, 0, 0)
            pygame.draw.rect(screen, bar_color, (bar_x, bar_y, current_bar_w, bar_h), border_radius=3)

    # --- UI HUD KIRI ATAS & TOMBOL BAG ---
    if health > 0:
        avatar_box = pygame.Rect(30, 20, 95, 95)
        pygame.draw.rect(screen, (40, 40, 50), avatar_box, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), avatar_box, 3, border_radius=12)
        if hud_avatar:
            screen.blit(hud_avatar, (32, 22))

        hud_bar_x = 145
        hud_bar_y = 25
        hud_bar_w = 260
        hud_bar_h = 20
        
        pygame.draw.rect(screen, (0, 0, 0), (hud_bar_x - 2, hud_bar_y - 2, hud_bar_w + 4, hud_bar_h + 4), border_radius=6)
        pygame.draw.rect(screen, (100, 0, 0), (hud_bar_x, hud_bar_y, hud_bar_w, hud_bar_h), border_radius=4)
        hud_current_w = int(hud_bar_w * (health / max_health))
        if hud_current_w > 0:
            hud_color = (0, 220, 0) if health > 40 else (220, 0, 0)
            pygame.draw.rect(screen, hud_color, (hud_bar_x, hud_bar_y, hud_current_w, hud_bar_h), border_radius=4)

        stamina_bar_y = hud_bar_y + 26
        stamina_bar_h = 16
        pygame.draw.rect(screen, (0, 0, 0), (hud_bar_x - 2, stamina_bar_y - 2, hud_bar_w + 4, stamina_bar_h + 4), border_radius=6)
        pygame.draw.rect(screen, (20, 20, 50), (hud_bar_x, stamina_bar_y, hud_bar_w, stamina_bar_h), border_radius=4)
        stamina_current_w = int(hud_bar_w * (stamina / max_stamina))
        if stamina_current_w > 0:
            pygame.draw.rect(screen, (0, 180, 255), (hud_bar_x, stamina_bar_y, stamina_current_w, stamina_bar_h), border_radius=4)

        status_txt = font.render(f"Waktu: {elapsed_seconds}s   |   Musuh: {len(enemies)}", True, (255, 255, 255))
        screen.blit(status_txt, (hud_bar_x, stamina_bar_y + 24))

        if active_buff_text:
            buff_txt = font.render(active_buff_text, True, (255, 215, 0))
            screen.blit(buff_txt, (hud_bar_x, stamina_bar_y + 65))

        pygame.draw.rect(screen, (90, 60, 40), btn_bag, border_radius=15)
        pygame.draw.rect(screen, (255, 215, 0), btn_bag, 4, border_radius=15)
        bag_lbl = font.render("BAG", True, (255, 255, 255))
        screen.blit(bag_lbl, (btn_bag.x + 30, btn_bag.y + 20))
    else:
        text_over = font_large.render("GAME OVER!", True, (255, 50, 50))
        screen.blit(text_over, (900, 230))
        pygame.draw.rect(screen, (0, 150, 255), btn_reset, border_radius=30)
        reset_lbl = font.render("RESET GAME", True, (255, 255, 255))
        screen.blit(reset_lbl, (btn_reset.x + 65, btn_reset.y + 45))

    # --- JENDELA POP-UP INVENTORI (TAS) ---
    if is_inventory_open:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        bag_window = pygame.Rect(600, 180, 1200, 720)
        pygame.draw.rect(screen, (50, 50, 60), bag_window, border_radius=25)
        pygame.draw.rect(screen, (255, 215, 0), bag_window, 6, border_radius=25)

        title_bag = font_large.render("INVENTORI TAS YUIKA", True, (255, 215, 0))
        screen.blit(title_bag, (bag_window.centerx - title_bag.get_width() // 2, bag_window.y + 30))

        guide_txt = font_small.render("Ketuk item untuk memilih, lalu tekan PAKAI atau BUANG", True, (200, 200, 200))
        screen.blit(guide_txt, (bag_window.centerx - guide_txt.get_width() // 2, bag_window.y + 110))

        slot_size = 110
        start_x = bag_window.x + 175
        start_y = bag_window.y + 150
        
        slot_idx = 0
        for row in range(3):
            for col in range(4):
                sx = start_x + col * (slot_size + 30)
                sy = start_y + row * (slot_size + 30)
                slot_rect = pygame.Rect(sx, sy, slot_size, slot_size)
                
                border_color = (0, 255, 0) if selected_slot == slot_idx else (120, 120, 140)
                pygame.draw.rect(screen, (30, 30, 35), slot_rect, border_radius=15)
                pygame.draw.rect(screen, border_color, slot_rect, 4, border_radius=15)

                if slot_idx < len(inventory_items):
                    item_type = inventory_items[slot_idx]
                    slot_img = item_def if item_type == 'def' else (item_atk if item_type == 'atk' else item_immune)
                    if slot_img:
                        scaled_item_img = pygame.transform.scale(slot_img, (75, 75))
                        screen.blit(scaled_item_img, (sx + (slot_size - 75) // 2, sy + (slot_size - 75) // 2))
                slot_idx += 1

        pygame.draw.rect(screen, (0, 180, 80), btn_use_item, border_radius=15)
        pygame.draw.rect(screen, (255, 255, 255), btn_use_item, 3, border_radius=15)
        screen.blit(font.render("PAKAI", True, (255, 255, 255)), (btn_use_item.x + 55, btn_use_item.y + 15))

        pygame.draw.rect(screen, (200, 40, 40), btn_drop_item, border_radius=15)
        pygame.draw.rect(screen, (255, 255, 255), btn_drop_item, 3, border_radius=15)
        screen.blit(font.render("BUANG", True, (255, 255, 255)), (btn_drop_item.x + 50, btn_drop_item.y + 15))

    # --- TOMBOL KONTROL UI KANAN BAWAH ---
    if not is_inventory_open:
        pygame.draw.circle(screen, (60, 60, 70), joystick_center, joystick_bg_radius)
        pygame.draw.circle(screen, (100, 100, 110), joystick_center, joystick_bg_radius, 6)
        pygame.draw.circle(screen, (180, 180, 200), (int(joystick_knob_pos[0]), int(joystick_knob_pos[1])), joystick_knob_radius)

        pygame.draw.circle(screen, (0, 180, 255), btn_jump.center, 90)
        screen.blit(font.render("LONCAT", True, (255, 255, 255)), (btn_jump.x + 18, btn_jump.y + 65))

        pygame.draw.circle(screen, (220, 40, 40), btn_shoot.center, 100)
        screen.blit(font.render("PISTOL", True, (255, 255, 255)), (btn_shoot.x + 35, btn_shoot.y + 75))

        pygame.draw.circle(screen, (150, 40, 220), btn_bomb.center, 100)
        screen.blit(font.render("BOM", True, (255, 255, 255)), (btn_bomb.x + 55, btn_bomb.y + 75))

    pygame.display.flip()

pygame.quit()
