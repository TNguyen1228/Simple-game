import tkinter as tk
from tkinter import messagebox
import random

class Minesweeper:
    def __init__(self, root, size=10, mines=10):
        self.root = root
        self.size = size
        self.mines = mines
        self.buttons = []
        self.mine_positions = []
        self.create_widgets()
        self.place_mines()
        self.update_counts()

    def create_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()  # Clear existing widgets

        for i in range(self.size):
            row = []
            for j in range(self.size):
                btn = tk.Button(self.root, width=4, height=2, command=lambda x=i, y=j: self.on_click(x, y))
                btn.bind('<Button-3>', lambda event, x=i, y=j: self.on_right_click(event, x, y))
                btn.grid(row=i, column=j)
                row.append(btn)
            self.buttons.append(row)

        # Add restart button
        restart_btn = tk.Button(self.root, text="Restart", command=self.restart_game)
        restart_btn.grid(row=self.size, column=0, columnspan=self.size, sticky="ew")

    def place_mines(self):
        self.mine_positions = random.sample([(i, j) for i in range(self.size) for j in range(self.size)], self.mines)

    def update_counts(self):
        self.counts = [[0 for _ in range(self.size)] for _ in range(self.size)]
        for x, y in self.mine_positions:
            for i in range(max(0, x-1), min(self.size, x+2)):
                for j in range(max(0, y-1), min(self.size, y+2)):
                    if (i, j) not in self.mine_positions:
                        self.counts[i][j] += 1

    def on_click(self, x, y):
        if (x, y) in self.mine_positions:
            self.buttons[x][y].config(text='X', bg='red')
            self.game_over()
        else:
            self.reveal(x, y)
        self.check_win()

    def on_right_click(self, event, x, y):
        current_text = self.buttons[x][y].cget('text')
        if current_text == 'F':
            self.buttons[x][y].config(text='')
        else:
            self.buttons[x][y].config(text='F')

    def reveal(self, x, y):
        if self.buttons[x][y].cget('state') == 'disabled':
            return

        count = self.counts[x][y]
        if 1 <= count <= 4:
            self.buttons[x][y].config(text=str(count), fg=self.get_color(count), bg='lightgray', relief=tk.SUNKEN, state='disabled')
        else:
            self.buttons[x][y].config(text='', bg='lightgray', relief=tk.SUNKEN, state='disabled')  # Remove number for empty cells

        if count == 0:
            for i in range(max(0, x-1), min(self.size, x+2)):
                for j in range(max(0, y-1), min(self.size, y+2)):
                    if (i, j) != (x, y):
                        self.reveal(i, j)

    def get_color(self, number):
        colors = {
            1: 'blue',
            2: 'green',
            3: 'red',
            4: 'purple',
        }
        return colors.get(number, 'black')

    def game_over(self):
        for x, y in self.mine_positions:
            self.buttons[x][y].config(text='*', bg='red')
        for row in self.buttons:
            for btn in row:
                btn.config(state='disabled')
        messagebox.showinfo("Game Over", "You hit a mine! Game Over.")

    def check_win(self):
        for row in self.buttons:
            for btn in row:
                if btn.cget('text') == '' or btn.cget('text') == 'F':
                    return
        messagebox.showinfo("Congratulations", "You have found all mines!")

    def restart_game(self):
        self.buttons = []
        self.mine_positions = []
        self.create_widgets()
        self.place_mines()
        self.update_counts()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Minesweeper")
    game = Minesweeper(root)
    root.mainloop()
