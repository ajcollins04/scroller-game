# Slashy Slashy Run Run Created by
# Emma Houchens, Daegon Stilz, Ethan Barker, Andrew Collins
# In January/February 2021

# Import the pygame module
import math
import random

import pygame

# Import pygame.locals for easier access to key coordinates
from pygame.locals import (
    RLEACCEL,
    # K_UP,
    # K_DOWN,
    K_SPACE,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_w,
    K_a,
    K_s,
    K_d,
    K_o
)

# Animations Lists
idle_animation = [r"assets\animations\player-sprite\idle-animation\Idle Animation 1.png",
                  r"assets\animations\player-sprite\idle-animation\Idle Animation 2.png",
                  r"assets\animations\player-sprite\idle-animation\Idle Animation 3.png",
                  r"assets\animations\player-sprite\idle-animation\Idle Animation 4.png"]
move_animation = [r"assets\animations\player-sprite\running-animation\Running Animation 1.png",
                  r"assets\animations\player-sprite\running-animation\Running Animation 2.png",
                  r"assets\animations\player-sprite\running-animation\Running Animation 3.png",
                  r"assets\animations\player-sprite\running-animation\Running Animation 4.png",
                  r"assets\animations\player-sprite\running-animation\Running Animation 5.png",
                  r"assets\animations\player-sprite\running-animation\Running Animation 6.png"]
jump_animation = [r"assets\animations\player-sprite\jumping-animation\Jumping Animation 1.png",
                  r"assets\animations\player-sprite\jumping-animation\Jumping Animation 2.png",
                  r"assets\animations\player-sprite\jumping-animation\Jumping Animation 3.png",
                  r"assets\animations\player-sprite\jumping-animation\Jumping Animation 4.png",
                  r"assets\animations\player-sprite\jumping-animation\Somersault Animation 1.png",
                  r"assets\animations\player-sprite\jumping-animation\Somersault Animation 2.png",
                  r"assets\animations\player-sprite\jumping-animation\Somersault Animation 3.png",
                  r"assets\animations\player-sprite\jumping-animation\Somersault Animation 4.png",
                  r"assets\animations\player-sprite\jumping-animation\Jumping Animation 2.png",
                  r"assets\animations\player-sprite\jumping-animation\Jumping Animation 1.png"]
sliding_animation = [r"assets\animations\player-sprite\sliding-animation\Sliding Animation 1.png",
                     r"assets\animations\player-sprite\sliding-animation\Sliding Animation 2.png",
                     r"assets\animations\player-sprite\sliding-animation\Standing Animation 1.png",
                     r"assets\animations\player-sprite\sliding-animation\Standing Animation 2.png",
                     r"assets\animations\player-sprite\sliding-animation\Standing Animation 3.png"]
attacking_animation = [r"assets\animations\player-sprite\attack-animation\Attack Animation 1.png",
                       r"assets\animations\player-sprite\attack-animation\Attack Animation 2.png",
                       r"assets\animations\player-sprite\attack-animation\Attack Animation 3.png",
                       r"assets\animations\player-sprite\attack-animation\Attack Animation 4.png",
                       r"assets\animations\player-sprite\attack-animation\Attack Animation 5.png"]
dying_animation = [r"assets\animations\player-sprite\dying-animation\Dying Animation 1.png",
                   r"assets\animations\player-sprite\dying-animation\Dying Animation 2.png",
                   r"assets\animations\player-sprite\dying-animation\Dying Animation 3.png",
                   r"assets\animations\player-sprite\dying-animation\Dying Animation 4.png",
                   r"assets\animations\player-sprite\dying-animation\Dying Animation 5.png",
                   r"assets\animations\player-sprite\dying-animation\Dying Animation 5.png",
                   r"assets\animations\player-sprite\dying-animation\Dying Animation 6.png",
                   r"assets\animations\player-sprite\dying-animation\Dying Animation 6.png",
                   r"assets\animations\player-sprite\dying-animation\Dying Animation 7.png",
                   r"assets\animations\player-sprite\dying-animation\Dying Animation 7.png"]
enemy_walking = [r"assets\animations\enemy-sprite\walking-animation\Slime.png",
                 r"assets\animations\enemy-sprite\walking-animation\longer slime.png"]
