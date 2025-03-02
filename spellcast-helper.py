import tkinter as tk
from tkinter import font, messagebox
import heapq
from collections import Counter
from functools import reduce
import os

# Letter point values in Spellcast
LETTER_VALUES = {
    'a': 1, 'b': 4, 'c': 5, 'd': 3, 'e': 1, 'f': 5, 'g': 3, 'h': 4, 'i': 1, 
    'j': 7, 'k': 3, 'l': 3, 'm': 4, 'n': 2, 'o': 1, 'p': 4, 'q': 8, 'r': 2, 
    's': 2, 't': 2, 'u': 4, 'v': 5, 'w': 5, 'x': 7, 'y': 4, 'z': 8
}

class SpellcastSolver:
    def __init__(self):
        self.word_list = self._load_dictionary()
        self.grid = None
        self.cell_multipliers = {}  # For future implementation of multipliers
        
    def _load_dictionary(self):
        """Load word list from file."""
        words = []
        dictionary_file = 'dictionary.txt'
        
        # Create a basic dictionary file if it doesn't exist
        if not os.path.exists(dictionary_file):
            try:
                import urllib.request
                print("Dictionary file not found. Downloading...")
                url = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"
                urllib.request.urlretrieve(url, dictionary_file)
                print(f"Downloaded dictionary to {dictionary_file}")
            except:
                print("Could not download dictionary. Creating a small sample.")
                with open(dictionary_file, 'w') as f:
                    sample_words = [
                        "apple", "banana", "cat", "dog", "elephant", "frog", 
                        "giraffe", "house", "impulse", "impulsive", "impulsively",
                        "jazz", "kingdom", "little", "mouse", "notebook", 
                        "orange", "purple", "quiet", "rabbit", "sunshine",
                        "tree", "umbrella", "violet", "window", "xylophone", 
                        "yellow", "zebra", "attempt", "quartz", "quick"
                    ]
                    f.write('\n'.join(sample_words))
        
        # Load the words
        try:
            with open(dictionary_file, 'r') as f:
                for line in f:
                    word = line.strip().lower()
                    if word and all(c.isalpha() for c in word):
                        words.append(word)
        except Exception as e:
            print(f"Error loading dictionary: {e}")
            words = ["example", "test", "word"]  # Fallback
            
        return words

    def set_grid(self, grid):
        """Set the current letter grid."""
        self.grid = [[c.lower() for c in row] for row in grid]

    def calculate_word_score(self, word):
        """Calculate the base score for a word."""
        score = sum(LETTER_VALUES.get(c, 0) for c in word)
        # Add long word bonus
        if len(word) > 6:
            score += 10
        return score

    def is_valid_path(self, word, allow_swaps=0):
        """Check if word can be formed on the grid with given number of letter swaps."""
        if not self.grid or not word:
            return False, [], []
            
        # Quick check if the grid has enough letters for the word
        grid_chars = Counter(''.join(''.join(row) for row in self.grid))
        word_chars = Counter(word)
        if sum((word_chars - grid_chars).values()) > allow_swaps:
            return False, [], []
            
        # Define the 8 possible moves (including diagonals)
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        def dfs(i, j, word_idx, path, swapped, remaining_swaps):
            """Depth-first search to find valid path."""
            if word_idx == len(word):
                return True, path, swapped
                
            for di, dj in directions:
                ni, nj = i + di, j + dj
                if 0 <= ni < 5 and 0 <= nj < 5 and (ni, nj) not in path:
                    # Try using the letter directly
                    if self.grid[ni][nj] == word[word_idx]:
                        path.append((ni, nj))
                        result, final_path, final_swapped = dfs(ni, nj, word_idx + 1, path, swapped, remaining_swaps)
                        if result:
                            return True, final_path, final_swapped
                        path.pop()
                    # Try swapping if allowed
                    elif remaining_swaps > 0:
                        path.append((ni, nj))
                        swapped.append((ni, nj))
                        result, final_path, final_swapped = dfs(ni, nj, word_idx + 1, path, swapped, remaining_swaps - 1)
                        if result:
                            return True, final_path, final_swapped
                        swapped.pop()
                        path.pop()
            
            return False, [], []
        
        # Try starting from each cell
        for i in range(5):
            for j in range(5):
                if self.grid[i][j] == word[0] or allow_swaps > 0:
                    start_path = [(i, j)]
                    start_swapped = [] if self.grid[i][j] == word[0] else [(i, j)]
                    start_remaining_swaps = allow_swaps if self.grid[i][j] == word[0] else allow_swaps - 1
                    
                    result, path, swapped = dfs(i, j, 1, start_path, start_swapped, start_remaining_swaps)
                    if result:
                        return True, path, swapped
                        
        return False, [], []

    def find_best_words(self, max_swaps=2, top_n=5):
        """Find best scoring words with given number of swaps."""
        results = []
        
        # Try with different swap counts
        for swaps in range(max_swaps + 1):
            swap_results = []
            
            # Sort words by descending potential score to check high value words first
            potential_words = [(self.calculate_word_score(word), word) for word in self.word_list]
            potential_words.sort(reverse=True)
            
            for score, word in potential_words:
                if len(swap_results) >= top_n:
                    # If we have enough results and next word can't beat our lowest score, skip
                    if score < swap_results[-1][0]:
                        break
                
                valid, path, swapped = self.is_valid_path(word, swaps)
                if valid:
                    # The actual score might be affected by multipliers (future feature)
                    actual_score = score  # For now it's the same
                    heapq.heappush(swap_results, (actual_score, word, path, swapped))
                    if len(swap_results) > top_n:
                        heapq.heappop(swap_results)  # Remove lowest score
            
            # Sort by score descending
            swap_results.sort(reverse=True)
            results.append(swap_results)
            
        return results


