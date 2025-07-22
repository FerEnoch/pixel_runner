import pygame
from random import randint, choice


###################
### Classes
###################
### Player sprite class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load("pixel_runner/graphics/player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("pixel_runner/graphics/player/player_walk_2.png").convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_jump = pygame.image.load("pixel_runner/graphics/player/jump.png").convert_alpha()
        self.player_walk_index = 0
        self.gravity = 0
        
        self.image = self.player_walk[self.player_walk_index]
        self.rect = self.image.get_rect(midbottom = (DEFAULT_PLAYER_START_X_POSITION, GROUND_LINE))
        
        self.jump_sound = pygame.mixer.Sound("pixel_runner/audio/jump.mp3")
        self.jump_sound.set_volume(0.3)  
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= GROUND_LINE:
            self.jump()
    
    def jump(self):
        self.gravity = -20
        self.jump_sound.play()  # Play the jump sound
    
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= GROUND_LINE:
            self.rect.bottom = GROUND_LINE
    
    def animation_state(self):
        if self.rect.bottom < GROUND_LINE:  # If the player is in the air
            self.image = self.player_jump
        else:
            self.player_walk_index += 0.1
            if self.player_walk_index >= len(self.player_walk):
                self.player_walk_index = 0
            self.image = self.player_walk[int(self.player_walk_index)] 

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

### Obstacle sprite class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            fly_frame_1 = pygame.image.load("pixel_runner/graphics/fly/fly1.png").convert_alpha()
            fly_frame_2 = pygame.image.load("pixel_runner/graphics/fly/fly2.png").convert_alpha()
            self.frames = [fly_frame_1, fly_frame_2]
            y_position = GROUND_LINE - 100
        else:
            snail_frame_1 = pygame.image.load("pixel_runner/graphics/snail/snail1.png").convert_alpha()
            snail_frame_2 = pygame.image.load("pixel_runner/graphics/snail/snail2.png").convert_alpha()
            self.frames = [snail_frame_1, snail_frame_2] 
            y_position = GROUND_LINE

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(TOTAL_WIDTH + 100, TOTAL_WIDTH + 300), y_position))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
        
    def destroy(self):
        if self.rect.x <= 0 - self.rect.width:
            self.kill()
        
    def update(self):
        self.animation_state()
        self.rect.x -= DEFAULT_OBSTACLES_SPEED
        self.destroy()
        

###################
### Helper functions
###################
def display_score():
    # get_ticks() get the time since pygame.init() was called
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = FONT.render(f"Score: {current_time}", False, (64,64,64))  # Render the score surface
    score_rect = score_surf.get_rect(center = (TOTAL_WIDTH / 2, 50))  # Center the score text
    SCREEN.blit(score_surf, score_rect)  # Blit the score surface onto the screen
    return current_time

# def obstacle_movement(obstacle_list):
    # Python evaluates empty lists as False
    # if obstacle_list:
    #     for obstacle_rect in obstacle_list:
    #         obstacle_rect.x -= DEFAULT_OBSTACLES_SPEED  # Move the obstacle to the left
    #         if obstacle_rect.bottom == GROUND_LINE:
    #             SCREEN.blit(snail_surface, obstacle_rect)
    #         else:
    #             SCREEN.blit(fly_surface, obstacle_rect)
        # Remove obstacles that are off the screen
    #     obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.right > 0] 
        
    #     return obstacle_list
    # else: return []

def collisions_sprite():
    collisions = pygame.sprite.spritecollide(player.sprite, obstacle_group, False)
    if collisions: obstacle_group.empty()
    return not collisions # not collisions, i.e., game still active

# def collisions (player, obstacles):
#     if obstacles:
#         for obstacle_rect in obstacles:
#             if player.colliderect(obstacle_rect):  # Check for collision between player and obstacle
#                 return False  # If there is a collision, return False (game over)
#     return True  # If no collisions, return True (game continues) 



###################
### Initialization
###################        
pygame.init()

GAME_TITLE = "Pixel Runner"

TOTAL_WIDTH = 800
TOTAL_HEIGHT = 400

CLOCK = pygame.time.Clock()
FONT = pygame.font.Font("pixel_runner/font/Pixeltype.ttf", 50)
DEFAULT_OBSTACLES_SPEED = 5
OBSTACLE_SPAWN_TIME = 1500  # Time in milliseconds (1.5 seconds)
DEFAULT_PLAYER_START_X_POSITION = 100 

