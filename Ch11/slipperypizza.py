# New Graphics Window
# Demonstrates creating a graphics window

from livewires import games
import random

games.init(screen_width = 640, screen_height = 480, fps = 50)

class Pizza(games.Sprite):
    def update(self):
        if self.right > games.screen.width or self.left < 0:
            self.dx = -self.dx
        if self.bottom > games.screen.height or self.top < 0:
            self.dy = -self.dy
    def handle_collide(self):
        self.x = random.randrange(games.screen.width)
        self.y = random.randrange(games.screen.height)
    
class Pan(games.Sprite):
    def update(self):
        self.x = games.mouse.x
        self.y = games.mouse.y
        self.check_collide()

    def check_collide(self):
        for pizza in self.overlapping_sprites:
            pizza.handle_collide()
def main():

    wall_image = games.load_image("wall.jpg", transparent = False)
    games.screen.background = wall_image

    pizza_image = games.load_image("pizza.bmp")
    pizza = Pizza(image = pizza_image, x = 320, y = 240, dx = 1, dy = 1)
    games.screen.add(pizza)

    pan_image = games.load_image("pan.bmp")
    the_pan = Pan(image = pan_image, x = games.mouse.x, y = games.mouse.y)
    games.screen.add(the_pan)
    games.mouse.is_visible = False
    games.screen.event_grab = True

    games.screen.mainloop()
#Kick it off
main();

input("Press enter to quit...")