birb_animation = [r"assets\animations\enemy-sprite\birb-animation\Birb Animation 1.png",
                  r"assets\animations\enemy-sprite\birb-animation\Birb Animation 2.png",
                  r"assets\animations\enemy-sprite\birb-animation\Birb Animation 3.png",
                  r"assets\animations\enemy-sprite\birb-animation\Birb Animation 4.png"]
spike_images = [r"assets\objects\booboo.png",
                r"assets\objects\booboo2.png",
                r"assets\objects\Cacti.png"]
health_icon = [r"assets\gui\healthbar\Health_Sun.png",
               r"assets\gui\healthbar\Health_Sun Outline.png"]
slime_die = [r"assets\animations\enemy-sprite\slime-die\simedie1.png",
             r"assets\animations\enemy-sprite\slime-die\simedie2.png",
             r"assets\animations\enemy-sprite\slime-die\simedie3.png",
             r"assets\animations\enemy-sprite\slime-die\simedie4.png"]

# Initializing pygame and window
pygame.init()
pygame.display.set_caption('Slashy Slashy Run Run')


# Collision function,jk jzefrxcjujk,er4filj;k.fvgcjk,mfvdxui;jersikjlu;cv i;ujlkrdfei;lo8frdviou;jlk.ertdx, gflk/ijm
def is_collision(other, self_box):
    return (self_box[0] < other[0] + other[2] and
            self_box[0] + self_box[2] > other[0] and
            self_box[1] < other[1] + other[3] and
            self_box[1] + self_box[3] > other[1])


