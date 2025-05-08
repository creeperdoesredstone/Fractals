import pygame
from math import ceil

pygame.init()
screen_height = 540
screen_width = 960

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Lévy C Curve")

clock = pygame.time.Clock()
running = True

BG_COL = "black"
FG_COL = "white"
FONT = pygame.font.SysFont("Consolas", 20)

points: list[pygame.Vector2] = [pygame.Vector2(300, 140), pygame.Vector2(660, 140)]

def split_points(points: list[pygame.Vector2]) -> list[pygame.Vector2]:
	new_points: list[pygame.Vector2] = []

	for i in range(len(points) - 1):
		point: pygame.Vector2 = points[i]
		next_point: pygame.Vector2 = points[i + 1]
		target_point: pygame.Vector2 = (next_point - point).rotate(45) / (2 ** 0.5)

		new_points.append(point)
		new_points.append(point + target_point)

	new_points.append(points[-1])

	return new_points

iterations: int = 0

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE and iterations < 18:
				points = split_points(points)
				iterations += 1
			if event.key == pygame.K_BACKSPACE and iterations > 0:
				points = points[::2]
				iterations -= 1

	screen.fill(BG_COL)
	pygame.draw.lines(screen, FG_COL, False, points, ceil((19 - iterations) / 3))

	text = FONT.render(f"Iteration: {iterations}", True, FG_COL)
	text_rect = text.get_rect()
	screen.blit(text, (10, 10), text_rect)

	pygame.display.flip()
	clock.tick(60)
