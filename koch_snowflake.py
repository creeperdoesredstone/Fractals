import pygame
from math import ceil, radians, sin

pygame.init()
screen_height = 540
screen_width = 960

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Koch Snowflake")

clock = pygame.time.Clock()
running = True

BG_COL = "black"
FG_COL = pygame.Color(100, 225, 255)
FONT = pygame.font.SysFont("Consolas", 20)

def split_points(points: list[pygame.Vector2]):
	new_points = []

	for i in range(len(points)):
		point = points[i]
		next_point: pygame.Vector2 = points[(i + 1) % len(points)]
		target_point: pygame.Vector2 = (next_point - point) / 3

		new_points.append(point)
		new_points.append(point + target_point)
		new_points.append(point + target_point + target_point.rotate(60))
		new_points.append(point + target_point + target_point.rotate(60) + target_point.rotate(-60))

	return new_points

HEIGHT = 300
points: list[pygame.Vector2] = [
	pygame.Vector2(480, 75),
	pygame.Vector2(480 - round(HEIGHT/sin(radians(60))) // 2, 75 + HEIGHT),
	pygame.Vector2(480 + round(HEIGHT/sin(radians(60))) // 2, 75 + HEIGHT),
]

iterations: int = 0

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE and iterations < 9:
				points = split_points(points)
				iterations += 1
			if event.key == pygame.K_BACKSPACE and iterations > 0:
				points = points[::4]
				iterations -= 1

	screen.fill(BG_COL)
	pygame.draw.lines(screen, FG_COL, True, points, ceil((10 - iterations) / 2))
	# pygame.draw.polygon(screen, FG_COL, points, 0)

	text = FONT.render(f"Iteration: {iterations}", True, FG_COL)
	text_rect = text.get_rect()
	screen.blit(text, (10, 10), text_rect)

	pygame.display.flip()
	clock.tick(60)
