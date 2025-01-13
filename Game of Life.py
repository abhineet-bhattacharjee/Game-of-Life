import pygame
import numpy as np


class GameOfLife:
    def __init__(self, width, height, cellsize, auto: bool = True):
        self.width = width
        self.height = height
        self.cellsize = cellsize
        self.cellsize = cellsize
        self.rows = (self.height - 60) // cellsize
        self.columns = self.width // cellsize

        self.Black = (0, 0, 0)
        self.White = (255, 255, 255)

        self.running = True
        self.pause = True
        self.auto = auto
        self.gen = 0
        self.fps = [1, 2, 3, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        self.fps_val = 4

        self.window = pygame.display.set_mode((self.width, self.height))
        self.grid = np.random.randint(low=0, high=2, size=(self.rows, self.columns), dtype=int) if self.auto else np.zeros((self.rows, self.columns), dtype=int)
        self.grid_display = False

        pygame.display.set_caption(f"Game of Life - {"Auto" if self.auto else "Manual"} Mode")

    def gui(self):
        font = pygame.font.Font(None, 30)
        gen_display = font.render(f"GENERATION: {self.gen}", True, self.White)
        run_display = font.render("Paused" if self.pause else "Running", True, self.White)
        fps_display = font.render(f"FPS: {self.fps[self.fps_val]}", True, self.White)
        self.window.blit(gen_display, (10, self.height - 50))
        self.window.blit(run_display, (self.width - 100, self.height - 50))
        self.window.blit(fps_display, (self.width // 2 - 25, self.height - 50))

    def grids(self):
        for y in range(self.rows):
            for x in range(self.columns):
                rectangle = pygame.Rect(x * self.cellsize, y * self.cellsize, self.cellsize, self.cellsize)
                if self.grid[y, x] == 0:
                    pygame.draw.rect(self.window, self.Black, rectangle)
                else:
                    pygame.draw.rect(self.window, self.White, rectangle)

                if self.grid_display:
                    pygame.draw.rect(self.window, self.White, rectangle, 1)

    def update_grid(self):
        temp_grid = self.grid.copy()
        for y in range(self.rows):
            for x in range(self.columns):
                alive_neighbours = np.sum(self.grid[max(0, y-1):min(y+2, self.rows), max(0, x-1):min(x+2, self.columns)]) - self.grid[y, x]

                if (alive_neighbours < 2 or alive_neighbours > 3) and self.grid[y, x] == 1:
                    temp_grid[y, x] = 0
                elif alive_neighbours == 3 and self.grid[y, x] == 0:
                    if alive_neighbours == 3:
                        temp_grid[y, x] = 1

        self.grid = temp_grid
        self.gen = self.gen + 1

    def manage_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.pause = not self.pause
                elif event.key == pygame.K_RETURN:
                    self.grid = np.random.randint(low=0, high=2, size=(self.rows, self.columns), dtype=int) if self.auto else np.zeros((self.rows, self.columns), dtype=int)
                    self.gen = 0
                elif event.key == pygame.K_LSHIFT:
                    self.grid_display = not self.grid_display
                elif event.key == pygame.K_RIGHT:
                    self.fps_val = 0 if self.fps_val == len(self.fps) - 1 else self.fps_val + 1
                elif event.key == pygame.K_LEFT:
                    self.fps_val = -1 if self.fps_val == 0 else self.fps_val - 1
                elif event.key == pygame.K_UP:
                    self.fps_val = -1
                elif event.key == pygame.K_DOWN:
                    self.fps_val = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if not y // self.cellsize > self.rows - 1:
                    self.grid[y // self.cellsize, x // self.cellsize] = not self.grid[y // self.cellsize, x // self.cellsize]

    def main(self):
        while self.running:
            self.manage_events()

            self.window.fill(self.Black)
            if not self.pause:
                self.update_grid()

            pygame.display.set_caption(f"Game of Life - {"Auto" if self.auto else "Manual"} Mode")

            self.grids()
            self.gui()
            pygame.display.flip()
            pygame.time.Clock().tick(self.fps[self.fps_val])


if __name__ == '__main__':
    pygame.init()
    GameOfLife(1200, 600, 10, auto=True).main()
