import pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Punch Demo")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (100, 100, 100)

# Player 1 setup
p1_x = 100
p1_y = 550
p1_width = 50
p1_height = 50
p1_facing = "right"

# Player 2 setup
p2_x = 400
p2_y = 550
p2_width = 50
p2_height = 50
p2_vel_x = 0

# bounding box collision (used here for the arm)
def is_colliding(ax, ay, aw, ah, bx, by, bw, bh):
    return (
        ax < bx + bw and
        ax + aw > bx and
        ay < by + bh and
        ay + ah > by
    )

clock = pygame.time.Clock()
running = True

while running: #GAME LOOP#####################################
    clock.tick(60) #FPS

    #input section--------------------------
    
    #event queue: look for keyboard presses, mouse clicks, etc
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #handle keyboard input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        p1_x -= 5
        p1_facing = "left"
        
    if keys[pygame.K_RIGHT]:
        p1_x += 5
        p1_facing = "right"
    
    if keys[pygame.K_z]:
        punch_arm = True #boolean value to check if user has pressed z
    else:
        punch_arm = False


    #physics/update section---------------------------
    
    #check if punching is activated
    if punch_arm == True:
        if p1_facing == "right":
            arm_x = p1_x + p1_width #if facing right, draw arm to the right
        else:
            arm_x = p1_x - 20 #otherwise draw it facing to the left        
        arm_y = p1_y + p1_height // 2 - 10 #set "arm's" height to the middle of the player (adjust based on sprite image)
        
        #check collision with player 2
        if is_colliding(arm_x, arm_y, 20, 20, p2_x, p2_y, p2_width, p2_height):
            if p1_facing == "right":
                p2_vel_x = 10 # if hit from the left, move backwards 10 pixels
            else:
                p2_vel_x = -10 # if hit from behind, move forwards 10 pixels
                
    
    #update p2's position based on velocity and friction
    p2_x += p2_vel_x
    p2_vel_x *= 0.9 #friction: change this number to make them slide more or less

    #RENDER SECTION------------------------------------------------
    screen.fill(WHITE)
    
    pygame.draw.rect(screen, BLUE, (p1_x, p1_y, p1_width, p1_height)) #draw player1
    pygame.draw.rect(screen, RED, (p2_x, p2_y, p2_width, p2_height)) #draw player2
    if punch_arm:
        pygame.draw.rect(screen, GRAY, (arm_x, arm_y, 20, 20)) #draw "arm"

    pygame.display.flip()

pygame.quit()

