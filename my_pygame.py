# Third party libraries
import random

# Import my code
from circle import Circle
from blob import Blob

# Import and initialize PyGame
import pygame
pygame.init()


CANVAS_WIDTH_HEIGHT = 600
AGENT_AREA_WIDTH_HEIGHT = 400
AGENT_AREA_RANGE = {"LOWER" : (CANVAS_WIDTH_HEIGHT - AGENT_AREA_WIDTH_HEIGHT) / 2,
					"UPPER" : (CANVAS_WIDTH_HEIGHT - AGENT_AREA_WIDTH_HEIGHT) / 2 + AGENT_AREA_WIDTH_HEIGHT}
BACKGROUND_COLOR = (10, 10, 10)
AGENT_AREA_COLOR = (50, 50, 50)
N_BLOBS = 20
FPS = 60
clock = pygame.time.Clock()

# Set up the drawing window
screen = pygame.display.set_mode([CANVAS_WIDTH_HEIGHT, CANVAS_WIDTH_HEIGHT])

my_circle = Circle(15, (100, 100, 200), 0)
blobs = []
for i in range(N_BLOBS):
	blob_radius = random.randrange(10, 30)
	blob_color = (240, 140, 120)
	blob_id = i
	blobs.append(Blob(blob_radius, blob_color, blob_id))

# Run until the user asks to quit
running = True
while running:
	# Did the user click the window close button?
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	# Fill the background with light gray
	screen.fill(BACKGROUND_COLOR)
	pygame.draw.rect(screen, AGENT_AREA_COLOR, (100, 100,
					 AGENT_AREA_WIDTH_HEIGHT, AGENT_AREA_WIDTH_HEIGHT))

	# Draw a solid blue circle in the center
	my_circle.move()
	my_circle.display(screen)
	for blob in blobs:
		blob.collide(blobs)
		blob.move()
		blob.display(screen)

	# Flip the display
	pygame.display.flip()

	pygame.display.update()
	clock.tick(FPS)

# Done! Time to quit.
pygame.quit()

##def say_something():
	##print("Time to say goodbye, darling...")
