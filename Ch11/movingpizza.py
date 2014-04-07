# New Graphics Window
# Demonstrates creating a graphics window

from livewires import games

class Pizza(games.Sprite):
    def update(self):
        if self.right > games.screen.width or self.left < 0:
            self.dx = -self.dx
        if self.bottom > games.screen.height or self.top < 0:
            self.dy = -self.dy
    
def main():
    games.init(screen_width = 640, screen_height = 480, fps = 50)

    wall_image = games.load_image("wall.jpg", transparent = False)
    games.screen.background = wall_image

    pizza_image = games.load_image("pizza.bmp")
    pizza = Pizza(image = pizza_image, x = 320, y = 240, dx = 1, dy = 1)
    games.screen.add(pizza)

    games.screen.mainloop()
#Kick it off
main();

input("Press enter to quit...")
