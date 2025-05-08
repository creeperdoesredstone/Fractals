import pygame
import numpy as np
import colorsys

# Pygame Setup
pygame.init()

# Window settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mandelbrot Set - Smooth Coloring")

# Mandelbrot parameters
xmin, xmax = -2.5, 1.5
ymin, ymax = -1.5, 1.5
max_iter = 200  # Higher = more detail

def mandelbrot_set(width, height, xmin, xmax, ymin, ymax, max_iter):
    """Computes Mandelbrot escape-time values with smooth coloring."""
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    X, Y = np.meshgrid(x, y)  # Create complex plane grid
    C = X + 1j * Y  # Convert to complex numbers
    Z = np.zeros_like(C, dtype=np.complex128)
    M = np.full(C.shape, max_iter, dtype=float)  # Default to max_iter (black inside set)

    for i in range(max_iter):
        mask = np.abs(Z) < 2  # Select non-escaped points
        Z[mask] = Z[mask] ** 2 + C[mask]  # Mandelbrot iteration
        escaped = mask & (np.abs(Z) >= 2)  # New escaping points
        M[escaped] = i + 1 - np.log(np.log(np.abs(Z[escaped]) + 1e-10)) / np.log(2)  # Smooth coloring

    return np.nan_to_num(M, nan=0.0)  # Ensure no NaN values

# Compute the Mandelbrot set once
mandelbrot_image = mandelbrot_set(WIDTH, HEIGHT, xmin, xmax, ymin, ymax, max_iter)

# Convert escape-time values to smooth colors
def mandelbrot_to_surface(mandelbrot_array, max_iter):
    """Converts Mandelbrot escape-time data into a Pygame surface with a balanced, smooth color palette."""
    norm = mandelbrot_array / max_iter  # Normalize escape time (0 to 1)
    
    surface = np.zeros((mandelbrot_array.shape[0], mandelbrot_array.shape[1], 3), dtype=np.uint8)
    
    # Convert escape values to colors using HSV → RGB
    for i in range(mandelbrot_array.shape[0]):
        for j in range(mandelbrot_array.shape[1]):
            if mandelbrot_array[i, j] >= max_iter:  # Mandelbrot set (inside)
                surface[i, j] = (0, 0, 0)  # Black for inside points
            else:
                hue = 0.5 + 0.3 * norm[i, j]  # Reduce blue, favor warmer colors
                saturation = 0.8  # Slightly desaturate fast escape points
                brightness = 0.9 - 0.4 * norm[i, j] # Increase brightness for fast escape points
                r, g, b = colorsys.hsv_to_rgb(hue, saturation, brightness)  # Convert to RGB
                surface[i, j] = (int(r * 255), int(g * 255), int(b * 255))

    surface = np.transpose(surface, (1, 0, 2))  # Fix Pygame orientation
    return pygame.surfarray.make_surface(surface)

# Generate and display the Mandelbrot image
surface = mandelbrot_to_surface(mandelbrot_image, max_iter)
screen.blit(surface, (0, 0))
pygame.display.flip()

# Event loop (to keep window open)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
