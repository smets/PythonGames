from livewires import games, color

games.init(screen_width = 640, screen_height = 480, fps = 50)

class Level(object):
    def __init__(self):
        self.platforms = []
        self.coins = []
        self.enemies = []
        self.pharaoh = None
        self.pyramid = None
        self.distanceTravelled = 0
    #Define methods for adding Platforms, Pharaoh, Enemies, and Coins
    def addPlatform(self, plat):
        self.platforms.append(plat)
    def addPharaoh(self, phar):
        self.pharaoh = phar
    def addEnemy(self, enem):
        self.enemies.append(enem)
    def addCoin(self, cn):
        self.coins.append(cn)
    def setPyramid(self, x, y):
        self.pyramid = Pyramid(x = x, y = y, level = self)
    #define a method to set gravity for all objects
    def startGravity(self, grav):
        self.pharaoh.gravity = grav
        for enem in self.enemies:
            enem.gravity = grav
    #Create methods for activating, resetting, and deactivating the level
    def activateLevel(self):
        for plat in self.platforms:
            plat.activate()
        for coin in self.coins:
            coin.activate()
        for en in self.enemies:
            en.activate()
        self.pyramid.activate()
        self.pharaoh.activate()
    def resetLevel(self):
        for plat in self.platforms:
            plat.resetBy(self.distanceTravelled)
        for coin in self.coins:
            coin.x += self.distanceTravelled
            if coin.isCollected:
                self.pharaoh.score -= 1
                coin.activate()
        for en in self.enemies:
            en.x += self.distanceTravelled
        self.pyramid.x += self.distanceTravelled
        self.pharaoh.x = games.screen.width/2
        self.pharaoh.y = games.screen.height/2
        self.pharaoh.refreshScore()
        self.distanceTravelled = 0
    def deactivateLevel(self):
        self.pharaoh.destroy()
        self.pyramid.deactivate()
        for plat in self.platforms:
            plat.deactivate()
        for coin in self.coins:
            coin.deactivate()
        for en in self.enemies:
            en.deactivate()
    def moveLevel(self):
        if(self.pharaoh.y >= games.screen.height):
            self.pharaoh.lives -= 1;
            if self.pharaoh.lives > 0:
                self.resetLevel()
        if(self.pharaoh.x >= games.screen.width/2 and self.pharaoh.dx >= 0):
            self.pharaoh.x = games.screen.width/2
            for plat in self.platforms:
                for tile in plat.tiles:
                    tile.dx -= self.pharaoh.dx
            for coin in self.coins:
                coin.dx -= self.pharaoh.dx
            for en in self.enemies:
                en.dx -= self.pharaoh.dx
            self.pyramid.dx -= self.pharaoh.dx
            self.distanceTravelled += self.pharaoh.dx
    
class Coin(games.Sprite):
    #Load the Coin image
    IMAGE = games.load_image("images/coin.gif")
    #Define the init method
    def __init__(self, x, y):
        #Call games.Sprite's init method
        super(Coin, self).__init__(
            image = Coin.IMAGE,
            x = x, y = y)
        #set the isCollected variable to false--this way
        #we can quickly tell if the Coin has been collected
        self.isCollected = False
    #Define the activate and deactivate methods
    def activate(self):
        games.screen.add(self)
        self.isCollected = False
    def deactivate(self):
        self.destroy()
        self.isCollected = True
    #Define the update method
    def update(self):
        #Call games.Sprite's update method
        super(Coin, self).update()
        self.dx = 0
        #Check to see if the Pharaoh is touching the coin.
        #If so, remove the Coin and increase the score
        for sprite in self.overlapping_sprites:
            if isinstance(sprite, Pharaoh):
                sprite.score += 1
                sprite.refreshScore()
                self.deactivate()
                    

class Actor(games.Sprite):
    #This class will be the basis
    #for Pharaoh and Enemy
    def __init__(self, x, y, image):
        super(Actor, self).__init__(image = image, x = x, y = y)
        self.jumping = False
        self.gravity = 0
        self.lives = 1
    def update(self):
        super(Actor, self).update();
        if self.lives == 0:
            self.deactivate()
