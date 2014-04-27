from livewires import games, color

games.init(screen_width = 640, screen_height = 480, fps = 50)

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
             
class Game(object):
    BACKGROUND = games.load_image("images/background.png", transparent=False)
    def __init__(self):
        games.screen.background = Game.BACKGROUND
        platform = Platform(x = games.screen.width/2-85,
                            y = games.screen.height/2,
                            direction = "HORIZONTAL",
                            hrd = 1,
                            num = 3)
                          
        platform.activate()
        games.screen.mainloop()
#The main body of the program
def main():
    gm = Game()
#Kick it off!
main()