# Sprite Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()

        # Creating the player surf
        self.surf = pygame.image.load(idle_animation[0]).convert()
        self.surf = pygame.transform.scale(self.surf, (270, 200))
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)

        # Surf box setting and positioning
        self.rect = self.surf.get_rect()
        self.rect.move_ip(SCREEN_WIDTH / 2 - 125, SCREEN_HEIGHT / 2 + 10)

        # Current Animation
        self.current_iter = iter(idle_animation)
        self.current_iter_name = "idle_animation"

        # Jumping variable and velocity
        self.is_jumping = False
        self.velocity = 0

        # State and direction for animations and keybinds
        self.state = "idle"
        self.direction = "right"
        self.is_dead = False

        # Initial player hitbox
        self.hitbox = (self.rect.x + 50, self.rect.y + 40, 135, 160)
        self.sword_hitbox = (self.rect.x + 50, self.rect.y + 40, 135, 160)

        self.max_health = 3
        self.health = 3
        self.can_attack = False
        self.slimes_killed = 0

        self.slime_hitbox = None

    # Animate the sprite based on user keypresses
    def update(self, keys):

        if self.is_dead and not self.is_jumping and self.state != "dying":
            self.state = "dying"
            self.animation("dying", "dying_animation", dying_animation)
        # Starts jumps
        if self.state == "jumping" and not self.is_jumping:
            self.is_jumping = True
            self.velocity = -10

        # Continues jump, accounts for gravity
        elif self.is_jumping:
            self.rect.move_ip(0, self.velocity)
            self.velocity += 0.2

        # Starts moving animation
        elif self.state == "idle" and (keys[K_a] or keys[K_d]):
            self.state = "moving"
            self.animation("moving", "move_animation", move_animation)

        elif self.state == "moving" and not (keys[K_a] or keys[K_d]):
            self.state = "idle"
            self.animation("idle", "idle_animation", idle_animation)

        # Starts jump animation
        elif keys[K_w] and (self.state == "idle" or self.state == "moving" or self.state == "sliding"):
            if self.state != "jumping":
                self.state = "jumping"
                self.animation("jumping", "jump_animation", jump_animation)

        # Starts slide animation
        elif keys[K_s]:
            if self.state == "idle" or self.state == "moving":
                self.state = "sliding"
                self.animation("sliding", "sliding_animation", sliding_animation)

        # Starts attack animation
        if keys[K_SPACE] and self.can_attack:
            if self.state == "idle" or self.state == "moving":
                self.slime_hitbox = slime.hitbox
                self.state = "attacking"
                self.animation("attacking", "attacking_animation", attacking_animation)

        # Changes direction of player if they aren't attacking or dying
        if self.state != "attacking" and not self.is_dead:
            if keys[K_a] and not keys[K_d] and self.direction == "right":
                self.direction = "left"
            elif keys[K_d] and self.direction == "left":
                self.direction = "right"

        # Player hitbox depending on state and direction
        if self.direction == "right":
            self.sword_hitbox = (self.rect.x + 120, self.rect.y, 135, 170)

            if self.state == "moving":
                self.hitbox = (self.rect.x + 105, self.rect.y + 40, 85, 160)

            elif self.state == "jumping":
                self.hitbox = (self.rect.x + 80, self.rect.y + 40, 125, 130)

            elif self.state == "sliding":
                self.hitbox = (self.rect.x + 80, self.rect.y + 115, 125, 75)

            elif self.state == "idle" or self.state == "attacking":
                self.hitbox = (self.rect.x + 75, self.rect.y + 40, 110, 160)

            elif self.state == "dying":
                self.hitbox = (self.rect.x + 95, self.rect.y + 40, 100, 160)

        elif self.direction == "left":
            self.sword_hitbox = (self.rect.x + 20, self.rect.y, 135, 170)

            if self.state == "moving":
                self.hitbox = (self.rect.x + 70, self.rect.y + 40, 85, 160)

            elif self.state == "jumping":
                self.hitbox = (self.rect.x + 65, self.rect.y + 40, 125, 130)

            elif self.state == "sliding":
                self.hitbox = (self.rect.x + 65, self.rect.y + 115, 125, 75)

            elif self.state == "idle" or self.state == "attacking":
                self.hitbox = (self.rect.x + 85, self.rect.y + 40, 110, 160)

            elif self.state == "dying":
                self.hitbox = (self.rect.x + 85, self.rect.y + 40, 80, 160)

    # Update current player animation
    def animation(self, state, new_iter_name, new_iter_list):
        if self.state == state:
            try:
                # Starts animation
                if self.current_iter_name is not new_iter_name:
                    self.current_iter = iter(new_iter_list)
                    self.current_iter_name = new_iter_name

                # Recreates surf to the next image in the animation
                next_iter_thing = next(self.current_iter)
                self.surf = pygame.image.load(next_iter_thing).convert()
                self.surf = pygame.transform.scale(self.surf, (270, 200))
                self.surf.set_colorkey((0, 0, 0), RLEACCEL)

                # Flips the sprite if it's moving left
                if self.direction == "left":
                    self.surf = pygame.transform.flip(self.surf, True, False)

            except StopIteration:  # Exception for resetting to the beginning of an animation
                if self.state == "dying":
                    self.state = "dead"
                    pygame.time.set_timer(ENDSCREEN, 1000, 1)

                else:
                    self.current_iter = iter(idle_animation)
                    self.state = "idle"
                    self.current_iter_name = "idle"
                    self.animation("idle", "idle_animation", idle_animation)