class Enemy(Actor):
    #Load the images for Enemy
    IMAGE_1 = games.load_image("images/enemy.png")#Face Left
    IMAGE_2 = games.load_image("images/enemy_back.png")#Face Right
    #Define the init method
    def __init__(self, x, y):
        super(Enemy, self).__init__(image = Enemy.IMAGE_1, x = x, y = y)
        self.mvSpeed = 0
        self.moving = False
    #Define the activate and deactivate methods
    def deactivate(self):
        self.destroy()
    def activate(self):
        games.screen.add(self)
    #Define the update method
    def update(self):
        #Call Actor's update method
        super(Enemy, self).update()
        #Refresh the velocity of the Enemy--necessary if the 
        self.dx = self.mvSpeed
        #If the sprite is close enough to the game screen, set
        #moving to True--we don't want Enemies at the end of the level
        #to start moving before we get there
        if self.x - games.screen.width <= 50:
            self.moving = True
        #Determine if the Enemy is in the air or on the ground;
        #Apply gravity if in the air
        if not self.overlapping_sprites:
            self.jumping = True
        if self.jumping:
            self.dy += self.gravity
        #if the Enemy is close enough to move, start moving to the left
        if self.moving:
            if self.mvSpeed == 0:
                self.mvSpeed = -1
        #Handle collision with the Pharaoh
        for sprite in self.overlapping_sprites:
            if isinstance(sprite, Pharaoh):
                if not self.spriteOnTop(sprite):
                    #if the Enemy hits the Pharaoh, Pharaoh loses a life
                    sprite.lives -= 1
                    sprite.game.level.resetLevel()
                    sprite.refreshLives()
                else:
                    #This will run if the Pharaoh 'stomps' on the Enemy
                    #In this case the Enemy gets hurt
                    self.lives -= 1
                    #Make the Pharaoh do a little 'hop' after
                    #he stomps the enemy
                    sprite.dy = -1
    def spriteOnTop(self, sprite):
        return sprite.bottom - self.top <= 7
        
    
