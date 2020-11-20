import pygame, sys, random

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (300,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (300,random_pipe_pos - 150))
    return bottom_pipe, top_pipe

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
           hit_sound.play()
           #return False

    if bird_rect.top <= -50 or bird_rect.bottom >= 450:
        return False

    return True

def score_display(game_state):
    if game_state == 'playing':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (144,50))
        screen.blit(score_surface,score_rect)

        high_score_surface = pygame.font.Font('04B_19.ttf',14).render(f'High Score: {int(high_score)}',True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(topright = (280,5))
        screen.blit(high_score_surface,high_score_rect)

    if game_state == 'gameover':
        score_surface = game_font.render(f'Score: {int(score)}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (144,50))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}',True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (144,80))
        screen.blit(high_score_surface,high_score_rect)

pygame.mixer.pre_init(frequency = 44100, size = 8, channels = 1, buffer = 512)
pygame.init()

screen = pygame.display.set_mode((288,516))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf',20)

#game variables
gravity = 0.2
bird_movement = 0
game_active = False
score = 0
high_score = 0

bg_day_surface = pygame.image.load('assets/background-day.png').convert() #convert to help speed consistent 
    #if scale: bg_surface = pygame.transform.scale2x(bg_surface)
bg_night_surface = pygame.image.load('assets/background-night.png').convert()

floor_surface = pygame.image.load('assets/base.png').convert()
floor_x_pos = 0

bird_downflap = pygame.image.load('assets/bluebird-downflap.png').convert_alpha()
bird_midflap = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('assets/bluebird-upflap.png').convert_alpha()

# bird_downflap = pygame.image.load('assets/dut.png').convert_alpha()
# bird_midflap = pygame.image.load('assets/dut.png').convert_alpha()
# bird_upflap = pygame.image.load('assets/dut.png').convert_alpha()
bird_frames = [bird_downflap,bird_midflap,bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (50,256))    #create a rectangle around the bird to check for collision later

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200) #change bird state every 200ms

pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)  #pipe every 1300ms
pipe_height = [200, 250, 300, 350, 400]

game_over_surface = pygame.image.load('assets/message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (144,256))

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0   #disable gravity before every jump
                bird_movement -= 5.5
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (50,256)
                bird_movement = 0
                score = 0
                score_sound_countdown = 100

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe()) #create new pipe after each 1200ms

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

        #flipping wing
        bird_surface = bird_frames[bird_index]
        bird_rect = bird_surface.get_rect(center = (100,bird_rect.centery))
    
    if ((score > 10) and (score <20)) or (score > 30):
        screen.blit(bg_night_surface,(0,0))
    else:
        screen.blit(bg_day_surface, (0,0))

    if game_active:
        #bird
        bird_movement += gravity
        rotated_bird = pygame.transform.rotozoom(bird_surface,-bird_movement * 2,1)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,bird_rect)
        game_active = check_collision(pipe_list)

        #pipes
        for pipe in pipe_list:
            pipe.centerx -= 2.5
            
            if pipe.bottom >= 512:
                screen.blit(pipe_surface,pipe)
            else:
                flip_pipe = pygame.transform.flip(pipe_surface,False,True)  #flip top pipes
                screen.blit(flip_pipe,pipe)
        
        #display score
        score += 0.01
        score_display('playing')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_surface,game_over_rect)
        if score > high_score:
            high_score = score
        score_display('gameover')

    #floor
    floor_x_pos -= 1    #decrease after every reload to make movement
    screen.blit(floor_surface,(floor_x_pos,450))
    screen.blit(floor_surface,(floor_x_pos + 288,450))
    if floor_x_pos <= -288:
        floor_x_pos = 0     #infinite loop

    pygame.display.update()
    clock.tick(100)     #no more than 90 frames per second