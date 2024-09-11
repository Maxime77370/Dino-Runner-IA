import argparse
import pygame
from Logique import LogicSimulation
from Menu import Menu

def run_with_gui():
    Menu()

def run_without_gui():
    sim = LogicSimulation( generations_num=100, population_num=500, neron_couche=[4,4,4,1], mutation_rate=0.1)
    while True:
        if sim.update() == False:
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dino Runner AI")
    parser.add_argument("--gui", action="store_true", help="Run with GUI")
    parser.add_argument("--no-gui", action="store_true", help="Run without GUI")
    args = parser.parse_args()

    if args.gui:
        run_with_gui()
    elif args.no_gui:
        run_without_gui()
    else:
        print("Please specify --gui or --no-gui")