class Slime(pygame.sprite.Sprite):
    def __init__(self, spawn_pos):
        super(Slime, self).__init__()
        self.width = 150
        self.height = round(self.width * 43 / 70)

        self.surf = pygame.image.load(enemy_walking[0]).convert()
        self.surf = pygame.transform.scale(self.surf, (self.width, self.height))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.move_ip(spawn_pos[0], spawn_pos[1])
        self.current_iter = iter(enemy_walking)
        self.current_iter_name = "enemy_walking"
        self.state = "enemy_moving"
        self.direction = "left"
        self.speed = 1

        self.hitbox = (self.rect.x, self.rect.y, self.width, self.height)

    def update(self, keys, player_instance):
        global slime_count

        if self.state != "slime_dying":
            if self.direction == "right":
                self.rect.move_ip(self.speed, 0)
            elif self.direction == "left":
                self.rect.move_ip(-self.speed, 0)

        if player_instance.state != "attacking" and not \
                player_instance.is_dead:
            if keys[K_d] or player_instance.state == "sliding" and player_instance.direction == "right":
                self.rect.move_ip(-5, 0)

            elif keys[K_a] or player_instance.state == "sliding" and player_instance.direction == "left":
                self.rect.move_ip(5, 0)

        if self.rect.centerx < player_instance.rect.centerx and self.direction != "right":
            self.direction = "right"
            self.surf = pygame.transform.flip(self.surf, True, False)
        elif self.rect.centerx > player_instance.rect.centerx and self.direction != "left":
            self.direction = "left"
            self.surf = pygame.transform.flip(self.surf, True, False)

        if self.rect.right < -500:
            self.kill()
            slime_count = 0
        elif self.rect.left > SCREEN_WIDTH + 500:
            self.kill()
            slime_count = 0

        self.hitbox = (self.rect.x, self.rect.y, self.width, self.height)

    def animation(self, state, new_iter_name, new_iter_list):
        global slime_count

        if self.state == state:

            # Try and except for if resetting animation to beginning
            try:
                if self.current_iter_name is not new_iter_name:
                    self.current_iter = iter(new_iter_list)
                    self.current_iter_name = new_iter_name

                self.surf = pygame.image.load(next(self.current_iter)).convert()

                self.surf = pygame.transform.scale(self.surf, (self.width, self.height))

                if self.state == "slime_dying":
                    self.surf = pygame.transform.scale(self.surf, (self.width + 50, self.height + 30))

                    self.surf.set_colorkey((0, 0, 0), RLEACCEL)
                else:
                    self.surf = pygame.transform.scale(self.surf, (self.width, self.height))
                    self.surf.set_colorkey((255, 255, 255), RLEACCEL)

                # Flips the sprite if it's moving left
                if self.direction == "right":
                    self.surf = pygame.transform.flip(self.surf, True, False)

            except StopIteration:
                if self.state == "slime_dying":
                    self.kill()
                    slime_count = 0
                else:
                    self.current_iter = iter(new_iter_list)
                    self.current_iter_name = new_iter_name
                    self.animation(state, new_iter_name, new_iter_list)


# Background sprite class
class Background(pygame.sprite.Sprite):
    def __init__(self, start_position):
        super(Background, self).__init__()
        self.surf = pygame.image.load(r"assets\backgrounds\Better Start Screen.png").convert()
        self.surf = pygame.transform.scale(self.surf, (round(SCREEN_WIDTH),
                                                       round(SCREEN_HEIGHT)))
        self.rect = self.surf.get_rect()
        self.speed = 5
        self.rect.move_ip(start_position, 0)

    # Move the background based on keypresses
    def update(self, keys, player_instance):
        if player_instance.state != "attacking" and not player_instance.is_dead:
            if keys[K_d] or player_instance.state == "sliding" and player_instance.direction == "right":
                self.rect.move_ip(-self.speed, 0)

            elif keys[K_a] or player_instance.state == "sliding" and player_instance.direction == "left":
                self.rect.move_ip(self.speed, 0)

        if self.rect.right <= 0:
            self.rect.move_ip(SCREEN_WIDTH - self.rect.left - 10, 0)
        elif self.rect.left >= SCREEN_WIDTH:
            self.rect.move_ip(-self.rect.left * 2 + 10, 0)


