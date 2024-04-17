import pygame, random


class Ball(pygame.sprite.Sprite):
    '''This class defines the sprite for our Ball.'''
    def __init__(self, screen,num,color):
        '''This initializer takes a screen surface as a parameter, initializes
        the image and rect attributes, and x,y direction of the ball.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)

        # Set the image and rect attributes for the Ball
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0,0,0))
        self.__color=color
        pygame.draw.circle(self.image, self.__color, (10, 10), 10, 0)
        self.rect = self.image.get_rect()
        self.rect.center = (screen.get_width()/2,screen.get_height()/2)

        # Instance variables to keep track of the screen surface
        # and set the initial x and y vector for the ball.
        self.__screen = screen
        if num==1:
            self.__dx = 5
            self.__dy = 3
        elif num==2:
            self.__dx = -5
            self.__dy = -3

    def change_direction(self):
        '''This method causes the x direction of the ball to reverse.'''
        self.__dy = -self.__dy

    def update(self):
        '''This method will be called automatically to reposition the
        ball sprite on the screen.'''
        # Check if we have reached the left or right end of the screen.
        # If not, then keep moving the ball in the same x direction.
        if ((self.rect.left > 50) and (self.__dx < 0)) or ((self.rect.right < self.__screen.get_width()-50) and (self.__dx > 0)):
            self.rect.left += self.__dx
        # If yes, then reverse the x direction.
        else:
            self.__dx = -self.__dx

        # Check if we have reached the top or bottom of the court.
        # If not, then keep moving the ball in the same y direction.
        if ((self.rect.top-40 > 62) and (self.__dy > 0)) or ((self.rect.bottom < self.__screen.get_height()) and (self.__dy < 0)):
            self.rect.top -= self.__dy
        # If yes, then reverse the y direction.
        else:
            self.__dy = -self.__dy


class Player(pygame.sprite.Sprite):
    '''This class defines the sprite for Player 1 and Player 2'''
    def __init__(self, screen, player_num):
        '''This initializer takes a screen surface, and player number as
        parameters.  Depending on the player number it loads the appropriate
        image and positions it on the left or right end of the court'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)

        # Define the image attributes for a black rectangle.
        self.__sizex=200
        self.__sizey=15
        self.image = pygame.Surface((self.__sizex,self.__sizey))
        self.image = self.image.convert()
        self.image.fill((128, 36, 117))
        self.rect = self.image.get_rect()

        # If we are initializing a sprite for player 1,
        if player_num==1:
            self.rect.right = screen.get_width()//2
            self.rect.top = screen.get_height()-65
            self.__screen = screen
            self.__dx = 0
        if player_num==2:
            self.image.fill((190, 231, 232))
            self.rect.right = screen.get_width()//2
            self.rect.top = screen.get_height()-45
            self.__screen = screen

            self.__dx = 0
        # position it 10 pixels from screen left.


    def change_direction(self, xy_change):
        '''This method takes a (x,y) tuple as a parameter, extracts the
        y element from it, and uses this to set the players x direction.'''
        self.__dx = xy_change[0]

    def half(self,screen,player_num):
        self.__sizex=100
        self.__sizey=15
        self.image = pygame.Surface((self.__sizex,self.__sizey))
        self.image = self.image.convert()
        self.image.fill((128, 36, 117))
        self.rect = self.image.get_rect()

        # If we are initializing a sprite for player 1,
        if player_num==1:
            self.rect.right = screen.get_width()//2
            self.rect.top = screen.get_height()-65
            self.__screen = screen
            self.__dx = 0
        if player_num==2:
            self.image.fill((190, 231, 232))
            self.rect.right = screen.get_width()//2
            self.rect.top = screen.get_height()-45
            self.__screen = screen

            self.__dx = 0

    def update(self):
        '''This method will be called automatically to reposition the
        player sprite on the screen.'''
        # Check if we have reached the top or bottom of the screen.
        # If not, then keep moving the player in the same y direction.
        if ((self.rect.left > 50) and (self.__dx > 0)) or ((self.rect.right < self.__screen.get_width()-50) and (self.__dx < 0)):
            self.rect.left -= (self.__dx*5)
        # If yes, then we don't change the y position of the player at all.

class EndZone(pygame.sprite.Sprite):
    '''This class defines the sprite for our left and right end zones'''
    def __init__(self, screen, x_position):
        '''This initializer takes a screen surface, and x position  as
        parameters.  For the left (player 1) endzone, x_position will = 0,
        and for the right (player 2) endzone, x_position will = 639.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)

        # Our endzone sprite will be a 1 pixel wide black line.
        self.image = pygame.Surface((screen.get_width(), 1))
        self.image = self.image.convert()
        self.image.fill((0, 0, 0))

        # Set the rect attributes for the endzone
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.top = x_position


class ScoreKeeper(pygame.sprite.Sprite):
    '''This class defines a label sprite to display the score.'''
    def __init__(self):
        '''This initializer loads the system font "Arial", and
        sets the starting score to 0:0'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)

        # Load our custom font, and initialize the starting score.
        self.__font = pygame.font.Font("Pixeboy.ttf", 50)
        self.__player1_score = 0
        self.__life = 3

    def player1_scored(self):
        '''This method adds one to the score for player 1'''
        self.__player1_score += 1
    def lifeLoose(self):
        '''This method adds one to the score for player 1'''
        self.__life -=1

    def lose(self,blocks):
        '''There is a winner when one player reaches 3 points.
        This method returns 0 if there is no winner yet, 1 if player 1 has
        won, or 2 if player 2 has won.'''
        if not blocks or self.__life==0:
            return 1
        else:
            return 0

    def update(self):
        '''This method will be called automatically to display
        the current score at the top of the game window.'''
        self.__message = "Score: %d                            Lives: %d" % (self.__player1_score,self.__life)
        self.image = self.__font.render(self.__message, 1, (232, 190, 209))
        self.rect = self.image.get_rect()
        self.rect.center = (300, 30)
class Win(pygame.sprite.Sprite):
    '''This class displays the end screen'''
    def __init__(self,screen,message,size,num):
        pygame.sprite.Sprite.__init__(self)
        self.__font = pygame.font.Font("Pixeboy.ttf", size)
        self.__message = message
        if num==1:
            self.image = self.__font.render(self.__message, 1, (212, 108, 155))
            self.rect = self.image.get_rect()
            self.rect.center = (screen.get_width()//2,screen.get_height()//2)
        elif num==2:
            self.image = self.__font.render(self.__message, 1, (232, 232, 232))
            self.rect = self.image.get_rect()
            self.rect.center = (screen.get_width()//2,(screen.get_height()//2)+150)
        elif num==3:
            self.image = self.__font.render(self.__message, 1, (232, 232, 232))
            self.rect = self.image.get_rect()
            self.rect.center = (screen.get_width()//2,(screen.get_height()//2)+250)

class Brick(pygame.sprite.Sprite):
     '''Our Bricks class inherits from the Sprite class'''
     def __init__(self, screen,color,col,row):
          # Call the parent __init__() method
          pygame.sprite.Sprite.__init__(self)

          # Set the image and rect attributes for the bricks

          self.__width=((screen.get_width()-100)//18)+1
          self.__height=30
          self.__x=self.__width*col
          self.__y=100+self.__height*row

          self.image=pygame.Surface((self.__width,self.__height))
          self.image.fill((color))
          self.rect=self.image.get_rect()
          self.rect.left=46+self.__x
          self.rect.top=self.__y
     def go_down(self):
          '''This method makes the bricks go down.'''
          self.rect.top+=2
