import tkinter as tk
from BlackBoxGame import *

"""
Todo: 
1. randomize atom starting positions or create popup window for player to input
2. setup print board in gui

"""

root = tk.Tk()
game = BlackBoxGame([(8,8), (1,1), (1,8)])
# setting the windows size
root.geometry("1280x720")
root.title("BlackBox Game")

# declaring string variable
# for storing coordinates for guessing and shooting
shoot_row_var = tk.StringVar()
shoot_col_var = tk.StringVar()
guess_row_var = tk.StringVar()
guess_col_var = tk.StringVar()

# defining a function that will get the current score
def getScore():
    """
    Todo: docstrings
    """
    score = game.get_score()
    guessScoreLabel = tk.Label(root, text='Current Score:' + str(score))
    guessScoreLabel.grid(row=10, column=1)

def guessAtom():
    """
    Todo: docstrings
    """
    guessRow = int(guess_row_var.get())
    guessCol = int(guess_col_var.get())
    guess = game.guess_atom(guessRow,guessCol)
    guessLabel = tk.Label(root, text = 'guess:'+str(guess))
    guessLabel.grid(row=8, column=1)
    guess_row_var.set("")
    guess_col_var.set("")

def shootRay():
    """
    Todo: docstrings
    """
    shootRow = int(shoot_row_var.get())
    shootCol = int(shoot_col_var.get())
    ray = game.shoot_ray(shootRow, shootCol)
    shootLabel = tk.Label(root, text = 'result:'+str(ray))
    shootLabel.grid(row=3, column=1)
    shoot_row_var.set("")
    shoot_col_var.set("")

def displayBoard():
    """
    Todo: docstrings    guessRow = int(guess_row_var.get())

    """
    board = game.print_board()
    boardLabel = tk.Label(root, text=board)
    boardLabel.grid(row=20, column=1)

def displayHelp():
    """
    Todo: docstrings
    """
    description = "To the play the game either enter (row, column) to guess an atom position or \n\
                   enter an entry row and column to specify where to shoot a ray into the blackbox from.\n\
                   For rules and additional information about blackbox visit:\n\
                   https://en.wikipedia.org/wiki/Black_Box_(game)"
    popup = tk.Tk()
    popup.wm_title('Help')
    helpLabel = tk.Label(popup, text=description)
    helpLabel.grid(row=0, column=0)
    popup.mainloop()


# creating a label for guess and shoot
guess_row_label = tk.Label(root, text='Row', font=('calibre', 10, 'bold')).grid(row=4, column=1)
guess_col_label = tk.Label(root, text='Column', font=('calibre', 10, 'bold')).grid(row=4, column=2)

shoot_row_label = tk.Label(root, text='Row', font=('calibre', 10, 'bold')).grid(row=1, column=1)
shoot_col_label = tk.Label(root, text='Column', font=('calibre', 10, 'bold')).grid(row=1, column=2)


# creating a entry for guessing atom position and shooting a ray to enumerate location
guess_row_entry = tk.Entry(root, textvariable=guess_row_var, font=('calibre', 10, 'normal'))
guess_col_entry = tk.Entry(root, textvariable=guess_col_var, font=('calibre', 10, 'normal'))
shoot_row_entry = tk.Entry(root, textvariable=shoot_row_var, font=('calibre', 10, 'normal'))
shoot_col_entry = tk.Entry(root, textvariable=shoot_col_var, font=('calibre', 10, 'normal'))



# creating a button using the widget
# Button that will call the submit function
score_btn = tk.Button(root, text='Get Current Score', command=getScore)
shoot_btn = tk.Button(root, text='Shoot Ray', command=shootRay)
guess_btn = tk.Button(root, text='Submit Guess', command=guessAtom)
board_btn = tk.Button(root, text='Display Board', command=displayBoard)
help_btn = tk.Button(root, text='Help', command=displayHelp)


# shoot entry and button
shoot_row_entry.grid(row=2, column=1)
shoot_col_entry.grid(row=2, column=2)
shoot_btn.grid(row=3, column=2)
# guess entry and button
guess_row_entry.grid(row=5, column=1)
guess_col_entry.grid(row=5, column=2)
guess_btn.grid(row=6, column=2)
# check score button
score_btn.grid(row=7, column=1)
# print gameboard button
board_btn.grid(row=7, column=2)
# help button
help_btn.grid(row=7, column=3)


# performing an infinite loop
# for the window to display
root.mainloop()


