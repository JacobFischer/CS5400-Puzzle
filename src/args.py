"""Handles and defines what the arg parms are for the CLI
"""

import argparse

_parser = argparse.ArgumentParser(
    description='Runs the Python 3 puzzle solver')

_parser.add_argument('algorithm', nargs='?', default='bfts')
_parser.add_argument('file', nargs='?', default='./puzzles/examplePuzzle.txt')

args = _parser.parse_args()