class Pharaoh(Actor):
    """"The Main Character"""
    #Load in the images for Pharaoh
    #One each for facing Right, facing Left,
    #Walking Right, and Walking Left
    IMAGE1_R = games.load_image("images/pharaoh1.bmp")#Face Right
    IMAGE1_L = games.load_image("images/pharaoh1_Back.bmp")#Face Left
    IMAGE2_R = games.load_image("images/pharaoh2.bmp")#Walk Right
    IMAGE2_L = games.load_image("images/pharaoh2_Back.bmp")#Walk Left
    WALK_SPEED = 20#The rate at which the pharaoh appears to walk (in Frames)

    #Initializer
    def __init__(self, x, y, game):
        #Call the Actor's initializer
        super(Pharaoh, self).__init__(
            image = Pharaoh.IMAGE1_R,
            x = x, y = y)
        #Give Pharaoh a way to access the Game object; will be used later
        self.game = game
        #Initially, make the pharaoh face right
        #Slide1 is standing, slide2 is stepping
        self.slide1 = Pharaoh.IMAGE1_R
        self.slide2 = Pharaoh.IMAGE2_R
        #Remember whether the pharaoh is 'standing' or 'stepping'
        self.activeImage = 1
        #This will be used to determine when the sprite should change
        #slides in order to look like it's walking
        self.walkTimer = 0
        self.score = 0
        self.lives = 2
        self.scoreTxt = games.Text(value = "Coins: "+str(self.score),
                                   size = 35, color = color.black,
                                   top = 5, left = 10)
        self.livesTxt = games.Text(value = "Lives: "+str(self.lives),
                                   size = 35, color = color.black,
                                   top = 5, right = games.screen.width - 10)

    #define an activate and deactivate method
    def activate(self):
        games.screen.add(self)
        games.screen.add(self.scoreTxt)
        games.screen.add(self.livesTxt)
    def deactivate(self):
        self.end_game()
        self.game.level.deactivateLevel()
        self.destroy()
    #Define the end_game method
    def end_game(self):
        end_message = games.Message(value = "Game Over",
                                    size = 90,
                                    color = color.red,
                                    x = games.screen.width/2,
                                    y = games.screen.height/2,
                                    lifetime = 2 * games.screen.fps,
                                    after_death = games.screen.quit)
        games.screen.add(end_message)
    #define methods for updating the score and number of lives
    def refreshScore(self):
        self.scoreTxt.value = "Coins: "+str(self.score)
    def refreshLives(self):
        self.livesTxt.value = "Lives: "+str(self.lives)
        self.livesTxt.right = games.screen.width - 10
    #Define the Update method.  This will be called on every frame
    def update(self):
        #Call Actor's update method
        super(Pharaoh, self).update()

        #Is the sprite in the air? If so, apply gravity
        if not self.overlapping_sprites:
            self.jumping = True
        
        if self.jumping:
            self.dy += self.gravity
        
        #Keep the pharaoh in the bounds of the screen
        if(self.left <= 0):
            self.left = 0
        if(self.right >= games.screen.width):
            self.right = games.screen.width
        #Get keyboard input and make the pharaoh act appropriately
        if games.keyboard.is_pressed(games.K_LEFT):
            #Face left, start moving left, and increment the walkTimer
            self.faceLeft()
            self.dx = -1
            self.walkTimer = self.walkTimer +1
        elif games.keyboard.is_pressed(games.K_RIGHT):
            #Face right, start moving right, and increment the walkTimer
            self.faceRight()
            self.dx = 1
            self.walkTimer = self.walkTimer +1
        elif not self.jumping:
            #Not walking anymore; set walkTimer to 0 and
            #make the pharaoh 'stand' still by
            #changing the active Image to slide 1
            self.walkTimer = 0
            self.activeImage = 1
            self.image = self.slide1
            self.dx = 0
        #Jump when the spacebar is pressed
        if games.keyboard.is_pressed(games.K_SPACE):
            if not self.jumping:
                self.dy = -4
                self.jumping = True
                self.image = self.slide2
            
        #Animate the pharaoh's walking
        if(self.walkTimer >= Pharaoh.WALK_SPEED):
            self.walkTimer = 0
            if(self.activeImage == 1):
                self.image = self.slide2
                self.activeImage = 2
            else:
                self.image = self.slide1
                self.activeImage = 1
        self.game.level.moveLevel()
    #define methods to make the Pharaoh face either right or left
    def faceLeft(self):
        self.slide1 = Pharaoh.IMAGE1_L
        self.slide2 = Pharaoh.IMAGE2_L
        self.refreshGraphic()
        
    def faceRight(self):
        self.slide1 = Pharaoh.IMAGE1_R
        self.slide2 = Pharaoh.IMAGE2_R
        self.refreshGraphic()

    #assign the proper 
    def refreshGraphic(self):
        if(self.activeImage == 1):
                self.image = self.slide1 
        else:
                self.image = self.slide2

class PlatformTile(games.Sprite):
    """A platform to stand on"""
    #Load the image for the sprite
    IMAGE = games.load_image("images/platform.png")
    
    #Initializer for PlatformTile
    def __init__(self, x, y, hrd):
        #call the original initializer in games.Sprite
        super(PlatformTile, self).__init__(
            image = PlatformTile.IMAGE,
            x = x, y = y)
        self.isHard = hrd

    #Define an activate and deactivate method
    def activate(self):
        games.screen.add(self)
    def deactivate(self):
        self.destroy()

    #Define a method that will determine if a sprite is standing on
    #top of PlatformTile--we will use this in the Update method
    def spriteOnTop(self, sprite):
        return sprite.bottom - self.top <= 7
    def spriteOnBottom(self, sprite):
        return self.bottom - sprite.top <= 7
    def spriteOnRight(self, sprite):
        return self.right - sprite.left <= 7
    def spriteOnLeft(self, sprite):
        return sprite.right - self.left <= 7
    #Define the update method; here we will handle
    #collisions between PlatformTile and other sprites
    def update(self):
        super(PlatformTile, self).update()
        self.dx = 0
        #Loop through the overlapping sprites
        for sprite in self.overlapping_sprites:
            #We only want to handle collisions with Actor sprites
            if isinstance(sprite, Actor):
                #Check to see if the sprite is standing on top of the tile
                if self.spriteOnTop(sprite) and sprite.dy >= 0:
                    #if so, set the sprite's bottom to the very top of the tile
                    sprite.bottom=self.top
                    sprite.jumping = False
                #if the sprite is not on top, is this a 'hard' or 'soft' tile?
                elif self.isHard == True:
                    #If so, check to see if the sprite is coming from the left,
                    #right, or bottom, and stop the sprite
                    if not self.spriteOnTop(sprite):
                        if self.spriteOnLeft(sprite):
                            sprite.right = self.left
                        elif self.spriteOnRight(sprite):
                            sprite.left = self.right
                        elif self.spriteOnBottom(sprite):
                            sprite.top = self.bottom
                            sprite.dy = -sprite.dy
                        #Is the sprite a Pharaoh or Enemy? We handle that
                        #a little differently
                        if isinstance(sprite, Enemy):
                                sprite.mvSpeed = sprite.mvSpeed * -1
                                if self.left == sprite.right:
                                    sprite.x -= 1
                                    sprite.image = Enemy.IMAGE_1
                                if self.right == sprite.left:
                                    sprite.x += 1
                                    sprite.image = Enemy.IMAGE_2
    
