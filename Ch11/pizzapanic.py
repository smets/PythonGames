# New Graphics Window
# Demonstrates creating a graphics window

from livewires import games, color
import random

games.init(screen_width = 640, screen_height = 480, fps = 50)

class Pizza(games.Sprite):
    #In Pizza, I added pizzasDropped to and a few other elements to keep track
    #of the numbers of pizzas not saved--the game ends after 5 pizzas have not
    #been caught
    image = games.load_image("pizza.bmp")
    speed = 1
    pizzasDropped = 0
    pizzasDroppedTxt = games.Text(value = "Fails Remaining: ",
                                  size = 25,
                                  color = color.black,
                                  top = 5,
                                  left = 0)
    pizzasDroppedNum = games.Text(value = 5,
                                  size = 25,
                                  color = color.black,
                                  top = 5,
                                  left = pizzasDroppedTxt.right + 5)
    games.screen.add(pizzasDroppedTxt)
    games.screen.add(pizzasDroppedNum)
    def __init__(self, x, y = 90):
        super(Pizza, self).__init__(image = Pizza.image,
                                    x = x, y = y, dy = Pizza.speed)
        
    def update(self):
        if self.bottom > games.screen.height:
            if Pizza.pizzasDropped == 4:
                self.end_game()
            else:
                Pizza.pizzasDropped += 1
                Pizza.pizzasDroppedNum.value -= 1
                self.destroy()
    def handle_caught(self):
        self.destroy()
    def end_game(self):
        end_message = games.Message(value = "Game Over",
                                    size = 90,
                                    color = color.red,
                                    x = games.screen.width/2,
                                    y = games.screen.height/2,
                                    lifetime = 2 * games.screen.fps,
                                    after_death = games.screen.quit)
        games.screen.add(end_message)
class Chef(games.Sprite):
    #I didn't look at the tutorial for a few of the methods in Chef, like
    #how it's supposed to spawn pizzas.  I also added some functionality
    #so over time Chef will drop pizzas more frequently
    #and move faster, and the odds of direction change, change randomly
    image = games.load_image("chef.bmp")
    def __init__(self,y=55, speed = 2, odds_change = 200):
        super(Chef, self).__init__(image = Chef.image, x=games.screen.width/2,
                               y=y, dx = speed)
        self.counter = 0.0
        self.odds_change = odds_change
        self.dropSpeed = 2.0
        self.totalTime = 0.0;
    def update(self):
        if self.left < 0:
            self.left = 0
            self.dx = -self.dx
        elif self.right > games.screen.width:
            self.right = games.screen.width
            self.dx = -self.dx
        elif random.randrange(self.odds_change) == 0:
            self.dx = -self.dx
        self.counter += 1
        if(self.counter / games.screen.fps > self.dropSpeed):
            self.spawn_pizza()
            self.totalTime += (self.counter / games.screen.fps)
            self.counter = 0

        if self.totalTime >= 5:
            
            self.totalTime = 0
            self.dropSpeed = self.dropSpeed * .9
            self.odds_change = random.randrange(250)
            self.dx = self.dx * 1.2
    def spawn_pizza(self):
        games.screen.add(Pizza(x = self.x))
        
class Pan(games.Sprite):
    image = games.load_image("pan.bmp")
    def __init__(self):
        super(Pan, self).__init__(image = Pan.image, x = games.mouse.x,
                                  bottom = games.screen.height)
        self.score = games.Text(value = 0, size = 25, color = color.black,
                                top = 5, right = games.screen.width - 10)
        games.screen.add(self.score)
    def update(self):
        self.x = games.mouse.x
        if self.left < 0:
           self.left = 0
        if self.right > games.screen.width:
           self.right = games.screen.width
        self.check_catch()

    def check_catch(self):
        for pizza in self.overlapping_sprites:
           self.score.value += 10
           self.score.right = games.screen.width - 10
           pizza.handle_caught()
def main():

    wall_image = games.load_image("wall.jpg", transparent = False)
    games.screen.background = wall_image

    the_chef = Chef()
    games.screen.add(the_chef)

    the_pan = Pan()
    games.screen.add(the_pan)
    games.mouse.is_visible = False
    games.screen.event_grab = True

    games.screen.mainloop()
#Kick it off
main();