SCREEN = pygame.display.set_mode((TOTAL_WIDTH, TOTAL_HEIGHT))  # Set the size of the window

pygame.display.set_caption(GAME_TITLE)

game_active = False

game_name = FONT.render(GAME_TITLE, False, (111, 196, 169))  # Render the game name
game_name_rect = game_name.get_rect(center = (TOTAL_WIDTH // 2, 50))  # Center the game name text

score = 0
start_time = 0

bg_music = pygame.mixer.Sound("pixel_runner/audio/music.wav")  # Load the background music
bg_music.set_volume(0.1)  # Set the volume of the background music
bg_music.play(loops = -1)  # Play the background music in a endless loop

# test_surface = pygame.Surface((100, 200))
# test_surface.fill("red") # or you can use RGB (255, 0, 0)
sky_surface = pygame.image.load("pixel_runner/graphics/sky.png").convert()
sky_height = sky_surface.get_height()  # Get the height of the sky surface

ground_surface = pygame.image.load("pixel_runner/graphics/ground.png").convert()
ground_height = ground_surface.get_height() # Get the height of the ground surface

GROUND_LINE = TOTAL_HEIGHT - (TOTAL_HEIGHT - sky_height)

# Arguments to render are: text, antialiasing (util with no pixel-art text), color (predefined, rgb or hex)
# text_surface = font.render("Pixel Runner",  False, "Black")

# Intro screen
player_stand = pygame.image.load("pixel_runner/graphics/player/player_stand.png").convert_alpha()
# player_stand = pygame.transform.scale(player_stand, (player_stand.get_width() * 2, player_stand.get_height() * 2))
# player_stand = pygame.transform.scale2x(player_stand)  # Scale the player stand image)
# Rotozoom use a filter that in some cases is better than scale2x alone.
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)  # 0 degree rotation and 2x scale the player stand image
player_stand_rect = player_stand.get_rect(center = (TOTAL_WIDTH // 2, TOTAL_HEIGHT // 2))

game_message = FONT.render("Press SPACE to run", False, (111, 196, 169))
get_message_rect = game_message.get_rect(center = (TOTAL_WIDTH // 2, TOTAL_HEIGHT // 1.2))

### Timer
OBSTACLE_TIMER = pygame.USEREVENT + 1
pygame.time.set_timer(OBSTACLE_TIMER, OBSTACLE_SPAWN_TIME) # Set the timer to trigger every 1500 milliseconds (1.5 seconds)

SNAIL_ANIMATION_TIMER = pygame.USEREVENT + 2
pygame.time.set_timer(SNAIL_ANIMATION_TIMER, 500) 

FLY_ANIMATION_TIMER = pygame.USEREVENT + 3
pygame.time.set_timer(FLY_ANIMATION_TIMER, 200) 

###################
### Groups
###################
### Player
player = pygame.sprite.GroupSingle()
player.add(Player())

### Obstacle
obstacle_group = pygame.sprite.Group()


###################
### Main Loop
###################
while True:
    ################
    ### Event Loop
    ################
    for event in pygame.event.get():
        ###############
        ### Exit Game
        ###############
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit() # The opposite of pygame.init()
                exit()
        if event.type == pygame.QUIT:
            pygame.quit() # The opposite of pygame.init()
            exit()
       
        ###############
        ### Game Logic
        ###############
        if game_active:
            ### Jump mechanics
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     if player_rectangle.collidepoint(event.pos) and player_rectangle.bottom >= GROUND_LINE:
            #         player_gravity = -20
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_SPACE and player_rectangle.bottom >= GROUND_LINE:
            #         player_gravity = -20
            ### Timer for obstacles
            if event.type == OBSTACLE_TIMER:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail']))) # 75% for snails
                # if randint(0, 2):
                #     # Here you can add logic to spawn obstacles or other game elements
                #     snail_rect = snail_surface.get_rect(bottomright = (randint(TOTAL_WIDTH + 100, TOTAL_WIDTH + 300), GROUND_LINE - 100))
                #     obstacle_rect_list.append(snail_rect)  # Add the snail rectangle to the obstacle list
                # else:
                #     fly_rect = fly_surface.get_rect(bottomright = (randint(TOTAL_WIDTH + 100, TOTAL_WIDTH + 300), GROUND_LINE))
                #     obstacle_rect_list.append(fly_rect)  # Add the fly rectangle to the obstacle list
            # if event.type == SNAIL_ANIMATION_TIMER:
            #     if snail_frame_index == 0: snail_frame_index = 1
            #     else: snail_frame_index = 0
            #     snail_surface = snail_frames[snail_frame_index] 
            # if event.type == FLY_ANIMATION_TIMER:
            #     if fly_frame_index == 0: fly_frame_index = 1
            #     else: fly_frame_index = 0
            #     fly_surface = fly_frames[fly_frame_index]
        ################
        ### Game (re))start
        ################
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    # snail_rectangle.midbottom = (TOTAL_WIDTH, TOTAL_HEIGHT - (TOTAL_HEIGHT - sky_height))
                    start_time = int(pygame.time.get_ticks() / 1000)  # Reset the start time when the game restarts
    
    ################
    ### Start Game Loop
    ################
    if game_active: 
        # blit -> block image transfer (i.e. one surface on another surface, that is the screen)
        SCREEN.blit(sky_surface, (0, 0))  
        SCREEN.blit(ground_surface, (0, sky_height))
        
        # screen.blit(text_surface, (300, 50))  # Positioning the text on the screen
        # pygame.draw.rect(screen, "#c0e8ec", score_rect)  # Draw the score rectangle
        # pygame.draw.rect(screen, "#c0e8ec", score_rect, 10)  # Draw the score rectangle

        score = display_score()  # Call the function to display the score

        # screen.blit(snail_surface, snail_rectangle)  # Positioning the snail on the screen
        # snail_rectangle.x -= 5  # Move the snail to the left
        # if snail_rectangle.right < 0:  # If the snail goes off the screen
        #     snail_rectangle.x = TOTAL_WIDTH

        # player_animation()  # Update the player animation
        # SCREEN.blit(player_surface, player_rectangle)  # Positioning the player on the screen
        
        
        player.draw(SCREEN)
        player.update()  
        
        obstacle_group.draw(SCREEN)
        obstacle_group.update()
          
        # ### Simulate gravity
        # player_gravity += 1 
        # player_rectangle.y += player_gravity  # Apply gravity to the player
        # if player_rectangle.bottom >= GROUND_LINE:  # If the player is on the ground
        #     player_rectangle.bottom = GROUND_LINE  # Keep the player on the ground

        ### Obstacles movement
        # obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        
        ### Collision
        # One type of collision detection
        # player_rectangle.colliderect(snail_rectangle)
        # Another: collide point
        # player_rectangle.collidepoint((snail_rectangle.midleft))
        # if snail_rect.colliderect(player_rectangle):
        #     game_active = False
        # game_active = collisions(player_rectangle, obstacle_rect_list)
        game_active = collisions_sprite()

    else:
        # If the game is not active, we can show a message or do something else
        # game_over_surface = FONT.render("Game Over", False, (111, 196, 169))
        # screen.blit(game_over_surface, game_over_surface.get_rect(center = (TOTAL_WIDTH // 2, TOTAL_HEIGHT // 2)))
        SCREEN.fill((94, 129, 162))
        SCREEN.blit(player_stand, player_stand_rect)
        
        # Remove all obstacles
        # obstacle_rect_list.clear()
        # Put my player on the ground
        # player_rectangle.midbottom = (DEFAULT_PLAYER_START_X_POSITION, GROUND_LINE)
        # player_gravity = 0  # Reset the gravity when the game is not active
                
        score_message = FONT.render(f"Your score: {score}", False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center = (TOTAL_WIDTH // 2, TOTAL_HEIGHT // 1.2))

        if score > 0:
            SCREEN.blit(score_message, score_message_rect)
        else:        
            SCREEN.blit(game_name, game_name_rect)
            SCREEN.blit(game_message, get_message_rect)
        
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_SPACE]: # That is, is the space key is reppresented with a 1 instead of 0
        #     print("Jump!")
    
    
    # Draw our elements, updating everything
    # Updates the display.set_mode to the not to dissapear.
    pygame.display.update()
    CLOCK.tick(60)  # Limit the while loop (i.e. framerate) to 60 FPS