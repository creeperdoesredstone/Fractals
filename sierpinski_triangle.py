import pygame
from math import radians, sin

pygame.init()
screen_height = 600
screen_width = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sierpinski Triangle")

clock = pygame.time.Clock()
running = True

BG_COL = "white"
FG_COL = "black"
FONT = pygame.font.SysFont("Consolas", 20)

iterations: int = 0

class Triangle:
	def __init__(self, top_point: pygame.Vector2, height: int) -> None:
		self.top_point = top_point
		self.height = height
	
	def get_points(self):
		side_length: int = round(self.height / sin(radians(60)))
		return [
			self.top_point,
			pygame.Vector2(self.top_point.x - side_length / 2, self.top_point.y + self.height),
			pygame.Vector2(self.top_point.x + side_length / 2, self.top_point.y + self.height)
		]
	
	def copy(self):
		return Triangle(self.top_point, self.height)

def split_triangles(triangles: list[Triangle]) -> list[Triangle]:
	new_triangles: list[Triangle] = []
	for triangle in triangles:
		triangle.height /= 2
		new_triangles.append(triangle)

		copy = triangle.copy()
		copy.top_point = triangle.get_points()[1]
		new_triangles.append(copy)

		copy2 = triangle.copy()
		copy2.top_point = triangle.get_points()[2]
		new_triangles.append(copy2)
	
	return new_triangles

def draw(triangles: list[Triangle]):
	for triangle in triangles:
		pygame.draw.polygon(screen, FG_COL, triangle.get_points(), 0)

base_triangle = Triangle(pygame.Vector2(screen_width >> 1, 0), screen_height)
triangles = [base_triangle]

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE and iterations < 15:
				triangles = split_triangles(triangles)
				iterations += 1
			if event.key == pygame.K_BACKSPACE and iterations > 0:
				triangles = triangles[::3]
				for triangle in triangles:
					triangle.height *= 2
				
				iterations -= 1

	screen.fill(BG_COL)
	draw(triangles)

	text = FONT.render(f"Iterations: {iterations}", True, FG_COL)
	text_rect = text.get_rect()
	# screen.blit(text, (10, 10), text_rect)

	pygame.display.flip()
	clock.tick(60)
