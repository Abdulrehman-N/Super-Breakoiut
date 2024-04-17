'''
Abdulrehman Nakhuda
November 7, 2022
Description: A completere Super breakout with extra features such as:
restarting and switching between singleplayer and multiplayer.
'''


# I - IMPORT AND INITIALIZE
import pygame, breakoutsprites
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1280,720))

# Create a list of Joystick objects.
joysticks = []
for joystick_no in range(pygame.joystick.get_count()):
    stick = pygame.joystick.Joystick(joystick_no)
    stick.init()
    joysticks.append(stick)
#Main game loop
def main():
    '''This function defines the 'mainline logic' for our pyPong game.'''

    # DISPLAY
    pygame.display.set_caption("Super Breakout")

    # ENTITIES
    rows=6
    cols=18
    color=(255,255,255)
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((46, 51, 47))
    screen.blit(background, (0, 0))
    bricks = []
    for row in range(rows):
        for col in range(cols):
            if row==0:
                color=(143, 0, 255)
            elif row==1:
                color=(255,0,0)
            elif row==2:
                color=(237, 237, 69)
            elif row==3:
                color=(227, 182, 57)
            elif row==4:
                color=(44, 212, 78)
            elif row==5:
                color=(0,0,255)
            bricks.append(breakoutsprites.Brick(screen,color,col,row))
            blocks = pygame.sprite.Group(bricks)

    # Sprites for: ScoreKeeper label, End Zones, Ball, and Players,End text sprites
    numberblocks=108
    score_keeper = breakoutsprites.ScoreKeeper()
    ball = breakoutsprites.Ball(screen,1,(191, 67, 63))
    ball2 = breakoutsprites.Ball(screen,2,(116, 114, 219))
    player1 = breakoutsprites.Player(screen, 1)
    player2 = breakoutsprites.Player(screen, 2)
    winner=breakoutsprites.Win(screen,"Game Over",150,1)
    retry=breakoutsprites.Win(screen,"Press space to retry",80,2)
    change=breakoutsprites.Win(screen,"Press c to change to singleplayer.",50,3)
    player_endzone = breakoutsprites.EndZone(screen,screen.get_height())
    allSprites = pygame.sprite.Group(score_keeper, player_endzone, ball,ball2, player1,player2,blocks)
    #Music entities
    pygame.mixer.music.load("breakoutbg.mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)
    lifelose=pygame.mixer.Sound("lifelose.wav")
    bounce=pygame.mixer.Sound("bouncey.mp3")
    blockhit=pygame.mixer.Sound("collect.wav")
    blockhit.set_volume(0.2)

# ASSIGN
    clock = pygame.time.Clock()
    keepGoing = True

    # Hide the mouse pointer
    pygame.mouse.set_visible(False)
    #Barriers
    pygame.draw.rect(screen,(128, 36, 117),((0,screen.get_height()-100),(46,50)),width=0)
    pygame.draw.rect(screen,(190, 231, 232),((screen.get_width()-46,screen.get_height()-100),(46,50)),width=0)
    pygame.draw.rect(screen,(137, 140, 138),((0,50),(46,screen.get_height()-120)),width=0)
    pygame.draw.rect(screen,(137, 140, 138),((0,50),(screen.get_width(),50)),width=0)
    pygame.draw.rect(screen,(137, 140, 138),((screen.get_width()-46,50),(46,screen.get_height()-120)),width=0)

    # LOOP
    while keepGoing:

        # TIME
        clock.tick(30)

        # EVENT HANDLING: Player 1 uses joystick, Player 2 uses arrow keys
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.JOYHATMOTION:
                if event.joy==0:
                    if event.value==(1,0):
                        player2.change_direction((-1,0))
                    elif event.value==(-1,0):
                        player2.change_direction((1,0))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player1.change_direction((1,0))
                elif event.key == pygame.K_RIGHT:
                    player1.change_direction((-1,0))
                elif event.key == pygame.K_SPACE and score_keeper.lose(blocks):
                    main()#Restart game
                elif event.key == pygame.K_c and score_keeper.lose(blocks):
                    main2()#Change to singleplayer

        # Check if players scores (i.e., ball hits player 1 endzone)
        if ball.rect.colliderect(player_endzone):
            score_keeper.lifeLoose()
            bounce.play(0)
            lifelose.play(0)
            ball.change_direction()
        if ball2.rect.colliderect(player_endzone):
            score_keeper.lifeLoose()
            bounce.play(0)
            lifelose.play(0)
            ball2.change_direction()


        # Check if ball hits Player 1 or 2
        # If so, change direction
        if ball.rect.colliderect(player1.rect) or ball.rect.colliderect(player2.rect):
            bounce.play(0)
            ball.change_direction()
        if ball2.rect.colliderect(player1.rect) or ball2.rect.colliderect(player2.rect):
            bounce.play(0)
            ball2.change_direction()
        if pygame.sprite.spritecollide(ball,blocks,True):
            blockhit.play(0)
            places=numberblocks-len(blocks)
            numberblocks-=places
            for i in range(places):
                for b in blocks:
                    b.go_down()
            score_keeper.player1_scored()
            ball.change_direction()
        if pygame.sprite.spritecollide(ball2,blocks,True):
            blockhit.play(0)
            places=numberblocks-len(blocks)
            numberblocks-=places
            for i in range(places):
                for b in blocks:
                    b.go_down()
            score_keeper.player1_scored()
            ball2.change_direction()
        # Check for game over (if a player loses 3 lives or finishes game)
        if score_keeper.lose(blocks):
            pygame.mixer.music.fadeout(2000)
            allSprites.clear(screen, background)
            allSprites.update()
            allSprites.draw(screen)
            allSprites=pygame.sprite.Group(winner,retry,change)

        #Checks if the score is half, if so, cuts the players in half.
        if len(blocks)==len(bricks)//2:
            player1.half(screen,1)
            player2.half(screen,2)

        # REFRESH SCREEN
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()

    # Unhide the mouse pointer
    pygame.mouse.set_visible(True)


# Call the main function

#Singleplayer main
def main2():
    '''This function defines the 'mainline logic' for our pyPong game.'''

    # DISPLAY
    pygame.display.set_caption("Super Breakout")

    # ENTITIES
    rows=6
    cols=18
    color=(255,255,255)
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((46, 51, 47))
    screen.blit(background, (0, 0))
    bricks = []
    for row in range(rows):
        for col in range(cols):
            if row==0:
                color=(143, 0, 255)
            elif row==1:
                color=(255,0,0)
            elif row==2:
                color=(237, 237, 69)
            elif row==3:
                color=(227, 182, 57)
            elif row==4:
                color=(44, 212, 78)
            elif row==5:
                color=(0,0,255)
            bricks.append(breakoutsprites.Brick(screen,color,col,row))
            blocks = pygame.sprite.Group(bricks)

    # Sprites for: ScoreKeeper label, End Zones, Ball, and Players
    numberblocks=108
    score_keeper = breakoutsprites.ScoreKeeper()
    ball = breakoutsprites.Ball(screen,1,(191, 67, 63))
    player1 = breakoutsprites.Player(screen, 1)
    winner=breakoutsprites.Win(screen,"Game Over",150,1)
    retry=breakoutsprites.Win(screen,"Press space to retry",80,2)
    change=breakoutsprites.Win(screen,"Press c to change to multiplayer.",50,3)
    player_endzone = breakoutsprites.EndZone(screen,screen.get_height())
    allSprites = pygame.sprite.Group(score_keeper, player_endzone, ball, player1,blocks)
    #Music entities
    pygame.mixer.music.load("breakoutbg.mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)
    lifelose=pygame.mixer.Sound("lifelose.wav")
    bounce=pygame.mixer.Sound("bouncey.mp3")
    blockhit=pygame.mixer.Sound("collect.wav")
    blockhit.set_volume(0.2)

# ASSIGN
    clock = pygame.time.Clock()
    keepGoing = True

    # Hide the mouse pointer
    pygame.mouse.set_visible(False)
    #Barriers
    pygame.draw.rect(screen,(128, 36, 117),((0,screen.get_height()-100),(46,50)),width=0)
    pygame.draw.rect(screen,(190, 231, 232),((screen.get_width()-46,screen.get_height()-100),(46,50)),width=0)
    pygame.draw.rect(screen,(137, 140, 138),((0,50),(46,screen.get_height()-120)),width=0)
    pygame.draw.rect(screen,(137, 140, 138),((0,50),(screen.get_width(),50)),width=0)
    pygame.draw.rect(screen,(137, 140, 138),((screen.get_width()-46,50),(46,screen.get_height()-120)),width=0)

    # LOOP
    while keepGoing:

        # TIME
        clock.tick(30)

        # EVENT HANDLING: Player 1 uses joystick, Player 2 uses arrow keys
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player1.change_direction((1,0))
                elif event.key == pygame.K_RIGHT:
                    player1.change_direction((-1,0))
                elif event.key == pygame.K_SPACE and score_keeper.lose(blocks):
                    main2()#Restart game
                elif event.key == pygame.K_c and score_keeper.lose(blocks):
                    main()#Switch to multiplayer

        # Check if players scores (i.e., ball hits player 1 endzone)
        if ball.rect.colliderect(player_endzone):
            score_keeper.lifeLoose()
            bounce.play(0)
            lifelose.play(0)
            ball.change_direction()


        # Check if ball hits Player 1 or 2
        # If so, change direction
        if ball.rect.colliderect(player1.rect):
            bounce.play(0)
            ball.change_direction()
        if pygame.sprite.spritecollide(ball,blocks,True):
            blockhit.play(0)
            places=numberblocks-len(blocks)
            numberblocks-=places
            for i in range(places):
                for b in blocks:
                    b.go_down()
            score_keeper.player1_scored()
            ball.change_direction()
        # Check for game over (if a player loses 3 lives or finishes game)
        if score_keeper.lose(blocks):
            pygame.mixer.music.fadeout(2000)
            allSprites.clear(screen, background)
            allSprites.update()
            allSprites.draw(screen)
            allSprites=pygame.sprite.Group(winner,retry,change)

        #Cuts the players in half
        if len(blocks)==len(bricks)//2:
            player1.half(screen,1)

        # REFRESH SCREEN
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()

    # Unhide the mouse pointer
    pygame.mouse.set_visible(True)


# Call the main function
main()