class Ground(pygame.sprite.Sprite):
    def __init__(self, start_position):
        super(Ground, self).__init__()
        self.surf = pygame.Surface((SCREEN_WIDTH, 20))
        self.surf.fill((255, 255, 255))

        self.rect = self.surf.get_rect()
        self.speed = 5
        self.rect.move_ip(start_position[0], start_position[1])

    # Move the background based on keypresses
    def update(self, keys, player_instance):
        pass

    def is_collision(self, other):
        x_collision = (math.fabs(self.rect.x - other.rect.x) * 2) < (self.rect.width + other.rect.width)
        y_collision = (math.fabs(self.rect.y - other.rect.y) * 2) < (self.rect.height + other.rect.height)
        return x_collision and y_collision


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super(Bird, self).__init__()
        self.width = 125

        self.surf = pygame.image.load(birb_animation[0]).convert()
        self.surf = pygame.transform.scale(self.surf, (self.width, self.width))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.surf = pygame.transform.flip(self.surf, True, False)
        self.rect = self.surf.get_rect()
        self.rect.move_ip(SCREEN_WIDTH + 10, SCREEN_HEIGHT / 2 - 200)
        self.state = "flying"
        self.current_iter = iter(birb_animation)
        self.current_iter_name = "birb_animation"
        self.direction = "left"
        self.speed = 6

        self.hitbox = (self.rect.x, self.rect.y, self.width, self.width)

    def update(self, keys, player_instance):
        if self.direction == "right":
            self.rect.move_ip(self.speed, 0)
        elif self.direction == "left":
            self.rect.move_ip(-self.speed, 0)

        if player_instance.state != "attacking" and not player_instance.is_dead:
            if keys[K_d] or player_instance.state == "sliding" and player_instance.direction == "right":
                self.rect.move_ip(-5, 0)

            elif keys[K_a] or player_instance.state == "sliding" and player_instance.direction == "left":
                self.rect.move_ip(5, 0)

        if self.rect.right < -10:
            self.kill()
            birbs_list.remove(self)

        self.hitbox = (self.rect.x, self.rect.y + 35, self.width, self.width - 70)

    def animation(self, state, new_iter_name, new_iter_list):
        if self.state == state:

            # Try and except for if resetting animation to beginning
            try:
                if self.current_iter_name is not new_iter_name:
                    self.current_iter = iter(new_iter_list)
                    self.current_iter_name = new_iter_name

                self.surf = pygame.image.load(next(self.current_iter)).convert()
                self.surf = pygame.transform.scale(self.surf, (self.width, self.width))
                self.surf.set_colorkey((255, 255, 255), RLEACCEL)

                # Flips the sprite if it's moving left
                if self.direction == "left":
                    self.surf = pygame.transform.flip(self.surf, True, False)

            except StopIteration:
                if self.state == "jumping" or self.state == "sliding" or self.state == "attacking" \
                        or self.state == "dying":
                    self.current_iter = iter(idle_animation)
                    self.state = "idle"
                    self.current_iter_name = "idle"
                    self.animation("idle", "idle_animation", idle_animation)
                else:
                    self.current_iter = iter(new_iter_list)
                    self.current_iter_name = new_iter_name
                    self.animation(state, new_iter_name, new_iter_list)


class Bamboo(pygame.sprite.Sprite):
    def __init__(self, image):
        super(Bamboo, self).__init__()
        self.image = image

        if self.image == spike_images[2]:
            self.width = 175
        else:
            self.width = 400

        self.surf = pygame.image.load(image).convert()
        self.surf = pygame.transform.scale(self.surf, (self.width, self.width))
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)

        self.rect = self.surf.get_rect()

        if self.image == spike_images[2]:
            if random.randint(0, 1) == 0:
                self.rect.move_ip(SCREEN_WIDTH / 2 + 400, SCREEN_HEIGHT / 2 + 50)
            else:
                self.rect.move_ip(-400, SCREEN_HEIGHT / 2 + 50)

        else:
            if random.randint(0, 1) == 0:

                self.rect.move_ip(SCREEN_WIDTH / 2 + 300, SCREEN_HEIGHT / 2 - 20)
            else:
                self.rect.move_ip(-300, SCREEN_HEIGHT / 2 - 20)

        if self.image == spike_images[0]:
            self.hitbox = (self.rect.x + 150, self.rect.y + 160, self.width - 305, self.width - 320)
        elif self.image == spike_images[1]:
            self.hitbox = (self.rect.x + 155, self.rect.y + 160, self.width - 315, self.width - 320)
        elif self.image == spike_images[2]:
            self.hitbox = (self.rect.x + 45, self.rect.y + 55, self.width - 90, self.width - 78)

    def update(self, keys, player_instance):
        if self.image == spike_images[0]:
            self.hitbox = (self.rect.x + 150, self.rect.y + 160, self.width - 305, self.width - 320)
        elif self.image == spike_images[1]:
            self.hitbox = (self.rect.x + 155, self.rect.y + 160, self.width - 315, self.width - 320)
        elif self.image == spike_images[2]:
            self.hitbox = (self.rect.x + 45, self.rect.y + 55, self.width - 90, self.width - 78)

        if player_instance.state != "attacking" and not player_instance.is_dead:
            if keys[K_d] or player_instance.state == "sliding" and player_instance.direction == "right":
                self.rect.move_ip(-5, 0)

            elif keys[K_a] or player_instance.state == "sliding" and player_instance.direction == "left":
                self.rect.move_ip(5, 0)


