import tkinter as tk
from BlackBoxGame import *

"""
Todo: 
1. need to setup responses to guesses and shoot rays
2. randomize atom starting positions
3. add check score button
4. setup print board in gui
5. 
"""

root = tk.Tk()
game = BlackBoxGame([(7, 1), (7, 3), (3, 6), (1, 6)])
game.print_board()
# setting the windows size
root.geometry("1280x800")

# declaring string variable
# for storing name and password
name_var = tk.StringVar()
guess_var = tk.StringVar()


# defining a function that will get the players' name
def startGame():
    name = name_entry.get()
    #nameLabel = tk.Label(root, text = 'Player:'+name)
    #nameLabel.grid(row=5, column=1)
    #name_var.set("")

def submit():
    guess = guess_var.get()
    guessLabel = tk.Label(root, text = 'guess:'+str(guess))
    guessLabel.grid(row=6, column=1)
    game.guess_atom(guess[0], guess[1])
    game.print_board()
    game.get_score()
    guess_var.set("")


# creating a label for name using widget Label
name_label = tk.Label(root, text='Player', font=('calibre', 10, 'bold'))

# creating a entry for input name using widget Entry
name_entry = tk.Entry(root, textvariable=name_var, font = ('calibre', 10, 'normal'))

# creating a label for guess
guess_label = tk.Label(root, text='Guess', font=('calibre', 10, 'bold'))

# creating a entry for password
guess_entry = tk.Entry(root, textvariable=guess_var, font=('calibre', 10, 'normal'))

# creating a button using the widget
# Button that will call the submit function
start_btn = tk.Button(root, text='Start Game', command=startGame)

submit_btn = tk.Button(root, text='Submit', command=submit)


# placing the label and entry in
# the required position using grid
# method
name_label.grid(row=0, column=0)
name_entry.grid(row=0, column=1)
guess_entry.grid(row=3, column=1)
start_btn.grid(row=2, column=1)
submit_btn.grid(row=4, column=1)

# performing an infinite loop
# for the window to display
root.mainloop()


