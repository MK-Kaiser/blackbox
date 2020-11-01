# blackbox

    What is blackbox?
    A game played on a 10x10 grid where the guessing player will start with 25 points during each turn, 
    the player will shoot rays into the black box. 
    5 points are lost for incorrect guesses, and 1 point is lost for each new entry/exit point. 
    Behavior of the ray serves as an indicator of where the player should guess.
    The goal is to correctly guess where each atom position is.
    
    *New
    Play via GUI




![image](https://raw.githubusercontent.com/MK-Kaiser/portfolio/master/images/BlackBox.png)
    
    
    Play via commandline
    Usage:
    use git clone or wget to pull BlackBoxGame.py
    from the commandline run with: python3 -i BlackBoxGame.py
    Have alternate player input/hide atom positions with command like:
            game = BlackBoxGame([(7, 1), (7, 3), (3, 6), (1, 6)])
            
    Shoot rays to ascertain where the atoms are with:
            game.shoot_ray(4,9)
            
    Once you think you know where an atom is positioned, guess with:
            game.guess_atom(4,5)
            
    Check the current score with:
            print(game.get_score())
           
    For additional information about the game blackbox and the rules refer to this page:
    https://en.wikipedia.org/wiki/Black_Box_(game)
    
    
    