class Platform(object):
    """Several platform tiles together"""
    #this is a collection of PlatformTiles
    
    #initializer
    def __init__(self, x, y, direction, hrd, num):
        #define an array of tiles
        self.tiles = []
        #Generate the tiles according to the parameters passed in the
        #initializer
        for i in range(0,num):
            xval = x
            yval = y
            #Generate a horizontal platform or a column, depending on
            #the value of direction.
            #Determine the x and y value of a tile in the platform
            if direction == "HORIZONTAL":
                xval = x + 85 * i
            else:
                yval = y + 65 * i
            #generate the tile and add it to the array
            plat = PlatformTile( x = xval, y = yval, hrd = hrd);
            self.tiles.append(plat)

    #Define the activate and deactivate methods
    def activate(self):
        for plat in self.tiles:
            plat.activate()
            
    def deactivate(self):
        for plat in self.tiles:
            plat.deactivate()
    #define a method to reset the platform to a previous position
    def resetBy(self, resetDistance):
        for plat in self.tiles:
            plat.x += resetDistance
class Pyramid(games.Sprite):
    IMAGE = games.load_image("images/pyramid.png")
    def __init__(self, x, y, level):
        super(Pyramid, self).__init__(image = Pyramid.IMAGE, x = x, y = y)
        self.level = level
    def activate(self):
        games.screen.add(self)
    def deactivate(self):
        self.destroy()
    def update(self):
        super(Pyramid, self).update()
        self.dx = 0
        for sprite in self.overlapping_sprites:
            if isinstance(sprite, Pharaoh):
                if sprite.x >= self.x:
                    self.level.nextLevel()
class LevelOne(Level):
    def __init__(self, pharaoh, game):
        super(LevelOne, self).__init__()
        self.game = game
        self.addPharaoh(pharaoh)
        self.addPlatform(Platform(x = 42,
                            y = games.screen.height,
                            direction = "HORIZONTAL",
                            hrd = True,
                            num = 20))
        self.addPlatform(Platform(x = 42,
                         y = games.screen.height - 60,
                         direction = "VERTICAL",
                         hrd = True,
                         num = 1))
        self.addPlatform(Platform(x = games.screen.width - 42,
                         y = games.screen.height - 60,
                         direction = "VERTICAL",
                         hrd = True,
                         num = 1))
        self.setPyramid(x = games.screen.width + 250,
                        y = games.screen.height/2 + 25)
        self.addPharaoh(self.pharaoh)
        self.addEnemy(Enemy(x = games.screen.width - 10,
                      y = games.screen.height/2))
        self.addCoin(Coin(x = games.screen.width/2+100,
                    y = 200))
        
    def activate(self):
        self.startGravity(.05)
        self.activateLevel()
    def nextLevel(self):
        self.pharaoh.x = games.screen.width/2
        self.pharaoh.y = games.screen.height/2
        self.pharaoh.dy = 0
        self.pharaoh.dx = 0
        self.deactivateLevel()
        self.game.level = LevelOne(game = self.game, pharaoh = self.pharaoh)
        self.game.level.activate()
class Game(object):
    BACKGROUND = games.load_image("images/background.png",transparent=False);
    def __init__(self):
        games.screen.background = Game.BACKGROUND;
        self.pharaoh = Pharaoh(x = games.screen.width/2,
                               y = games.screen.height/2,
                               game = self)
        self.level = LevelOne(pharaoh = self.pharaoh, game = self)
        self.level.activate()
        games.screen.mainloop()


 
#The main body of the program            
def main():
    gm = Game()

#Kick it off!
main()
