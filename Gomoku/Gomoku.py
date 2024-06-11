import tkinter as tk

class CaroChess:
    def __init__(self, root):
        self.root = root
        self.root.title("Caro Chess")
        self.board_size = 15
        self.cell_size = 40
        self.canvas = tk.Canvas(root, width=self.board_size * self.cell_size, height=self.board_size * self.cell_size)
        self.canvas.pack()
        
        self.board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = 1
        
        self.draw_board()
        self.canvas.bind("<Button-1>", self.click_event)
        
    def draw_board(self):
        for i in range(self.board_size):
            self.canvas.create_line(0, i * self.cell_size, self.board_size * self.cell_size, i * self.cell_size)
            self.canvas.create_line(i * self.cell_size, 0, i * self.cell_size, self.board_size * self.cell_size)
    
    def click_event(self, event):
        x = event.x // self.cell_size
        y = event.y // self.cell_size
        
        if self.board[y][x] == 0:
            self.board[y][x] = self.current_player
            self.draw_move(x, y, self.current_player)
            if self.check_winner(x, y):
                self.canvas.create_text(self.board_size * self.cell_size / 2, self.board_size * self.cell_size / 2, 
                                        text=f"Player {self.current_player} wins!", font=('Arial', 24), fill="red")
                self.canvas.unbind("<Button-1>")
            else:
                self.current_player = 3 - self.current_player
    
    def draw_move(self, x, y, player):
        if player == 1:
            color = "black"
        else:
            color = "white"
        self.canvas.create_oval(x * self.cell_size + 5, y * self.cell_size + 5, 
                                (x + 1) * self.cell_size - 5, (y + 1) * self.cell_size - 5, fill=color)
    
    def check_winner(self, x, y):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            count = 1
            for i in range(1, 5):
                if self.check_direction(x + dx * i, y + dy * i, self.current_player):
                    count += 1
                else:
                    break
            for i in range(1, 5):
                if self.check_direction(x - dx * i, y - dy * i, self.current_player):
                    count += 1
                else:
                    break
            if count >= 5:
                return True
        return False
    
    def check_direction(self, x, y, player):
        if 0 <= x < self.board_size and 0 <= y < self.board_size:
            return self.board[y][x] == player
        return False

if __name__ == "__main__":
    root = tk.Tk()
    CaroChess(root)
    root.mainloop()
