import tkinter as tk
import random
import time

CELL_SIZE = 20
ROWS, COLS = 30, 30  # Works for even or odd sizes now

class MazeSolver:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Maze Pathfinder with Multiple Solutions in Python")
        self.canvas = tk.Canvas(root, width=COLS*CELL_SIZE, height=ROWS*CELL_SIZE, bg="white")
        self.canvas.pack()

        self.maze = [[1 for _ in range(COLS)] for _ in range(ROWS)]
        self.paths_found = []
        self.generating = False
        self.solving = False

        frame = tk.Frame(root)
        frame.pack()
        tk.Button(frame, text="Generate New Maze", command=self.generate_maze).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Solve Maze", command=self.solve_maze).pack(side=tk.LEFT, padx=5)

        self.generate_maze()

    def generate_maze(self):
        if self.generating:
            return
        self.generating = True
        self.paths_found = []

        for r in range(ROWS):
            for c in range(COLS):
                self.maze[r][c] = 1

        def carve(r, c):
            dirs = [(0,1), (1,0), (0,-1), (-1,0)]
            random.shuffle(dirs)
            for dr, dc in dirs:
                nr, nc = r + dr*2, c + dc*2
                if 0 <= nr < ROWS and 0 <= nc < COLS and self.maze[nr][nc] == 1:
                    self.maze[r+dr][c+dc] = 0
                    self.maze[nr][nc] = 0
                    carve(nr, nc)

        start_r, start_c = 0, 0
        self.maze[start_r][start_c] = 0
        carve(start_r, start_c)

        # FIX: Always open exit cell
        self.maze[ROWS-1][COLS-1] = 0

        # For even sizes, also open adjacent cells to bottom-right corner if they are walls
        if ROWS % 2 == 0:
            if self.maze[ROWS-2][COLS-1] == 1:
                self.maze[ROWS-2][COLS-1] = 0
        if COLS % 2 == 0:
            if self.maze[ROWS-1][COLS-2] == 1:
                self.maze[ROWS-1][COLS-2] = 0

        self.draw_maze()
        self.generating = False

    def draw_maze(self):
        self.canvas.delete("all")
        for r in range(ROWS):
            for c in range(COLS):
                color = "black" if self.maze[r][c] == 1 else "white"
                self.canvas.create_rectangle(
                    c*CELL_SIZE, r*CELL_SIZE, 
                    (c+1)*CELL_SIZE, (r+1)*CELL_SIZE,
                    fill=color, outline="gray"
                )

    def solve_maze(self):
        if self.solving:
            return
        self.solving = True
        self.paths_found = []

        visited = [[False]*COLS for _ in range(ROWS)]
        self.dfs(0, 0, [], visited)

        colors = ["red", "blue", "green"]
        for i, path in enumerate(self.paths_found[:3]):
            for r, c in path:
                self.canvas.create_rectangle(
                    c*CELL_SIZE, r*CELL_SIZE,
                    (c+1)*CELL_SIZE, (r+1)*CELL_SIZE,
                    fill=colors[i], outline=""
                )
            self.root.update()
            time.sleep(0.3)

        # Highlight final successful path in purple with black outline
        if self.paths_found:
            final_path = self.paths_found[-1]
            for r, c in final_path:
                self.canvas.create_rectangle(
                    c*CELL_SIZE, r*CELL_SIZE,
                    (c+1)*CELL_SIZE, (r+1)*CELL_SIZE,
                    fill="purple", outline="black"
                )
            self.root.update()

        self.solving = False

    def dfs(self, r, c, path, visited):
        if len(self.paths_found) >= 3:
            return

        if not (0 <= r < ROWS and 0 <= c < COLS) or self.maze[r][c] == 1 or visited[r][c]:
            return

        visited[r][c] = True
        path.append((r, c))

        # Animate exploration
        self.canvas.create_rectangle(
            c*CELL_SIZE, r*CELL_SIZE, (c+1)*CELL_SIZE, (r+1)*CELL_SIZE,
            fill="yellow", outline=""
        )
        self.root.update()
        time.sleep(0.05)

        if r == ROWS - 1 and c == COLS - 1:
            self.paths_found.append(list(path))
        else:
            for dr, dc in [(1,0), (0,1), (-1,0), (0,-1)]:
                self.dfs(r+dr, c+dc, path, visited)

        # Backtrack: erase highlight only if cell is not part of any found path
        if not any((r, c) in p for p in self.paths_found):
            self.canvas.create_rectangle(
                c*CELL_SIZE, r*CELL_SIZE, (c+1)*CELL_SIZE, (r+1)*CELL_SIZE,
                fill="white", outline="gray"
            )
            self.root.update()
            time.sleep(0.02)

        visited[r][c] = False
        path.pop()


if __name__ == "__main__":
    root = tk.Tk()
    app = MazeSolver(root)
    root.mainloop()