class SpellcastApp:
    def __init__(self, root):
        self.root = root
        self.solver = SpellcastSolver()
        self.setup_ui()
        
    def setup_ui(self):
        self.root.title("Discord Spellcast Helper")
        self.root.geometry("640x400")
        self.root.resizable(False, False)
        
        # Custom fonts
        self.title_font = font.Font(family="Arial", size=14, weight="bold")
        self.grid_font = font.Font(family="Arial", size=16)
        self.result_font = font.Font(family="Arial", size=12)
        
        # Set up the grid frame
        self.grid_frame = tk.Frame(self.root, padx=20, pady=20)
        self.grid_frame.pack(side=tk.LEFT, fill=tk.BOTH)
        
        # Create the 5x5 letter input grid
        self.grid_cells = []
        self.grid_vars = []
        
        for i in range(5):
            row_cells = []
            row_vars = []
            for j in range(5):
                var = tk.StringVar()
                entry = tk.Entry(
                    self.grid_frame, 
                    textvariable=var, 
                    width=2,
                    font=self.grid_font,
                    justify='center'
                )
                entry.grid(row=i, column=j, padx=5, pady=5)
                
                # Tab navigation between cells
                entry.bind("<KeyRelease>", lambda e, i=i, j=j: self.on_key_release(e, i, j))
                
                row_cells.append(entry)
                row_vars.append(var)
            self.grid_cells.append(row_cells)
            self.grid_vars.append(row_vars)
        
        # Generate button
        self.btn_generate = tk.Button(
            self.grid_frame,
            text="Find Best Words",
            command=self.find_words,
            font=self.title_font
        )
        self.btn_generate.grid(row=5, column=0, columnspan=5, pady=20)
        
        # Clear button
        self.btn_clear = tk.Button(
            self.grid_frame,
            text="Clear Grid",
            command=self.clear_grid,
            font=self.result_font
        )
        self.btn_clear.grid(row=6, column=0, columnspan=5)
        
        # Results frame
        self.results_frame = tk.Frame(self.root, padx=20, pady=20)
        self.results_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Results labels
        self.result_labels = []
        tk.Label(self.results_frame, text="Best Words:", font=self.title_font).pack(anchor='w', pady=(0, 10))
        
        for i in range(3):
            swap_frame = tk.Frame(self.results_frame)
            swap_frame.pack(fill=tk.X, pady=5)
            
            swap_title = tk.Label(
                swap_frame, 
                text=f"{i} swaps:",
                font=self.result_font,
                width=10,
                anchor='w'
            )
            swap_title.pack(side=tk.LEFT)
            
            result_label = tk.Label(
                swap_frame,
                text="",
                font=self.result_font,
                fg="#333333",
                anchor='w',
                justify='left'
            )
            result_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.result_labels.append(result_label)
        
        # Set focus to first cell
        self.grid_cells[0][0].focus_set()
        
    def on_key_release(self, event, i, j):
        """Handle key releases in the letter grid."""
        if event.char.isalpha():
            # If a letter was entered, automatically move to the next cell
            val = self.grid_vars[i][j].get()
            if val:
                # Move to next cell
                next_i, next_j = i, j + 1
                if next_j >= 5:
                    next_i, next_j = i + 1, 0
                if next_i < 5:
                    self.grid_cells[next_i][next_j].focus_set()
        elif event.keysym == 'BackSpace':
            # If current cell is empty and backspace was pressed, go to previous cell
            val = self.grid_vars[i][j].get()
            if not val:
                prev_i, prev_j = i, j - 1
                if prev_j < 0:
                    prev_i, prev_j = i - 1, 4
                if prev_i >= 0:
                    self.grid_cells[prev_i][prev_j].focus_set()
    
    def clear_grid(self):
        """Clear all input cells."""
        for i in range(5):
            for j in range(5):
                self.grid_vars[i][j].set("")
        
        # Clear results
        for label in self.result_labels:
            label.config(text="")
            
        # Set focus to first cell
        self.grid_cells[0][0].focus_set()
    
    def highlight_word(self, result_label, word, path, swapped):
        """Highlight a word path when hovering over result."""
        original_bg = self.grid_cells[0][0].cget('background')
        original_fg = self.grid_cells[0][0].cget('foreground')
        
        def on_enter(event):
            # Save current letters
            current_letters = [[var.get() for var in row] for row in self.grid_vars]
            
            # Highlight path
            for idx, (i, j) in enumerate(path):
                if (i, j) in swapped:
                    # Highlight swapped letters in red
                    self.grid_cells[i][j].config(background='red', foreground='white')
                    # Show the actual letter from the word
                    self.grid_vars[i][j].set(word[idx])
                else:
                    # Highlight normal path in blue
                    self.grid_cells[i][j].config(background='blue', foreground='white')
        
        def on_leave(event):
            # Reset grid
            for i in range(5):
                for j in range(5):
                    self.grid_cells[i][j].config(background=original_bg, foreground=original_fg)
            
            # Reset to original board
            grid = self.get_current_grid()
            for i in range(5):
                for j in range(5):
                    self.grid_vars[i][j].set(grid[i][j])
        
        # Bind hover events
        result_label.bind("<Enter>", on_enter)
        result_label.bind("<Leave>", on_leave)
    
    def get_current_grid(self):
        """Get the current grid values."""
        return [[var.get().lower() if var.get() else '.' for var in row] for row in self.grid_vars]
    
    def find_words(self):
        """Find and display best words."""
        grid = self.get_current_grid()
        
        # Check if grid is sufficiently filled
        filled_cells = sum(1 for row in grid for cell in row if cell != '.')
        if filled_cells < 10:  # Require at least 10 letters
            messagebox.showwarning("Incomplete Grid", "Please fill more letters in the grid (at least 10).")
            return
        
        self.solver.set_grid(grid)
        best_words = self.solver.find_best_words(max_swaps=2, top_n=3)
        
        # Display results
        for swap_count, results in enumerate(best_words):
            if results:
                # Take the best word
                score, word, path, swapped = results[0]
                result_text = f"{word} ({score} pts)"
                self.result_labels[swap_count].config(text=result_text)
                
                # Set up highlighting on hover
                self.highlight_word(self.result_labels[swap_count], word, path, swapped)
            else:
                self.result_labels[swap_count].config(text="No word found")


if __name__ == "__main__":
    root = tk.Tk()
    app = SpellcastApp(root)
    root.mainloop()
