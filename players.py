import pygame

class Arrow:
    def __init__(self, x, y, direction_string, shooter_num, charge_level=1):
        self.pos = pygame.math.Vector2(x, y)
        self.dir_str = direction_string
        self.shooter_num = shooter_num
        
        # Sets damage and speed from the player's charge level
        self.damage = charge_level
        self.speed = 12
        
        # Calculates moving direction vectors
        self.velocity = pygame.math.Vector2(0, 0)
        if self.dir_str == "left":   self.velocity.x = -1
        elif self.dir_str == "right": self.velocity.x = 1
        elif self.dir_str == "up":    self.velocity.y = -1
        elif self.dir_str == "down":  self.velocity.y = 1
        
        # Loads arrow image asset safely
        try:
            self.image = pygame.image.load("arrow.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (48, 48))
        except pygame.error:
            self.image = pygame.Surface((48, 48), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (220, 160, 90), (0, 20, 48, 8))

        # 4-Way angle rotation lock for the arrow sprite
        if self.dir_str == "right":
            pass 
        elif self.dir_str == "left":
            self.image = pygame.transform.rotate(self.image, 180)
        elif self.dir_str == "up":
            self.image = pygame.transform.rotate(self.image, 90)
        elif self.dir_str == "down":
            self.image = pygame.transform.rotate(self.image, -90)

        # Team color profiles: blue for player 1, red for player 2
        if self.shooter_num == 1:
            if self.damage == 3:
                self.image.fill((200, 230, 255), special_flags=pygame.BLEND_RGB_MULT)
            else:
                self.image.fill((130, 150, 255), special_flags=pygame.BLEND_RGB_MULT)
        elif self.shooter_num == 2:
            if self.damage == 3:
                self.image.fill((255, 200, 100), special_flags=pygame.BLEND_RGB_MULT)
            else:
                self.image.fill((255, 100, 100), special_flags=pygame.BLEND_RGB_MULT)

        self.rect = self.image.get_rect()
        self.rect.topleft = (self.pos.x, self.pos.y)

    def update(self):
        # Moves arrow forward
        self.pos += self.velocity * self.speed
        self.rect.topleft = (self.pos.x, self.pos.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Player:
    def __init__(self, start_x, start_y, player_num=1):
        self.player_num = player_num
        self.pos = pygame.math.Vector2(start_x, start_y)
        self.speed = 5
        self.is_moving = False
        self.health = 10  

        # Sprite sizes
        self.frame_w = 32
        self.frame_h = 32
        self.scale_factor = 3.0     

        self.screen_width = 800
        self.screen_height = 600

        self.current_dir = "down"
        self.current_frame = 0

        # Charging states and timers
        self.is_charging = False
        self.charge_frame = 0         
        self.charge_speed = 150       # Slowed down slightly so players can intentionally time their charge tiers
        self.charge_timer = pygame.time.get_ticks()

        self.shoot_cooldown = 600  
        self.last_shot = pygame.time.get_ticks()

        self.idle_cooldown = 320
        self.walk_cooldown = 120
        self.last_update = pygame.time.get_ticks()

        # Load walking and breathing sprite sheets
        self.idle_animations, self.walk_animations = self._load_and_slice_assets()
        
        # Reload status warning trackers
        self.reload_popup_timer = 0       # Tracks how long the popup stays visible
        self.reload_font = pygame.font.SysFont("Courier New", 16, bold=True)

        
        # Loads the 4 progressive bow frames
        self.bow_frames = []
        for i in range(4):
            try:
                img = pygame.image.load(f"bow{i}.png").convert_alpha()
                img = pygame.transform.scale(img, (32, 48))
                if self.player_num == 1:
                    img.fill((130, 150, 255), special_flags=pygame.BLEND_RGB_MULT)
                elif self.player_num == 2:
                    img.fill((255, 120, 120), special_flags=pygame.BLEND_RGB_MULT)
                self.bow_frames.append(img)
            except pygame.error:
                fallback = pygame.Surface((12 + (i * 4), 32), pygame.SRCALPHA)
                if self.player_num == 1: fallback.fill((50, 100, 255))
                else: fallback.fill((220, 40, 40))
                self.bow_frames.append(fallback)

        self.rect = pygame.Rect(
            self.pos.x, self.pos.y, 
            int(self.frame_w * self.scale_factor), 
            int(self.frame_h * self.scale_factor)
        )

    def _load_and_slice_assets(self):
        try:
            walk_sheet = pygame.image.load("placeholder_sheet.png").convert_alpha()
            idle_sheet = pygame.image.load("idleholder_sheet.png").convert_alpha()
        except pygame.error:
            walk_sheet = pygame.Surface((self.frame_w * 4, self.frame_h * 5), pygame.SRCALPHA)
            idle_sheet = pygame.Surface((self.frame_w * 4, self.frame_h * 5), pygame.SRCALPHA)

        row_map = {"down": 0, "right": 1, "up": 4}
        idle_pool = {"down": [], "right": [], "up": []}
        walk_pool = {"down": [], "right": [], "up": []}

        for direction, row_index in row_map.items():
            new_size = (int(self.frame_w * self.scale_factor), int(self.frame_h * self.scale_factor))
            for col_index in range(4):
                x = col_index * self.frame_w
                y = row_index * self.frame_h
                rect = pygame.Rect(x, y, self.frame_w, self.frame_h)

                # Processes Idle animation frames and apply team colors
                frame_idle = pygame.Surface(rect.size, pygame.SRCALPHA)
                frame_idle.blit(idle_sheet, (0,0), rect)
                frame_idle.set_colorkey((0, 0, 0))
                frame_idle = pygame.transform.scale(frame_idle, new_size)
                if self.player_num == 1:
                    frame_idle.fill((130, 150, 255), special_flags=pygame.BLEND_RGB_MULT)
                elif self.player_num == 2:
                    frame_idle.fill((255, 130, 130), special_flags=pygame.BLEND_RGB_MULT)
                idle_pool[direction].append(frame_idle)

                # Processes Walking animation frames and apply team colors
                frame_walk = pygame.Surface(rect.size, pygame.SRCALPHA)
                frame_walk.blit(walk_sheet, (0, 0), rect)
                frame_walk.set_colorkey((0, 0, 0))
                frame_walk = pygame.transform.scale(frame_walk, new_size)
                if self.player_num == 1:
                    frame_walk.fill((130, 150, 255), special_flags=pygame.BLEND_RGB_MULT)
                elif self.player_num == 2:
                    frame_walk.fill((255, 130, 130), special_flags=pygame.BLEND_RGB_MULT)
                walk_pool[direction].append(frame_walk)
            
        return idle_pool, walk_pool
    
    def update(self, arrow_list):
        keys = pygame.key.get_pressed()
        now = pygame.time.get_ticks()   

        direction = pygame.math.Vector2(0, 0)
        attack_key_held = False
        
        # Captures separate keyboard direction tracks
        if self.player_num == 1:
            if keys[pygame.K_a]:   direction.x = -1; self.current_dir = "left"
            elif keys[pygame.K_d]: direction.x = 1;  self.current_dir = "right"
            elif keys[pygame.K_w]: direction.y = -1; self.current_dir = "up"
            elif keys[pygame.K_s]: direction.y = 1;  self.current_dir = "down"
            if keys[pygame.K_SPACE]: attack_key_held = True
        else:
            if keys[pygame.K_LEFT]:    direction.x = -1; self.current_dir = "left"
            elif keys[pygame.K_RIGHT]: direction.x = 1;  self.current_dir = "right"
            elif keys[pygame.K_UP]:    direction.y = -1; self.current_dir = "up"
            elif keys[pygame.K_DOWN]:  direction.y = 1;  self.current_dir = "down"
            if keys[pygame.K_RCTRL] or keys[pygame.K_RETURN]: attack_key_held = True
        
        # Runtime physics vector (zero delay)
        if direction.length() > 0:
            self.is_moving = True
            self.pos += direction * 4

            if self.pos.x < 0: self.pos.x = 0
            elif self.pos.x > self.screen_width - self.rect.width: self.pos.x = self.screen_width - self.rect.width
            if self.pos.y < 0: self.pos.y = 0
            elif self.pos.y > self.screen_height - self.rect.height: self.pos.y = self.screen_height - self.rect.height

            self.rect.topleft = (self.pos.x, self.pos.y)
        else:
            self.is_moving = False

        # Independent combat system and re-arming timers
        if attack_key_held:
            # Checks if they are button spamming before weapon is re-armed
            if now - self.last_shot < self.shoot_cooldown:
                # Flash the short warning alert over their head (Lasts 400ms)
                self.reload_popup_timer = now + 400
            else:
                # Weapon is fully reloaded
                if not self.is_charging:
                    self.is_charging = True
                    self.charge_frame = 0
                    self.charge_timer = now
                else:
                    if now - self.charge_timer >= self.charge_speed:
                        self.charge_timer = now
                        self.charge_frame = min(3, self.charge_frame + 1)
        else:
            # Discharge arrow project files
            if self.is_charging:
                self.is_charging = False
                self.last_shot = now
                
                if self.charge_frame == 3:
                    final_damage = 2    # Double Damage when charged 
                    final_speed = 16    
                else:
                    final_damage = 1    
                    final_speed = 9     
                
                spawn_x = self.rect.centerx - 24
                spawn_y = self.rect.centery - 24
                
                if self.current_dir == "up": spawn_y -= 15 
                elif self.current_dir == "down": spawn_y += 15 
                elif self.current_dir == "right": spawn_x += 15; spawn_y += 10 
                elif self.current_dir == "left": spawn_x -= 15; spawn_y += 10 
                
                new_arrow = Arrow(spawn_x, spawn_y, self.current_dir, self.player_num, final_damage)
                new_arrow.speed = final_speed
                arrow_list.append(new_arrow)
                self.charge_frame = 0

        # Cycle sprite walking/breathing animation frame ticks
        active_cooldown = self.walk_cooldown if self.is_moving else self.idle_cooldown
        if now - self.last_update >= active_cooldown:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % 4

    def draw(self, screen):
        if self.health <= 0:
            return  

        lookup_dir = "right" if self.current_dir == "left" else self.current_dir
        
        # Selects the active animation pool based on movement state
        if self.is_moving:
            current_pool = self.walk_animations[lookup_dir]
        else:
            current_pool = self.idle_animations[lookup_dir]

        # If the list is empty, this creates a quick fallback surface to prevent a crash
        if not current_pool:
            fallback_surf = pygame.Surface((96, 96), pygame.SRCALPHA)
            current_pool = [fallback_surf]

        # This should ensure index never exceeds list length
        safe_frame = self.current_frame % len(current_pool)
        sprite_to_draw = current_pool[safe_frame]

        if self.current_dir == "left":
            sprite_to_draw = pygame.transform.flip(sprite_to_draw, True, False)
        
        active_bow_texture = self.bow_frames[self.charge_frame]
        center_x = self.rect.centerx
        center_y = self.rect.centery

        if self.current_dir == "up":
            screen.blit(active_bow_texture, (center_x - 22, center_y - 24))
            screen.blit(sprite_to_draw, self.rect)
        elif self.current_dir == "down":
            screen.blit(sprite_to_draw, self.rect)
            screen.blit(active_bow_texture, (center_x - 16, center_y - 4))
        else:
            screen.blit(sprite_to_draw, self.rect)
            if self.current_dir == "right":
                screen.blit(active_bow_texture, (center_x + 6, center_y + 2))
            elif self.current_dir == "left":
                flipped_bow = pygame.transform.flip(active_bow_texture, True, False)
                screen.blit(flipped_bow, (center_x - 38, center_y + 2))

        now = pygame.time.get_ticks()
        if now < self.reload_popup_timer:
            reload_surf = self.reload_font.render("RELOADING...", True, (255, 60, 60))
            txt_x = self.rect.centerx - (reload_surf.get_width() // 2)
            txt_y = self.rect.top - 25  
            screen.blit(reload_surf, (txt_x, txt_y))


# =====================================================================
# STANDALONE SOLO TESTING ENVIRONMENT BLOCK
# =====================================================================

if __name__ == "__main__":
    import sys
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    
    p1 = Player(100, 300, player_num=1)
    p2 = Player(600, 300, player_num=2)
    active_arrows = []
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
                
        if p1.health > 0: p1.update(active_arrows)
        if p2.health > 0: p2.update(active_arrows)
        
        for arrow in active_arrows[:]:
            arrow.update()
            if arrow.pos.x < 0 or arrow.pos.x > 800 or arrow.pos.y < 0 or arrow.pos.y > 600:
                active_arrows.remove(arrow)
                continue
                
            if arrow.shooter_num == 1 and p2.health > 0:
                if arrow.rect.colliderect(p2.rect):
                    p2.health -= arrow.damage
                    active_arrows.remove(arrow)
                    print(f"Player 2 Hit by Tier {arrow.damage} Shot! Health remaining: {p2.health}")
            elif arrow.shooter_num == 2 and p1.health > 0:
                if arrow.rect.colliderect(p1.rect):
                    p1.health -= arrow.damage
                    active_arrows.remove(arrow)
                    print(f"Player 1 Hit by Tier {arrow.damage} Shot! Health remaining: {p1.health}")
                    
        screen.fill((50, 60, 75))
        for arrow in active_arrows:
            arrow.draw(screen)
        p1.draw(screen)
        p2.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

