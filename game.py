import numpy as np
import pandas as pd

from keras.models import model_from_json
import pygame
pygame.font.init()
pygame.init()

WIN_WIDTH = 840
WIN_HEIGHT = 840
WHITE = (255,255,255)
BLACK = (0,0,0)
STAT_FONT = pygame.font.SysFont("comicsans", 50)

if __name__ == '__main__':

	with open("model.json", "r") as json_file:
	    model_json = json_file.read()
	model = model_from_json(model_json)
	model.load_weights('model.h5')

	win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
	drag = False
	while True:
		clock = pygame.time.Clock()
		clock.tick(30)
		done = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			elif event.type == pygame.KEYDOWN:
				win.fill(BLACK)

			elif event.type == pygame.MOUSEBUTTONDOWN:
				x,y = event.pos
				x = min(x-x%5,WIN_WIDTH - WIN_WIDTH//28)
				y = min(y-y%5,WIN_WIDTH - WIN_WIDTH//28)

				pygame.draw.rect(win, WHITE, (x, y, WIN_WIDTH//28, WIN_WIDTH//28))

				drag = True

			elif event.type == pygame.MOUSEBUTTONUP:
				drag = False
				done = True

			elif drag == True and event.type == pygame.MOUSEMOTION:
				x,y = event.pos
				x = min(x-x%5,WIN_WIDTH - WIN_WIDTH//28)
				y = min(y-y%5,WIN_WIDTH - WIN_WIDTH//28)
				
				pygame.draw.rect(win, WHITE, (x, y, WIN_WIDTH//28, WIN_WIDTH//28))

		pygame.display.update()

		if done:
			pixels = []
			test = []
			
			for y in range(0,WIN_WIDTH,WIN_WIDTH//28):
				row = []
				for x in range(0,WIN_WIDTH,WIN_WIDTH//28):
					val = 0
					for k in range(WIN_WIDTH//28):
						val += win.get_at((x+k, y+k))[0]
					row.append(val/(WIN_WIDTH//28))
					test.append(val/(WIN_WIDTH//28))
				pixels.append(row)

#			for y in range(28):
#				for x in range(28):
#					val = pixels[y][x]
#					pygame.draw.rect(win, (val,val,val),(x*(WIN_WIDTH//28), y*(WIN_WIDTH//28), (WIN_WIDTH//28), (WIN_WIDTH//28)))
					
			test = np.array(test)
			test = test/255
			test = test.reshape(-1, 28, 28 ,1)

			result = model.predict(test)
			result = np.argmax(result,axis = 1)

			text = STAT_FONT.render("Result: " + str(result), True, WHITE)
			pygame.draw.rect(win, BLACK, ((WIN_WIDTH - (WIN_WIDTH//28) - text.get_width(), 10, text.get_width(), text.get_height())))
			win.blit(text, (WIN_WIDTH - (WIN_WIDTH//28) - text.get_width(), 10))

		pygame.display.update()