class Health(pygame.sprite.Sprite):
    def __init__(self, in_list):
        super(Health, self).__init__()

        self.surf = pygame.image.load(health_icon[0]).convert()
        self.surf = pygame.transform.scale(self.surf, (100, 100))
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)

        self.rect = self.surf.get_rect()
        self.rect.move_ip(in_list * 75, SCREEN_HEIGHT - 100)

        self.filled = True

    def update(self, fill):
        if fill:
            self.surf = pygame.image.load(health_icon[0]).convert()
            self.surf = pygame.transform.scale(self.surf, (100, 100))
            self.surf.set_colorkey((0, 0, 0), RLEACCEL)

            self.filled = True
        else:
            self.surf = None
            self.surf = pygame.image.load(health_icon[1]).convert()
            self.surf = pygame.transform.scale(self.surf, (100, 100))
            self.surf.set_colorkey((255, 255, 255), RLEACCEL)

            self.filled = False


# Screen Setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Events
IDLEANIMATION = pygame.USEREVENT + 1
pygame.time.set_timer(IDLEANIMATION, 250)

MOVEANIMATION = pygame.USEREVENT + 2
pygame.time.set_timer(MOVEANIMATION, 175)

JUMPANIMATION = pygame.USEREVENT + 3
pygame.time.set_timer(JUMPANIMATION, 100)

SLIDINGANIMATION = pygame.USEREVENT + 4
pygame.time.set_timer(SLIDINGANIMATION, 175)

ATTACKINGANIMATION = pygame.USEREVENT + 5
pygame.time.set_timer(ATTACKINGANIMATION, 125)

dying_frame_skip = 0
DYINGANIMATION = pygame.USEREVENT + 6
pygame.time.set_timer(DYINGANIMATION, 100)

SPAWNSLIME = pygame.USEREVENT + 7
pygame.time.set_timer(SPAWNSLIME, 1000)

BIRDANIMATION = pygame.USEREVENT + 8
pygame.time.set_timer(BIRDANIMATION, 140)

SPAWNBIRD = pygame.USEREVENT + 9
pygame.time.set_timer(SPAWNBIRD, 1000)

SLIMEANIMATION = pygame.USEREVENT + 10
pygame.time.set_timer(SLIMEANIMATION, 200)

SPAWNSPIKE = pygame.USEREVENT + 11
pygame.time.set_timer(SPAWNSPIKE, 1000)

INVINC = pygame.USEREVENT + 12
pygame.time.set_timer(INVINC, 1000, 1)

ENDSCREEN = pygame.USEREVENT + 13

LETHIT = pygame.USEREVENT + 14
pygame.time.set_timer(LETHIT, 1000)

# Sprite Groups
all_sprites = pygame.sprite.Group()
backgrounds = pygame.sprite.Group()
grounds = pygame.sprite.Group()
spikes = pygame.sprite.Group()
slimes = pygame.sprite.Group()
birbs_list = []

health_filled = 3
health_list = []
invinc = False

# Classes Initialization
player = Player()

slime_count = 0
slime = None

background1 = Background(0)
backgrounds.add(background1)

background2 = Background(SCREEN_WIDTH - 10)
backgrounds.add(background2)

ground1 = Ground([0, 510])
grounds.add(ground1)

for i in range(player.max_health):
    health_list.append(Health(i))

clock = pygame.time.Clock()

# Start and end screen images, fonts, and text
start_screen = pygame.image.load(r"assets\backgrounds\NewStartScreen.png")
start_screen = pygame.transform.scale(start_screen, (800, 600))
font = pygame.font.Font(r"fonts\Pixelar.ttf", 50)
smaller_font = pygame.font.Font(r"fonts\Pixelar.ttf", 30)

end_screen = pygame.image.load(r"assets\backgrounds\NewEndScreen.png")
end_screen = pygame.transform.scale(end_screen, (800, 600))

