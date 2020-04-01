# -*- coding: utf-8 -*-
import argparse
import random
from colorama import Back, init
import os

# Windows coloring
init()
_, height = os.get_terminal_size()

parser = argparse.ArgumentParser("")
parser.add_argument('slots', type=int, help='Number of slots')

args = parser.parse_args()

class Game:
    def __init__(self, slots):
        self.slots = slots
        self.char = ""
        self.colors = {
            "w":Back.WHITE, 
            "r":Back.RED,
            "g":Back.GREEN,
            "b":Back.CYAN
        }
        self.board = list()
        _tmp = list()
        for _ in range(self.slots):
            _tmp.append(random.choice(list(self.colors.keys())))
        self.solution = State(self.slots, _tmp)
        self.status = "running"
        
    def display(self):
        #self.solution.display(self.char, self.colors, True)
        i = 0
        for state in self.board:
            print(f"R{i}", end="")
            i += 1
            state.display(self.char, self.colors, False)
            
    def start(self):
        print("== Game started ==")
        round = 0
        while self.status == "running":
            print("\n"*height)
            self.display()
            print(f"Available colors: {list(self.colors.keys())}")
            print(f"== [Round {round}] Enter your prediction ==")
            self.board.append(State(self.slots, list()).get_next(self.solution, self.colors))
            
            if self.board[-1].pred == self.solution.pred:
                self.status = "closed"
            round += 1
        
        print(f"Human won in round {round-1}. The solution was:")
        self.solution.display(self.char, self.colors, True)
        print("== Game closed ==")
        
    def run_unendlich(self):
        while True:
            self.start()
            _in = input("Do you want to play again? (yes) ")
            if _in != "" and _in != "yes" and _in != "y":
                exit(0)
            self.__init__(self.slots)
        
    
class State:
    def __init__(self, slots, pred):
        self.slots = slots
        self.pred = pred
        self.eval = list()
        
    def display(self, char, colors, solution):
        print("\t", end="")
        for x in self.pred:
            print(f"{colors[x]}{char}\t", end="")
        if not solution:
            print(f"{Back.RESET}\t", end="")
            print(self.eval)
        else:
            print(Back.RESET)
        
    def get_next(self, solution, colors):
        for _ in range(self.slots):
            _in = input()
            if _in in colors: self.pred.append(_in)
            else:
                print(f"Color not found. The available colors: {list(colors.keys())}")            
                exit(1)
        self.evaluate(solution)
        
        return self
        
    def evaluate(self, solution):
        pred = self.pred[:]
        sol = solution.pred[:]
        # hard correct
        i, j = 0, 0
        while j < self.slots:
            j += 1
            if pred[i] == sol[i]:
                del pred[i]
                del sol[i]
                self.eval.append("X")
            else:
                i += 1
        # soft correct   
        for x in pred:
            if x in sol:
                sol.remove(x)
                self.eval.append("+")
                
def main(args):
    print("== Welcome to mmind ==")
    game = Game(args.slots)
    game.run_unendlich()
    
main(args)
