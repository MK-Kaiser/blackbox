#!/usr/bin/env python3
# Author: Mark Kaiser
# Date: 8/11/20
# Description:
from BlackBoxGame import *
import unittest


class Tie(unittest.TestCase):
    """unit testing class"""

    def test_deflections(self):
        """tests proper handling of deflections"""
        game = BlackBoxGame([(7, 1), (7, 3), (3, 6), (1, 6)])
        #print(game.get_score())
        self.assertEqual(game.shoot_ray(4,9), (9,7)) # left to down deflection
        self.assertEqual(game.shoot_ray(9,4), (8,9)) # up to right deflection
        self.assertEqual(game.shoot_ray(0,4), (6,9)) # down to right deflection
        self.assertEqual(game.shoot_ray(9,5), (4,0)) # up to left deflection
        #game.print_board()
        #print(game.get_score())

    def test_double_deflections(self):
        """tests proper handling of double deflections"""
        game = BlackBoxGame([(5, 2), (5, 4), (3, 6), (1, 6)])
        #print(game.get_score())
        self.assertEqual(game.shoot_ray(2,9), (2,9)) # horizontal double deflection
        self.assertEqual(game.shoot_ray(9,3), (9,3)) # vertical double deflection
        #game.print_board()
        #print(game.get_score())

    def test_reflections(self):
        """tests proper handling of reflections"""
        game = BlackBoxGame([ (4, 5), (8, 8), (8, 3), (1, 6)])
        #print(game.get_score())
        self.assertEqual(game.shoot_ray(0,5), (0,5)) # reflection check on top row
        self.assertEqual(game.shoot_ray(9,4), (9,4)) # reflection check on bottom row
        self.assertEqual(game.shoot_ray(7,9), (7,9)) # reflection check on right column
        #game.print_board()
        #print(game.get_score())

    def test_mixed_detours(self):
        """tests proper handling of a mixture of deflections, double deflections and reflections"""
        game = BlackBoxGame([(2, 5), (6, 5), (6, 7)])
        #print(game.get_score())
        self.assertEqual(game.shoot_ray(3,9), (3,9)) # deflects 2 times
        self.assertEqual(game.shoot_ray(3,0), (5,0)) # detour
        #game.print_board()
        #print(game.get_score())

    def test_hit_miss(self):
        """tests proper handling of hits and misses"""
        game = BlackBoxGame([(8,8), (1,1), (1,8)])
        #print(game.get_score())
        self.assertEqual(game.shoot_ray(0,4), (9,4))     # vertical miss
        self.assertEqual(game.shoot_ray(4,9), (4,0))     # horizontal miss
        self.assertEqual(game.shoot_ray(1,0), None)     # vertical hit
        self.assertEqual(game.shoot_ray(9,1), None)     # horizontal hit
        #game.print_board()
        #print(game.get_score())

    def test_guess(self):
        """tests proper handling of special cases"""
        game = BlackBoxGame([(3, 4), (4, 5), (8, 8), (7, 1), (7, 3), (3, 6), (1, 6)])
        #print(game.get_score())
        self.assertEqual(game.guess_atom(4,5), True)     # correct guess
        self.assertEqual(game.guess_atom(8,8), True)     # correct guess
        self.assertEqual(game.guess_atom(9,1), False)     # incorrect guess
        self.assertEqual(game.guess_atom(1,1), False)     # incorrect guess
        self.assertEqual(game.guess_atom(1,1), False)     # repeat incorrect guess
        #game.print_board()
        #print(game.get_score())

    def test_invalid(self):
        """tests handling of invalid inputs and options"""
        game = BlackBoxGame([(3, 4), (4, 5), (8, 8), (7, 1), (7, 3), (3, 6), (1, 6)])
        #print(game.get_score())
        self.assertEqual(game.shoot_ray(9,9), False) # lower right corner square
        self.assertEqual(game.shoot_ray(0,9), False) # upper right corner square
        self.assertEqual(game.shoot_ray(0,0), False) # upper left corner square
        self.assertEqual(game.shoot_ray(9,0), False) # lower left corner square
        #game.print_board()
        #print(game.get_score())

if __name__ == '__main__':
    unittest.main()