text = font.render("Press Space to Play.", True, (0, 0, 0))

# Start game loop
start_game = True
while start_game:
    for event in pygame.event.get():

        # Stop the game on escape
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                start_game = False

        # Stop the game when window X is pressed
        if event.type == QUIT:
            quit()

    screen.fill((0, 0, 0))
    screen.blit(start_screen, (0, 0))

    screen.blit(text, (SCREEN_WIDTH / 2 - text.get_width() / 2, SCREEN_HEIGHT / 2 -
                       text.get_height() / 2))

    # Update the display
    pygame.display.flip()

    # Ensure program maintains a rate of 120 frames per second
    clock.tick(120)

game_loop = True
end_game = False

# Main loop
while game_loop:
    # Game loop
    if not end_game:
        # Collision Detection
        if player.health > 0:
            for birb in birbs_list:
                if is_collision(birb.hitbox, player.hitbox):
                    if not player.is_dead and not invinc:
                        player.health -= 1
                        invinc = True
                        pygame.time.set_timer(INVINC, 1000, 1)

            for spike in spikes:
                if is_collision(spike.hitbox, player.hitbox):
                    if not player.is_dead and not invinc:
                        player.health -= 1
                        invinc = True
                        pygame.time.set_timer(INVINC, 1000, 1)

        for slime in slimes:
            if player.slime_hitbox is not None and \
                    is_collision(player.slime_hitbox, player.sword_hitbox) and player.state == "attacking" \
                    and slime.state != "slime_dying":
                slime.state = "slime_dying"
                slime.animation("slime_dying", "slime_die", slime_die)
                slime.rect.move_ip((-25, -25))
                player.slimes_killed += 1

            elif is_collision(slime.hitbox, player.hitbox) and slime.state != "slime_dying":
                slime.speed = 0

                if not player.is_dead and not invinc:
                    player.health -= 1
                    invinc = True
                    pygame.time.set_timer(INVINC, 1000, 1)
            else:
                slime.speed = 1

        # Set the background to black
        screen.fill((0, 0, 0))

        # Assign pressed keys to a variable for usage later
        pressed_keys = pygame.key.get_pressed()

        # Loop through the userevents
        for event in pygame.event.get():

            # Stop the game on escape
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    game_loop = False

            # Stop the game when window X is pressed
            if event.type == QUIT:
                quit()

            # Switches to end scren after 1 second being dead
            if event.type == ENDSCREEN:
                end_game = True

            # Userevent for animations
            if event.type == IDLEANIMATION:
                player.animation("idle", "idle_animation", idle_animation)
            if event.type == MOVEANIMATION:
                player.animation("moving", "move_animation", move_animation)
            if event.type == JUMPANIMATION:
                player.animation("jumping", "jump_animation", jump_animation)
            if event.type == SLIDINGANIMATION:
                player.animation("sliding", "sliding_animation", sliding_animation)
            if event.type == ATTACKINGANIMATION:
                player.animation("attacking", "attacking_animation", attacking_animation)
            if event.type == SLIMEANIMATION:
                if slime_count != 0:
                    slime.animation("enemy_moving", "enemy_walking", enemy_walking)
                    slime.animation("slime_dying", "slime_die", slime_die)
            if event.type == BIRDANIMATION:
                for birb in birbs_list:
                    birb.animation("flying", "birb_animation", birb_animation)

            if event.type == DYINGANIMATION:
                dying_frame_skip += 1
                if dying_frame_skip >= 2:
                    dying_frame_skip = 0
                    player.animation("dying", "dying_animation", dying_animation)

            # User events for spawning
            if event.type == SPAWNSLIME and slime_count == 0:
                if random.randint(0, 2) == 1:
                    slime = Slime([SCREEN_WIDTH + 50, SCREEN_HEIGHT / 2 + 115])
                else:
                    slime = Slime([-250, SCREEN_HEIGHT / 2 + 115])

                slimes.add(slime)
                slime_count += 1

            if event.type == SPAWNBIRD and len(birbs_list) <= 1:
                if random.randint(1, 8) == 1:
                    birb = Bird()
                    all_sprites.add(birb)
                    birbs_list.append(birb)

            if event.type == SPAWNSPIKE:
                spike_on_screen = False
                for spike in spikes:
                    if spike.hitbox[0] + spike.hitbox[2] > -SCREEN_WIDTH and spike.hitbox[0] < SCREEN_WIDTH * 2:
                        spike_on_screen = True

                if random.randint(1, 2) == 1 and not spike_on_screen:
                    spike = Bamboo(random.choice(spike_images))

                    all_sprites.add(spike)
                    spikes.add(spike)

            # User Events for invincible time between hits and time you cant hit during spawn
            if event.type == INVINC:
                invinc = False
            if event.type == LETHIT:
                player.can_attack = True

        # Updates and rendering
        for background in backgrounds:
            background.update(pressed_keys, player)
            screen.blit(background.surf, background.rect)

        for sprite in all_sprites:
            sprite.update(pressed_keys, player)
            screen.blit(sprite.surf, sprite.rect)

        for faces in reversed(health_list):
            if health_filled > player.health and faces.filled:
                faces.update(fill=False)
                health_filled -= 1

        for faces in health_list:
            if health_filled < player.health and not faces.filled:
                faces.update(fill=True)
                health_filled += 1

        for faces in health_list:
            screen.blit(faces.surf, faces.rect)

        if player.health == 0:
            player.is_dead = True
            slime.speed = 0

        for ground in grounds:
            # screen.blit(ground.surf, ground.rect)
            if pygame.sprite.collide_rect(ground, player):
                player.state = "idle"
                player.animation("idle", "idle_animation", idle_animation)
                player.is_jumping = False
                player.velocity = 0
                player.rect.move_ip(0, -1)

        # Updates and renders the player
        player.update(pressed_keys)
        screen.blit(player.surf, player.rect)

        for slime in slimes:
            slime.update(pressed_keys, player)
            screen.blit(slime.surf, slime.rect)
    # End game loop
    else:
        for event in pygame.event.get():

            # Stop the game on escape
            if event.type == KEYDOWN:
                if event.key == K_SPACE:

                    # Sprite Groups
                    all_sprites = pygame.sprite.Group()
                    backgrounds = pygame.sprite.Group()
                    grounds = pygame.sprite.Group()
                    spikes = pygame.sprite.Group()
                    slimes = pygame.sprite.Group()
                    birbs_list = []

                    slime_count = 0
                    slime = None

                    background1 = Background(0)
                    backgrounds.add(background1)

                    background2 = Background(SCREEN_WIDTH - 10)
                    backgrounds.add(background2)

                    ground1 = Ground([0, 510])
                    grounds.add(ground1)

                    health_filled = 3
                    health_list = []
                    invinc = False

                    # Classes Initialization
                    player = Player()

                    for i in range(player.max_health):
                        health_list.append(Health(i))

                    end_game = False

            # Stop the game when window X is pressed
            if event.type == QUIT:
                quit()

        screen.fill((0, 0, 0))
        screen.blit(end_screen, (0, 0))

        text = font.render("You died.", True, (0, 0, 0))
        screen.blit(text, (SCREEN_WIDTH / 2 - text.get_width() / 2 + 100, SCREEN_HEIGHT / 2 -
                           text.get_height() / 2 - .5 * text.get_height()))
        text = font.render("Press Space to Play Again.", True, (0, 0, 0))
        screen.blit(text, (SCREEN_WIDTH / 2 - text.get_width() / 2 + 100, SCREEN_HEIGHT / 2 -
                           text.get_height() / 2 + .5 * text.get_height()))
        text = font.render(f"You killed", True, (255, 255, 255))
        screen.blit(text, (SCREEN_WIDTH - 45 - text.get_width(), 10))
        text = font.render(f"{player.slimes_killed} Simes.", True, (255, 255, 255))  # Sime is the name of the Slime
        screen.blit(text, (SCREEN_WIDTH - 45 - text.get_width(), 10 + text.get_height()))

    # Update the display
    pygame.display.flip()

    # Ensure program maintains a rate of 120 frames per second
    clock.tick(120)

# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
# Sime is the name of the Slime
