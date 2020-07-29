import tkinter as tk
import itertools
import collections
from timeit import default_timer as timer

class TileSelection(object):
    
    def __init__(self, root, row, col):
        self.row = row
        self.col = col
        self.root = root
        self.grid = self.create_grid()
        self.create_textbox()
        self.create_enter()
        self.root.mainloop()
        
    def create_grid(self):
        global grid
        grid = []
        blank = " " * 4
        for i in range(self.row):
            global row
            row = []
            for j in range(self.col):
                global b
                b = tk.Button(self.root, text=blank)
                b.config(command=lambda widget=b: self.select_button(widget))
                b.grid(row=i, column=j)
                b.position = (j, i)
                row.append(b)
            grid.append(row)
        global ary
        ary = [[0 for j in range(self.col)] for i in range(self.row)]
        global hold
        hold = []
        return

    def select_button(self, widget):
        j, i = widget.position
        self.evaluate_tiles(i,j)
        widget.config(bg='green')
        widget["state"] = "disabled"
        
    def evaluate_tiles(self, i, j):
        ary[i][j] = 4
        #east
        if j > (self.col-2):
            ary[i][self.col % (j + 1)] += 1
            if ary[i][self.col % (j + 1)] == 3:
                hold.append((i, self.col % (j + 1)))
        else:
            ary[i][j + 1] += 1
            if ary[i][j + 1] == 3:
                hold.append((i, j+1))
        #west
        if j < 1:
            ary[i][self.col - 1] += 1
            if ary[i][self.col - 1] == 3:
                hold.append((i, self.col - 1))
        else:
            ary[i][j-1] += 1
            if ary[i][j-1] == 3:
                hold.append((i, j - 1))
        #south
        if (i + 2) > self.row:
            ary[self.row % (i+1)][j] += 1
            if ary[self.row % (i+1)][j] == 3:
                hold.append((self.row % (i + 1), j))
        else:
            ary[i + 1][j] += 1
            if ary[i + 1][j] == 3:
                hold.append((i + 1, j))
        #north
        if i < 1:
            ary[self.row - 1][j] += 1
            if ary[self.row-1][j] == 3:
                hold.append((self.row - 1, j))
        else:
            ary[i-1][j] += 1
            if ary[i-1][j] == 3:
                hold.append((i - 1, j))
            
    def create_enter(self):
       # tk.Button(self.root, text='Done Selecting Tiles', fg='blue',
                 # bg='white', command=self.update_hold).place(x=300,y=50)
        tk.Button(self.root, text='Find Minimum Set', fg='blue', 
                  bg='white', command=self.find_min_set).place(x=300,y=20)
                  
    def find_min_set(self):
        start = timer()
        ds = [] 
        e = 0
        ne = 0
        rary = collections.deque([i for i in range(self.row)])
        cary = collections.deque([i for i in range(self.col)])
        s = [(i,j) for i in range(self.row) for j in range(self.col)]
        if self.col > self.row:
            t = self.col - 1
        else:
            t = self.row-1
        while not ds:
            t += 1
            combos = itertools.combinations(s,t)
            for combos in itertools.combinations(s,t):
                x = False
                for (i,j) in combos:
                    if i in rary:
                        rary.remove(i)
                    if j in cary:
                        cary.remove(j)
                    if i == 0 and j == 0:
                        x = True
                if not rary and not cary and x:
                    e += 1
                    for (i,j) in combos: 
                        self.evaluate_tiles(i,j)
                    self.update_hold()
                    for r in range(self.row):
                        for c in range(self.col):
                            ary[r][c] = 0
                    if count == self.row * self.col:
                        ds.append(combos)
                else:
                    ne += 1
                rary.clear()
                cary.clear()
                for i in range(self.row):
                    rary.append(i)
                for i in range(self.col):
                    cary.append(i) 
        print(ds)
        print("number of determining sets", len(ds))
        print("evaluated", e)
        print("did not evaluate", ne)
        end = timer()
        print("Minutes ", (end - start) / 60)
                
    def update_hold(self):
        while hold:
            for i, j in hold:
                self.evaluate_tiles(i, j)
                hold.remove((i, j))
        global count 
        count = 0
        for i in range(self.row):
            for j in range(self.col):
                if ary[i][j] >= 3:
                    ary[i][j] = 4
                    count += 1
            
    def delete_grid(self):
        for widgets in root.winfo_children():
            widgets.destroy()
        self.create_textbox() 
        
    def create_textbox(self):
        tk.Label(self.root, text='Resize the Grid:', font='Helvetica 8 bold').place(x=10,y=265)
        tk.Label(self.root, text='x-dimension').place(x=10,y=290)
        tk.Label(self.root, text='y-dimension').place(x=10,y=320)

        global xd
        xd = tk.Entry(self.root)
        global yd
        yd = tk.Entry(self.root)

        xd.place(x=85,y=290)
        yd.place(x=85,y=320)
        
        tk.Button(self.root, text='Exit', command=self.root.quit).place(x=10,y=350)
        tk.Button(self.root, text='Submit', command=self.get_entry).place(x=50,y=350)
        
    def get_entry(self):
        print("x-dimension: " + xd.get() + "\ny-dimension: " + yd.get())
        self.row = int(yd.get())
        self.col = int(xd.get())
        xd.delete(0, tk.END)
        yd.delete(0, tk.END)
        self.delete_grid()
        self.create_grid()
        self.create_enter()
                    
if __name__ == '__main__':
    root = tk.Tk()
    root.title('Minimum Determining Set Algorithm')
    root.geometry("500x400")
    app = TileSelection(root, 3, 3)
